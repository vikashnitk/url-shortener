# URL Shortener API

A simple URL shortener API built with Flask and PostgreSQL.


## Run Locally

Open the terminal and clone the project

```bash
  git clone https://github.com/vikashnitk/url-shortener.git
  cd url-shortener

```
Create virtual environment

```bash
  Unix/macOS: python3 -m venv env
  Windows: py -m venv env

```
Activate virtual environment

```bash
  Unix/macOS: source env/bin/activate
  Windows: .\env\Scripts\activate

```
Install the dependencies

```bash
  pip install -r requirements.txt

```
#### Configuration
- Set tha path of Postgresql database (postgresql://username:password@localhost/database_name) to DATABASE_URL in app.py file
```bash
  app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///sqlite.db')
```
- Convert the URL in shorturl.html & stats.html pages in template file
```bash
  from https://url-shortener-v.herokuapp.com to http://127.0.0.1:5000

```

Start the server

```bash
  python app.py

```

## Usage

Open the browser to http://127.0.0.1:5000

To generate a short URL, simply pass a long URL in given box at home page and submit.

This will return a shortened URL such as:
```bash
  http://127.0.0.1:5000/keFl0
  ```
When a user opens the short URL they will be redirected to the long URL location.


#### Statistics

API stores the metadata about short URL - total number of hits, hourly hits. It is available at:

  http://127.0.0.1:5000/stats
 
#### Search

API have an endpoint for search. Search returns results matching the title of the URL
```bash
  http://127.0.0.1:5000/search/<search_term>
  ```
Say the term “Python”, API will return all pages which have a partial or full match for the term
```bash
  http://127.0.0.1:5000/search/python
  ```

## API hosted on Heroku


  
  https://url-shortener-v.herokuapp.com/


