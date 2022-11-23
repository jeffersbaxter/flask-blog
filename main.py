import os

from flask import Flask, render_template, request
import requests
import smtplib, ssl

EMAIL = os.environ.get("EMAIL")
PASSWORD = os.environ.get("PASSWORD")
GMAIL_SMTP_SERVER = "smtp.gmail.com"
PORT = int(os.environ.get("PORT"))
context = ssl.create_default_context()

response = requests.get('https://api.npoint.io/91612816151b8a1ed4ac')
response.raise_for_status()
data = response.json()

blogs = data['blogs']

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", blogs=blogs)


@app.route('/about')
def about_redirect():
    return render_template('about.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        from_email = request.form["email"]
        phone = request.form["phone"]
        message = request.form["message"]

        with smtplib.SMTP_SSL(GMAIL_SMTP_SERVER) as connection:
            connection.login(user=EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=from_email,
                to_addrs=EMAIL,
                msg=f"Subject: Let's Connect!\n\nName: {name}\nEmail: {from_email}\nPhone: {phone}\nMessage: {message}"
            )

        return render_template('contact.html', message_sent=True)
    return render_template('contact.html', message_sent=False)


@app.route('/post/<int:blog_id>')
def get_post(blog_id):
    selected_post = None
    for blog in blogs:
        if blog['id'] == blog_id:
            selected_post = blog
    return render_template('post.html', post=selected_post)


if __name__ == "__main__":
    app.run(debug=True)
