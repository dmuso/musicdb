from django.urls import path
from django.conf.urls import include

from .views import HomePageView, SearchResultsView, BrowseInstrumentView, BrowseComposerView, BrowseShelfLocationView, BrowsePublisherView, PieceDetailView

urlpatterns = [
  path('', HomePageView.as_view(), name="home"),
  path('accounts/', include('django.contrib.auth.urls')),
  path('search/', SearchResultsView.as_view(), name="search_results"),
  path('browse/instrument', BrowseInstrumentView.as_view(), name="browse_by_instrument"),
  path('browse/composer', BrowseComposerView.as_view(), name="browse_by_composer"),
  path('browse/shelf_location', BrowseShelfLocationView.as_view(), name="browse_by_shelf_location"),
  path('browse/publisher', BrowsePublisherView.as_view(), name="browse_by_publisher"),
  path('pieces/<int:pk>', PieceDetailView.as_view(), name="view_piece"),
]
