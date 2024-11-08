import json
from flask import abort, render_template, flash, redirect, url_for, request
import pendulum
from slugify import slugify
from sqlalchemy import select
from app import app
from app import db
from app.forms import CreateArticleForm, LoginForm, SignUpForm
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
from urllib.parse import urlsplit

from app.models.article import Article
from app.models.user import User

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

@app.route('/hello')
def hello():
	return "hello, world"

@app.route("/")
def index():
	# articles = load_data()
	query = db.select(Article).order_by(Article.date_published.desc()).limit(5)
	articles = db.session.scalars(query).all()[:5]
	return render_template('index.html', context=articles)

@app.route("/register", methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = SignUpForm()
	if form.validate_on_submit():
		user = User(email=form.email.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Perfekt! You have been registered')
		return redirect(url_for('login'))
	return render_template('auth/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = LoginForm()
	if form.validate_on_submit():
		user = db.session.scalar(
			select(User).where(User.email == form.email.data)
        )
		if not user or not user.check_password(form.password.data):
			flash("Invalid Credentials")
			return redirect(url_for('login'))
		login_user(user, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or urlsplit(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(url_for('index'))
	return render_template('auth/login.html', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
	return render_template('dashboard/index.html')

@app.route('/dashboard/create/article', methods=['GET', 'POST'])
@login_required
def create_article():
	form = CreateArticleForm()
	if form.validate_on_submit():
		article = Article(title=form.title.data, 
					description=form.description.data, 
					is_published=form.published.data, author=current_user, image_url='')
		db.session.add(article)
		db.session.commit()
		flash('The article has been created')
		return redirect(url_for('dashboard'))
	return render_template('dashboard/create_article.html', form=form)

@app.route('/articles/<article_type>-articles/<slug>')
def show_article(slug, article_type):
	articles = load_data()
	context = [article for article in articles if slugify(article.get('title')) == slug]
	if len(context) < 1:
		abort(404)
	return render_template('articles/index.html', context=context[0])