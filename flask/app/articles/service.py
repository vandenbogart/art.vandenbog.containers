import os
import shutil
from app.producers import ArticleProducer
from app.models import Article
from bs4 import BeautifulSoup
from git import Repo
from datetime import datetime, timezone
from pymongo import MongoClient

ARTICLES_REPO = "https://github.com/vandenbogart/art.vandenbog.articles.git"
client = MongoClient(os.environ['MONGO_CONNECT'])
db = client['articles_db']
col = db['articles']

def get_article_by_filename(filename):
    return col.find_one({'_id': filename})

def get_articles_list():
    return { 'articles': list(col.find({'deleted': False}, {'html': False}).sort('created_date', -1)) }

def reconcile_articles():
    producer = ArticleProducer()
    repo_name = 'temp_repo'
    print("Cloning articles repository...")
    shutil.rmtree(repo_name, ignore_errors=True)
    repo = Repo.clone_from(ARTICLES_REPO, repo_name)
    with os.scandir(repo_name) as entries:
        for entry in entries:
            if entry.is_file():
                existing_article = col.find_one({'_id': entry.name})
                last_modified = repo.git.log('-1', entry.name, format='%aI')
                lm_date = datetime.fromisoformat(last_modified)
                if (existing_article != None
                    and (datetime.fromisoformat(existing_article['last_modified_date']) == lm_date)):
                    "Skip files which have not changed"
                    continue
                created = repo.git.log(entry.name, format='%aI', diff_filter='A').split('\n')[-1]
                created_date = datetime.fromisoformat(created)
                with open(entry, 'r') as f:
                    data = f.read()
                    soup = BeautifulSoup(data, 'html.parser')
                    print('Publishing article key: ' + entry.name)
                    article = Article({
                                'title': soup.title.string,
                                'filename': entry.name,
                                'html': data,
                                'created_date': created_date.astimezone(tz=timezone.utc).isoformat(),
                                'last_modified_date': lm_date.astimezone(tz=timezone.utc).isoformat(),
                                'deleted': False
                    })
                    producer.send(article)
    "Mark non-existant articles for deletion"
    for article in col.find({}, {'_id':0}):
        article_c = Article(article)
        if not os.path.exists(os.path.join(repo_name, article_c.filename)):
            article_c.deleted = True
            producer.send(article_c)

    print("Cleaning up temporary files...")
    shutil.rmtree(repo_name)
    return "success"
