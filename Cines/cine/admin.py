from django.contrib import admin
from cine.models import Cinema, Movie, Actor, Room, MovieByRoom, General

# Register your models here.
admin.site.register(Cinema)
admin.site.register(Movie)
admin.site.register(MovieByRoom)
admin.site.register(Room)

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date', 'getShortMovies', 'getLongMovies', 'getMeanShortMovieDuration', 'getMaxMovieDuration',
                    'getMinMovieDuration')

    search_fields = ('name', 'birth_date')
    list_filter = ('name', 'birth_date')
    ordering = ('name',)

    def getShortMovies(self, obj):
        return obj.getShortMovies()

    def getLongMovies(self, obj):
        return obj.getLongMovies()

    def getMeanShortMovieDuration(self, obj):
        return obj.getMeanShortMovieDuration()

    def getMaxMovieDuration(self, obj):
        return obj.getMaxMovieDuration()

    def getMinMovieDuration(self, obj):
        return obj.getMinMovieDuration()

    getShortMovies.short_description = 'Short movies'
    getLongMovies.short_description = 'Long movies'
    getMeanShortMovieDuration.short_description = 'Mean duration of Short movies'
    getMaxMovieDuration.short_description = 'Max duration of movies'
    getMinMovieDuration.short_description = 'Min duration of movies'


admin.site.register(Actor, ActorAdmin)
admin.site.register(General)