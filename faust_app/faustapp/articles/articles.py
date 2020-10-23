'''Faust processor for articles'''
import shutil
import os
import faust
from bs4 import BeautifulSoup
from faust.web import Request, Response, View
from faustapp.app import app
from git import Repo
from datetime import datetime, timezone

ARTICLES_REPO = "https://github.com/vandenbogart/art.vandenbog.articles.git"

class Article(faust.Record):
    "Definition of an Article record"
    title: str
    filename: str
    html: str
    created_date: datetime
    last_modified_date: datetime
    deleted: bool = False

topic = app.topic('articles', key_type=str, value_type=Article)

articles_table = app.Table(
        'articles_table',
        default=None,
        key_type=str,
        value_type=Article
)

def handle_error(func, path, execinfo):
    "Generic message for debugging"
    print('Unable remove directory' + path)

@app.page('/reconcile/')
class ReconcileArticles(View):
    "HTTP request handler for worker"
    async def post(self, request: Request) -> Response:
        repo_name = 'temp_repo'
        print("Cloning articles repository...")
        shutil.rmtree(repo_name, ignore_errors=True)
        repo = Repo.clone_from(ARTICLES_REPO, repo_name)
        with os.scandir(repo_name) as entries:
            for entry in entries:
                if entry.is_file():
                    # fetch most recent dates for file from git repo
                    last_modified = repo.git.log('-1', entry.name, format='%aI')
                    lm_date = datetime.fromisoformat(last_modified)
                    # create or update existing article
                    if (entry.name in articles_table
                        and lm_date == articles_table[entry.name].last_modified_date):
                        # file has not been changed so do nothing
                        continue
                    else:
                        # create or update entry in article table
                        with open(entry, 'r') as f:
                            data = f.read()
                            soup = BeautifulSoup(data, 'html.parser')
                            await topic.send(
                                    key=entry.name,
                                    value=Article(
                                        title=soup.title.string,
                                        filename=entry.name,
                                        html=data,
                                        created_date=(articles_table[entry.name].created_date
                                            if entry.name in articles_table else datetime.now(
                                                timezone.utc
                                                )),
                                        last_modified_date=lm_date,
                                        deleted=False
                                        )
                                    )
        # mark articles as deleted
        for filename, article in articles_table.items():
            if not os.path.exists(os.path.join(repo_name, filename)):
                article.deleted = True
                await topic.send(
                        key=filename,
                        value=article)
        print("Cleaning up temporary files...")
        shutil.rmtree(repo_name, onerror=handle_error)
        return self.json({'error': None})

@app.page('/articles/{word}')
@app.table_route(table=articles_table, match_info='word')
async def get_articles(web, request, word):
    return web.json(list(articles_table.values()))

@app.agent(topic)
async def process_articles(articles):
    async for article in articles.group_by(Article.filename):
        print(article.filename)
        articles_table[article.filename] = article
