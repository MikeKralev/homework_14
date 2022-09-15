import json
import sqlite3


def sqlite_query(query):
    """Получить данные из базы по запросу"""
    with sqlite3.connect("data/netflix.db") as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()


def title_function(title):
    """Вернуть отформатированные данные для одного кинофильма"""
    query = f""" SELECT title, country, release_year, listed_in, description
                    FROM netflix
                    WHERE title LIKE '%{title}%'
                    ORDER BY release_year DESC
                    LIMIT 1"""

    result = sqlite_query(query)

    formatted = {
        "title": result[0][0],
        "country": result[0][1],
        "release_year": result[0][2],
        "genre": result[0][3],
        "description": result[0][4]
    }
    return formatted


def between_years_function(from_year, to_year):
    """Вернуть отформатированные данные для списка кинофильмов в промежутке между годами"""
    query = f""" SELECT title, release_year
                    FROM netflix
                    WHERE release_year BETWEEN {from_year} and {to_year}
                    ORDER BY release_year ASC
                    LIMIT 100"""

    result = sqlite_query(query)

    formatted = []
    for el in result:
        formatted.append({"title": el[0], "release_year": el[1]})
    return formatted


def by_rating_function(group):
    """Вернуть отформатированные данные по рейтинговой группе"""
    list_of_ratings = {
        "children": "('G')",
        "family": ('G', 'PG', 'PG-13'),
        "adult": ('R', 'NC-17')
    }
    query = f"""SELECT title, rating, description
                    FROM netflix
                    WHERE rating IN {list_of_ratings[group.lower()]}
                    ORDER BY rating DESC"""
    result = sqlite_query(query)
    formatted = []
    for el in result:
        formatted.append({"title": el[0], "rating": el[1], "description": el[2]})
    return formatted


def by_genre_function(genre):
    """Вернуть отформатированные данные для списка кинофильмов по жанру"""
    query = f"""SELECT title, description
                    FROM netflix
                    WHERE listed_in LIKE '%{genre}%'
                    ORDER BY release_year DESC
                    LIMIT 10"""
    result = sqlite_query(query)
    formatted = []
    for el in result:
        formatted.append({"title": el[0], "description": el[1]})
    return formatted


def get_actor_pair(actor_1, actor_2):
    """ Получает в качестве аргументов имена двух актеров, возвращает список тех, кто играет с ними в паре больше 2
    раз """
    query = f"""SELECT netflix.cast
                FROM netflix
                WHERE netflix.cast LIKE '%{actor_1}%{actor_2}%'"""
    casts = (sqlite_query(query))

    actor_dict = {}
    for cast in casts:
        for actor in cast[0].split(', '):
            if actor in actor_dict:
                actor_dict[actor] += 1
            else:
                actor_dict[actor] = 1

    result = []
    for k, v in actor_dict.items():
        if v > 2 and k not in [actor_1, actor_2]:
            result.append(k)

    return ' '.join(result)


def get_by_type_year_genre(_type, year, genre):
    """ Получает в качестве аргументов тип, год, жанр кинокартины, возвращает список картин с их названиями и описаниями
        в JSON """
    query = f"""SELECT title, description
        FROM netflix
        WHERE type = '{_type}'
        AND release_year = {year}
        AND listed_in LIKE '%{genre}%'"""

    return json.dumps(sqlite_query(query))
