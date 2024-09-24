from django.shortcuts import render, get_object_or_404
from main.models import PlaceTb, ReviewTb, CodeTb
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef, Value
from django.http import JsonResponse
import json


def content_reviews(request):
    place_id = request.GET.get("place_id")
    place_category_cd = request.GET.get("place_category_cd")
    array = request.GET.get("array", "latest")  # 정렬 방식 가져오기 (기본값은 최신순)
    page = request.GET.get("page", 1)  # 페이지 기본 1page

    photo_subquery = (
        ReviewTb.objects.filter(place_id=place_id, review_photo__gt="")
        .exclude(review_photo="h")
        .values_list("review_photo", flat=True)[:1]
    )

    # 리뷰에서 최대 4개의 사진을 가져오되, 값이 'h'인 사진은 제외
    review_photos = (
        ReviewTb.objects.filter(place_id=place_id, review_photo__gt="")
        .exclude(review_photo="h")
        .values_list("review_photo", flat=True)[:4]
    )

    place = (
        PlaceTb.objects.filter(place_id=place_id)
        .annotate(
            review_photo=Subquery(photo_subquery)
        )  # 리뷰 사진 가져오기 (Subquery 결과를 이용해 각 객체에 review_photo라는 필드를 추가)
        .first()
    )  # place_review_num을 기준으로 정렬
    print(place)

    # place = get_object_or_404(PlaceTb, pk=place_id)  # 콘텐츠 가져오기, 없으면 404
    daily_tag_subquery = CodeTb.objects.filter(
        parent_code="rd", code=OuterRef("review_daily_tag_cd")
    ).values("kor_code_name")[:1]

    with_tag_subquery = CodeTb.objects.filter(
        code=OuterRef("review_with_tag_cd"),
        parent_code="rw",
    ).values("kor_code_name")[:1]

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

    # 리뷰 데이터를 JSON 형식으로 변환
    review_field_names = [field.name for field in ReviewTb._meta.fields]
    review_field_names.extend(["daily_tag_name", "with_tag_name"])

    serialized_reviews = list(page_obj.object_list.values(*review_field_names))

    # 텍스트가 너무 길면 자르기 (30자로 제한)
    for review in serialized_reviews:
        if len(review["kor_review_text"]) > 30:
            review["kor_review_text"] = review["kor_review_text"][:30] + "..."

    # ------------------place_feature--------------------
    # features = {}
    # raw_feature = place.place_feature

    # if raw_feature:
    #     print(f"raw_feature: ${raw_feature}")
    #     for item in raw_feature.split(","):
    #         key, value = item.replace("'", "").split(" : ")
    #         features[key.strip()] = int(value.strip())
    # else:
    #     print("raw_feature none")

    # parsed_data = [features]

    # --------------place category / tag-----------------

    # place_category_cd와 일치하는 kor_code_name 가져오기
    try:
        category_code = CodeTb.objects.get(code=place_category_cd)
        category_name = category_code.kor_code_name
    except CodeTb.DoesNotExist:
        category_name = ""

    # place_tag_cd와 일치하는 kor_code_name 가져오기
    try:
        place = PlaceTb.objects.filter(
            place_id=place_id
        ).first()  # first()는 결과가 없을 때 None을 반환합니다.

        if place is not None:
            # place가 None이 아닐 경우에만 place_tag_cd에 접근
            tag_cd = place.place_tag_cd
        else:
            # None일 경우 처리 로직
            print("PlaceTb에서 해당 id에 맞는 레코드가 없습니다.")

        # tag_name = tag_code.kor_code_name
    except CodeTb.DoesNotExist:
        tag_name = ""

    # -------------- review daily_tag_cd / with_tag_cd --------------
    # 각각의 리뷰에서 daily_tag와 with_tag의 code_name을 가져오기
    # for review in page_obj:
    #     review.daily_tag_name = ""
    #     review.with_tag_name = ""

    #     if review.review_daily_tag_cd:
    #         try:
    #             daily_tag = CodeTb.objects.get(code=review.review_daily_tag_cd)
    #             review.daily_tag_name = daily_tag.code_name
    #         except CodeTb.DoesNotExist:
    #             review.daily_tag_name = "Unknown Tag"

    #     if review.review_with_tag_cd:
    #         try:
    #             with_tag = CodeTb.objects.get(code=review.review_with_tag_cd)
    #             review.with_tag_name = with_tag.code_name
    #         except CodeTb.DoesNotExist:
    #             review.with_tag_name = "Unknown Tag"
    # -----------------------------------------------------
    place_feature = place.place_feature

    # 문자열을 ', '로 먼저 분리하고 각 요소에서 ' : '로 나눔
    feature_list = [feature.split(" : ") for feature in place_feature.split(", ")]
    # 공백 및 숫자가 아닌 문자를 제거하고 딕셔너리로 변환
    feature_dict = {
        key: int(value.replace("'", "").strip()) for key, value in feature_list
    }

    # ---------------------context-------------------------

    pos = place.place_pos_review_num
    neg = place.place_neg_review_num
    total = place.place_review_num

    pos_ratio = round((pos / total) * 100, 2)
    neg_ratio = round((neg / total) * 100, 2)
    neutral = round(100 - (pos_ratio + neg_ratio), 2)

    # -----------------------------------------------------

    real = place.place_review_num_real
    real_ratio = round((real / total) * 100, 2)
    ad = place.place_ad_review_num

    # -----------------------------------------------------

    context = {
        "place": place,
        "reviews": page_obj,
        "photo_subquery": photo_subquery,
        "feature_dict": feature_dict,
        "category_name": category_name,
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
    }

    # "review": review,
    # "features": features,
    # "parsed_data": parsed_data,

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        context = {
            "array": array,
            "serialized_reviews": serialized_reviews,
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
        }
        return JsonResponse(context, safe=False)

    return render(request, "review/reviews.html", context)


def reviews_more(request):
    place_id = request.GET.get("place_id")
    place_category_cd = request.GET.get("place_category_cd")
    array = request.GET.get("array", "latest")  # 정렬 방식 가져오기 (기본값은 최신순)
    page = request.GET.get("page", 1)  # 페이지 기본 1page

    photo_subquery = (
        ReviewTb.objects.filter(place_id=place_id, review_photo__gt="")
        .exclude(review_photo="h")
        .values_list("review_photo", flat=True)[:1]
    )

    place = (
        PlaceTb.objects.filter(place_id=place_id)
        .annotate(
            review_photo=Subquery(photo_subquery)
        )  # 리뷰 사진 가져오기 (Subquery 결과를 이용해 각 객체에 review_photo라는 필드를 추가)
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

    context = {
        "place": place,
        "reviews": page_obj,
        "photo_subquery": photo_subquery,
        "array": array,
        "current_page": page_obj.number,
        "total_pages": paginator.num_pages,
        "reviews": serialized_reviews,
    }

    # "review": review,
    # "features": features,
    # "parsed_data": parsed_data,

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        context = {
            "array": array,
            "serialized_reviews": serialized_reviews,
            "current_page": page_obj.number,
            "total_pages": paginator.num_pages,
        }
        return JsonResponse(context, safe=False)

    return render(request, "review/more.html", context)
