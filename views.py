from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect

# Create your views here.
from django.template.loader import render_to_string
from django.views import generic
from django.views.generic import CreateView, DetailView, TemplateView, UpdateView
from django.views.generic.base import View

from core.calculations import get_calc_object
from core.forms import AddCustomerForm, NewQuoteForm
from core.models import Customer, VehicleQuote
from core.template_objects import PDFQuoteObject

import weasyprint


class NewQuoteView(LoginRequiredMixin, CreateView) :
    template_name = 'quote/new.html'
    form_class =  NewQuoteForm


    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        pk = self.kwargs.get('pk');
        self.customer = Customer.objects.get(pk=pk)
        initial['customer'] = self.customer.id
        return initial


    def form_valid(self, form):
        quote = form.save()
        return redirect('core:WorksheetView', pk=quote.id)

class NewUpdatedQuoteView(LoginRequiredMixin, CreateView) :
    template_name = 'quote/new.html'
    form_class =  NewQuoteForm


    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        pk = self.kwargs.get('pk');

        oldQuote = VehicleQuote.objects.get(pk=pk)

        #make deep copy so new quote is saved
        initial['customer'] = oldQuote.customer.id
        initial['model_program'] = oldQuote.model_program.id
        initial['sec_deposits'] = oldQuote.sec_deposits
        initial['miles_at_inception'] = oldQuote.miles_at_inception
        initial['msrp'] = oldQuote.msrp
        initial['sale_price'] = oldQuote.sale_price
        initial['kahu'] = oldQuote.kahu
        initial['cash_down'] = oldQuote.cash_down
        initial['miles_per_year'] = oldQuote.miles_per_year
        initial['addl_miles_per_year'] = oldQuote.addl_miles_per_year
        initial['tax_tags_upfront'] = oldQuote.tax_tags_upfront
        initial['acq_fee_upfront'] = oldQuote.acq_fee_upfront
        initial['rate_markup'] = oldQuote.rate_markup
        initial['mf_markup'] = oldQuote.mf_markup
        initial['doc_fee'] = oldQuote.doc_fee
        initial['acq_fee'] = oldQuote.acq_fee
        initial['trade_value'] = oldQuote.trade_value
        initial['trade_payoff'] = oldQuote.trade_payoff
        initial['trade_description'] = oldQuote.trade_description
        initial['trade_miles'] = oldQuote.trade_miles
        initial['increments'] = oldQuote.increments





        return initial


    def form_valid(self, form):
        quote = form.save()
        return redirect('core:WorksheetView', pk=quote.id)


class UpdateQuoteView(LoginRequiredMixin, UpdateView) :
    template_name = 'quote/update.html'
    form_class =  NewQuoteForm
    queryset = VehicleQuote.objects.all()


    def form_valid(self, form):
        quote = form.save()
        return redirect('core:WorksheetView', pk=quote.id)


