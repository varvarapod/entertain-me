import os

import pandas as pd

id = int('133093')

movie_db_path = 'data/imdb_mini.csv'
df_ = pd.read_csv(movie_db_path)
df_m = df_[df_['imdb_id'] == id]
#df = df[df['imdb_id'].to_string() == id]

df_l = df_m.iloc[:1]
df_h = df_l.reset_index(drop=True)

# movie = {'imdb_id': df_l['imdb_id'], 'title': df_l['title'], 'rating': df_l['rating'], 'image': df_l['poster_url'],
#          'summary': df_l['plot']}
# movie = df_l.values.tolist()

movies_list = []
for index, row in df_l.iterrows():
    movies_list.append({
        'imdb_id': row['imdb_id'],
        'title': row['title'],
        'rating': row['rating'],
        'image': row.get('poster_url'),
        'summary': row.get('plot'),
    })
movie = movies_list[0]
print('\nResult dataframe :\n', movies_list)
print('\n')
print(movie)