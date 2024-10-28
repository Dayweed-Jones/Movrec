import requests
import pandas as pd
import numpy
from concurrent.futures import ThreadPoolExecutor
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
from django.core.management.base import BaseCommand
from homepage.models import (
    Movies,
    Images,
    Genres,
    Person,
    Credits,
)


class Command(BaseCommand):
    help = "populate db"

    def handle(self, *args, **options):
        session = requests.Session()
        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        def fetch_url(url, headers):
            return session.get(url, headers=headers).json()

        def get_movie_items(mov_id, tmdb_id):
            movie_url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?language=en-US"
            credits_url = (
                f"https://api.themoviedb.org/3/movie/{tmdb_id}/credits?language=en-US"
            )
            person_url = "https://api.themoviedb.org/3/person/{}?language=en-US"
            image_url = "https://image.tmdb.org/t/p/w500"

            headers = {
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwOTQzNWIxNGZmM2Y5OGY4MzU2NGQ1MjJkNDhiNTRjZCIsInN1YiI6IjY2MDU3ZDI5ZmNlYzJlMDE4NmM1MTY0ZSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.3WWWkAbtcpnj_SVXkZqgbg8PPH1Y3FGavANp2nDNYJ4",
            }

            data = fetch_url(movie_url, headers)

            if data.get("success", True) == False:
                return 1

            credits = fetch_url(credits_url, headers)

            name = data.get("title", data["original_title"])
            adult = data["adult"]
            release_date = data["release_date"]
            file_name = data["poster_path"]
            genres = data["genres"]
            description = data["overview"]

            movie = Movies.get_movie_by_name(name=name, release_date=release_date)
            if not movie:
                movie = Movies.objects.create(
                    name=name,
                    adult=adult,
                    release_date=release_date,
                    description=description,
                )

                genre_ids = [Genres.get_id_by_name(genre["name"]) for genre in genres]
                movie.genres.add(*filter(None, genre_ids))

            def process_crew(person):
                if (
                    person["department"] == "Directing"
                    and person["job"] == "Director"
                    or person["department"] == "Writing"
                    and person["job"] in ("Screenplay", "Story", "Writer")
                ):
                    person_info = fetch_url(
                        person_url.format(person["id"]), headers
                    )
                    person_obj = Person.get_person_by_name(
                        name=person_info["name"], birthday=person_info["birthday"]
                    )
                    if person_obj is None:
                        person_obj = Person.objects.create(
                            name=person_info["name"],
                            birthday=person_info["birthday"],
                        )
                    Credits.objects.create(
                        person_id=person_obj,
                        movie_id=movie,
                        department=person["department"],
                        job=person["job"],
                        character=None,
                    )
            def process_cast(person):
                if person["order"] < 12:
                    person_info = fetch_url(
                        person_url.format(person["id"]), headers
                    )
                    person_obj = Person.get_person_by_name(
                        name=person_info["name"], birthday=person_info["birthday"]
                    )
                    if person_obj is None:
                        person_obj = Person.objects.create(
                            name=person_info["name"],
                            birthday=person_info["birthday"],
                        )
                    Credits.objects.create(
                        person_id=person_obj,
                        movie_id=movie,
                        department="Acting",
                        job=None,
                        character=person["character"],
                    )
            with ThreadPoolExecutor() as executor:
                executor.map(process_cast, credits["cast"])
                executor.map(process_crew, credits["crew"])

            if file_name and not Images.objects.filter(movie=movie).exists():
                img_url = image_url + file_name
                image = Images.objects.create(movie=movie, is_poster=True)
                image.get_image_from_url(img_url, file_name)
                image.save()

        df = pd.read_csv("links.csv")
        error_rows = []
        for index, row in df.iterrows():
            if get_movie_items(row["movieId"], row["tmdbId"]):
                print(row)
                print(index)
                error_rows.append(index)

        new_df = df.drop(error_rows)

        new_df.to_csv("new_df.csv")
