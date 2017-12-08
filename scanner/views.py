from django.shortcuts import render
# from django.contrib.auth.models import UserUser
from scanner.models import Person
from scanner.models import Photo
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

import requests
import vk
from io import BytesIO
from photoGrabber import PhotoGrabber
# from object_detection_tutorial import scanImage
from classify_image import run_inference_on_image
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
                "redirect_uri" : "https://safe-everglades-40623.herokuapp.com/scanner/login",
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
    return render(request, 'new.html')

def create(request):
    token = request.session.get("access_token", "")
    labels = []
    target_id = request.POST['target_id']
    if token != "":
        if (Person.objects.filter(social_id=target_id).exists()):
            person = Person.objects.get(social_id=target_id)
        else:
            session = vk.Session()
            vkapi = vk.API(access_token=token, session = session)
            params = vkapi.users.get(user_ids=target_id)[0]
            person = Person(social_id=target_id, name=params["first_name"], surname=params["last_name"])
        request.session["target_id"] = target_id
        grabber = PhotoGrabber(token)
        urls = grabber.loadPhotos(target_id)
        person.save()
        for url in urls:
            response = requests.get(url)
            photo = Photo(url=url, labels=run_inference_on_image(BytesIO(response.content)))
            labels += photo.labels
            if (not person.photo_set.filter(url=url).exists()):
                person.photo_set.add(photo, bulk=False)
                photo.save()
            del photo
        del person
        del grabber
        del urls
        del token
        del target_id
    # context = {'target_id': labels}

    # next 5 lines just create a matplotlib plot
    c = Counter(labels)
    del labels
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.pie(c.values(), labels=c.keys(), autopct='%1.1f%%', shadow=True, startangle=90)

    imgdata = BytesIO()

    fig1.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data
    plt.close()
    # Django's HttpResponse reads the buffer and extracts the image
    # response = HttpResponse(content_type='image/png')
    # image.save(response, 'PNG')
    return HttpResponse(imgdata.getvalue(), content_type='image/png')
