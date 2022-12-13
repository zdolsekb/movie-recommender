import math
import pickle

import pandas
import collections
class Recommender:
    def __init__(self,predictor):
        self.predictor = predictor
        self.uim = None
    def fit(self,X):
        self.uim = X
        self.predictor.data = X.data
        self.predictor.fit(X) #testiraj
    def recommend(self, userID, n=10, rec_seen=True):
        items = self.predictor.predict(userID)
        df = pandas.DataFrame(list(items.items()), columns=['movieID', 'rating'])
        df = df.sort_values(['rating','movieID'], ascending=[False,True])
        if(~rec_seen):
            rated_movies = self.uim.data[self.uim.data['userID'] == userID].movieID
            df = df[~df['movieID'].isin(rated_movies)]
        df = df.head(n)
        d = pandas.Series(df.rating.values,index = df.movieID).to_dict()
        od = collections.OrderedDict(sorted(d.items()))
        l = list(od.items())
        return sorted(l, key=lambda x: (-x[1], x[0]))

    def evaluate(self,test_data,n):
        users = self.uim.data['userID'].unique()
        users_in_test = test_data.data['userID'].unique()
        rmseStevec = 0
        maeStevec = 0

        precisionStevec = 0
        precision = 0
        recall = 0
        cn = 0
        with open('difs_ucna.pkl','rb') as input:
            self.predictor.diff = pickle.load(input)

        for user in set(users_in_test).intersection(users):
            predictions = self.predictor.predict(user)
            user_ratings = test_data.data[test_data.data['userID'] == user]
            for key, value in sorted(predictions.items()):
                actual_rating = user_ratings[user_ratings['movieID'] == key]['rating']

                if(len(predictions) >= n and ~actual_rating.empty ):
                    precisionStevec+=1
                elif(len(predictions) >= n and actual_rating.empty):
                    precisionStevec-=1
                if(actual_rating.empty):
                    continue
                else:
                    actual_rating = actual_rating.values[0]
                    maeStevec += abs(value - actual_rating)
                    rmseStevec += math.pow((value - actual_rating),2)
                    cn+=1
            if(len(predictions) >= n and precisionStevec > 0):
                precision += (precisionStevec / len(predictions))
                if(user_ratings.shape[0] > n):
                    recall+= (precisionStevec / user_ratings.shape[0])
            precisionStevec = 0
        mae = maeStevec / cn
        rmse = math.sqrt(rmseStevec/cn)
        precision = precision / len(set(users_in_test).intersection(users))
        recall = recall / len(set(users_in_test).intersection(users))
        F1 = 2*recall*precision/(precision+recall)
        return rmse,mae,precision,recall,F1