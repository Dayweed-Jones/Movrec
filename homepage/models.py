from django.db import models
from django.core.files.temp import NamedTemporaryFile
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.files import File
from django.core.exceptions import ObjectDoesNotExist
from urllib.request import urlopen
from django.contrib.auth.models import User
from datetime import datetime


class Genres(models.Model):
    genre = models.CharField(unique=True, max_length=50)

    class Meta:
        db_table = "genres"

    def __str__(self) -> str:
        return f"{self.genre}"

    @classmethod
    def get_id_by_name(cls, genre):
        try:
            genre = cls.objects.get(genre=genre)
            return genre.id
        except cls.DoesNotExist:
            return None

    @classmethod
    def exists(cls, genre):
        return cls.objects.filter(genre=genre).exists()


class Ratings(models.Model):
    movie = models.ForeignKey(
        "Movies", on_delete=models.PROTECT, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.PROTECT, null=False, blank=False)
    score = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(0)],
    )
    time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "ratings"


class Movies(models.Model):
    name = models.CharField(null=True, max_length=255)
    adult = models.BooleanField(null=True, blank=True)
    release_date = models.DateField(null=True, auto_now=False)
    genres = models.ManyToManyField(Genres)
    description = models.CharField(null=True, max_length=1024)
    rating = models.ManyToManyField(User, through=Ratings, blank=True)
    movie_credits = models.ManyToManyField("Person", through="Credits", blank=True)

    class Meta:
        unique_together = ('name', 'release_date')
        db_table = "movies"

    def __str__(self) -> str:
        return f"{self.name}"
    
    @classmethod
    def get_movie_by_name(cls, name, release_date):
        movies = cls.objects.filter(name=name)
        matching_movie = None
        release_date = datetime.strptime(release_date, "%Y-%m-%d").date()
        for movie in movies:
            if movie.release_date == release_date:
                matching_movie = movie
                break
        return matching_movie
    
    def genre_binary_list(self):
        # Get all genres ordered by genreid (or however you want them ordered)
        all_genres = Genres.objects.all().order_by('id')
        
        # Get the genres associated with this movie
        movie_genres = self.genres.all()

        # Create the binary list
        binary_list = []
        for genre in all_genres:
            if genre in movie_genres:
                binary_list.append(1)
            else:
                binary_list.append(0)
        
        return binary_list


class Images(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, null=False, blank=False)
    is_poster = models.BooleanField(null=True, blank=False)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        db_table = "images"

    def __str__(self) -> str:
        return f"{self.movie.name} - Image {self.id}"

    def get_image_from_url(self, url, name):
        img_tmp = NamedTemporaryFile(delete=True)
        with urlopen(url) as uo:
            assert uo.status == 200
            img_tmp.write(uo.read())
            img_tmp.flush()
        img = File(img_tmp)
        path = "." + name
        self.image.save(path, img)


class Credits(models.Model):
    person_id = models.ForeignKey(
        "Person", on_delete=models.CASCADE, null=False, blank=False
    )
    movie_id = models.ForeignKey(
        "Movies", on_delete=models.CASCADE, null=False, blank=False
    )
    department = models.CharField(null=True, max_length=255)
    character = models.CharField(null=True, max_length=255)
    job = models.CharField(null=True, max_length=255)


class Person(models.Model):
    name = models.CharField(null=True, max_length=255)
    birthday = models.DateField(null=True, auto_now=False)

    @classmethod
    def get_person_by_name(cls, name, birthday):
        persons = cls.objects.filter(name=name)
        matching_person = None
        for person in persons:
            if person.birthday == birthday:
                matching_person = person
                break
        return matching_person
    
class List(models.Model):
    movie = models.ForeignKey(
        "Movies", on_delete=models.CASCADE, null=False, blank=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    time = models.DateTimeField(default=datetime.now)

class MLRatings(models.Model):
        movie = models.ForeignKey(
        Movies, on_delete=models.CASCADE, null=False, blank=False)
        score = models.IntegerField()
        user = models.IntegerField()