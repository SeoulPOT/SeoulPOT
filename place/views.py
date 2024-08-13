from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
def category(request):
    gu = request.GET.get('gu')
    category = request.GET.get('category') 

    gu = gu if gu else '중구'
    category = category if category else 'food'

    # 테이블 명 바꿔야함
    context = {
        'shop' : shop_tb.object.filter(gu = gu, category = category)
    }
    return render(request, 'place/place.html', context)

def get_spots_by_category(request):
    gu = request.GET.get("gu")
    category = request.GET.get('category')     

    data = shop_tb.object.filter(gu = gu, category = category)

    return JsonResponse(data, safe=False)