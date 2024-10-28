from django.shortcuts import render
from django.http import JsonResponse
from main.models import DistrictTb, CodeTb, PlaceTb, ReviewTb
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.db.models import Count, Min, Case, When, Q, CharField, Value
from django.db.models import F, FloatField, ExpressionWrapper
from utils import SaveLog

# Create your views here.
def category(request, lang):
    
    print("Place Page")
    
    
    # Get parameters from request
    district_id = request.GET.get('district_id')
    place_category_cd = request.GET.get('place_category_cd') 
    sortBy = request.GET.get('sortBy') 
    place_thema_cd = request.GET.get('place_thema_cd','')
    page = request.GET.get('page', 1)
    search_text = request.GET.get('search_text', "")

    SaveLog(request, {'lang' : lang, 'district_id':district_id, 'place_category_cd':place_category_cd,'place_thema_cd':place_thema_cd, 'page':page, 'sortBy':sortBy, 'search_text':search_text})
    # Validate page number
    try:
        page = int(page)
    except ValueError:
        page = 1

    # Set default values if parameters are not provided
    district_id = district_id if district_id else '8'
    place_category_cd = place_category_cd if place_category_cd else 'PC00'
    sortBy = sortBy if sortBy else '0'

    print(f'sortBy : {sortBy}')
    print(f'search_text : {search_text}')
    # sortBy = sortBy if sortBy else '0'
    
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
    # 기본 필터링 조건
    filters = {
        'district_id': district_id,
        'place_category_cd': place_category_cd,
    }

    # place_thema_cd가 빈 문자열이 아닐 경우 조건 추가
    if place_thema_cd != '':
        filters['place_thema_cd__contains'] = place_thema_cd
        print(f'테마있음: {place_thema_cd}')


    order_field = '-place_review_num'  # 필요에 따라 정렬 기준 설정 (예: 이름 순)
    # sortBy 값에 따라 정렬 기준 설정
    if sortBy == '-1' or sortBy is None:
        # sortBy가 -1일 때는 place_name에 search_text가 포함되는 데이터 조회
        filters['place_name__contains'] = search_text  # place_name에서 search_text 검색
        order_field = '-place_name'  # 필요에 따라 정렬 기준 설정 (예: 이름 순)
    if sortBy == '0':
        order_field = '-pos_review_ratio'  # place_sentiment 내림차순
    elif sortBy == '1':
        order_field = '-place_distance'          # distance 내림차순
    elif sortBy == '2':
        order_field = '-place_review_num' # place_review_num 내림차순
    

    places = PlaceTb.objects.filter(
            **filters
    ).annotate(
        review_photo=Subquery(photo_subquery),
        place_tag_name =  Subquery(catagoty_tag_subquery),
        pos_review_ratio=ExpressionWrapper(
            F('place_pos_review_num') / F('place_review_num'),
            output_field=FloatField())
    ).order_by(order_field)

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
            'sortBy' : sortBy,
        }
        return JsonResponse(data, safe=False)

    # Render the HTML template with context
    context = {
        'district': district,
        'place_list': list(page_obj),
        'categories': list(CodeTb.objects.filter(parent_code='PC').exclude(code='PC03').values()),
        'category' : place_category_cd,
        'sortBy' : sortBy,
        'place_thema_cd' : place_thema_cd,
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