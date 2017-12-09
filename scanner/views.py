from django.shortcuts import render
# from django.contrib.auth.models import UserUser
from scanner.models import Person
from scanner.models import Photo
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

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
import json

empty_label="-empty-"
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
            if (not person.photo_set.filter(url=url).exists()):
                response = requests.get(url)
                photo_labels = empty_label#run_inference_on_image(BytesIO(response.content))[0]
                person.photo_set.create(url = url, labels = json.dumps(photo_labels))
            else:
                photo_labels = json.loads(person.photo_set.get(url=url).labels)
            labels.append(photo_labels)
        del person
        del grabber
        del urls
        del token
        del target_id
    # context = {'target_id': labels}

    # next 5 lines just create a matplotlib plot
    # c = Counter(labels)
    # del labels
    # fig1 = plt.figure()
    # ax1 = fig1.add_subplot(111)
    # ax1.pie(c.values(), labels=c.keys(), autopct='%1.1f%%', shadow=True, startangle=90)

    # imgdata = BytesIO()

    # fig1.savefig(imgdata, format='png')
    # imgdata.seek(0)  # rewind the data
    # plt.close()
    # Django's HttpResponse reads the buffer and extracts the image
    # response = HttpResponse(content_type='image/png')
    # image.save(response, 'PNG')
    # return HttpResponse(imgdata.getvalue(), content_type='image/png')
    return render(request, "show.html")

def scanPhoto(request):
    target_id = request.session.get("target_id", "")
    if target_id == "":
        return JsonResponse({"error":"target id not found"})
    if not (Person.objects.filter(social_id=target_id).exists()):
        return JsonResponse({"error":"person does not exist"})

    person = Person.objects.get(social_id=target_id)
    photos_count = person.photo_set.count()

    if person.photo_set.filter(labels=empty_label):
        photo = person.photo_set.filter(labels=empty_label)[0]

        response = requests.get(photo.url)
        photo.labels=run_inference_on_image(BytesIO(response.content))
        photo.save()
        username = request.GET.get('username', None)
        data = {
            'status': "Processing..."
        }
        return JsonResponse(data)
    else:
        return JsonResponse({"status": "Done!"})

def makeChart(request):
    target_id = request.session.get("target_id", "")
    if target_id == "":
        return HttpResponse("")
    if not (Person.objects.filter(social_id=target_id).exists()):
        return HttpResponse("")

    person = Person.objects.get(social_id=target_id)
    photos = person.photo_set.all()        
    labels=[photo.labels for photo in photos]

    c = Counter(labels)
    del labels
    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax1.pie(c.values(), labels=c.keys(), autopct='%1.1f%%', shadow=True, startangle=90)

    imgdata = BytesIO()

    fig1.savefig(imgdata, format='png')
    imgdata.seek(0)  # rewind the data
    plt.close()   

    return HttpResponse(imgdata.getvalue(), content_type='image/png') 