from flask import Flask, render_template, request
import pickle
import numpy as np
popular_df = pickle.load(open('new.popular.pkl','rb'))
book_list = pickle.load(open('book_list.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Num-Rating'].values),
                           rating=list(popular_df['Avg-Rating'].values),
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(pt.index == user_input)[0][0]
    distance = similarity[index]
    similar_items = sorted(list(enumerate(distance)), key=lambda x: x[1], reverse=True)[1:5]
    data = []
    for i in similar_items:
        item = []
        temp_df = book_list[book_list['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)
    print(data)
    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)