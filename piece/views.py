# from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from .models import Category, Instrument, Composer, Publisher, Piece

class HomePageView(TemplateView):
  template_name='home.html'

class SearchResultsView(ListView):
  model = Piece
  template_name = 'search_results.html'
  
  def get_queryset(self):
    instrument_query = self.request.GET.get('instrument')
    composer_query = self.request.GET.get('composer')
    category_query = self.request.GET.get('category')
    publisher_query = self.request.GET.get('publisher')
    if instrument_query:
      object_list = Piece.objects.filter(
        instrument=instrument_query
      )
    elif composer_query:
      object_list = Piece.objects.filter(
        composers=composer_query
      )
    elif category_query:
      object_list = Piece.objects.filter(
        category=category_query
      )
    elif publisher_query:
      object_list = Piece.objects.filter(
        publisher=publisher_query
      )
    else:
      query = self.request.GET.get('q')
      object_list = Piece.objects.filter(
        Q(title__icontains=query)
        | Q(catalogue_number__icontains=query)
        | Q(isbn__icontains=query)
        | Q(notes__icontains=query)
        | Q(composers__last_name__icontains=query)
      )
    return object_list

class BrowseInstrumentView(ListView):
  model = Instrument
  template_name = 'browse_by_instrument.html'

class BrowseComposerView(ListView):
  model = Composer
  template_name = 'browse_by_composer.html'

class BrowseCategoryView(ListView):
  model = Category
  template_name = 'browse_by_category.html'

class BrowsePublisherView(ListView):
  model = Publisher
  template_name = 'browse_by_publisher.html'

class PieceDetailView(DetailView):
  model = Piece
  template_name = 'view_piece.html'

