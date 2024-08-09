from django.shortcuts import render

# Create your views here.
def district(request):
    return render(request, 'district/district.html')