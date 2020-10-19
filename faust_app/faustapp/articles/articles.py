import shutil
import os
import faust
from faust.web import Request, Response, View
from faustapp.app import app
from git import Repo

topic = app.topic('articles')

def handle_error(func, path, execinfo):
    print('Unable remove directory' + path)

@app.page('/articles/')
class process(View):
    async def post(self, request: Request) -> Response:
        repo_name = 'temp_repo'
        print("Cloning articles repository...")
        Repo.clone_from("https://github.com/vandenbogart/art.vandenbog.articles.git", repo_name)
        with os.scandir(repo_name) as entries:
            for entry in entries:
                if entry.is_file():
                    with open(entry, 'r') as f:
                        data = f.read()
                        print(entry.name)
                        print(data)
        print("Cleaning up temporary files...")
        shutil.rmtree(repo_name, onerror=handle_error) 
        return self.json({'error': None})




