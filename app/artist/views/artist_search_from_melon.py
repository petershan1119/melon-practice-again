from django.shortcuts import render


def artist_search_from_melon(request):
    context = {}
    if request.method == 'POST':
        keyword = request.POST['keyword']
        if keyword:
            artist_info_list = []
    return render(request, 'artist/artist_search_from_melon.html', context)