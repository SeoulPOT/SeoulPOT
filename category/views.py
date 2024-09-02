from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import DistrictTb, PlaceTb, ReviewTb, CodeTb
from django.db.models import Count, Subquery, OuterRef
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

# 구별 간략 정보 DB 조회
@require_http_methods(["GET"])
def get_districts(request, lang):
    try:
        print(lang)
        districts = DistrictTb.objects.all()
        response_data = {
            "districts": [
                {
                    "district_id": district.district_id,
                    "district_name": district.district_name,
                    "district_img": district.district_img,
                    "district_desc": district.district_desc
                }
                for district in districts
            ],
            "categories": list(CodeTb.objects.filter(parent_code='PC').exclude(code='PC03').values()),
            "lang": lang,
        }
        return response_data
    
    except Exception as e:
        logger.error(f"Error fetching districts: {str(e)}")
        return JsonResponse({
            "error": "bad_request",
            "message": "The request is required and must be a valid language code."
        }, status=400)

# 구별 대시보드 렌더링

logger = logging.getLogger(__name__)

def category(request, lang):
        logger.debug("District view function called with lang: %s", lang)
        context = get_districts(request, lang)

        context = get_districts(request, lang)
        selected_category_code = request.GET.get('category', 'PC01')
        selected_category_name = "가족"
        selected_category_icon = "👨‍👩‍👦"
        district_id = request.GET.get('district_id', None)
        places = []
        if district_id:
            places = choose_district(district_id, selected_category_code)

        context.update({
            "selected_category_code": selected_category_code,
            "selected_category_name": selected_category_name,
            "selected_category_icon": selected_category_icon,
            "places": places,
        })

        return render(request, 'category/category_choice.html', context)

def district(request, lang, place_category_cd):
    logger.debug("District view function called with lang: %s", lang)
    context = get_districts(request, lang)
    
    selected_category_code = place_category_cd
    selected_category_name = "가족"  # 예시로 지정, 실제로는 `categories`에서 이름을 찾아서 설정해야 함
    selected_category_icon = "👨‍👩‍👦"  # 예시로 지정

    district_id = request.GET.get('district_id', None)
    places = []
    if district_id:
        places = choose_district(district_id, selected_category_code)

    context.update({
        "selected_category_code": selected_category_code,
        "selected_category_name": selected_category_name,
        "selected_category_icon": selected_category_icon,
        "places": places,
    })

    return render(request, 'category/category_district.html', context)



# 구 선택 버튼 시 db 정보 조회
def choose_district(district_id, place_category_cd):
    data = []

    photo_subquery = (
        ReviewTb.objects
        .filter(place_id=OuterRef('place_id'))
        .exclude(review_photo='')
        .order_by('review_date')
        .values('review_photo')[:1]
    )

    catagoty_tag_subquery = CodeTb.objects.filter(
            code=OuterRef('place_tag_cd'),
            parent_code='pt',
        ).values('code_name')[:1]

    top_places = (PlaceTb.objects
                    .filter(district_id=district_id, place_category_cd=place_category_cd)
                    .annotate(review_photo=Subquery(photo_subquery),  # 리뷰 사진 가져오기
                                place_tag_name = Subquery(catagoty_tag_subquery)
                                ) 
                    .order_by('-place_review_num')[:4])  # place_review_num을 기준으로 정렬

    for place in top_places:
            data.append({
                "place_category_cd": place.place_category_cd,
                "place_name": place.place_name,
                "place_tag_cd": place.place_tag_cd,
                "place_review_num": place.place_review_num,  
                "review_photo": place.review_photo if place.review_photo else "",
                "place_id": place.place_id,
                "place_tag_name": place.place_tag_name,
            })

    return data

# 카테고리별 장소 가져오기
@require_http_methods(["GET"])
def get_places_by_category(request, lang, place_category_cd):
    if  not place_category_cd:
        return JsonResponse({"error": "district_id and place_category_cd are required"}, status=400)

    all_data = choose_district( place_category_cd)

    filtered_data = [
        place for place in all_data
        if place['place_category_cd'] == place_category_cd
    ]

    response = {
        "data": filtered_data
    }

    return JsonResponse(response, safe=False)



