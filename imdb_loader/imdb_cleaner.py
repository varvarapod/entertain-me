import pandas as pd
def main():

    movie_db_path = '../data/imdb_mini.csv'
    movies = pd.read_csv(movie_db_path, index_col=False)
    movies.dropna(subset=['movie_name', 'imdb_id', 'title', 'genres',
                          'plot', 'poster_url', 'year', 'rating', 'votes'], inplace=True)
    movies.to_csv(movie_db_path, index=False)
    return 0

if __name__ == "__main__":
    main()