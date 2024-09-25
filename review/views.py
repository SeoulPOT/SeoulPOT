from django.shortcuts import render, get_object_or_404
from main.models import PlaceTb, ReviewTb, CodeTb
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef, Value
from django.http import JsonResponse
import json


def content_reviews(request, lang):
    place_id = request.GET.get("place_id")
    array = request.GET.get("array", "latest")  # 정렬 방식 가져오기 (기본값은 최신순)
    page = request.GET.get("page", 1)  # 페이지 기본 1page

    profile_photo = (
        ReviewTb.objects.filter(place_id=place_id, review_photo__gt="")
        .exclude(review_photo="h")
        .values_list("review_photo", flat=True)[:1]
    )

    # 리뷰에서 최대 4개의 사진을 가져오되, 값이 'h'인 사진은 제외
    review_photos = (
        ReviewTb.objects.filter(place_id=place_id, review_photo__gt="")
        .exclude(review_photo="h")
        .values_list("review_photo", flat=True)[1:5]
    )

    place = (
        PlaceTb.objects.filter(place_id=place_id)
        .annotate()  # 리뷰 사진 가져오기 (Subquery 결과를 이용해 각 객체에 review_photo라는 필드를 추가)
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
    try:
        feature_dict = {}
        place_feature = place.place_feature
        # 문자열을 ', '로 먼저 분리하고 각 요소에서 ' : '로 나눔
        feature_list = [feature.split(" : ") for feature in place_feature.split(", ")]
        # 공백 및 숫자가 아닌 문자를 제거하고 딕셔너리로 변환
        feature_dict = {
            key.replace("'", "").strip(): int(value.replace("'", "").strip())
            for key, value in feature_list
        }
        first_key = list(feature_dict.keys())[0]
        first_value = list(feature_dict.values())[0]
    except:
        first_key = []
        first_value = []
        place_feature = ""

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
    review_dict = {
        review.kor_review_text: review.similar_review
        for review in reviews
        if review.similar_review  # similar_review가 존재하는 경우만
    }

    # -----------------------------------------------------

    context = {
        "place": place,
        "reviews": page_obj,
        "profile_photo": profile_photo,
        "feature_dict": feature_dict,
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
    place_id = request.GET.get("place_id")
    array = request.GET.get("array", "latest")  # 정렬 방식 가져오기 (기본값은 최신순)
    page = request.GET.get("page", 1)  # 페이지 기본 1page

    profile_photo = (
        ReviewTb.objects.filter(place_id=place_id, review_photo__gt="")
        .exclude(review_photo="h")
        .values_list("review_photo", flat=True)[:1]
    )

    place = (
        PlaceTb.objects.filter(place_id=place_id)
        .annotate()  # 리뷰 사진 가져오기 (Subquery 결과를 이용해 각 객체에 review_photo라는 필드를 추가)
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
    total = place.place_review_num

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

    # ----------------------------------------------------------------------------
    # try:
    #     feature_dict = {}
    #     place_feature = place.place_feature

    #     # 문자열을 ', '로 먼저 분리하고 각 요소에서 ' : '로 나눔
    #     feature_list = [feature.split(" : ") for feature in place_feature.split(", ")]
    #     # 공백 및 숫자가 아닌 문자를 제거하고 리스트로 변환
    #     feature_keys = [key.replace("'", "").strip() for key, value in feature_list]
    #     feature_values = [
    #         int(value.replace("'", "").strip()) for key, value in feature_list
    #     ]

    # except Exception as e:
    #     feature_keys = []
    #     feature_values = []
    #     print(f"Error occurred: {e}")

    try:
        feature_dict = {}
        place_feature = place.place_feature

        first_key = list(feature_dict.keys())[0]
        first_value = list(feature_dict.values())[0]

        # 문자열을 ', '로 먼저 분리하고 각 요소에서 ' : '로 나눔
        feature_list = [feature.split(" : ") for feature in place_feature.split(", ")]
        # 공백 및 숫자가 아닌 문자를 제거하고 딕셔너리로 변환
        feature_dict = {
            key.replace("'", "").strip(): int(value.replace("'", "").strip())
            for key, value in feature_list
        }
    except:
        place_feature = ""
        first_key = []
        first_value = []

    context = {
        "place": place,
        "reviews": page_obj,
        "profile_photo": profile_photo,
        "array": array,
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "reviews": serialized_reviews,
        "kor_place_tag": kor_place_tag,
        "eng_place_tag": eng_place_tag,
        "thema_name": thema_name,
        "feature_dict": feature_dict,
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
