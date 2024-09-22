from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from main.models import DistrictTb, PlaceTb, ReviewTb, CodeTb
from django.db.models import Count
from django.db.models import Subquery, OuterRef
import logging
from utils import SaveLog

# 로깅 설정
logger = logging.getLogger(__name__)

#구별 간략 정보 DB 조회
@require_http_methods(["GET"]) # GET 메소드로만 호출될 수 있게 제한
def get_districts(request, lang):
    SaveLog(request)
    try:
        print(lang)
        # 해당 언어에 맞게 구별 정보를 불러옴 (예시로 한국어로만 처리) #리턴데이터형식맞추기
        districts = DistrictTb.objects.all()
        response_data = {
            "districts": [
                {
                    "district_id": district.district_id,
                    "district_name": district.kor_district_name if lang == 'kor' else district.eng_district_name,
                    "district_name_kor": district.kor_district_name,
                    "district_desc": district.kor_district_desc if lang == 'kor' else district.eng_district_desc
                }
                for district in districts
            ],
            "categories" : list(CodeTb.objects.filter(parent_code='PC').exclude(code='PC03').values()),
            "lang" : lang,
        }
        return response_data 
    
    except Exception as e:
        logger.error(f"Error fetching districts: {str(e)}")
        return JsonResponse({
            "error": "bad_request",
            "message": "The request is required and must be a valid language code."
        }, status=400)

# 구별 대시보드 렌더링
def district(request, lang):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        pass

    context = get_districts(request, lang)

    return render(request, 'district/district.html', context)

#구 선택 버튼 시 db 정보 조회
def choose_district(district_id, place_category_cd, lang):
    data = []


    # 첫 번째 서브쿼리: 첫 번째 리뷰 이미지 가져오기
    photo_subquery = (
        ReviewTb.objects
        .filter(place_id=OuterRef('place_id'))
        .exclude(review_photo='')
        .order_by('review_date')
        .values('review_photo')[:1]
    )

    catagoty_tag_subquery = CodeTb.objects.filter(
            code=OuterRef('place_category_cd'),
            parent_code='pc',
        ).values('kor_code_name' if lang == 'kor' else 'eng_code_name')[:1]

    # for category in categories:
    #     # 각 카테고리에 대해 리뷰 수가 많은 상위 4개 장소를 가져옴
    #     top_places = (PlaceTb.objects
    #                   .filter(district_id=district_id, place_category_cd=place_category_cd)
    #                   .annotate(review_photo=Subquery(photo_subquery))  # 리뷰 사진 가져오기
    #                   .order_by('-place_review_num')[:4])  # place_review_num을 기준으로 정렬

    #     # 각 장소의 정보를 리스트에 추가
    #     # data.append([ #카테고리 이름 반환하고!!!!!
    #     #     {
    #     #         "place_category_cd": place.place_category_cd,
    #     #         "place_name": place.place_name,
    #     #         "place_tag_cd": place.place_tag_cd,
    #     #         "place_review_num": place.place_review_num,  
    #     #         "review_photo": place.review_photo if place.review_photo else ""
    #     #     }
    #     #     for place in top_places
    #     # ])
    #     for place in top_places:
    #         data.append({
    #             "place_category_cd": place.place_category_cd,
    #             "place_name": place.place_name,
    #             "place_tag_cd": place.place_tag_cd,
    #             "place_review_num": place.place_review_num,  
    #             "review_photo": place.review_photo if place.review_photo else ""
    #         })

    top_places = (PlaceTb.objects
                      .filter(district_id=district_id, place_category_cd=place_category_cd)
                      .annotate(review_photo=Subquery(photo_subquery),  # 리뷰 사진 가져오기
                                place_tag_name =  Subquery(catagoty_tag_subquery)
                                ) 
                      .order_by('-place_review_num')[:4])  # place_review_num을 기준으로 정렬

    for place in top_places:
            data.append({
                "place_category_cd": place.place_category_cd,
                "place_name": place.place_name,
                "place_tag_cd": place.place_tag_cd,
                "place_review_num": place.place_review_num,  
                "review_photo": place.review_photo if place.review_photo else "",
                "place_id" : place.place_id,
                'place_tag_name' : place.place_tag_name,
            })

    return data #리스트 형식으로 프론트와 상의 필요 + 대시보드 바뀌는 거 render 다시 해줘야하는지

@require_http_methods(["GET"])
def get_places_by_districts(request):
    SaveLog(request)
    district_id = request.GET.get('district_id')  # 요청에서 district_id 가져오기
    
    if not district_id:
        return JsonResponse({"error": "district_id is required"}, status=400)

    data = choose_district(district_id)

    response = {
        "data": data
    }

    return JsonResponse(response, safe=False)


@require_http_methods(["GET"])
def get_places_by_category(request, lang, district_id, place_category_cd):
    SaveLog(request)
    print('get_places_by_category')
    
    # 필수 파라미터가 없으면 에러 반환
    if not district_id or not place_category_cd:
        return JsonResponse({"error": "district_id and place_category_cd are required"}, status=400)

    # 선택된 구에 대한 데이터 조회
    all_data = choose_district(district_id, place_category_cd, lang)

    # place_category_cd에 해당하는 데이터 필터링
    filtered_data = [
        place for place in all_data
        if place['place_category_cd'] == place_category_cd
    ]

    # 필터링된 데이터 반환
    response = {
        "data": filtered_data
    }

    return JsonResponse(response, safe=False)