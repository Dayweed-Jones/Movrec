from django.template import Library




register = Library()

@register.filter()
def get_movie_rating(object, id):
    return object.filter(movie=id).first()
