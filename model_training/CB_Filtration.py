import psycopg2
from scipy.sparse import coo_matrix
from datetime import datetime
from mov_rec import settings
import numpy as np
from homepage.models import Movies, Credits
from sentence_transformers import SentenceTransformer
import numpy as np


class CB_Filtration(object):
    def __init__(self, min_sim=0.1, model="all-MiniLM-L6-v2"):
        self.min_sim = min_sim
        self.db = settings.DATABASES['default']['ENGINE']
        self.model = SentenceTransformer(model)

    def load_data(self):
        movies = list(Movies.objects.all())
        ids = []
        name = []
        description = []
        genres = []
        cast = []
        writers = []
        directors = []
        for m in movies:
            ids.append(m.id)
            name.append(m.name)
            description.append(m.description)
            genres.append(m.genre_binary_list())
            cast.append(list(Credits.objects.filter(department='Acting', movie_id=m.id).values_list('person_id', flat=True)))
            writers.append(list(Credits.objects.filter(department='Writing', movie_id=m.id).values_list('person_id', flat=True)))
            directors.append(list(Credits.objects.filter(department='Directing', movie_id=m.id).values_list('person_id', flat=True)))
        

        self.data = {"id": ids, 
                "name": name,
                "description": description,
                "genres": genres,
                "cast": cast,
                "writers": writers,
                "directors": directors}

    def text_similarity(self, text):
        embeddings = self.model.encode(text)
        similarities = np.dot(embeddings, embeddings.T)
        norms = np.linalg.norm(embeddings, axis=1)
        similarities = similarities / np.outer(norms, norms)
        np.fill_diagonal(similarities, 1.0)
        return similarities

    def jaccard_similarity_genre(self):
        n = len(self.data["genres"])
        similarities = np.zeros((n, n))

        for i in range(n):
            print(i)
            for j in range(i, n):
                intersection = np.sum(np.logical_and(self.data["genres"][i], self.data["genres"][j]))
                union = np.sum(np.logical_or(self.data["genres"][i], self.data["genres"][j]))
                similarities[i, j] = intersection / union if union != 0 else 0
                similarities[j, i] = similarities[i, j]

        return similarities

    def jaccard_similarity_cast(self, data):
        n = len(data)
        similarities = np.zeros((n, n))

        for i in range(n):
            set_i = set(data[i])
            for j in range(i, n):
                set_j = set(data[j])
                intersection = len(set_i.intersection(set_j))
                union = len(set_i.union(set_j))
                similarities[i, j] = intersection / union if union != 0 else 0
                similarities[j, i] = similarities[i, j]

        return similarities

    def calc_similarity(self):
        self.load_data()
        plot_similarities = self.text_similarity(self.data["description"])
        title_similarities = self.text_similarity(self.data["name"])
        genre_similarities = self.jaccard_similarity_genre()
        cast_similarities = self.jaccard_similarity_cast(self.data["cast"])
        writer_similarities = self.jaccard_similarity_cast(self.data["writers"])
        director_similarities = self.jaccard_similarity_cast(self.data["directors"])

        start_time = datetime.now()

        print([
            genre_similarities ,
            title_similarities ,
            cast_similarities ,
            writer_similarities ,
            director_similarities ,
            plot_similarities
        ], sep="\n")

        self.similarity = (
            0.25 * genre_similarities +
            0.2 * title_similarities +
            0.2 * cast_similarities +
            0.15 * writer_similarities +
            0.1 * director_similarities +
            0.1 * plot_similarities
        )

        print(f'Similarity calculated in {datetime.now() - start_time} seconds')


    def save_similarities(self, created=datetime.now()):
            start_time = datetime.now()
            print(f'truncating table in {datetime.now() - start_time} seconds')
            sims = []
            no_saved = 0
            start_time = datetime.now()
            coo = coo_matrix(self.similarity)
            csr = coo.tocsr()

            print(f'instantiation of coo_matrix in {datetime.now() - start_time} seconds')

            query = "insert into cb_similarity (date, movie_1_id, movie_2_id, similarity) values %s;"

            conn= self.get_conn()
            cur = conn.cursor()

            cur.execute('truncate table cb_similarity')

            print(f'{coo.count_nonzero()} similarities to save')
            xs, ys = coo.nonzero()
            for x, y in zip(xs, ys):

                if x == y:
                    continue

                sim = float(csr[x, y])
                x_id = str(self.data["id"][x])
                y_id = str(self.data["id"][y])
                if sim < self.min_sim:
                    continue

                if len(sims) == 100000:
                    psycopg2.extras.execute_values(cur, query, sims)
                    sims = []
                    print(f"{no_saved} saved in {datetime.now() - start_time}")

                new_similarity = (str(created), x_id, y_id, sim)
                no_saved += 1
                sims.append(new_similarity)

            psycopg2.extras.execute_values(cur, query, sims, template=None, page_size=1000)
            conn.commit()
            print('{} Similarity items saved, done in {} seconds'.format(no_saved, datetime.now() - start_time))

    def get_conn(self):
        dbUsername = settings.DATABASES['default']['USER']
        dbPassword = settings.DATABASES['default']['PASSWORD']
        dbName = settings.DATABASES['default']['NAME']
        host = "db"
        port = "5432"
        conn_str = "dbname={} user={} password={} host={} port={}".format(dbName,
                                                          dbUsername,
                                                          dbPassword, host, port)
        print(conn_str)
        conn = psycopg2.connect(conn_str)
        return conn
