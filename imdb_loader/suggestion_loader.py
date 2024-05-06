#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd
from recommendations.suggestion import results


def main():
    # movie_db_path = '../data/imdb_mini.csv'
    movie_db_output_path = '../data/imdb_mini_rec.csv'

    movies = pd.read_csv(movie_db_output_path, index_col=False)
    i = 0

    for index, row in movies.iterrows():
        #try:
        movie_name = row['movie_name']
        movie_id = row['imdb_id']
        recommendations = row['recommendations']
        if not recommendations or pd.isna(recommendations):
            print(i, "add recommendations: " + movie_name)
            recommendations = results(movies, movie_id, 5)
            print(recommendations, '\n')
            movies.at[i, 'recommendations'] = str(recommendations)
            if i % 100 == 0:
                print("Save DB: ", i)
                movies.to_csv(movie_db_output_path, index=False)
        i = i + 1
        # except (Exception,):
        #     print("Error get info for movie: " + movie_name)
        #     i = i + 1
        #     continue
        # finally:
        #     print("finally")
        #     movies.to_csv(movie_db_output_path, index=False)
    return 0


if __name__ == "__main__":
    main()
