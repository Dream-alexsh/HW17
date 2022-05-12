# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()
director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)
genres_schema = GenreSchema(many=True)


api = Api(app)
movie_ns = api.namespace('movies')
director_ns = api.namespace('directors')
genre_ns = api.namespace('genres')


@movie_ns.route('/')
class MoviesView(Resource):
    def get(self):
        try:
            query = request.args['page']
            if query == '1':
                all_movies = db.session.query(Movie).limit(10).all()
                return movies_schema.dump(all_movies), 200
            elif query == '2':
                all_movies = db.session.query(Movie).limit(10).offset(10).all()
                return movies_schema.dump(all_movies), 200
        except Exception as e:
            return str(e), 404

    def post(self):
        req_json = request.get_json()
        new_movie = Movie(**req_json)
        db.session.add(new_movie)
        db.session.commit()
        db.session.close()

        return "", 201


@movie_ns.route('/<int:bid>')
class MovieView(Resource):
    def get(self, bid: int):
        try:
            movie = db.session.query(Movie.title, Movie.description).filter(Movie.id == bid).one()
            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404

    def put(self, bid: int):
        movie = db.session.query(Movie).get(bid)
        req_json = request.get_json()

        movie.title = req_json['title']
        movie.description = req_json['description']
        movie.trailer = req_json['trailer']
        movie.year = req_json['year']
        movie.rating = req_json['rating']
        movie.genre_id = req_json['genre_id']
        movie.director_id = req_json['director_id']

        db.session.add(movie)
        db.session.commit()
        db.session.close()

        return "", 204

    def patch(self, bid: int):
        movie = db.session.query(Movie).get(bid)
        req_json = request.get_json()

        if 'title' in req_json:
            movie.title = req_json['title']
        if 'description' in req_json:
            movie.title = req_json['description']
        if 'trailer' in req_json:
            movie.title = req_json['trailer']
        if 'year' in req_json:
            movie.title = req_json['year']
        if 'rating' in req_json:
            movie.title = req_json['rating']
        if 'genre_id' in req_json:
            movie.title = req_json['genre_id']
        if 'director_id' in req_json:
            movie.title = req_json['director_id']

        db.session.add(movie)
        db.session.commit()
        db.session.close()

        return "", 204

    def delete(self, bid: int):
        movie = db.session.query(Movie).get(bid)

        db.session.delete(movie)
        db.session.commit()
        db.session.close()

        return "", 204


@director_ns.route('/')
class DirectorsView(Resource):
    def get(self):
        try:
            directors = db.session.query(Director).all()
            return directors_schema.dump(directors), 200
        except Exception as e:
            return str(e), 404

    def post(self):
        req_json = request.get_json()
        new_director = Director(**req_json)
        db.session.add(new_director)
        db.session.commit()
        db.session.close()

        return "", 201


@director_ns.route('/<int:bid>')
class DirectorView(Resource):
    def get(self, bid: int):
        try:
            director = db.session.query(Director).filter(Director.id == bid).one()
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404

    def put(self, bid: int):
        director = db.session.query(Director).get(bid)
        req_json = request.get_json()

        director.name = req_json['name']

        db.session.add(director)
        db.session.commit()
        db.session.close()

        return "", 204

    def patch(self, bid: int):
        director = db.session.query(Director).get(bid)
        req_json = request.get_json()

        if 'name' in req_json:
            director.name = req_json['name']

        db.session.add(director)
        db.session.commit()
        db.session.close()

        return "", 204

    def delete(self, bid: int):
        director = db.session.query(Director).get(bid)

        db.session.delete(director)
        db.session.commit()
        db.session.close()

        return "", 204


@movie_ns.route('/d')
class DirectorViews(Resource):
    def get(self):
        try:
            query = request.args['director_id']
            movie = db.session.query(Movie).filter(Movie.director_id == query).all()
            return movies_schema.dump(movie), 200
        except Exception as e:
            str(e), 404


@movie_ns.route('/g')
class GenreView(Resource):
    def get(self):
        try:
            query = request.args['genre_id']
            genre = db.session.query(Movie).filter(Movie.genre_id == query).all()
            return movies_schema.dump(genre), 200
        except Exception as e:
            str(e), 404


@genre_ns.route('/')
class GenresView(Resource):
    def get(self):
        try:
            genres = db.session.query(Genre).all()
            return genres_schema.dump(genres), 200
        except Exception as e:
            str(e), 404

    def post(self):
        req_json = request.get_json()
        new_genre = Genre(**req_json)
        db.session.add(new_genre)
        db.session.commit()
        db.session.close()

        return "", 201


@genre_ns.route('/<int:bid>')
class GenreView(Resource):
    def get(self, bid: int):
        try:
            genre = db.session.query(Genre).filter(Genre.id == bid).all()
            return genres_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404

    def put(self, bid: int):
        genre = db.session.query(Genre).get(bid)
        req_json = request.get_json()

        genre.name = req_json['name']

        db.session.add(genre)
        db.session.commit()
        db.session.close()

        return "", 204

    def patch(self, bid: int):
        genre = db.session.query(Genre).get(bid)
        req_json = request.get_json()

        if 'name' in req_json:
            genre.name = req_json['name']

        db.session.add(genre)
        db.session.commit()
        db.session.close()

        return "", 204

    def delete(self, bid: int):
        genre = db.session.query(Genre).get(bid)

        db.session.delete(genre)
        db.session.commit()
        db.session.close()

        return "", 204


@movie_ns.route('/t')
class MovieView(Resource):
    def get(self):
        try:
            query_1 = request.args['director_id']
            query_2 = request.args['genre_id']
            movie = db.session.query(Movie).filter(Movie.genre_id == query_2, Movie.director_id == query_1).all()
            return movies_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404


if __name__ == '__main__':
    app.run(debug=True)
