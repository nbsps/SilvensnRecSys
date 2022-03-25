import os
import random

from flask import Flask, render_template, jsonify, session
from flask import request

from rec.nearline.UserAction import UserAction
from rec.nearline.kafkaManager import kafkaInc
from rec.online.datastructer.DataManager import DataManager
from rec.utils.object2jsonable import object2jsonable
import rec.online.recFuncs.similarRec as similarRec
import rec.online.recFuncs.recForYou as recForYou
from rec.utils.redisManager import RedisManager

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# @app.errorhandler(Exception)
# def global_exception_handler(e):
#     return 'Error', 500


@app.before_request
def global_header_set():
    if 'userId' not in session:
        session['userId'] = 1


# @app.route('/')
# @app.route('/index.html')
# def index():
#     return render_template('index.html')
#
#
# @app.route('/movie.html')
# def movie():
#     args = request.args
#     movieId = args['movieId']
#     userId = session['userId']
#     kafkaInc.send(UserAction(userId, movieId, "click").csvFormat())
#     return render_template('movie.html')


@app.route('/movieclick')
def movieclick():
    args = request.args
    movieId = args['movieId']
    userId = session['userId']
    kafkaInc.send(UserAction(userId, movieId, "click").csvFormat())
    return "ok", 200


# @app.route('/user.html')
# def user():
#     return render_template('user.html')
#
#
# @app.route('/collection.html')
# def collection():
#     return render_template('collection.html')


@app.route('/changeUid')
def changeUID():
    session['userId'] = request.args['uid']
    return "change success", 200, [('Content-Type', 'application/json; charset=utf-8')]


@app.route('/getAllUsers', methods=['GET'])
def getAllUsers():
    users = random.sample(list(dataManager.userMap.values()), 30)
    users = object2jsonable(users)
    return jsonify(users), 200, [('Content-Type', 'application/json; charset=utf-8')]


@app.route('/getAllGenres', methods=['GET'])
def getAllGenres():
    genres = random.sample([i[0] for i in sorted(dataManager.genreMoviesMap.items(), key=lambda g:len(g[1]), reverse=True)], 5)
    genres = object2jsonable(genres)
    return jsonify(genres), 200, [('Content-Type', 'application/json; charset=utf-8')]


@app.route('/getRecommendMovie', methods=['GET'])
def recommendM():
    args = request.args
    genre = args['genre']
    size = args['size']
    sortby = args['sortby']
    movies = dataManager.getMoviesByGenre(genre, int(size), sortby)
    movies = object2jsonable(movies)
    return jsonify(movies), 200, [('Content-Type', 'application/json; charset=utf-8')]


@app.route('/getHotMovies', methods=['GET'])
def recHotM():
    args = request.args
    size = args['size']
    # hot top 10
    r = RedisManager()
    k = r.keys("hot*")
    movies = {i[3:]: r.get(i) for i in k}
    movies = [dataManager.getMoviesById(int(m[0])) for m in sorted(movies.items(), key=lambda i: i[1], reverse=True)[:int(size)]]
    movies = object2jsonable(movies)
    return jsonify(movies), 200, [('Content-Type', 'application/json; charset=utf-8')]


@app.route('/getrecforyou', methods=['GET'])
def rec_for_you():
    args = request.args
    userId = args['id']
    size = args['size']
    model = args['model']
    movies = recForYou.getRecList(int(userId), int(size), model)
    movies = object2jsonable(movies)
    return jsonify(movies), 200, [('Content-Type', 'application/json; charset=utf-8')]


@app.route('/getsimilarmovie', methods=['GET'])
def rec_by_similarM():
    args = request.args
    movieId = args['movieId']
    size = args['size']
    model = args['model']
    movies = similarRec.getRecList(int(movieId), int(size), model)
    print(movies)
    movies = object2jsonable(movies)
    return jsonify(movies), 200, [('Content-Type', 'application/json; charset=utf-8')]


@app.route('/getmovie', methods=['GET'])
def movie_info():
    args = request.args
    movieId = args['id']
    movie = dataManager.getMoviesById(int(movieId))
    movie = object2jsonable(movie)
    return jsonify(movie), 200, [('Content-Type', 'application/json; charset=utf-8')]


@app.route('/getuser', methods=['GET'])
def user_info():
    args = request.args
    userId = args['id']
    user = dataManager.getUserById(int(userId))
    user = object2jsonable(user)
    return jsonify(user), 200, [('Content-Type', 'application/json; charset=utf-8')]


@app.after_request
def global_header_set(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


dataManager = DataManager()
dataManager.loadData('static/sampledata/movies.csv', 'static/sampledata/links.csv',
                     'static/sampledata/ratings.csv', 'static/modeldata/item2vecEmb.csv',
                     'static/modeldata/userEmb.csv', '', '')

if __name__ == '__main__':
    app.run(debug=True)
