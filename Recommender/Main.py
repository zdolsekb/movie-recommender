from UserItemData import UserItemData
from MovieData import MovieData
from RandomPredictor import RandomPredictor
from Recommender import Recommender
from AveragePredictor import AveragePredictor
from ViewsPredictor import ViewsPredictor
from ItemBasedPredictor import ItemBasedPredictor
from SlopeOnePredictor import SlopeOnePredictor

print("Branje ocen")
uim = UserItemData('../data/user_ratedmovies.dat')
print(uim.NRatings())
uim = UserItemData('../data/user_ratedmovies.dat', start_date='12.1.2007', end_date='16.2.2008', min_ratings=100)
print(uim.NRatings())

print()

print("Branje filmov")
md = MovieData('../data/movies.dat')
print(md.get_title(1))

print()

print("Naključni prediktor")
md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat')
rp = RandomPredictor(1, 5)
rp.fit(uim)
pred = rp.predict(78)
print(type(pred))
items = [1, 3, 20, 50, 100]
for item in items:
    print("Film: {}, ocena: {}".format(md.get_title(item), pred[item]))

print()

print("Priporočanje")
md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat')
rp = RandomPredictor(1, 5)
rec = Recommender(rp)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print()

print("Napovedovanje s povprečjem")
md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat')
ap = AveragePredictor(100)
rec = Recommender(ap)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print()

print("Priporočanje najbolj gledanih filmov")
md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat')
vp = ViewsPredictor()
rec = Recommender(vp)
rec.fit(uim)
rec_items = rec.recommend(78, n=5, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print()

print("Napovedovanje ocen s podobnostjo med produkti")
md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat', min_ratings=1000)
rp = ItemBasedPredictor()
rec = Recommender(rp)
rec.fit(uim)
print("Podobnost med filmoma 'Men in black'(1580) in 'Ghostbusters'(2716): ", rp.similarity(1580, 2716))
print("Podobnost med filmoma 'Men in black'(1580) in 'Schindler's List'(527): ", rp.similarity(1580, 527))
print("Podobnost med filmoma 'Men in black'(1580) in 'Independence day'(780): ", rp.similarity(1580, 780))

print()

print("Napovedovanje za posameznega uporabnika:")
print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print("Najbolj podobni filmi")
rp.sim_movies(20,md)

print()

print("Priporočanje glede na trenutno ogledano vsebino")
rec_items = rp.similarItems(4993, 10)
print('Filmi podobni "The Lord of the Rings: The Fellowship of the Ring": ')
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print()

print("Priporočilo zase")
uim = UserItemData('../data/user_ratedmovies_mojivnosi.dat', min_ratings=1000)
rp = ItemBasedPredictor()
rec = Recommender(rp)
rec.fit(uim)
print("Predictions for Blaz Zdolsek(-1): ")
rec_items = rec.recommend(-1, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print()

print("Slope one")
md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat', min_ratings=1000)
rp = SlopeOnePredictor()
rec = Recommender(rp)
rec.fit(uim)

print()

print("Predictions for 78: ")
rec_items = rec.recommend(78, n=15, rec_seen=False)
for idmovie, val in rec_items:
    print("Film: {}, ocena: {}".format(md.get_title(idmovie), val))

print()

print("Evalvacija")
md = MovieData('../data/movies.dat')
uim = UserItemData('../data/user_ratedmovies.dat', min_ratings=1000, end_date='1.1.2008')
rp = SlopeOnePredictor()
rec = Recommender(rp)
rec.fit(uim)

uim_test = UserItemData('../data/user_ratedmovies.dat', min_ratings=200, start_date='2.1.2008')
mse, mae, precision, recall, f = rec.evaluate(uim_test, 20)
print(mse, mae, precision, recall, f)