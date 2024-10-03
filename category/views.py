from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from main.models import DistrictTb, PlaceTb, ReviewTb, CodeTb
from django.db.models import Count, Subquery, OuterRef
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce
from django.shortcuts import render
from main.models import CodeTb
from django.db.models import Q
import logging
from utils import SaveLog



# 로깅 설정
logger = logging.getLogger(__name__)


def category_choice(request, lang):
    SaveLog(request, {'lang':lang})
    # 1. CodeTb에서 parent_code가 'ph'로 시작하는 코드들 가져오기
    categories = CodeTb.objects.filter(parent_code='ph').values('code', 'kor_code_name', 'eng_code_name')

    # 2. HTML 템플릿에 전달할 context
    context = {
        'categories': list(categories),
        'lang': lang  # 언어 정보도 같이 전달
    }

    # 3. category_choice.html 렌더링
    return render(request, 'category/category_choice.html', context)


@require_http_methods(["GET"])
def district_view(request, lang, place_thema_cd):
    SaveLog(request, {'lang':lang, 'place_thema_cd':place_thema_cd})
    print("district_view 함수가 호출되었습니다.")
    logger.info(f"Request received for lang: {lang}, place_tag_cd: {place_thema_cd}")
    
    try:
        # 이모지와 카테고리 이름을 코드에 따라 매핑
        category_map = {
            'ph01': {'emoji': '👨‍👩‍👦'},
            'ph02': {'emoji': '💖'},
            'ph03': {'emoji': '🕺'},
            'ph04': {'emoji': '🐕'},
            'ph05': {'emoji': '😎'},
            'ph06': {'emoji': '🧘‍♀️'},
            'ph07': {'emoji': '🚴‍♂️'},
            'ph08': {'emoji': '🌳'},
            'ph09': {'emoji': '💰'},

            # 필요한 카테고리 추가
        }

        category_info = category_map.get(place_thema_cd, {'emoji': ''})

        place_thema = CodeTb.objects.get(code=place_thema_cd)
        
        

        if place_thema and lang == "kor":
            place_thema_name = f"{category_info['emoji']} {place_thema.kor_code_name}"
        elif place_thema and lang == "eng":
            place_thema_name = f"{category_info['emoji']} {place_thema.eng_code_name}"
        else:
            place_thema_name = f"{category_info['emoji']} {category_info['name']}"
        
        # 전체 구별 정보 반환
        districts = DistrictTb.objects.annotate(
            place_count=Count('placetb', filter=Q(placetb__place_thema_cd=place_thema_cd))
        )
        response_data = {
            "districts": [
                {
                    "district_id": district.district_id,
                    "kor_district_name": district.kor_district_name,
                    "eng_district_name":district.eng_district_name,
                    # "district_img": district.district_img,
                    "kor_district_desc": district.kor_district_desc,
                    "eng_district_desc":district.eng_district_desc,
                    "district_lat":district.district_lat,
                    "district_lon":district.district_lon,
                    "place_count": district.place_count
                }
                for district in districts
            ],
            "categories": list(CodeTb.objects.filter(parent_code='PC').exclude(code='PC03').values()),
            "lang": lang,
            "place_thema_cd": place_thema_cd,
            "place_thema_name": place_thema_name,
            
            
        }

        # 대시보드를 렌더링할 때
        #AJAX 요청이 아닌 경우: 전체 HTML 페이지를 렌더링해서 클라이언트에게 반환
        #AJAX 요청인 경우: 이 조건문이 실행되지 않고, 아래의 코드에서 JSON 데이터를 반환

        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return render(request, 'category/category_district.html', response_data)

        print("Response data:", response_data)
        logger.info(f"Response data: {response_data}")
        return JsonResponse(response_data, safe=False, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        logger.error(f"Error fetching districts: {str(e)}")
        return JsonResponse({
            "error": "bad_request",
            "message": "The request is required and must be valid."
        }, status=400)


@require_http_methods(["GET"])
def category_district(request, lang, district_id, place_category_cd, place_thema_cd):
    SaveLog(request, {'lang': lang, 'district_id' : district_id, 'place_category_cd' : place_category_cd, 'place_thema_cd' : place_thema_cd})
    

    try:
        # place_category_cd가 없으면 오류 반환
        if not place_category_cd:
            return JsonResponse({"error": "place_category_cd is required"}, status=400)

        # 선택된 구에 대한 데이터 조회
        data = choose_district(district_id, place_category_cd, lang, place_thema_cd)

        response = {
            "data": data
        }

        print("Response data:", response)
        logger.info(f"Response data: {response}")

        return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        logger.error(f"Error fetching places for district {district_id}: {str(e)}")
        return JsonResponse({
            "error": "bad_request",
            "message": "The request is required and must be valid."
        }, status=400)


def choose_district(district_id, place_category_cd, lang, place_thema_cd):
    data = []

    photo_subquery = (
        ReviewTb.objects
        .filter(place_id=OuterRef('place_id'))
        .filter(has_photo=True)  # has_photo 필드를 사용
        .order_by('review_date')
        .values('review_photo')[:1]
    )

    if lang == 'kor':
        category_tag_subquery = CodeTb.objects.filter(
            code=OuterRef('place_tag_cd'),
            parent_code='pt',
        ).values('kor_code_name')[:1]
    elif lang == 'eng':
        category_tag_subquery = CodeTb.objects.filter(
            code=OuterRef('place_tag_cd'),
            parent_code='pt',
        ).values('eng_code_name')[:1]

    top_places = (
        PlaceTb.objects
        .filter(district_id=district_id, place_thema_cd=place_thema_cd, place_category_cd=place_category_cd)
        .annotate(
            review_photo=Subquery(photo_subquery),  # 리뷰 사진 가져오기
            place_tag_name=Subquery(category_tag_subquery)
        )
        .order_by('-place_review_num_real')[:4]  # 리뷰 수를 기준으로 정렬
    )

    for place in top_places:
        data.append({
            "place_category_cd": place.place_category_cd,
            "place_name": place.place_name,
            "place_tag_cd": place.place_tag_cd,
            "place_review_num": place.place_review_num_real,
            "review_photo": place.review_photo if place.review_photo else "",
            "place_id": place.place_id,
            "place_tag_name": place.place_tag_name,
        })

    return data

