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

    def _calculate_score(self, name):

        video = self.collection.find_one({"name": name})
        video_up = video["thumbs_up"]
        video_down = video["thumbs_down"]
        score = video_up - (video_down / 2)
        query1 = {"name": name}
        query2 = {"$set": {"score": score}}
        self.collection.update(query1, query2)

    def thumbs_up(self, name):

        query1 = {"name": name}
        query2 = {"$inc": {"thumbs_up": 1}}
        self.collection.update(query1, query2)
        self._calculate_score(name)

    def thumbs_down(self, name):
        query1 = {"name": name}
        query2 = {"$inc": {"thumbs_down": 1}}
        self.collection.update(query1, query2)
        self._calculate_score(name)

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

    def get_theme_ranking(self):

        theme_score = {}
        ordened_theme_score = {}
        object_list = []
        for video in self.collection.find():

            if video["theme"] not in theme_score:

                theme_score[video["theme"]] = video["score"]

            else:

                theme_score[video["theme"]] += video["score"]

        for theme in sorted(theme_score, key=theme_score.get, reverse=True):

            ordened_theme_score[theme] = theme_score[theme]

        for key in ordened_theme_score:

            temp_dict = {"theme": key, "score": ordened_theme_score[key]}
            object_list.append(temp_dict)

        output = {"ranking": object_list}

        return output








db = Database()
number = 0


@view_config(route_name='home', renderer='templates/home_content.jinja2')
def home(request):

    name = ""

    if request.POST.get('name'):
        name = str(request.POST.get('name'))

        if request.POST.get('action') == "1":
            db.thumbs_up(name)

        else:
            db.thumbs_down(name)

    videos = db.get_videos()
    return videos


@view_config(route_name='themes', renderer='templates/themes_content.jinja2')
def themes(request):

    ranking = db.get_theme_ranking()

    return ranking


@view_config(route_name='create', renderer='json')
def create(request):
    name = str(request.POST.get('name'))
    theme = str(request.POST.get('theme'))
    db.upload_video(name, theme)

    return HTTPFound('/')