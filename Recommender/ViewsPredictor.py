import pandas
import collections
class ViewsPredictor:
    def __init__(self):
        self.data = None
    def fit(self, X):
        self.data = X.data
    def predict(self, user_id):
        items = self.data.movieID.unique()
        movie_views = {}
        for movie_id in items:
            n = self.data[self.data['movieID'] == movie_id].count().values[0]
            movie_views[movie_id] = n
        return movie_views