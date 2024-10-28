from django.db.models import Q
from decimal import Decimal
from homepage.models import Ratings, MLRatings
from ..models import CFSimilarity


class CollaborativeRecommender:

    def __init__(self, min_sim=0.1, max_candidates=100):
        self.min_sim = min_sim
        self.max_candidates = max_candidates

    def get_similar_movies(self, movie_id, top_n=10):
        """
        Get top N similar movies for a given movie_id based on similarity score.
        """
        similar_movies = CFSimilarity.objects.filter(movie_1_id=movie_id, similarity__gte=self.min_sim) \
                                               .order_by('-similarity')[:top_n]
        recommendations = [(sim.movie_2_id, sim.similarity) for sim in similar_movies]
        return recommendations

    @staticmethod
    def seeded_rec(content_ids, take=6):
        """
        Get recommendations based on a set of seed content IDs.
        """
        data = CFSimilarity.objects.filter(movie_1__in=content_ids) \
                                    .order_by('-similarity') \
                                    .values('movie_2', 'similarity')[:take]
        return list(data)

    def recommend_items(self, user_id, num=6):
        active_user_items = Ratings.objects.filter(user_id=user_id).order_by('-score')[:100]
        active_user_items = active_user_items.values()
        if len(active_user_items) == 0:
            return []

        movie_ids = {movie['movie_id']: movie['score'] for movie in active_user_items}
        user_mean = sum(movie_ids.values()) / len(movie_ids)

        sims = CFSimilarity.objects.filter(Q(movie_1__in=movie_ids.keys())
                                            & ~Q(movie_2__in=movie_ids.keys())
                                            & Q(similarity__gt=self.min_sim)) \
                                    .order_by('-similarity')[:self.max_candidates]

        recs = {}
        targets = set(s.movie_2_id for s in sims if not s.movie_2_id == '')
        for target in targets:
            pre = 0
            sim_sum = 0
            rated_items = [sim for sim in sims if sim.movie_2_id == target]

            if len(rated_items) > 0:
                for sim_item in rated_items:
                    r = Decimal(movie_ids[sim_item.movie_1_id] - user_mean)
                    pre += sim_item.similarity * r
                    sim_sum += sim_item.similarity

                if sim_sum > 0:
                    recs[target] = {
                        'prediction': Decimal(user_mean) + pre / sim_sum,
                        'sim_items': [r.movie_1_id for r in rated_items]
                    }

        sorted_recs = sorted(recs.items(), key=lambda item: -float(item[1]['prediction']))
        return sorted_recs[:num]

    def predict_score(self, user_id, item_id, train=False):
        if train:
            user_items = MLRatings.objects.filter(user=user_id).exclude(movie_id=item_id).order_by('-score').values()[:100]
        else:
            user_items = Ratings.objects.filter(user_id=user_id).exclude(movie_id=item_id).order_by('-score').values()[:100]
        movie_ids = {movie['movie_id']: movie['score'] for movie in user_items}
        user_mean = sum(movie_ids.values()) / len(movie_ids)

        sims = CFSimilarity.objects.filter(Q(movie_1__in=movie_ids.keys())
                                            & Q(movie_2_id=item_id)
                                            & Q(similarity__gt=self.min_sim)).order_by('-similarity')

        pre = 0
        sim_sum = 0
        prediction = Decimal(0.0)

        if len(sims) > 0:
            for sim_item in sims:
                r = Decimal(movie_ids[sim_item.movie_1_id] - user_mean)
                pre += sim_item.similarity * r
                sim_sum += sim_item.similarity

            prediction = Decimal(user_mean) + pre / sim_sum
        return prediction
        

