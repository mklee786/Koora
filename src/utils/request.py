import jwt
import requests
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser 
from utils.koora import generate_url_for
from django.conf import settings



JWT_SECRET = settings.SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM
JWT_EXP_DELTA_SECONDS = settings.JWT_EXP_DELTA_SECONDS



def parse_body(request, for_method="PUT"):

    if (request.method == "POST"):
        return

    # set post temporarily to access _load_post_and_files method
    request.method = "POST"

    request._load_post_and_files()
    request.method = for_method

    if for_method == 'PUT':
        request.PUT = request.POST

    elif for_method == 'PATCH':
        request.PATCH = request.POST

    elif for_method == 'DELETE':
        request.DELETE = request.POST



def set_user(request):
    # user_id = request.headers.get('Token', None)
    # try:
    #     request.user = User.objects.get(id=user_id)
    # except Exception:
    #     request.user = AnonymousUser()


    active_user = AnonymousUser()

    try:
        access_token = request.META['Token']
        print('you bring me : ', access_token)  
        decoded = jwt.decode(access_token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        active_user = User.objects.get(id=decoded['user_id'])
        print('HI : ', active_user)
    except Exception as ee:
        print('invalid token', ee)


    request.user = active_user




def api_call(*args, **kwargs):

    request = kwargs['request']

    csrftoken = kwargs['request'].POST.get('csrfmiddlewaretoken', '')

    headers = {
        'X-CSRFToken' : csrftoken,
        'Token' : request.META['Token']
    }

    cookies = {
        'csrftoken' : csrftoken
    }

    reverse_kwargs = kwargs.get('reverse_kwargs', None)
    reverse_params = kwargs.get('reverse_params', None)
    reverse_for = kwargs.get('reverse_for', '')

    data = kwargs.get('data', None)
    files = kwargs.get('files', None)
    
    return getattr(requests, kwargs.get('method', 'get'))(url = request.build_absolute_uri(generate_url_for(reverse_for, kwargs=reverse_kwargs, query=reverse_params)), headers=headers, cookies=cookies, data=data, files=files)
