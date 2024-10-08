import json, pendulum
from flask import Flask, render_template, abort
from slugify import slugify

app = Flask(__name__)

@app.template_filter("humanize")
def humanize_date(date_string: str):
	date = pendulum.parse(date_string)
	return date.diff_for_humans()

@app.template_filter("slugify")
def slugify_text(slug):
	return slugify(slug)

app.jinja_env.filters['humanize_date'] = humanize_date
app.jinja_env.filters['slugify'] = slugify_text

file_path = "data.json"

def load_data() -> list[dict]:
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

@app.route('/articles/<article_type>-articles/<slug>')
def show_article(slug, article_type):
	articles = load_data()
	context = [article for article in articles if slugify(article.get('title')) == slug]
	if len(context) < 1:
		abort(404)
	return render_template('articles/index.html', context=context[0])

if __name__ == "__main__":
	app.run(debug=True)