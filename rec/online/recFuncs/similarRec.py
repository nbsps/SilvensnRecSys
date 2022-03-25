from typing import Set, Dict, List

from rec.online.datastructer.DataManager import DataManager
from rec.online.datastructer.Movie import Movie


d = DataManager()


def getRecList(movieId, size, model):
    movie = d.getMoviesById(movieId)
    if movie is None:
        return None
    movies = matchingMovies(movie)
    movies = rankingMovies(movie, movies, model)
    if len(movies) > size:
        return movies[:size]


# matching: genres
def matchingMovies(movie: Movie):
    candidates: Set[Movie] = set()
    genres = movie.genres
    for i in genres:
        movies = d.getMoviesByGenre(i, 100, "rating")
        candidates.update(movies)
    if movie in candidates:
        candidates.remove(movie)
    return list(candidates)


def rankingMovies(movie, movies, model):
    candidates: Dict[Movie, float] = {}
    for i in movies:
        if model == "emb":
            similarity = calculateEmbSimilarScore(movie, i)
        else:
            similarity = calculateSimilarScore(movie, i)
        candidates[i] = similarity
    candidates: List[Movie] = [c[0] for c in sorted(candidates.items(), key=lambda m: m[1], reverse=True)]
    return candidates


def calculateEmbSimilarScore(movie, another):
    if movie is None or another is None:
        return -1
    return movie.getEmb().calculateSimilarity(another.getEmb())


def calculateSimilarScore(movie, another):
    same = 0
    for i in movie.genres:
        if another.genres.index(i) != -1:
            same += 1
    similarity = same / (len(movie.genres) + len(another.genres)) / 2
    rating = another.averageRating / 5
    simw = 0.7
    ratw = 0.3
    return simw * similarity + ratw * rating
