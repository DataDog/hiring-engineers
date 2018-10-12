from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.contrib.messages import info, error
from django.shortcuts import get_object_or_404, redirect, render
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.csrf import csrf_protect

from mezzanine.conf import settings
from mezzanine.accounts import get_profile_model
from mezzanine.blog.models import BlogPost, BlogCategory

import omise

# Returns the name to be used for reverse profile lookups from the user
# object. That's "profile" for the ``drum.links.Profile``, but otherwise
# depends on the model specified in ``AUTH_PROFILE_MODULE``.
USER_PROFILE_RELATED_NAME = get_profile_model().user.field.related_query_name()

def blog_post_detail(request, slug, year=None, month=None, day=None,
                     template="blog/blog_post_detail.html",
                     extra_context=None):
    """. Custom templates are checked for using the name
    ``blog/blog_post_detail_XXX.html`` where ``XXX`` is the blog
    posts's slug.
    """
    blog_posts = BlogPost.objects.published(
                                     for_user=request.user).select_related()
    blog_post = get_object_or_404(blog_posts, slug=slug)
    related_posts = blog_post.related_posts.published(for_user=request.user)
    context = {"blog_post": blog_post, "editable_obj": blog_post,
               "related_posts": related_posts}
    context.update(extra_context or {})
    templates = [u"blog/blog_post_detail_%s.html" % str(slug), template]
    return TemplateResponse(request, templates, context)

@csrf_protect
def upgrade_status(request, template="auth/upgrade_status.html", extra_context=None):
    if request.method == "POST":
        card_id = request.POST["omiseToken"]
        username = request.user.username
        users = User.objects.select_related(USER_PROFILE_RELATED_NAME)
        lookup = {"username__iexact": username, "is_active": True}
        profile_user = get_object_or_404(users, **lookup)
        customer_id = profile_user.profile.relangprofile.omise_customer_id
        omise.api_public = getattr(settings, "OMISE_PKEY", None)
        omise.api_secret = getattr(settings, "OMISE_SKEY", None)
        if omise.api_public and omise.api_secret and customer_id is not "":
            customer = omise.Customer.retrieve(customer_id)
            customer.update(
                card=card_id
            )
            omise.Schedule.create(
                every=1,
                period='month',
                on={
                    'weekday_of_month': '2nd_monday'
                },
                 end_date='2199-05-01',
                charge={
                    'customer': customer_id,
                    'amount': 500,
                    'description': 'Membership fee'
                }
            )
            profile_user.profile.relangprofile.customer_status= "Premium"
            profile_user.profile.relangprofile.save()
            info(request, _("Successfully Upgraded to Premium"))
    context = {"title": _("Upgrade")}
    context.update(extra_context or {})
    return TemplateResponse(request, template, context)


from django.db.models.signals import post_delete
from django.dispatch import receiver

@receiver(post_delete, sender=None)
def user_postdelete(sender, instance, **kwargs):
        if sender.omise_customer_id:
            omise.api_public = getattr(settings, "OMISE_PKEY", None)
            omise.api_secret = getattr(settings, "OMISE_SKEY", None)
            try:
                customer = omise.Customer.retrieve(instance.omise_customer_id)
                if customer:
                    customer.destroy()
                    if customer.destroyed:
                        pass
            except:
                pass
