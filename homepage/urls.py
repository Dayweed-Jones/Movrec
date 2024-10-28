"""mov_rec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import *

urlpatterns = [
    path("", Homepage_view.as_view(), name="home"),
    path("home", Homepage_view.as_view(), name="home_page"),
    path("signup", signup, name="signup"),
    path("search", search, name="search"),
    path("rate-movie", rate_movie, name="rate-movie"),
    path("watch-later", watch_later, name="watch-later"),
    path("watch-later-list", watch_later_list, name="watch-later-list"),
    path('history', history, name="wath-history"),
    path('top-rated', top_rated, name="top-rated"),
    path('movie/<int:movie_id>/', movie_details, name='movie-details'),
]
