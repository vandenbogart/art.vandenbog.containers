from flask import Flask
import app.articles as articles

app = Flask(__name__)

@app.route('/articles/<filename>')
def get_article_by_filename(filename):
    return articles.get_article_by_filename(filename)

@app.route('/articles')
def get_articles_list():
    return articles.get_articles_list()

@app.route('/reconcile-articles')
def reconcile_articles():
    return articles.reconcile_articles()
