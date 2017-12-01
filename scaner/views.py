from django.shortcuts import render
import requests
from django.contrib.auth.models import User
import vk
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    code = request.GET.get('code', "")
    
    url = "https://oauth.vk.com/access_token"
    params = {"client_id": "6258947",
                "client_secret" : "7m6jlVFSkE4QgWT3528l",
                "redirect_uri" : "https://safe-everglades-40623.herokuapp.com/scaner/login",
                "code" : code
                }
    response = requests.get(url, params = params)
    response = response.json()
    token=""
    if "access_token" in response:
        token = response["access_token"]

    session = vk.Session()
    vkapi = vk.API(access_token=token, session = session)
    id = str(vkapi.users.get()[0]["uid"])
    if (User.objects.filter(username=id).count() == 0):
        user = User.objects.create_user(id, "")
        user.profile.access_token = token
        user.save()
    user = authenticate(username=id, password="")
    if user is not None:
        login(request, user)
        context = {'access_token': token}
        return render(request, 'new.html', context)

def create(request):
    target_id = request.POST['target_id']
    context = {'target_id': target_id}
    return render(request, 'show.html', context)
