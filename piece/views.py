from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from .models import Instrument, Piece

class HomePageView(TemplateView):
  template_name='home.html'

class SearchResultsView(ListView):
  model = Piece
  template_name = 'search_results.html'
  
  def get_queryset(self):
    instrument_query = self.request.GET.get('instrument')
    if instrument_query:
      object_list = Piece.objects.filter(
        instrument=instrument_query
      )
    else:
      query = self.request.GET.get('q')
      object_list = Piece.objects.filter(
        Q(title__icontains=query)
        | Q(catalogue_number__icontains=query)
        | Q(isbn__icontains=query)
        | Q(notes__icontains=query)
      )
    return object_list

class BrowseInstrumentView(ListView):
  model = Instrument
  template_name = 'browse_by_instrument.html'
