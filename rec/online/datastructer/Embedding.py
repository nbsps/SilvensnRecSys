from math import sqrt
from typing import List


class Embedding:

    def __init__(self, embVector: List[float]=[]):
        self.embVector: List[float] = embVector

    def addElem(self, elem: float):
        self.embVector.insert(elem)

    def getEmbVector(self):
        return self.embVector

    def calculateSimilarity(self, anotherEmb) -> float:
        if(self.embVector is None or anotherEmb is None or anotherEmb.getEmbVector() or
                len(self.embVector) != len(anotherEmb.size())):
            return -1
        dotProduct = 0
        denominator1 = 0
        denominator2 = 0
        for i in range(len(self.embVector)):
            dotProduct += self.embVector[i] * anotherEmb[i]
            denominator1 += self.embVector[i] * self.embVector[i]
            denominator2 += anotherEmb[i] * anotherEmb[i]
        return dotProduct / sqrt(denominator1 * denominator2)


