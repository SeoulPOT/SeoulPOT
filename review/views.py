from django.shortcuts import render, get_object_or_404
from main.models import PlaceTb, ReviewTb
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef
import json

def content_reviews(request):
    place_id = request.GET.get('place_id')
    place_category_cd = request.GET.get('place_category_cd')

    if place_category_cd == 'PC04': #popup 코드는 지정 필요
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
    
    paginator = Paginator(reviews, 4)  # 리뷰를 6개씩 나눠서 페이지를 나눈다
    page_obj = paginator.get_page(page)  # 페이지 번호에 해당하는 리뷰 객체 가져오기

    context = {
        
        'place': place, 
        'reviews': page_obj,
        'array': array,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    }
    
    return render(request, 'review/reviews.html', context)



