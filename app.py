import json
from flask import Flask, render_template

app = Flask(__name__)

file_path = "data.json"

def load_data():
	articles = None
	with open(file_path, 'r') as data:
		articles = json.loads(data.read())
	return articles

@app.route("/")
def index():
	articles = load_data()
	return render_template('index.html', context=articles)

@app.route("/register")
def register():
	return render_template('auth/register.html')

@app.route('/login')
def login():
	return render_template('auth/login.html')

@app.route('/news/breaking-news/<slug>')
def show_news(slug):
	return render_template('news/index.html')

if __name__ == "__main__":
	app.run(debug=True)