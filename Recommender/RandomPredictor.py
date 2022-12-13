import random
import collections
class RandomPredictor:
    def __init__(self,min,max):
        self.min = min
        self.max = max
        self.data = None
    def fit(self,X):
        self.data = X.data
    def predict(self,user_id):
        items = self.data.movieID
        d = {}
        for item in items.unique():
            d[item] = random.randint(self.min,self.max)
        return d