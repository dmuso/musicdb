from django.urls import path

from .views import HomePageView, SearchResultsView, BrowseInstrumentView

urlpatterns = [
  path('', HomePageView.as_view(), name="home"),
  path('search/', SearchResultsView.as_view(), name="search_results"),
  path('browse/instrument', BrowseInstrumentView.as_view(), name="browse_by_instrument"),
]
