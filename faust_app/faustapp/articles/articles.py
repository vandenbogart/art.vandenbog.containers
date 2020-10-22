import shutil
import requests
import os
import faust
from bs4 import BeautifulSoup
from faust.web import Request, Response, View
from faustapp.app import app
from git import Repo

gitrepo = 'https://github.com/vandenbogart/art.vandenbog.articles.git'

class Article(faust.Record):
    title: str
    filename: str
    html: str
    deleted: bool = False

topic = app.topic('articles', key_type=str, value_type=Article)

articles_table = app.Table(
        'articles_table',
        default=None,
        key_type=str,
        value_type=Article
)

def handle_error(func, path, execinfo):
    print('Unable remove directory' + path)

@app.page('/reconcile/')
class reconcile_articles(View):
    async def post(self, request: Request) -> Response:

        changelog = await request.text()
        print(changelog)
        split_lines = changelog.split('\n')
        # drop metadata about sha
        split_lines.pop(0)
        for item in split_lines:
            op, filename = item.split('\t')
            if op == 'A' or op == 'M' or op == 'D':
                print('Detected changed file: ' + op + ' ' + filename)
                print('Fetching updated version...')
                article = requests.get(gitrepo + filename)
                print('Parsing file...')
                soup = BeautifulSoup(article.text, 'html.parser')
                print('Publishing change to topic...')
                await topic.send(key=filename,
                            value=Article(
                                title=soup.title.string,
                                filename=filename,
                                html=article.text,
                                deleted=True if op == 'D' else False
                                )
                            )
            else:
                print('Unrecognized operation: ' + op + ' ignoring line.')
                continue
        return self.json({'error': None})

@app.page('/articles/{word}')
@app.table_route(table=articles_table, match_info='word')
async def get_articles(web, request, word):
    return web.json(list(articles_table.values()))

@app.agent(topic)
async def process_articles(articles):
    async for article in articles.group_by(Article.filename):
        articles_table[article.filename] = article



