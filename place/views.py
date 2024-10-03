from django.shortcuts import render
from django.http import JsonResponse
from main.models import DistrictTb, CodeTb, PlaceTb, ReviewTb
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.db.models import Count, Min, Case, When, Q, CharField, Value
from utils import SaveLog

# Create your views here.
def category(request, lang):
    
    print("Place Page")
    
    
    # Get parameters from request
    district_id = request.GET.get('district_id')
    place_category_cd = request.GET.get('place_category_cd') 
    page = request.GET.get('page', 1)

    SaveLog(request, {'lang' : lang, 'district_id':district_id, 'place_category_cd':place_category_cd, 'page':page})
    # Validate page number
    try:
        page = int(page)
    except ValueError:
        page = 1

    # Set default values if parameters are not provided
    district_id = district_id if district_id else '8'
    place_category_cd = place_category_cd if place_category_cd else 'PC00'
    
    # Retrieve the district object
    try:
        district = DistrictTb.objects.get(district_id=district_id)
    except DistrictTb.DoesNotExist:
        district = None

    # 첫 번째 서브쿼리: 첫 번째 리뷰 이미지 가져오기
    photo_subquery = (
        ReviewTb.objects
        .filter(place_id=OuterRef('place_id'))
        .filter(has_photo=True)  # has_photo 필드를 사용
        .order_by('-review_date')
        .values('review_photo')[:1]
    )

    catagoty_tag_subquery = CodeTb.objects.filter(
                code=OuterRef('place_tag_cd'),
                parent_code='pt',
            ).values('kor_code_name' if lang == 'kor' else 'eng_code_name')[:1]

    # Filter places based on district and category, annotate with the first photo
    places = PlaceTb.objects.filter(
        district_id=district_id,
        place_category_cd=place_category_cd
    ).annotate(
        review_photo=Subquery(photo_subquery),
        place_tag_name =  Subquery(catagoty_tag_subquery)
    ).order_by('-place_review_num_real')

    # Paginate the results
    paginator = Paginator(places, 12)
    
    try:
        page_obj = paginator.get_page(page)
    except Exception as e:
        print(f"Pagination error: {e}")
        page_obj = paginator.get_page(1)

    # Handle AJAX request for dynamic loading
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        print('XMLHttpRequest')
        field_names = [field.name for field in PlaceTb._meta.fields]
        field_names.extend(['review_photo','place_tag_name'])
        serialized_places = list(page_obj.object_list.values(*field_names))
    
        data = {
            'place_list': serialized_places,
            'current_page' : page,
            'total_pages' : paginator.num_pages,
            'lang' : lang,
        }
        return JsonResponse(data, safe=False)

    # Render the HTML template with context
    context = {
        'district': district,
        'place_list': list(page_obj),
        'categories': list(CodeTb.objects.filter(parent_code='PC').exclude(code='PC03').values()),
        'category' : place_category_cd,
        'current_page' : page,
        'total_pages' : paginator.num_pages,
        'lang' : lang,
    }
    return render(request, 'place/place.html', context)

def get_spots_by_category(request):
    district_name = request.GET.get('district_name')
    place_category_cd = request.GET.get('place_category_cd') 

    SaveLog(request, {'district_name': district_name, 'place_category_cd': place_category_cd})

    data = DistrictTb.object.filter(district_name = district_name)
    PlaceTb.object.filter(place_category_cd = place_category_cd)

    return JsonResponse(data, safe=False)