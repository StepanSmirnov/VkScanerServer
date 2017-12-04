from django.shortcuts import render
from django.contrib.auth.models import User
from scaner.models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from os import path

import requests
import vk
from PIL import Image
from io import BytesIO
from photoGrabber import PhotoGrabber
from object_detection_tutorial import scanImage
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from collections import Counter

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
    request.session["vk_uid"]=id
    request.session["access_token"] = token
    # if (User.objects.filter(username=id).count() == 0):
    #     user = User.objects.create_user(username=id, password="")
    #     user.profile.access_token = token
    #     user.save()
    # user = authenticate(username=id, password="")
    # if user is not None:
    #     login(request, user)
    return render(request, 'new.html')
    # else:
    #     return render(request, "index.html")

def create(request):
    token = request.session.get("access_token", "")
    labels = []
    target_id = request.POST['target_id']
    if token != "":
        grabber = PhotoGrabber(token)
        del token
        urls = grabber.loadPhotos(target_id)
        for url in urls:
            response = requests.get(url)
            photo = Image.open(BytesIO(response.content))
            labels += (scanImage(photo))
            del photo
        del grabber
        del urls

    # next 5 lines just create a matplotlib plot
    c = Counter(labels)
    plt.pie(c.values(), labels=c.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    url = path.join(settings.STATIC_ROOT + ,"chart.png")
    plt.savefig(url, format='png')
    plt.close()
    # Django's HttpResponse reads the buffer and extracts the image
    # response = HttpResponse(content_type='image/png')
    # image.save(response, 'PNG')
    context = {'chart_src': url}
    return render(request, 'show.html', context)
