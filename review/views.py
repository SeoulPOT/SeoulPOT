from django.shortcuts import render, get_object_or_404
from main.models import PlaceTb, ReviewTb, CodeTb
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef, Value
from django.http import JsonResponse
import json
from utils import SaveLog

def content_reviews(request, lang):
    SaveLog(request)

    place_id = request.GET.get("place_id")
    array = request.GET.get("array", "latest")  # 정렬 방식 가져오기 (기본값은 최신순)
    page = request.GET.get("page", 1)  # 페이지 기본 1page

    # 첫 번째 서브쿼리: 첫 번째 리뷰 이미지 가져오기
    photo_subquery = (
        ReviewTb.objects.filter(place_id=OuterRef("place_id"))
        .exclude(review_photo="")
        .order_by("-review_date")
        .values("review_photo")[:1]
    )

    # 리뷰에서 최대 4개의 사진을 가져오되, 값이 'h'인 사진은 제외
    review_photos = (
        ReviewTb.objects.filter(place_id=place_id, review_photo__gt="")
        .exclude(review_photo="h")
        .values_list("review_photo", flat=True)[1:5]
    )

    place = (
        PlaceTb.objects.filter(place_id=place_id)
        .annotate(profile_photo=Subquery(photo_subquery))  # 리뷰 사진 가져오기
        .first()
    )  # place_review_num을 기준으로 정렬
    print(place)

    # 기본 리뷰 쿼리셋
    reviews = ReviewTb.objects.filter(place_id=place_id).annotate(
        daily_tag_name=Subquery(
            CodeTb.objects.filter(
                parent_code="rd", code=OuterRef("review_daily_tag_cd")
            ).values("kor_code_name")[:1]
        ),
        with_tag_name=Subquery(
            CodeTb.objects.filter(
                code=OuterRef("review_with_tag_cd"), parent_code="rw"
            ).values("kor_code_name")[:1]
        ),
    )

    # 장소 태그 정보
    if lang == "kor":
        place_tag = CodeTb.objects.get(code=place.place_tag_cd)

    else:
        place_tag = CodeTb.objects.get(code=place.place_tag_cd)

    kor_place_tag = place_tag.kor_code_name
    eng_place_tag = place_tag.eng_code_name
    # -------------------------------------------------------------------------------

    thema_name = get_code_name_for_thema_cd(place.place_thema_cd, lang)

    # 정렬 방식에 따른 필터링
    if array == "latest":
        reviews = reviews.order_by("-review_date")[:5]  # 최신순으로 5개
    elif array == "positive":
        reviews = reviews.filter(review_sentiment=1).order_by("review_date")[
            :5
        ]  # 긍정(1) 리뷰 5개
    elif array == "negative":
        reviews = reviews.filter(review_sentiment=-1).order_by("review_date")[
            :5
        ]  # 부정(-1) 리뷰 5개

    paginator = Paginator(reviews, 10)  # 리뷰를 10개씩 나누어서 페이지를 나눈다
    page_obj = paginator.get_page(page)
    ########################################################################################################
    # 리뷰 데이터를 JSON 형식으로 변환
    review_field_names = [field.name for field in ReviewTb._meta.fields]
    review_field_names.extend(["daily_tag_name", "with_tag_name"])

    serialized_reviews = list(page_obj.object_list.values(*review_field_names))

    # 텍스트가 너무 길면 자르기 (30자로 제한)
    if lang == "kor":
        for review in serialized_reviews:
            if len(review["kor_review_text"]) > 25:
                review["kor_review_text"] = review["kor_review_text"][:25] + "..."
    else:
        for review in serialized_reviews:
            if len(review["eng_review_text"]) > 45:
                review["eng_review_text"] = review["eng_review_text"][:45] + "..."

    # 키워드 가져오기

    feature_dict, mapped_feature_dict, first_key, first_value = (
        map_place_feature_to_language(place, lang)
    )

    # 긍정 비율 계산

    pos = place.place_pos_review_num
    neg = place.place_neg_review_num
    total = place.place_review_num_real

    pos_ratio = round((pos / total) * 100, 2)
    neg_ratio = round((neg / total) * 100, 2)
    neutral = round(100 - (pos_ratio + neg_ratio), 2)

    # 부정 비율 계산

    real = place.place_review_num_real
    ad = place.place_ad_review_num
    real_ratio = round(((real - ad) / total) * 100, 2)

    # 광고성 리뷰 가져오기
    reviews = ReviewTb.objects.filter(place_id=place_id)

    # kor_review_text와 similar_review를 딕셔너리 형태로 저장
    if lang == "kor":
        review_dict = {
            review.kor_review_text: review.similar_review
            for review in reviews
            if review.similar_review  # similar_review가 존재하는 경우만
        }
    else:
        review_dict = {
            review.kor_review_text: review.similar_review
            for review in reviews
            if review.similar_review  # similar_review가 존재하는 경우만
        }

    # -----------------------------------------------------

    context = {
        "place": place,
        "reviews": page_obj,
        "feature_dict": feature_dict,
        "mapped_feature_dict": mapped_feature_dict,
        "kor_place_tag": kor_place_tag,
        "eng_place_tag": eng_place_tag,
        "thema_name": thema_name,
        "array": array,
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "pos_ratio": pos_ratio,
        "neg_ratio": neg_ratio,
        "neutral": neutral,
        "pos": pos,
        "total": total,
        "real": real,
        "real_ratio": real_ratio,
        "ad": ad,
        "review_photos": review_photos,  # 리뷰 사진 추가
        "reviews": serialized_reviews,
        "lang": lang,
        "first_key": first_key,
        "first_value": first_value,
        "review_dict": review_dict,

    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        context = {
            "array": array,
            "serialized_reviews": serialized_reviews,
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
        }
        return JsonResponse(context, safe=False)

    return render(request, "review/reviews.html", context)


def reviews_more(request, lang):
    SaveLog(request)

    place_id = request.GET.get("place_id")
    array = request.GET.get("array", "latest")  # 정렬 방식 가져오기 (기본값은 최신순)
    page = request.GET.get("page", 1)  # 페이지 기본 1page

    # 첫 번째 서브쿼리: 첫 번째 리뷰 이미지 가져오기
    photo_subquery = (
        ReviewTb.objects.filter(place_id=OuterRef("place_id"))
        .exclude(review_photo="")
        .order_by("-review_date")
        .values("review_photo")[:1]
    )

    place = (
        PlaceTb.objects.filter(place_id=place_id)
        .annotate(profile_photo=Subquery(photo_subquery))  # 리뷰 사진 가져오기
        .first()
    )  # place_review_num을 기준으로 정렬
    print(place)

    # 기본 리뷰 쿼리셋
    if lang == "kor":
        reviews = ReviewTb.objects.filter(place_id=place_id).annotate(
            daily_tag_name=Subquery(
                CodeTb.objects.filter(
                    parent_code="rd", code=OuterRef("review_daily_tag_cd")
                ).values("kor_code_name")[:1]
            ),
            with_tag_name=Subquery(
                CodeTb.objects.filter(
                    code=OuterRef("review_with_tag_cd"), parent_code="rw"
                ).values("kor_code_name")[:1]
            ),
        )
    else:
        reviews = ReviewTb.objects.filter(place_id=place_id).annotate(
            daily_tag_name=Subquery(
                CodeTb.objects.filter(
                    parent_code="rd", code=OuterRef("review_daily_tag_cd")
                ).values("eng_code_name")[:1]
            ),
            with_tag_name=Subquery(
                CodeTb.objects.filter(
                    code=OuterRef("review_with_tag_cd"), parent_code="rw"
                ).values("eng_code_name")[:1]
            ),
        )
    # 전체 리뷰 수
    # total = place.place_review_num
    total = place.place_review_num_real

    # 장소 태그 정보
    if lang == "kor":
        place_tag = CodeTb.objects.get(code=place.place_tag_cd)

    else:
        place_tag = CodeTb.objects.get(code=place.place_tag_cd)

    kor_place_tag = place_tag.kor_code_name
    eng_place_tag = place_tag.eng_code_name
    thema_name = get_code_name_for_thema_cd(place.place_thema_cd, lang)

    # 정렬 방식에 따른 필터링
    if array == "latest":
        reviews = reviews.order_by("-review_date")[:10]  # 최신순으로 10개
    elif array == "positive":
        reviews = reviews.filter(review_sentiment=1).order_by("review_date")[
            :10
        ]  # 긍정(1) 리뷰 10개
    elif array == "negative":
        reviews = reviews.filter(review_sentiment=-1).order_by("review_date")[
            :10
        ]  # 부정(-1) 리뷰 10개

    paginator = Paginator(reviews, 10)  # 리뷰를 10개씩 나누어서 페이지를 나눈다
    page_obj = paginator.get_page(page)

    # 리뷰 데이터를 JSON 형식으로 변환
    review_field_names = [field.name for field in ReviewTb._meta.fields]
    review_field_names.extend(["daily_tag_name", "with_tag_name"])

    serialized_reviews = list(page_obj.object_list.values(*review_field_names))

    # 키워드 가져오기
    feature_dict, mapped_feature_dict, first_key, first_value = (
        map_place_feature_to_language(place, lang)
    )

    context = {
        "place": place,
        "reviews": page_obj,
        "array": array,
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "reviews": serialized_reviews,
        "kor_place_tag": kor_place_tag,
        "eng_place_tag": eng_place_tag,
        "thema_name": thema_name,
        "feature_dict": feature_dict,
        "mapped_feature_dict": mapped_feature_dict,
        "first_key": first_key,
        "first_value": first_value,
        "total": total,
        "lang": lang,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        context = {
            "array": array,
            "serialized_reviews": serialized_reviews,
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
        }
        return JsonResponse(context, safe=False)

    return render(request, "review/more.html", context)


def get_code_name_for_thema_cd(thema_cd, lang):


    if not thema_cd:
        return []

    if lang == "kor":
        # 코드별 이모지 매핑
        emoji_mapping = {
            "ph01": "가족👨‍👩‍👧‍👦",
            "ph02": "연인💕",
            "ph03": "혼놀🕺",
            "ph04": "반려동물🐕",
            "ph05": "트렌드(MZ)😎",
            "ph06": "힐링🌳",
            "ph07": "로컬애용🚲",
            "ph08": "인테리어🛋️",
            "ph09": "가성비💰",
        }
    else:
        emoji_mapping = {
            "ph01": "Family👨‍👩‍👧‍👦",
            "ph02": "Couple💕",
            "ph03": "Solo Play🕺",
            "ph04": "Pet🐕",
            "ph05": "Trendy(Gen Z)😎",
            "ph06": "Healing🌳",
            "ph07": "Local favorite🚲",
            "ph08": "Interior🛋️",
            "ph09": "Cost-effective💰",
        }

    # place_thema_cd에 있는 코드를 분리
    thema_cd_list = thema_cd.split(", ")

    # 코드 이름을 저장할 리스트
    kor_code_names = []

    # 각 코드를 조회하여 kor_code_name에 이모지를 추가하여 리스트에 추가
    for code in thema_cd_list:
        try:
            code_obj = CodeTb.objects.get(code=code)
            # 이모지가 매핑된 경우 이모지를 추가, 그렇지 않으면 기본 kor_code_name 사용
            kor_code_name_with_emoji = emoji_mapping.get(code, code_obj.kor_code_name)
            kor_code_names.append(kor_code_name_with_emoji)
        except CodeTb.DoesNotExist:
            kor_code_names.append(f"Unknown code: {code}")

    return kor_code_names  # 리스트 반환


def get_code_name_for_place_tag_cd(place_tag_cd):
    # 코드 이름을 저장할 리스트
    kor_code_names = []

    # 각 코드를 조회하여 kor_code_name에 이모지를 추가하여 리스트에 추가
    for code in place_tag_cd:
        code_obj = CodeTb.objects.get(code=code)
        kor_code_names.append(code_obj.kor_code_name)
    return kor_code_names


def map_place_feature_to_language(place, lang):
    korean_english_mapping = {
        "커피가 맛있어요": "The coffee is delicious",
        "디저트가 맛있어요": "The dessert is delicious",
        "음료가 맛있어요": "The drinks are delicious",
        "특별한 메뉴가 있어요": "There's a special menu",
        "가성비가 좋아요": "The value for money is good",
        "건강한 맛이에요": "It tastes healthy",
        "비싼 만큼 가치있어요": "It's worth the price",
        "메뉴 구성이 알차요": "The menu composition is substantial",
        "음식이 맛있어요": "The food is delicious",
        "양이 많아요": "The portions are generous",
        "재료가 신선해요": "The ingredients are fresh",
        "빵이 맛있어요": "The bread is delicious",
        "차가 맛있어요": "The tea is delicious",
        "술이 다양해요": "There's a wide variety of alcohol",
        "기본 안주가 좋아요": "The complimentary snacks are good",
        "코스요리가 알차요": "The course meals are substantial",
        "주문제작을 잘해줘요": "They are good at custom orders",
        "종류가 다양해요": "There is a wide variety of choices",
        "인테리어가 멋져요": "The interior is stylish",
        "사진이 잘 나와요": "The place is great for taking photos",
        "대화하기 좋아요": "It's a good place to have a conversation",
        "집중하기 좋아요": "It's a good place to focus",
        "뷰가 좋아요": "The view is nice",
        "매장이 넓어요": "The store is spacious",
        "아늑해요": "It's cozy",
        "야외공간이 멋져요": "The outdoor space is great",
        "음악이 좋아요": "The music is good",
        "차분한 분위기에요": "The atmosphere is calm",
        "컨셉이 독특해요": "The concept is unique",
        "단체모임 하기 좋아요": "It's good for group gatherings",
        "혼밥하기 좋아요": "It's good for dining alone",
        "혼술하기 좋아요": "It's good for drinking alone",
        "친절해요": "The staff is friendly",
        "매장이 청결해요": "The store is clean",
        "화장실이 깨끗해요": "The restroom is clean",
        "주차하기 편해요": "Parking is convenient",
        "좌석이 편해요": "The seats are comfortable",
        "룸이 잘 되어있어요": "The rooms are well set up",
        "반려동물과 가기 좋아요": "It's a good place to go with pets",
        "아이와 가기 좋아요": "It's a good place to go with children",
        "선물하기 좋아요": "It's a good place for gift shopping",
        "오래 머무르기 좋아요": "It's a good place to stay for a long time",
        "음식이 빨리 나와요": "The food comes out quickly",
        "읽을만한 책이 많아요": "There are many books worth reading",
        "특별한 날 가기 좋아요": "It's a great place for special occasions",
        "포장이 깔끔해요": "The packaging is neat",
        "파티하기 좋아요": "It's a good place for parties",
        "고기 질이 좋아요": "Good quality meat",
        "직접 잘 구워줘요": "They grill it for you",
        "반찬이 잘 나와요": "They serve good side dishes",
    }

    try:
        feature_dict = {}
        mapped_feature_dict = {}
        place_feature = place.place_feature

        # 문자열을 ', '로 먼저 분리하고 각 요소에서 ' : '로 나눔
        feature_list = [feature.split(" : ") for feature in place_feature.split(", ")]

        # 공백 및 숫자가 아닌 문자를 제거하고 딕셔너리로 변환
        feature_dict = {
            key.replace("'", "").strip(): int(value.replace("'", "").strip())
            for key, value in feature_list
        }

        # lang이 'kor'인 경우: 그대로 시행
        if lang == "kor":
            first_key = list(feature_dict.keys())[0]
            first_value = list(feature_dict.values())[0]

        # lang이 'kor'이 아닌 경우: 영어로 매핑된 값을 사용
        else:
            mapped_feature_dict = {
                korean_english_mapping.get(
                    key, key
                ): value  # 매핑된 값이 있으면 사용, 없으면 그대로 사용
                for key, value in feature_dict.items()
            }
            first_key = list(mapped_feature_dict.keys())[0]
            first_value = list(mapped_feature_dict.values())[0]

        return feature_dict, mapped_feature_dict, first_key, first_value

    except:
        place_feature = ""
        first_key = []
        first_value = []
        return feature_dict, mapped_feature_dict, first_key, first_value
