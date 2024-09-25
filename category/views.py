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



# 로깅 설정
logger = logging.getLogger(__name__)


def category_choice(request, lang):
    # 1. CodeTb에서 parent_code가 'pt'로 시작하는 코드들 가져오기
    categories = CodeTb.objects.filter(parent_code='pt').values('code', 'code_name')

    # 2. HTML 템플릿에 전달할 context
    context = {
        'categories': list(categories),
        'lang': lang  # 언어 정보도 같이 전달
    }

    # 3. category_choice.html 렌더링
    return render(request, 'category/category_choice.html', context)


@require_http_methods(["GET"])
def district_view(request, lang, place_tag_cd):

    print("district_view 함수가 호출되었습니다.")
    logger.info(f"Request received for lang: {lang}, place_tag_cd: {place_tag_cd}")
    
    try:
        # 이모지와 카테고리 이름을 코드에 따라 매핑
        category_map = {
            'pt01': {'emoji': '👨‍👩‍👦'},
            'pt02': {'emoji': '💑'},
            'pt03': {'emoji': '🎶'},
            'pt04': {'emoji': '🌲'},
            'pt05': {'emoji': '🕺'},
            'pt06': {'emoji': '🐕'},
            'pt07': {'emoji': '🧑‍🤝‍🧑'},
            'pt08': {'emoji': '🍔'},
            'pt09': {'emoji': '😎'},
            'pt10': {'emoji': '🏛️'},
            'pt11': {'emoji': '🛍️'},
            'pt12': {'emoji': '🧘‍♀️'},
            # 필요한 카테고리 추가
        }

        category_info = category_map.get(place_tag_cd, {'emoji': ''})

        place_tag = CodeTb.objects.get(code=place_tag_cd)
        
        if place_tag:
            place_tag_name = f"{category_info['emoji']} {place_tag.code_name}"
        else:
            place_tag_name = f"{category_info['emoji']} {category_info['name']}"
        
        # 전체 구별 정보 반환
        districts = DistrictTb.objects.annotate(
            place_count=Count('placetb', filter=Q(placetb__place_tag_cd=place_tag_cd))
        )
        response_data = {
            "districts": [
                {
                    "district_id": district.district_id,
                    "district_name": district.district_name,
                    "district_img": district.district_img,
                    "district_desc": district.district_desc,
                    "place_count": district.place_count
                }
                for district in districts
            ],
            "categories": list(CodeTb.objects.filter(parent_code='PC').exclude(code='PC03').values()),
            "lang": lang,
            "place_tag_cd": place_tag_cd,
            "place_tag_name": place_tag_name,
            
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
def category_district(request, lang, place_tag_cd, district_id, place_category_cd):

    print(f"category_district_view 호출됨: lang={lang}, place_tag_cd={place_tag_cd}, district_id={district_id}, place_category_cd={place_category_cd}")

    logger.info(f"Request received for lang: {lang}, place_tag_cd: {place_tag_cd}, district_id: {district_id}, place_category_cd: {place_category_cd}")

    try:
        # place_category_cd가 없으면 오류 반환
        if not place_category_cd:
            return JsonResponse({"error": "place_category_cd is required"}, status=400)

        # 선택된 구에 대한 데이터 조회
        data = choose_district(district_id, place_category_cd, place_tag_cd)

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


def choose_district(district_id, place_category_cd, place_tag_cd):
    data = []

    photo_subquery = (
        ReviewTb.objects
        .filter(place_id=OuterRef('place_id'))
        .exclude(review_photo='')
        .order_by('review_date')
        .values('review_photo')[:1]
    )

    category_tag_subquery = CodeTb.objects.filter(
        code=OuterRef('place_tag_cd'),
        parent_code='pt',
    ).values('code_name')[:1]

    top_places = (
        PlaceTb.objects
        .filter(district_id=district_id, place_category_cd=place_category_cd)
        .annotate(
            review_photo=Subquery(photo_subquery),  # 리뷰 사진 가져오기
            place_tag_name=Subquery(category_tag_subquery)
        )
        .order_by('-place_review_num')[:4]  # 리뷰 수를 기준으로 정렬
    )

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

