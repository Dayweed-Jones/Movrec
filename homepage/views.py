from typing import Any
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import *
from .forms import RegistrationForm
from recsys.rec_models.CB import ContentBasedRecommender
from recsys.rec_models.CF import CollaborativeRecommender
from recsys.rec_models.Hybrid import FeatureWeightedLinearStacking
from django.db.models import Count, Avg
from django.db.models import Q


class Homepage_view(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            user_ratings = Ratings.objects.filter(user=self.request.user)
            context["ratings"] = user_ratings
            context["rated_movies"] = user_ratings.values_list("movie", flat=True)
            recommender = FeatureWeightedLinearStacking()
            movie_rec = recommender.recommend_items(
                user_id=self.request.user.id, num=36
            )
            movie_ids = [movie[0] for movie in movie_rec]
            movies = Movies.objects.filter(id__in=movie_ids)
        else:
            movies = Movies.objects.all()
        paginator = Paginator(movies, 18)

        page_number = self.request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        context["movies"] = page_obj

        return context


def movie_details(request, movie_id):
    movie = get_object_or_404(Movies, pk=movie_id)
    actors = Credits.objects.filter(movie_id=movie, department="Acting")
    directors = Credits.objects.filter(movie_id=movie, department="Directing")
    writers = Credits.objects.filter(movie_id=movie, department="Writing")
    poster = Images.objects.filter(movie=movie, is_poster=True).first()
    similair = ContentBasedRecommender().get_similar_movies(movie_id=movie_id, top_n=12)
    similair = [movie[0] for movie in similair]
    similair = Movies.objects.filter(id__in=similair)
    print(directors)
    context = {
        "movie": movie,
        "actors": actors,
        "directors": directors,
        "writers": writers,
        "poster": poster,
        "similair": similair,
    }
    return render(request, "movie_details.html", context)


def signup(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/home")

    else:
        form = RegistrationForm()

    return render(request, "registration/signup.html", {"form": form})


def search(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            ratings = Ratings.objects.filter(user=request.user)
        search = request.POST.get("search", "")
        rated_movies = Ratings.objects.values_list("movie", flat=True)
        movies = Movies.objects.filter(name__icontains=search)
        return render(
            request,
            "search.html",
            {"movies": movies, "ratings": ratings, "rated_movies": rated_movies, "search": search},
        )
    else:
        return render(request, "search.html")


def rate_movie(request):
    if request.method == "POST":
        mov_id = request.POST.get("mov_id")
        score = request.POST.get("score")
        user_id = request.user.id
        rating = Ratings.objects.filter(movie_id=mov_id, user_id=user_id).first()
        if rating:
            rating.score = score
            rating.save()
        else:
            rating = Ratings.objects.create(
                movie_id=mov_id, user_id=user_id, score=score
            )
            rating.save()
        return JsonResponse({"success": "true", "score": rating.score}, safe=True)
    return JsonResponse({"success": "false"})


def watch_later(request):
    if request.method == "POST":
        mov_id = request.POST.get("mov_id")
        user_id = request.user.id
        watch_later = List.objects.filter(movie_id=mov_id, user_id=user_id).first()
        if watch_later:
            watch_later.delete()
        else:
            watch_later = List.objects.create(movie_id=mov_id, user_id=user_id)
            watch_later.save()
        return JsonResponse({"success": "true"}, safe=True)
    return JsonResponse({"success": "false"})


def history(request):
    if request.user.is_authenticated:
        ratings = Ratings.objects.filter(user=request.user)
        watched_movies = Movies.objects.filter(Q(ratings__user=request.user))
        rated_movies = ratings.values_list("movie", flat=True)
        paginator = Paginator(watched_movies, 18)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "history.html",
            {"movies": page_obj, "ratings": ratings, "rated_movies": rated_movies},
        )
    else:
        return redirect("login")


def watch_later_list(request):
    if request.user.is_authenticated:
        ratings = Ratings.objects.filter(user=request.user)
        list = List.objects.filter(user=request.user)
        movies = Movies.objects.filter(id__in=list.values_list("movie", flat=True))
        rated_movies = ratings.values_list("movie", flat=True)
        paginator = Paginator(movies, 18)

        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(
            request,
            "watch_later.html",
            {
                "list": list,
                "movies": page_obj,
                "ratings": ratings,
                "rated_movies": rated_movies,
            },
        )
    else:
        return redirect("login")
    

def top_rated(request):
    if request.user.is_authenticated:
        ratings = Ratings.objects.filter(user=request.user)
    rated_movies = Ratings.objects.values_list("movie", flat=True)
    movies = (
    Movies.objects
    .annotate(
        num_ratings=Count('mlratings__user', distinct=True), 
        avg_score=Avg('mlratings__score')
    )
    .filter(num_ratings__gte=36)
    .order_by('-avg_score')
)
    paginator = Paginator(movies, 18)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    print(movies)
    return render(
            request,
            "homepage.html",
            {"movies": page_obj, "ratings": ratings, "rated_movies": rated_movies})
