from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import string
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqlite.db'    #os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Urls(db.Model):
	id_ = db.Column("id_", db.Integer, primary_key=True)
	long = db.Column("long", db.String())
	short = db.Column("short", db.String(5))
	visits = db.Column(db.Integer, default=0)
	date_created = db.Column(db.DateTime, default=datetime.now)
	hourly_visit = db.Column(db.Float, default=0)

	def __init__(self, long, short):
		self.long = long
		self.short = short

@app.before_first_request
def create_tables():
    db.create_all()

def shorten_url():
	letters = string.digits + string.ascii_letters
	while True:
		rand_letters = random.choices(letters, k=5)
		rand_letters = "".join(rand_letters)
		short_url = Urls.query.filter_by(short=rand_letters).first()
		if not short_url:
			return rand_letters

@app.route('/', methods=['POST', 'GET'])
def home():
	if request.method == "POST":
		url_recieved = request.form["nm"]
		found_url = Urls.query.filter_by(long=url_recieved).first()
		if found_url:
			return redirect(url_for("display_short_url", url=found_url.short))
			
		else:
			short_url = shorten_url()
			new_url = Urls(url_recieved, short_url)
			db.session.add(new_url)
			db.session.commit()
			return redirect(url_for("display_short_url", url=short_url))

	else:
		return render_template('home.html')

@app.route('/display/<url>')
def display_short_url(url):
	return render_template('shorturl.html', short_url_display=url)	

@app.route('/<short_url>')
def redirection(short_url):
	long_url = Urls.query.filter_by(short=short_url).first()
	long_url.visits = long_url.visits + 1

	db.session.commit()

	if long_url:
		return redirect(long_url.long)
	else:
		return f'<h1>Url doesnt exist</h1>'

@app.route('/stats')
def display_all():
	urls = Urls.query.all()
	for url in urls:
		hourly_delta =  datetime.now() - url.date_created
		hourly_delta = hourly_delta.total_seconds() / 3600	
		if hourly_delta <= 1:
			url.hourly_visit = url.visits
		else:
			url.hourly_visit = round((float(url.visits) / hourly_delta), 1)
	
	db.session.commit()
	return render_template('stats.html', vals=Urls.query.all())


@app.route('/search/<search_term>')
def search(search_term):    
	results = Urls.query.filter(Urls.long.like('%'+search_term+'%')).all()
	if results:
		return render_template('search.html', vals=results)
	else:
		return f'<h1>Url doesnt exist</h1>'


if __name__ == '__main__':
	app.run(port=5000, debug=True)
