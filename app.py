from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
	return render_template('index.html')

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