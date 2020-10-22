import shutil
import os
import faust
from bs4 import BeautifulSoup
from faust.web import Request, Response, View
from faustapp.app import app
from git import Repo
from datetime import datetime

articles_repo = "https://github.com/vandenbogart/art.vandenbog.articles.git"

class Article(faust.Record):
    title: str
    filename: str
    html: str
    deleted: bool = False
    created: datetime
    last_modified: datetime

topic = app.topic('articles', key_type=str, value_type=Article)

articles_table = app.Table(
        'articles_table',
        default=None,
        key_type=str,
        value_type=Article
)

def handle_error(func, path, execinfo):
    print('Unable remove directory' + path)

@app.page('/publish/')
class publish_articles(View):
    async def post(self, request: Request) -> Response:
        repo_name = 'temp_repo'
        print("Cloning articles repository...")
        shutil.rmtree(repo_name, ignore_errors=True) 
        repo = Repo.clone_from(articles_repo, repo_name)
        with os.scandir(repo_name) as entries:
            for entry in entries:
                if entry.is_file():
                    last_modified = repo.git.log('-1', format='%ci', 'a_good_time.html')
                    print(last_modified)
                    with open(entry, 'r') as f:
                        data = f.read()
                        soup = BeautifulSoup(data, 'html.parser')
                        print(soup.title.string)
                        print(data)
                        #await topic.send(key=entry.name, value=Article(title=soup.title.string, filename=entry.name, html=data))
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
        articles_table[article.filename] = article



