import os

import pandas as pd
from flask import (Flask, redirect, render_template, request, session,
                   send_from_directory, url_for)

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))

# Route for receiving user preferences and providing movie suggestions
@app.route('/movielist', methods=['GET', 'POST'])
def movielist():
    # Get user preferences from the form
    # genre = request.form.get('genre')
    # min_rating = float(request.form.get('min_rating'))
    name = request.form.get('name')
    page = int(request.args.get('page', 1))
    per_page = 1

    if name:
        name = name.lower()
        session['moviesearch'] = name
    elif 'moviesearch' in session:
        name = session['moviesearch']
    else:
        return redirect(url_for('index'))


    # Search for movies based on user preferences
    #movies = ia.search_movie(genre)
    movie_db_path = 'data/imdb_mini.csv'
    df = pd.read_csv(movie_db_path)
    movies = df[df['title'].str.lower().str.contains("(?i)" + name)]

    movies_list = []
    for index, row in movies.head(4).iterrows():
        movies_list.append({
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
