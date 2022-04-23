# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from .models import Category, Instrument, Composer, Arranger, Publisher, Piece

class HomePageView(LoginRequiredMixin, TemplateView):
  template_name='home.html'

class SearchResultsView(LoginRequiredMixin, ListView):
  model = Piece
  template_name = 'search_results.html'
  
  def get_queryset(self):
    instrument_query = self.request.GET.get('instrument')
    composer_query = self.request.GET.get('composer')
    arranger_query = self.request.GET.get('arranger')
    category_query = self.request.GET.get('category')
    publisher_query = self.request.GET.get('publisher')
    query = self.request.GET.get('query')

    queryset = Piece.objects.all()
    if instrument_query:
      queryset = queryset.filter(instruments=instrument_query)
    if composer_query:
      queryset = queryset.filter(composers=composer_query)
    if arranger_query:
      queryset = queryset.filter(arranger=arranger_query)
    if category_query:
      queryset = queryset.filter(categories=category_query)
    if publisher_query:
      queryset = queryset.filter(publishers=publisher_query)
    if query:
      queryset = queryset.filter(
        Q(title__icontains=query) |
        Q(catalogue_number__icontains=query) |
        Q(isbn__icontains=query) |
        Q(notes__icontains=query) |
        Q(composers__last_name__icontains=query)
      )

    # search_results = Piece.objects.filter(
    #   title__icontains=query,
    # )
    # search_results = Piece.objects.filter(
    #   **query_dict)
    object_list = dict(
      search_results=queryset,
      categories=Category.objects.all(),
      category_query=category_query,
      composers=Composer.objects.all(),
      composer_query=composer_query,
      arrangers=Arranger.objects.all(),
      arranger_query=arranger_query,
      publishers=Publisher.objects.all(),
      publisher_query=publisher_query,
      instruments=Instrument.objects.all(),
      instrument_query=instrument_query,
      query=query,
    )
    return object_list

class BrowseInstrumentView(LoginRequiredMixin, ListView):
  model = Instrument
  template_name = 'browse_by_instrument.html'

class BrowseComposerView(LoginRequiredMixin, ListView):
  model = Composer
  template_name = 'browse_by_composer.html'

class BrowseCategoryView(LoginRequiredMixin, ListView):
  model = Category
  template_name = 'browse_by_category.html'

class BrowsePublisherView(LoginRequiredMixin, ListView):
  model = Publisher
  template_name = 'browse_by_publisher.html'

class PieceDetailView(LoginRequiredMixin, DetailView):
  model = Piece
  template_name = 'view_piece.html'

