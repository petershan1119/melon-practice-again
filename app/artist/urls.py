from django.urls import path

from . import views

app_name = 'artist'
url_patterns = [
    path('', views.artist_list, name='artist-list'),
    path('<int:artist_pk>', views.artist_detail, name='artist-detail'),
    path('add/', views.artist_add, name='artist-add'),
    path('search/melon/', views.artist_search_from_melon, name='artist-search-from-melon'),

]