from datetime import datetime
import time


class UserAction:

    def __init__(self, userId, movieId, action, score=0):
        self.userId: int = userId
        self.movieId: int = movieId
        self.timestamp: datetime = datetime.fromtimestamp(int(time.time()))
        self.action: str = action  # score click
        self.score = score

    def csvFormat(self):
        # if self.action == "score":
        #     return ",".join([str(i) for i in self.__dict__.values()])
        # else:
        #     return ",".join([str(i[1]) for i in self.__dict__.items() if i[0] != "score"])
        if self.action == "score":
            return ",".join(str(i) for i in [self.userId, self.movieId, self.score, self.timestamp])
        else:
            return ",".join(str(i) for i in [self.userId, self.movieId, self.timestamp])


# print(datetime.fromtimestamp(time.time()))
