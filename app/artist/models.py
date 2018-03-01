from datetime import datetime
from django.core.files import File
from django.db import models

from crawler.artist import ArtistData
from utils.file import download, get_buffer_ext


class ArtistManager(models.Manager):
    def update_or_create_from_melon(self, artist_id):
        artist = ArtistData(artist_id)
        artist.get_detail()
        name = artist.name
        url_img_cover = artist.url_img_cover
        # .get: dict에서 key있으면 반환 없으면 ''
        real_name = artist.personal_information.get('본명', '')
        nationality = artist.personal_information.get('국적', '')
        birth_date_str = artist.personal_information.get('생일', '')
        constellation = artist.personal_information.get('별자리', '')
        blood_type = artist.personal_information.get('혈액형', '')

        for short, full in Artist.CHOICE_BLOOD_TYPE:
            if blood_type.strip() == full:
                blood_type = short
                break
            else:
                blood_type = Artist.BLOOD_TYPE_OTHER

        artist, artist_created = self.update_or_create(
            melon_id=artist_id,
            defaults={
                'name': name,
                'real_name': real_name,
                'nationality': nationality,
                'birth_date': datetime.strptime(birth_date_str, '%Y.%m.%d') if birth_date_str else None,
                'constellation': constellation,
                'blood_type': blood_type,
            }
        )
        # img_profile필드에 저장할 파일확장자를 바이너리 데이터 자체의 MIME_TYPE에서 가져옴
        # 파일명은 artist_id를 사용
        #
        # def download(url):
        #     # url로부터 다운받은 데이터를 BytesIO객체에 쓰고 리턴
        #     response = requests.get(url)
        #     binary_data = response.content
        #     temp_file = BytesIO()
        #     temp_file.write(binary_data)
        #     temp_file.seek(0)
        #     return temp_file
        # def get_buffer_ext(buffer):
        #     buffer.seek(0)
        #     mime_info = magic.from_buffer(buffer.read(), mime=True)
        #     buffer.seek(0)
        #     return mime_info.split('/')[-1]

        temp_file = download(url_img_cover)
        file_name = '{artist_id}.{ext}'.format(
            artist_id=artist_id,
            ext=get_buffer_ext(temp_file),
        )
        if artist.img_profile:
            artist.img_profile.delete()
        artist.img_profile.save(file_name, File(temp_file))
        return artist, artist_created


class Artist(models.Model):
    BLOOD_TYPE_A = 'a'
    BLOOD_TYPE_B = 'b'
    BLOOD_TYPE_O = 'o'
    BLOOD_TYPE_AB = 'c'
    BLOOD_TYPE_OTHER = ' x'
    CHOICES_BLOOD_TYPE = (
        (BLOOD_TYPE_A, 'A형'),
        (BLOOD_TYPE_B, 'B형'),
        (BLOOD_TYPE_O, 'O형'),
        (BLOOD_TYPE_AB, 'AB형'),
        (BLOOD_TYPE_OTHER, '기타'),

    )
    melon_id = models.CharField(
        '멜론 Artist ID',
        max_length=20,
        blank=True,
        null=True,
        unique=True,
    )
    img_profile = models.ImageField(
        '프로필 이미지',
        upload_to='artist',
        blank=True,
    )
    name = models.CharField(
        '이름',
        max_length=50,
    )
    real_name = models.CharField(
        '본명',
        max_length=30,
        blank=True,
    )
    nationality = models.CharField(
        '국적',
        max_length=50,
        blank=True,
    )
    birth_date = models.DateField(
        '생년월일',
        blank=True,
        null=True,
    )
    constellation = models.CharField(
        '별자리',
        max_length=30,
        blank=True,
    )
    blood_type = models.CharField(
        '혈액형',
        max_length=1,
        choices=CHOICES_BLOOD_TYPE,
        blank=True,
    )
    intro = models.TextField(
        '소개',
        blank=True,
    )


    def __str__(self):
        return self.name
