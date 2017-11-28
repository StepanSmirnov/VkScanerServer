from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    token = request.GET.get('access_token', "")
    if token == "":
        token = "failed"
    context = {'access_token': token}
    return render(request, 'login.html', context)