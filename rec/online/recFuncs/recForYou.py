from copy import deepcopy
from typing import Dict, List

from rec.online.datastructer.DataManager import DataManager
from rec.online.datastructer.Movie import Movie
from rec.utils.redisManager import RedisManager

d = DataManager()
r = RedisManager()


def getRecList(userId, size, model):
    user = d.getUserById(userId)
    if user is None:
        return None
    CANDIDATE_SIZE = 800
    movies = d.getMovies(CANDIDATE_SIZE, "rating")  # matching: rating
    # TODO: load userEmb
    movies = rankingMovies(user, movies, model)
    movies = movies[:size-10]
    # hot top 10
    k = r.keys("hot*")
    candidates = {i[3:]: r.get(i) for i in k}
    print(k, candidates)
    for i in deepcopy(movies):
        if i.movieId in candidates.keys():
            movies.remove(i)
    print(movies)
    candidates = deepcopy(set([d.getMoviesById(int(m[0])) for m in sorted(candidates.items(), key=lambda i:i[1], reverse=True)[:10]]))
    for m in candidates:
        m.onhot = True
    print(candidates)
    print(movies)
    candidates.update(movies)
    return candidates


def rankingMovies(user, movies, model):
    candidates: Dict[Movie, float] = {}
    for i in movies:
        if model == "emb":
            similarity = calculateEmbSimilarScore(user, i)
            candidates[i] = similarity
        elif model == "nerualcf":
            # similarity = cal
            pass
        else:  # nerualcf
            candidates[i] = movies.index(i)
    candidates: List[Movie] = [c[0] for c in sorted(candidates.items(), key=lambda m: m[1], reverse=True)]
    return candidates


def calculateEmbSimilarScore(user, another):
    if user is None or another is None or user.getEmb() is None:
        return -1
    return user.getEmb().calculateSimilarity(another.getEmb())


# def calculateSimilarScore(movie, another):
#     same = 0
#     for i in movie.genres:
#         if another.genres.index(i) != -1:
#             same += 1
#     similarity = same / (len(movie.genres) + len(another.genres)) / 2
#     rating = another.averageRating / 5
#     simW = 0.7
#     ratW = 0.3
#     return simW * similarity + ratW * rating
