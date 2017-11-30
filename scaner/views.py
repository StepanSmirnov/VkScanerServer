from django.shortcuts import render
import requests

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

    context = {'access_token': token}
    return render(request, 'login.html', context)