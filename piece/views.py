from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Q
from .models import Piece

class HomePageView(TemplateView):
  template_name='home.html'

class SearchResultsView(ListView):
  model = Piece
  template_name = 'search_results.html'
  
  def get_queryset(self):
    query = self.request.GET.get('q')
    object_list = Piece.objects.filter(
      Q(title__icontains=query)
      | Q(catalogue_number__icontains=query)
      | Q(isbn__icontains=query)
      | Q(notes__icontains=query)
    )
    return object_list
