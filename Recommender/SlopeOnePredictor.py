import itertools
import pandas
import pickle

class SlopeOnePredictor:
    def __init__(self):
        self.data = None
        self.dict = {}
        self.diff = {}
    def fit(self, X):
        self.data = X.data
        if not self.dict:
            self.construct_diff()
        # with open('difs_ucna.pkl','rb') as input:
        #     self.diff = pickle.load(input)
    def predict(self, user_id):
        predicted_ratings = {}
        #pickle
        if not self.diff:
              self.construct_diff()
        # with open('difs_ucna.pkl','rb') as input:
        #     self.diff = pickle.load(input)
        user_data = self.data.loc[self.data['userID'] == user_id]
        user_rated = user_data[['movieID','rating']]
        user_r_d = pandas.Series(user_rated.rating.values,index=user_rated.movieID).to_dict()
        movies = self.data[~self.data['movieID'].isin(user_rated['movieID'])]
        predict_m = movies['movieID'].unique()
        dic_helper = pandas.DataFrame(self.diff)
        for movie in predict_m:
            imenovalec = 0
            stevec = 0
            for m in user_rated['movieID']:
                user_rating_m = user_r_d[m]
                d = self.diff[m,movie][0]
                n = self.diff[m,movie][1]
                stevec += (user_rating_m - d) * n
                imenovalec += n
            predicted_ratings[movie] = stevec / imenovalec
        return predicted_ratings

    def construct_diff(self):
        items = self.data.movieID.unique()
        l = items.tolist()
        for pair in itertools.product(l, repeat=2):
            if (pair[0] == pair[1]):  # se stestiraj!
                continue
            ratings1 = self.data.loc[self.data['movieID'] == pair[0]]
            ratings2 = self.data.loc[self.data['movieID'] == pair[1]]
            users = pandas.Series(list(set(ratings1['userID']).intersection(set(ratings2['userID']))))
            ratings = self.data.loc[self.data['userID'].isin(users)]
            matrix = ratings.pivot(index='userID', columns='movieID', values='rating')
            difs = matrix[pair[0]] - matrix[pair[1]]
            n = matrix.shape[0]
            dif = difs.sum() / n
            self.diff[pair] = (dif,n)
        with open('difs_ucna.pkl', 'wb') as output:
            pickle.dump(self.diff,output,pickle.HIGHEST_PROTOCOL)
        return self.diff