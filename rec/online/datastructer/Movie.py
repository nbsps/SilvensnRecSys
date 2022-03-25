from typing import List, Dict
from rec.online.datastructer.Rating import Rating
from rec.online.datastructer.Embedding import Embedding


class Movie:
    TOP_RATING_SIZE: int = 10

    def __init__(self, movieId, title, releaseYear, genres):
        self.imdbId: str = ""
        self.tmdbId: str = ""
        self.ratingNumber: int = 0
        self.averageRating: float = 0
        self.__ratings: List[Rating] = []
        self.__emb: Embedding = None
        self.__movieFeatures: Dict[str, str] = {}
        self.__topRatings: List[Rating] = []

        self.movieId: int = movieId
        self.releaseYear: int = releaseYear
        self.title: str = title
        self.genres: List[str] = []
        for i in genres:
            self.genres.append(i)

    def setImdbId(self, imdbId):
        self.imdbId = imdbId

    def setTmdbId(self, tmdbId):
        self.tmdbId = tmdbId

    def addRating(self, rating):
        self.averageRating = (self.averageRating * self.ratingNumber + rating.score ) / (self.ratingNumber + 1)
        self.ratingNumber = self.ratingNumber + 1
        self.__ratings.append(rating)

    def addTopRating(self, rating):
        index = 0
        for r in self.__topRatings:
            if r.score < rating:
                break
            index += 1
        self.__topRatings.insert(index, rating)
        if len(self.__topRatings) > self.TOP_RATING_SIZE:
            self.__topRatings.pop(self.TOP_RATING_SIZE)

    def setEmb(self, emb):
        self.__emb = emb

    def getEmb(self):
        return self.__emb

# m = Movie()
# m1 = Movie()
# print(m.topRatings == m1.topRatings)
