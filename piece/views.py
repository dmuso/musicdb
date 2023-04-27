# from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from .models import ShelfLocation, EnsemblePart, Instrument, Composer, Arranger, Publisher, Piece, Grade, Genre, Status
from django.http import JsonResponse

class HomePageView(LoginRequiredMixin, ListView):
  template_name='home.html'

  def get_queryset(self):
    return SearchHeader.get_queryset(self)

class SearchResultsView(LoginRequiredMixin, ListView):
  model = Piece
  template_name = 'search_results.html'

  def get_queryset(self):
    return SearchHeader.get_queryset(self)

class BrowseInstrumentView(LoginRequiredMixin, ListView):
  model = Instrument
  template_name = 'browse_by_instrument.html'

class BrowseComposerView(LoginRequiredMixin, ListView):
  model = Composer
  template_name = 'browse_by_composer.html'

class BrowseShelfLocationView(LoginRequiredMixin, ListView):
  model = ShelfLocation
  template_name = 'browse_by_shelf_location.html'

class BrowsePublisherView(LoginRequiredMixin, ListView):
  model = Publisher
  template_name = 'browse_by_publisher.html'

class PieceDetailView(LoginRequiredMixin, DetailView):
  model = Piece
  template_name = 'view_piece.html'

class SuggestedCatalogueNoView(LoginRequiredMixin, View):
  def get(self, request, *args, **kwargs):
    instruments = request.GET.getlist('instruments', [])
    shelf_locations = request.GET.getlist('shelf_locations', [])

    suggested_catalogue_no = Piece.suggested_cat_number(Instrument.objects.get(pk=instruments[0]), ShelfLocation.objects.get(pk=shelf_locations[0]))
    data = {'suggested_catalogue_no': suggested_catalogue_no}
    return JsonResponse(data)

class SearchHeader():
  @staticmethod
  def get_queryset(self):
    instrument_query = self.request.GET.get('instrument')
    composer_query = self.request.GET.get('composer')
    arranger_query = self.request.GET.get('arranger')
    shelf_location_query = self.request.GET.get('shelf_location')
    publisher_query = self.request.GET.get('publisher')
    grade_query = self.request.GET.get('grade')
    accompaniment_query = self.request.GET.get('accompaniment')
    ensemble_part_query = self.request.GET.get('ensemble_part')
    genre_query = self.request.GET.get('genre')
    status_query = self.request.GET.get('status')
    query = self.request.GET.get('query')

    queryset = Piece.objects.all()
    if instrument_query:
      queryset = queryset.filter(instruments=instrument_query)
    if shelf_location_query:
      queryset = queryset.filter(shelf_locations=shelf_location_query)
    if composer_query:
      queryset = queryset.filter(composers=composer_query)
    if arranger_query:
      queryset = queryset.filter(arranger=arranger_query)
    if publisher_query:
      queryset = queryset.filter(publishers=publisher_query)
    if grade_query:
      queryset = queryset.filter(grades=grade_query)
    if accompaniment_query:
      queryset = queryset.filter(accompaniment=accompaniment_query)
    if ensemble_part_query:
      queryset = queryset.filter(ensemble_parts=ensemble_part_query)
    if genre_query:
      queryset = queryset.filter(genres=genre_query)
    if status_query:
      queryset = queryset.filter(status=status_query)
    if query:
      queryset = queryset.filter(
        Q(title__icontains=query) |
        Q(catalogue_number__icontains=query) |
        Q(isbn__icontains=query) |
        Q(notes__icontains=query) |
        Q(song_list__icontains=query) |
        Q(composers__last_name__icontains=query)
      )

    queryset = queryset.order_by('title')

    object_list = dict(
      search_results=queryset,
      shelf_locations=ShelfLocation.objects.all(),
      shelf_location_query=shelf_location_query,
      composers=Composer.objects.all(),
      composer_query=composer_query,
      arrangers=Arranger.objects.all(),
      arranger_query=arranger_query,
      publishers=Publisher.objects.all(),
      publisher_query=publisher_query,
      instruments=Instrument.objects.all(),
      instrument_query=instrument_query,
      grades=Grade.objects.all(),
      grade_query=grade_query,
      accompaniments=Instrument.objects.all(),
      accompaniment_query=accompaniment_query,
      ensemble_parts=EnsemblePart.objects.all(),
      ensemble_part_query=ensemble_part_query,
      genres=Genre.objects.all(),
      genre_query=genre_query,
      statuses=Status.objects.all(),
      status_query=status_query,
      query=query,
    )
    return object_list

