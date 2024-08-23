from django.shortcuts import render, get_object_or_404
from .models import Place_tb, Review_tb, Code_tb
from django.core.paginator import Paginator



def content_reviews(request, place_id, place_category_cd, place_tag_cd): 
    
    if place_category_cd == 'pc03': #popup 코드
        return render(request, 'popup_reviews.html', {'place_id': place_id})
    
    array = request.GET.get('array', 'latest')  # 정렬 방식 가져오기 (기본값은 최신순)
    page = request.GET.get('page', 1)  # 페이지 기본 1page

    
    place = get_object_or_404(Place_tb, pk=place_id)  # 콘텐츠 가져오기, 없으면 404
    reviews = Review_tb.objects.filter(place_id=place_id).order_by('-review_date')
    

    if array == 'oldest':
        reviews = reviews.order_by('review_date')
    
    paginator = Paginator(reviews, 6)  # 리뷰를 6개씩 나눠서 페이지를 나눈다
    page_obj = paginator.get_page(page)  # 페이지 번호에 해당하는 리뷰 객체 가져오기

    #------------------place_feature--------------------
    raw_feature = place.place_feature
    features = {}
    if raw_feature:
        for item in raw_feature.split(","):
            key, value = item.replace("'", "").split(" : ")
            features[key.strip()] = int(value.strip())
    
    parsed_data = [features]

    #--------------place category / tag-----------------

    # place_category_cd와 일치하는 code_name 가져오기
    try:
        category_code = Code_tb.objects.get(code=place_category_cd)
        category_name = category_code.code_name
    except Code_tb.DoesNotExist:
        category_name = ''

    # place_tag_cd와 일치하는 code_name 가져오기
    try:
        tag_code = Code_tb.objects.get(code=place_tag_cd)
        tag_name = tag_code.code_name
    except Code_tb.DoesNotExist:
        tag_name = ''
    
    #--------------context----------------------------
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
    }

    
    return render(request, 'reviews.html', context)





