from typing import List, Dict
from rec.online.datastructer.Rating import Rating
from rec.online.datastructer.Embedding import Embedding


class User:

    def __init__(self, user_Id):
        self.userId: int = user_Id
        self.averageRating: float = 0
        self.highestRating: float = 0
        self.lowestRating: float = 5.0
        self.ratingCount: int = 0

        self.__ratings: List[Rating] = []
        self.__emb: Embedding = None
        self.__userFeatures: Dict[str, str] = {}

    def addRating(self, rating):
        self.__ratings.append(rating)

    def setEmb(self, emb):
        self.__emb = emb

    def getEmb(self):
        return self.__emb
