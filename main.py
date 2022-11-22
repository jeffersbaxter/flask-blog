from flask import Flask, render_template
import requests

response = requests.get('https://api.npoint.io/91612816151b8a1ed4ac')
response.raise_for_status()
data = response.json()

blogs = data['blogs']

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", blogs=blogs)


@app.route('/post/<int:blog_id>')
def get_post(blog_id):
    selected_post = None
    for blog in blogs:
        if blog['id'] == blog_id:
            selected_post = blog
    return render_template('post.html', post=selected_post)


if __name__ == "__main__":
    app.run(debug=True)
