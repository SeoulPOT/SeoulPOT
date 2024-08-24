from django.shortcuts import render, get_object_or_404
from main.models import PlaceTb, ReviewTb, CodeTb
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef
from django.http import JsonResponse
import json

def content_reviews(request): 
    place_id = request.GET.get('place_id')
    place_category_cd = request.GET.get('place_category_cd')
    

    if place_category_cd == 'pc03': #popup 코드
        return render(request, 'popup_reviews.html', {'place_id': place_id})
    
    array = request.GET.get('array', 'latest')  # 정렬 방식 가져오기 (기본값은 최신순)
    page = request.GET.get('page', 1)  # 페이지 기본 1page

    photo_subquery = ReviewTb.objects.filter(
        place_id=OuterRef('place_id'),
        review_photo__gt=''
    ).values('review_photo')[:1]

    place = (PlaceTb.objects
                      .filter(place_id=place_id)
                      .annotate(review_photo=Subquery(photo_subquery))  # 리뷰 사진 가져오기 (Subquery 결과를 이용해 각 객체에 review_photo라는 필드를 추가)
                      .first())  # place_review_num을 기준으로 정렬
    print(place)

    
    # place = get_object_or_404(PlaceTb, pk=place_id)  # 콘텐츠 가져오기, 없으면 404

    reviews = ReviewTb.objects.filter(place_id=place_id).order_by('-review_date')

    if array == 'oldest':
        reviews = reviews.order_by('review_date')
    
    paginator = Paginator(reviews, 6)  # 리뷰를 6개씩 나눠서 페이지를 나눈다
    page_obj = paginator.get_page(page)  # 페이지 번호에 해당하는 리뷰 객체 가져오기
    
    review_field_names = [field.name for field in ReviewTb._meta.fields]
    serialized_reviews = list(page_obj.object_list.values(*review_field_names))
    #------------------place_feature--------------------
    features = {}
    raw_feature = place.place_feature
    
    if raw_feature:
        print(f'raw_feature: ${raw_feature}');
        for item in raw_feature.split(","):
            key, value = item.replace("'", "").split(" : ")
            features[key.strip()] = int(value.strip())
    else:
        print('raw_feature none')
    
    parsed_data = [features]

    #--------------place category / tag-----------------

    # place_category_cd와 일치하는 code_name 가져오기
    try:
        category_code = CodeTb.objects.get(code=place_category_cd)
        category_name = category_code.code_name
    except CodeTb.DoesNotExist:
        category_name = ''

    # place_tag_cd와 일치하는 code_name 가져오기
    try:
        tag_code = CodeTb.objects.get(code=place.place_tag_cd)
        tag_name = tag_code.code_name
    except CodeTb.DoesNotExist:
        tag_name = ''

    # -------------- review daily_tag_cd / with_tag_cd --------------
    # 각각의 리뷰에서 daily_tag와 with_tag의 code_name을 가져오기
    for review in page_obj:
        review.daily_tag_name = ''
        review.with_tag_name = ''

        if review.review_daily_tag_cd:
            try:
                daily_tag = CodeTb.objects.get(code=review.review_daily_tag_cd)
                review.daily_tag_name = daily_tag.code_name
            except CodeTb.DoesNotExist:
                review.daily_tag_name = "Unknown Tag"

        if review.review_with_tag_cd:
            try:
                with_tag = CodeTb.objects.get(code=review.review_with_tag_cd)
                review.with_tag_name = with_tag.code_name
            except CodeTb.DoesNotExist:
                review.with_tag_name = "Unknown Tag"

    #---------------------context-------------------------

    context = {     
        'place': place,
        'reviews': page_obj,
        'features': features,
        'category_name': category_name,
        'tag_name': tag_name,
        'array': array,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'parsed_data': parsed_data,
        'review_num': place.place_review_num,
        'review': review,

    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        context = {
            'array': array,
            'reviews': serialized_reviews,
            'current_page': page_obj.number,
            'total_pages': paginator.num_pages,
        }
        return JsonResponse(context, safe=False)

    
    return render(request, 'review/reviews.html', context)