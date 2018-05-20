from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .models import Entry
from .forms import EntryForm
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexTemplateView(TemplateView):
    template_name = 'myapp/index.html'


class CalendarListView(LoginRequiredMixin, ListView):
    template_name = 'myapp/calendar.html'
    model = Entry
    context_object_name = 'entries'

    def get_queryset(self, *args, **kwargs):
        return Entry.objects.filter(author=self.request.user)


class EntryDetailView(LoginRequiredMixin, DetailView):
    template_name = 'myapp/details.html'
    model = Entry
    context_object_name = 'entry'

# CreateView

# DeleteView


@login_required
def add(request):

    if request.method == 'POST':
        form = EntryForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            date = form.cleaned_data['date']
            description = form.cleaned_data['description']

            Entry.objects.create(
                name=name,
                author=request.user,
                date=date,
                description=description,
            ).save()

            return HttpResponseRedirect('/calendar')

    else:
        form = EntryForm()

    return render(request, 'myapp/form.html', {'form': form})

@login_required
def delete(request, pk):

    if request.method == 'DELETE':
        entry = get_object_or_404(Entry, pk=pk)
        entry.delete()

    return HttpResponseRedirect('/')

def signup(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/calendar')

    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})
