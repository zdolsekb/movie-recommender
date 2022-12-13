import collections
from MovieData import MovieData
import pandas
import math
import itertools
class ItemBasedPredictor:
    def __init__(self,min_values=0,threshold=0):
        self.data = None
        self.min_values=min_values
        self.threshold = threshold
        self.dict = {}
    def fit(self, X):
        self.data = X.data
        self.construct_matrix()
    def user_sim(self, user_id):
        min_sim = 0.7
        user_similarities = {}
        our_user_avg_r = self.data.loc[self.data["userID"] == user_id].groupby('userID').mean()['rating'].values[0]
        our_user_movie_ratings = self.data.loc[self.data['userID'] == user_id]
        our_user_rated_movies = self.data.loc[self.data["userID"] == user_id]['movieID'].values
        other_users = self.data.loc[self.data['movieID'].isin(our_user_rated_movies)]['userID'].unique()
        other_users = other_users[other_users!=user_id]
        for user in other_users:
            other_user_movie_ratings = self.data.loc[self.data['userID'] == user]
            other_user_avg_r = self.data.loc[self.data["userID"] == user].groupby('userID').mean()['rating'].values[0]
            other_user_rated_movies = self.data.loc[self.data['userID'] == user]['movieID'].values
            both_rated = pandas.Series(list(set(our_user_rated_movies).intersection(set(other_user_rated_movies))))
            stevec = 0
            imenovalecLevo = 0
            imenovalecDesno = 0
            for movie in both_rated:
                our_user_movie_rating = our_user_movie_ratings[our_user_movie_ratings['movieID'] == movie]['rating'].values[0]
                other_user_movie_rating = other_user_movie_ratings[other_user_movie_ratings['movieID'] == movie]['rating'].values[0]
                stevec += (our_user_movie_rating - our_user_avg_r) * (other_user_movie_rating- other_user_avg_r)
                imenovalecLevo += math.pow((our_user_movie_rating - our_user_avg_r), 2)
                imenovalecDesno += math.pow((other_user_movie_rating- other_user_avg_r), 2)
            imenovalec = (math.sqrt(imenovalecLevo) * math.sqrt(imenovalecDesno))
            if(imenovalec == 0):
                sim = -1
            else:
                sim = stevec / imenovalec
            if(sim >= min_sim):
                user_similarities[user] = sim
        return user_similarities

    def predict(self, user_id):
        movies_predictions = {}
        user_similarities = self.user_sim(user_id)
        for movie in self.data.movieID.unique():
            stevec = 0
            imenovalec = 0
            our_user_avg_r = self.data.loc[self.data["userID"] == user_id].groupby('userID').mean()['rating'].values[0]
            for user in user_similarities:
                #je sploh ocenil
                try:
                    other_user_rating = self.data.loc[(self.data['userID'] == user) & (self.data['movieID'] == movie)]['rating'].values[0]
                except:
                    continue
                other_user_avg_r = self.data.loc[self.data["userID"] == user].groupby('userID').mean()['rating'].values[0]
                stevec += user_similarities[user] * (other_user_rating - other_user_avg_r)
                imenovalec+=user_similarities[user]
            movies_predictions[movie] = our_user_avg_r + stevec/imenovalec
        return movies_predictions

    def similarity(self,p1,p2):
        if not self.dict:
            self.construct_matrix()
            return self.dict[(p1, p2)]
        else:
            return self.dict[(p1,p2)]
    def construct_matrix(self):
        items = self.data.movieID.unique()
        l = items.tolist()
        for pair in itertools.product(l, repeat=2):
            if (pair[0] == pair[1]): #se stestiraj!
                continue
            self.dict[pair] = self.compute_similarity(pair[0],pair[1])
    def compute_similarity(self,p1,p2):
        usersP1 = self.data.loc[self.data['movieID'].isin([p1])]['userID']
        usersP2 = self.data.loc[self.data['movieID'].isin([p2])]['userID']
        users = pandas.Series(list(set(usersP1).intersection(set(usersP2))))

        r_avg = list(self.data.loc[self.data["userID"].isin(users)].groupby('userID').mean()['rating'])
        rua = list(self.data.loc[(self.data['movieID'] == p1) & (self.data['userID'].isin(users))]['rating'])
        rub = list(self.data.loc[(self.data['movieID'] == p2) & (self.data['userID'].isin(users))]['rating'])

        if (users.shape[0] < self.min_values):
            return 0.0

        imenovalec = 0
        stevecLevo = 0
        stevecDesno = 0
        for i, user in enumerate(users):
            imenovalec += (rua[i] - r_avg[i]) * (rub[i] - r_avg[i])
            stevecLevo += math.pow((rua[i] - r_avg[i]), 2)
            stevecDesno += math.pow((rub[i] - r_avg[i]), 2)
        sim = imenovalec / (math.sqrt(stevecLevo) * math.sqrt(stevecDesno))
        if (sim < self.threshold):
            return 0.0
        return sim

    def sim_movies(self,n=20,md=None):
        if not self.dict:
             self.construct_matrix()
        od = collections.OrderedDict(sorted(self.dict.items()))
        i=0
        for t in sorted(od, key=od.get, reverse=True):
            i+=1
            if(i == n):
                break
            f1 = md.get_title(t[0])
            f2 = md.get_title(t[1])
            print("Film1: {} Film2: {} Sim: {}".format(f1,f2,od[t]))

    def similarItems(self, item, n):
        if not self.dict:
             self.construct_matrix()
        d = {}
        for key in self.dict:
            if(key[0] != item and key[1] != item):
                continue
            if(key[0] == n):
                d[key[1]] = self.dict[key]
            else:
                d[key[0]] = self.dict[key]
        od = collections.OrderedDict(sorted(d.items()))
        l = list(od.items())
        sl= sorted(l, key=lambda x: (-x[1], x[0]))
        return sl[:n]