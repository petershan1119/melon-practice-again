from django.urls import path

from . import views

url_patterns = [
    path('search/melon/', views.artist_search_from_melon, name='artist-search-from-melon'),
]