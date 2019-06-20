from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pymongo import MongoClient


class Database(object):

    def __init__(self):

        self.client = MongoClient()
        self.db = self.client["videos"]
        self.collection = self.db["videos"]

    def get_videos(self):

        videos = []
        for video in self.collection.find():
            videos.append(video)

        videos = {"videos": videos}

        return videos

    def thumbs_up(self, name):

        query1 = {"name": name}
        query2 = {"$inc": {"thumbs_up": 1}}
        self.collection.update(query1, query2)

    def thumbs_down(self, name):
        query1 = {"name": name}
        query2 = {"$inc": {"thumbs_down": 1}}
        self.collection.update(query1, query2)

    def upload_video(self, name, theme):

        video = {

            "name": name,
            "theme": theme,
            "thumbs_up": 0,
            "thumbs_down": 0,
            "score": 0
        }
        self.collection.insert(video)

        return {"response": "video created"}


db = Database()
number = 0


@view_config(route_name='home', renderer='templates/home_content.jinja2')
def home(request):

    name = ""

    if request.POST.get('name'):
        name = str(request.POST.get('name'))

        if request.POST.get('action') == "1":
            print("Joinha")
            db.thumbs_up(name)

        else:
            print("Não gostei")
            db.thumbs_down(name)

    videos = db.get_videos()
    return videos


@view_config(route_name='themes', renderer='templates/themes_content.jinja2')
def themes(request):

    return {}


@view_config(route_name='create', renderer='json')
def create(request):
    name = str(request.POST.get('name'))
    theme = str(request.POST.get('theme'))
    db.upload_video(name, theme)

    return HTTPFound('/')