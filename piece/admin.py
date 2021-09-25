from django.contrib import admin
from .models import Piece, InstrumentGroup, Instrument, Category

admin.site.register(Piece)
admin.site.register(InstrumentGroup)
admin.site.register(Instrument)
admin.site.register(Category)
