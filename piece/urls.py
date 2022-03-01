from django.urls import path

from .views import HomePageView, SearchResultsView, BrowseInstrumentView, BrowseComposerView, BrowseCategoryView, BrowsePublisherView, PieceDetailView

urlpatterns = [
  path('', HomePageView.as_view(), name="home"),
  path('search/', SearchResultsView.as_view(), name="search_results"),
  path('browse/instrument', BrowseInstrumentView.as_view(), name="browse_by_instrument"),
  path('browse/composer', BrowseComposerView.as_view(), name="browse_by_composer"),
  path('browse/category', BrowseCategoryView.as_view(), name="browse_by_category"),
  path('browse/publisher', BrowsePublisherView.as_view(), name="browse_by_publisher"),
  path('pieces/<int:pk>', PieceDetailView.as_view(), name="view_piece"),
]
