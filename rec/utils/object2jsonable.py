from typing import List, TypeVar, Union

from flask import jsonify

from rec.online.datastructer.Movie import Movie
from rec.online.datastructer.Embedding import Embedding

T = TypeVar('T', object, List[object])

# int(bool)、float、bool、complex  y
# str  y
# - list  y
# - tuple y
# - set   x
# dict    y
# object  x


def simpleType(x):
    for i in [int, str, float, bool, complex, str]:
        if type(x) == i:
            return True
    return False


def object2jsonable(obj: T):
    if obj is None:
        return []
    if simpleType(obj):
        return obj
    if type(obj) == list:
        nobj = []
        for i in obj:
            nobj.append(object2jsonable(i))
        return nobj
    if type(obj) == tuple:
        nobj = []
        for i in obj:
            nobj.append(object2jsonable(i))
        return tuple(nobj)
    if type(obj) == set:
        nobj = []
        for i in obj:
            nobj.append(object2jsonable(i))
        return nobj
    if type(obj) == dict:
        nobj = {}
        for i in obj.keys():
            nobj[i] = object2jsonable(obj[i])
        return nobj
    # objson = dict(obj.__dict__)  # object
    # priname = "_" + obj.__class__.__name__
    # for i in objson.keys():
    #     if i.startswith(priname):
    #         objson.pop(i)
    #         continue
    #     print(priname, i, i.startswith(priname))
    #     objson[i] = object2jsonable(objson.get(i))
    objson = {}  # object
    obdict = obj.__dict__
    priname = "_" + obj.__class__.__name__
    for i in obdict.keys():
        if i.startswith(priname):
            continue
        objson[i] = object2jsonable(obdict.get(i))
    return objson

# a = 1
# print(isinstance(a, tuple))
# print(type(Simple))

m = set([1, 3])
print(object2jsonable(m))

# m = [Movie(1, (1, {'2': Movie(3, Movie(1, 1, 3, ["5"]), 3, ["3"])}), 1, ["1"])]
# [{'imdbId': '', 'tmdbId': '', 'ratingNumber': 0, 'averageRating': 0, 'ratings': [], 'emb': [], 'movieFeatures': {}, 'topRatings': [], 'movie_Id': 1, 'releaseYear': 1, 'title': 1, 'genres': ['1']}, {'imdbId': '', 'tmdbId': '', 'ratingNumber': 0, 'averageRating': 0, 'ratings': [], 'emb': [], 'movieFeatures': {}, 'topRatings': [], 'movie_Id': 2, 'releaseYear': 2, 'title': 2, 'genres': ['2']}]
# m = object2jsonable(m)
# print(m)
# print(jsonify(m))

# m = Movie(1, 1, 1, ["1"])
# m.setEmb(Embedding([1.1, 2.1]))
# d = m.__dict__
# print(m.emb)
# print(object2jsonable(m))
# print(m.emb)
# print(d["movieId"])
# print(m.movieId)
# d = dict(d)
# d["movieId"] = 2423
# print(d["movieId"])
# print(m.movieId)
