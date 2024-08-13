from django.shortcuts import render
from datetime import datetime

# Create your views here.
def main(request):
    context = {
        "now_time" : datetime.now().isoformat(),
        "temperature" : "36.5"
    }
    return render(request, 'main/main.html', context)