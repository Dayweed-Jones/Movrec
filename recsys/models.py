from django.db import models
from homepage.models import Movies


class CBSimilarity(models.Model):
    date = models.DateField()
    movie_1 = models.ForeignKey(Movies, on_delete=models.CASCADE, null=False, related_name='cb_similarity_set_1')
    movie_2 = models.ForeignKey(Movies, on_delete=models.CASCADE, null=False, related_name='cb_similarity_set_2')
    similarity = models.DecimalField(max_digits=8, decimal_places=7)

    class Meta:
        db_table = 'cb_similarity'

class CFSimilarity(models.Model):
    date = models.DateField()
    movie_1 = models.ForeignKey(Movies, on_delete=models.CASCADE, null=False, related_name='col_similarity_set_1')
    movie_2 = models.ForeignKey(Movies, on_delete=models.CASCADE, null=False, related_name='col_similarity_set_2')
    similarity = models.DecimalField(max_digits=8, decimal_places=7)

    class Meta:
        db_table = 'col_similarity'
