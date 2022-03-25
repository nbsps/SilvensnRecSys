class Rating:

    def __init__(self, movie_Id, user_Id, score, timestamp):
        self.movieId: int = movie_Id
        self.userId: int = user_Id
        self.score: float = score
        self.timestamp: int = timestamp
