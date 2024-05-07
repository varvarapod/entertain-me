import os
import ast
import pandas as pd
from flask import (Flask, redirect, render_template, request, session,
                   send_from_directory, url_for)

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

movie_db_path = 'data/imdb_mini.csv'
df = pd.read_csv(movie_db_path)
df.drop_duplicates(subset=['imdb_id'], inplace=True)


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/movie', methods=['GET', 'POST'])
def movie():
    id = request.args.get('id')
    if id:
        session['movieid'] = id
    elif 'movieid' in session:
        id = session['movieid']
    else:
        return redirect(url_for('index'))

    df_movie = df[df['imdb_id'] == int(id)].iloc[:1]

    if not df_movie.empty:
        movies_list = []
        for index, row in df_movie.iterrows():
            movies_list.append({
                'imdb_id': row['imdb_id'],
                'year': int(row['year']),
                'title': row['title'],
                'rating': row['rating'],
                'image': row.get('poster_url'),
                'summary': row.get('plot'),
                'recommendations': row.get('recommendations'),
            })
        movie = movies_list[0]

        # get suggestions ids from recommendations and receive suggestion movies df
        suggestions_ids = list(map(int, ast.literal_eval(movie['recommendations'])))
        #suggestions_ids =[23938]
        mask = df['imdb_id'].isin(suggestions_ids)
        suggestions_df = df[mask]

        # get suggestions list
        suggestions = []
        for index, row in suggestions_df.iterrows():
            suggestions.append({
                'imdb_id': row['imdb_id'],
                'year': int(row['year']),
                'title': row['title'],
                'rating': row['rating'],
                'image': row.get('poster_url'),
                'summary': row.get('plot'),
                'recommendations': row.get('recommendations'),
            })

        return render_template('movie.html', movie=movie, suggestions=suggestions)
    else:
        return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')




@app.route('/about', methods=['GET'])
def test():
    return render_template('about.html')


# Route for receiving user preferences and providing movie suggestions
@app.route('/movielist', methods=['GET', 'POST'])
def movielist():
    # Get user preferences from the form
    # genre = request.form.get('genre')
    # min_rating = float(request.form.get('min_rating'))
    name = request.form.get('name')
    page = int(request.args.get('page', 1))
    session['page'] = page
    per_page = 6

    if name:
        name = name.lower()
        session['moviesearch'] = name
    elif 'moviesearch' in session:
        name = session['moviesearch']
    else:
        return redirect(url_for('index'))

    # Search for movies based on user preferences
    # movies = ia.search_movie(genre)

    movies = df[df['title'].str.lower().str.contains("(?i)" + name)]

    movies_list = []
    for index, row in movies.iterrows():
        movies_list.append({
            'imdb_id': row['imdb_id'],
            'title': row['title'],
            'rating': row['rating'],
            'image': row.get('poster_url'),
            'summary': row.get('plot'),
        })

    # Pagination
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    num_pages = (len(movies_list) + per_page - 1) // per_page
    movies_list = movies_list[start_index:end_index]

    # Render the suggestions template with the movie suggestions and pagination data
    return render_template('list.html', movies_list=movies_list, page=page, num_pages=num_pages)


if __name__ == '__main__':
    app.run()
