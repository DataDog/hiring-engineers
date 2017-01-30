from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.utils import timezone
from .models import Question
from django.views import generic
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from datadog import ThreadStats
from datadog.dogstatsd import statsd
import time
import random

from datadog import api
from datadog import initialize
options = {
    'api_key':'4b7643802de69e1ef132ee1235ecf3b4',
    'app_key':'a314ca8cfb6e6d436bbfe8c7549274fdbf54ebea'
}
initialize(**options)

stats = ThreadStats()
stats.start()
title = "Something big happened!"
text = 'Someone voted for Freddy'
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        print(random.random())
        stats.gauge('random',random.random())
        start_time = time.time()
        results = api.Metric.send(metric='latency_Query', points=1000)
        duration = time.time() - start_time
        statsd.histogram('database.query.time', duration, tags=['page:home'])
        stats.increment('page.views', tags=["support", "page:IndexView"])
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        start_time = time.time()
        results = api.Metric.send(metric='latency_Query', points=1000)
        duration = time.time() - start_time
        statsd.histogram('database.query.time', duration, tags=['page:detail'])
        stats.increment('page.views', tags=["support", "page:DetailView"])
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    statsd.timed("page.latency", tags=["support", "page:results"])
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
        # api.Event.create(title=title, text=text)
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
    	# stats.increment('home.page.hits')
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))