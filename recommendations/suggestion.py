import pandas as pd
import numpy as np
import ast
from scipy import spatial
import operator


# https://hendra-herviawan.github.io/Movie-Recommendation-based-on-KNN-K-Nearest-Neighbors.html

def main():
    movie_db_path = '../data/imdb_mini.csv'
    movies = pd.read_csv(movie_db_path, index_col=False)
    movies['Id'] = range(1, len(movies) + 1)

    print('DB is loaded \n')

    all_genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                  'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
                  'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

    movieProperties = movies.drop(columns=['movie_name', 'imdb_id', 'title', 'genres',
                                           'plot', 'poster_url', 'year', 'rating', 'recommendations'])
    movieNumRatings = pd.DataFrame(movieProperties['votes'])
    movieNormalizedNumRatings = movieNumRatings.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    # print(movieNormalizedNumRatings.head())

    movieDict = {}
    for index, row in movies.head(len(movies) - 1).iterrows():
        # for index, row in movies.head(5).iterrows():
        Id = int(row['Id'])
        movie_id = row['imdb_id']
        title = row['title']
        genres = row['genres']
        rating = float(row['rating'])
        votes = float(row['votes'])

        movie_genres = ast.literal_eval(genres)
        genres_array = [1 if genre in movie_genres else 0 for genre in all_genres]
        movieDict[Id] = (title, genres_array, movieNormalizedNumRatings.loc[Id].get('votes'),
                         rating, movie_id)
        # print(movieDict[Id])
        # movie_genres = ['Animation', 'Adventure', 'Comedy', 'Family', 'Fantasy']
        # output_array = [1 if genre in movie_genres else 0 for genre in genres]

    # print(ComputeDistance(movieDict[1], movieDict[2]))
    K = 3
    avgRating = 0

    # m_id =

    m_id = findId(movieDict, int('0133093'))
    print('\n')
    print(movieDict[m_id], '\n')

    similar = []
    neighbors = getNeighbors(movieDict, m_id, K)  # Toy Story (1995)
    for neighbor in neighbors:
        avgRating += movieDict[neighbor][3]
        print(movieDict[neighbor][0] + " " + str(movieDict[neighbor][3]) + " " + str(movieDict[neighbor][4]))
        similar.append(str(movieDict[neighbor][4]))

    avgRating /= K
    print('\n', similar)

    return 0


def results(movies, imdb_id, recommendation_qty):
    recommendations_list = []
    movie_dict = combine_data(movies)
    recommendations_list = find_similar(movie_dict, imdb_id, recommendation_qty)
    return recommendations_list


def find_similar(movieDict, imdb_id, K):
    m_id = findId(movieDict, int(imdb_id))
    similar = []
    neighbors = getNeighbors(movieDict, m_id, K)
    for neighbor in neighbors:
        #print(movieDict[neighbor][0] + " " + str(movieDict[neighbor][3]) + " " + str(movieDict[neighbor][4]))
        similar.append(str(movieDict[neighbor][4]))
    return similar


def combine_data(movies):
    movies['Id'] = range(1, len(movies) + 1)
    all_genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
                  'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
                  'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']

    movieProperties = movies.drop(columns=['movie_name', 'imdb_id', 'title', 'genres',
                                           'plot', 'poster_url', 'year', 'rating', 'recommendations'])
    movieNumRatings = pd.DataFrame(movieProperties['votes'])
    movieNormalizedNumRatings = movieNumRatings.apply(lambda x: (x - np.min(x)) / (np.max(x) - np.min(x)))
    # print(movieNormalizedNumRatings.head())

    movieDict = {}
    for index, row in movies.head(len(movies) - 1).iterrows():
        # for index, row in movies.head(5).iterrows():
        Id = int(row['Id'])
        movie_id = row['imdb_id']
        title = row['title']
        genres = row['genres']
        rating = float(row['rating'])
        votes = float(row['votes'])

        movie_genres = ast.literal_eval(genres)
        genres_array = [1 if genre in movie_genres else 0 for genre in all_genres]
        movieDict[Id] = (title, genres_array, movieNormalizedNumRatings.loc[Id].get('votes'),
                         rating, movie_id)
    return movieDict


def ComputeDistance(a, b):
    genresA = a[1]
    genresB = b[1]
    genreDistance = spatial.distance.cosine(genresA, genresB)
    popularityA = a[2]
    popularityB = b[2]
    popularityDistance = abs(popularityA - popularityB)
    return genreDistance + popularityDistance


def getNeighbors(movie_dict, movieID, K):
    distances = []
    for movie in movie_dict:
        if movie != movieID:
            dist = ComputeDistance(movie_dict[movieID], movie_dict[movie])
            distances.append((movie, dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(K):
        neighbors.append(distances[x][0])
    return neighbors


def findId(movie_dict, imdb_id):
    res = 1
    for i in movie_dict:
        if movie_dict[i][4] == imdb_id:
            res = i
            break
    return res
