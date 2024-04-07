#!/usr/bin/env python
# -*- coding: utf-8 -*-
import imdb
import pandas as pd

# creating instance of IMDb
ia = imdb.IMDb()

def getMovie(movie_name):
    # searching the Id
    movies = ia.search_movie(movie_name)
    movieId = movies[0].movieID
    movie = ia.get_movie(movieId)
    return movie

def main():
    movie_db_path = 'data/imdb_mini.csv'
    movies = pd.read_csv(movie_db_path)
    i = 0
    #for index, row in movies.head(6).iterrows():
    for index, row in movies.iterrows():
        try:
            movie_name = row['movie_name']
            movie_id = row['imdb_id']
            if not movie_id or pd.isna(movie_id):
                print("add: " + movie_name)
                mv = getMovie(movie_name)
                imdb_id = str(mv.get('imdbID'))
                title = str(mv.get('title'))
                genres = str(mv.get('genres'))
                plot = str(mv.get('plot outline'))
                poster_url = str(mv.get('full-size cover url'))
                year = str(mv.get('year'))
                rating = str(mv.get('rating'))
                votes = str(mv.get('votes'))

                movies.at[i, 'imdb_id'] = imdb_id
                movies.at[i, 'title'] = title
                movies.at[i, 'genres'] = genres
                movies.at[i, 'plot'] = plot
                movies.at[i, 'poster_url'] = poster_url
                movies.at[i, 'year'] = year
                movies.at[i, 'rating'] = rating
                movies.at[i, 'votes'] = votes
            i = i + 1
        except:
            print("Error get info for movie: " + movie_name)
            i = i + 1
            continue
        finally:
            #print("finally")
            movies.to_csv(movie_db_path, index=False)
    return 0


if __name__ == "__main__":
    main()
