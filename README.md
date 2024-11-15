### Hello App

Hello App is a news review app that allows users verify that the title or image of a news article matches its description to address misinformation and clickbait.

#### Feature Breakdown

- AI-powered Text analysis
- Personalized Feed
- Human voting
- Leaderboard: The best contribution earns a certain amount every month.
- Image description matching
- Credibility Score
- Revamped headline that matches the description
- Real-time notification
- Insights and dashboard
- User Authentication
- Comment Section and Discussion
- Bookmarks


### Technologies

- HTML
- CSS
- Flask
- Postgresql

Running the Project

- Create a virtual environment

```
virtualenv -p python3 venv
```

- Install the packages in the requirements.txt file

```
pip install -r requirements.txt
```

- Add a .env file with a SECRET_KEY for the forms

```
SECRET_KEY='...'
```

- Add an SQLALCHEMY_DATABASE_URI for the postgresql database configuration to the env file

```
SQLALCHEMY_DATABASE_URI='...'
```

- Run the app
```
python app.py
```

### To perform a database migration

```
flask db init
```

```
flask db migrate -m "message"
```

```
flask db upgrade
```

NOTE:

- For the first time initialization of the db migrations, import the models to the env.py file to be able to migrate and subsequently upgrade.