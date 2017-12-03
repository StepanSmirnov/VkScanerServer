from django.shortcuts import render
import requests
from django.contrib.auth.models import User
from scaner.models import Profile
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
import vk
from PIL import Image
import requests
from io import BytesIO
from photoGrabber import PhotoGrabber
from object_detection_tutorial import scanImage
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from io import StringIO
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
    context = {'access_token': token}
    return render(request, 'new.html', context)
    # else:
    #     return render(request, "index.html")

def create(request):
    token = request.session.get("access_token", "")
    labels = []
    target_id = request.POST['target_id']
    if token != "":
        grabber = PhotoGrabber(token)
        urls = grabber.loadPhotos(target_id)
        for url in urls:
            response = requests.get(url)
            photo = Image.open(BytesIO(response.content))
            labels += (scanImage(photo))
    # context = {'target_id': labels}

    # next 5 lines just create a matplotlib plot
    c = Counter(labels)
    fig1, ax1 = plt.subplots()
    ax1.pie(c.values(), labels=c.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
    buffer = StringIO()
    canvas = plt.get_current_fig_manager().canvas
    canvas.draw()
    pil_image = Image.fromstring('RGB', canvas.get_width_height(), 
                 canvas.tostring_rgb())
    pil_image.save(buffer, 'PNG')
    plt.close()
    # Django's HttpResponse reads the buffer and extracts the image
    return HttpResponse(buffer.getvalue(), mimetype='image/png')

    # return render(request, 'show.html', context)
