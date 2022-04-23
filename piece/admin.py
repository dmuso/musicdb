from django.contrib import admin
from .models import Composer, Location, Piece, InstrumentGroup, Instrument, Category, Publisher, Genre, Arranger, Grade, Status, EnsemblePart

admin.site.register(Piece)
admin.site.register(InstrumentGroup)
admin.site.register(Instrument)
admin.site.register(Category)
admin.site.register(Publisher)
admin.site.register(Location)
admin.site.register(Composer)
admin.site.register(Arranger)
admin.site.register(Genre)
admin.site.register(Grade)
admin.site.register(Status)
admin.site.register(EnsemblePart)

