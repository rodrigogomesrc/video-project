from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/home_content.jinja2')
def home(request):
    return {'project': 'video-project'}


@view_config(route_name='videos', renderer='templates/video_content.jinja2')
def videos(request):

    videos = {"videos": [
        {"video_name": "video1", "video_theme": "tema"},
        {"video_name": "video2", "video_theme": "tema"},
        {"video_name": "video3", "video_theme": "tema"},
        {"video_name": "video4", "video_theme": "tema"},
        {"video_name": "video5", "video_theme": "tema"},
        {"video_name": "video6", "video_theme": "tema"}
    ]}

    return videos


@view_config(route_name='themes', renderer='templates/themes_content.jinja2')
def themes(request):
    return {}




