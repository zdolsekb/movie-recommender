class AveragePredictor:
    def __init__(self, b):
        self.b = b
        self.data = None
    def fit(self, X):
        self.data = X.data
    def predict(self, user_id):
        items = self.data.movieID.unique()
        g_avg = self.data['rating'].mean()
        movie_rating = {}
        #print(pandas.Series(items).is_unique)
        for movie_id in items:
            vs = self.data.loc[self.data['movieID'] == movie_id]['rating'].sum()
            n =  self.data[self.data['movieID'] == movie_id].count().values[0]
            movie_rating[movie_id] = (vs + self.b * g_avg) / (n + self.b)
        return movie_rating