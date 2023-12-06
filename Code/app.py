from flask import Flask,render_template,request
import pandas as pd
import numpy as np

df = pd.read_pickle("popular.pkl")
pivot = pd.read_pickle("pivot.pkl")
finaldf = pd.read_pickle("finaldf.pkl")
similarityscores = pd.read_pickle("similarityscores.pkl")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           movie_title = list(df['title'].values),
                           num_ratings=list(df['num_ratings'].values),
                           avg_ratings=list(df['average_rating'].values))

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_movies',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pivot.index == user_input)[0][0]
    similar_items = sorted(list(enumerate(similarityscores[index])),key=lambda x:x[1],reverse=True)[1:6]

    data = []
    for i in similar_items:
        item = []
        temp_df = finaldf[finaldf['title'].reindex(finaldf.index) == pivot.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('title')['title'].values))
        item.extend(list(temp_df.drop_duplicates('title')['genres'].values))
        item.extend(list(temp_df.drop_duplicates('title')['rating'].values))
        item.extend(list(temp_df.drop_duplicates('title')['movieId'].values))
        data.append(item)
    print(data)
    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)
