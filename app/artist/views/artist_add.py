from django.shortcuts import redirect, render

from ..forms import ArtistForm

__all__ = (
    'artist_add',
)


def artist_add(request):
    """
    1. artist_add.html 작성
    2. url과 연결, /artist/add/에 매핑
    3. GET요청 시 잘 되는지 확인
    4. form method설정  후 POST요청시 artist_add() view 분기
    5. POST 요청의 값이 request.POST에 잘 오는지 확인
        name값만 받아서 name만 갖는 Artist를 먼저 생성
        성공시 나머지 값들을 하나씩 적용해보기
    6. request.POST에 담긴 값을 사용해 Artist인스턴스 생성
    7. 생성 완료후 'artist:artist-list' URL에 해당하는 view로 이동
    """
    # if request.method == "POST":
    #     name = request.POST['name']
    #     Artist.objects.create(
    #         name=name,
    #     )
    #     return redirect('artist:artist-list')
    # else:
    #     return render(request, 'artist/artist_add.html')
    if request.method == "POST":
        form = ArtistForm(request.POST, request.FILES)
        form.save()
        return redirect('artist:artist-list')
    else:
        form = ArtistForm()
    context = {
        'artist_form': form,
    }
    return render(request, 'artist/artist_add.html', context)