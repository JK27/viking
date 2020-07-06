from django.shortcuts import render


# ------------------------------------- INDEX
def index(request):
    return render(request, 'home/index.html')
