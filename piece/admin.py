from django.contrib import admin
from .models import Composer, Location, Piece, InstrumentGroup, Instrument, Category, Publisher

admin.site.register(Piece)
admin.site.register(InstrumentGroup)
admin.site.register(Instrument)
admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(Location)
admin.site.register(Composer)
