from pyramid.view import view_config
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

    def thumbs_up(self):
        pass

    def thumbs_down(self):
        pass

    def upload_video(self, name, theme):
        pass


@view_config(route_name='home', renderer='templates/home_content.jinja2')
def home(request):

    db = Database()
    videos = db.get_videos()

    return videos


@view_config(route_name='themes', renderer='templates/themes_content.jinja2')
def themes(request):
    return {}


@view_config(route_name='create', renderer='json')
def create(request):
    name = str(request.POST.get('name'))
    theme = str(request.POST.get('theme'))
    return {"response": "video created"}