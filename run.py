from flask import Flask, render_template
from utils import title_function, between_years_function, by_rating_function, by_genre_function

app = Flask(__name__)


@app.route("/movie/<title>")
def searching_by_title(title):
    """ Страница фильма по названию"""
    result = title_function(title)
    return render_template("searching_by_title.html", movie=result)


@app.route("/movie/<from_year>/to/<to_year>")
def show_list_between_years(from_year, to_year):
    """ Страница фильмов в промежутке годов"""
    result = between_years_function(from_year, to_year)
    return render_template("show_list_between_years.html", list=result)


@app.route('/rating/<group>')
def show_list_by_rating(group):
    """ Страница фильмов по рейтингу"""
    result = by_rating_function(group)
    return render_template("show_list_by_rating.html", list=result)


@app.route('/genre/<genre>')
def show_list_by_genre(genre):
    """ Страница фильмов по жанру"""
    result = by_genre_function(genre)
    return render_template("show_list_by_genre.html", list=result)


if __name__ == '__main__':
    app.run()
