from django.shortcuts import render, get_object_or_404
from .models import Place_tb, Review_tb
from django.core.paginator import Paginator

def content_reviews(request, place_id):
    array = request.GET.get('array', 'latest')  # 정렬 방식 가져오기 (기본값은 최신순)
    page = request.GET.get('page', 1)  # 페이지 기본 1page

    
    place = get_object_or_404(Place_tb, pk=place_id)  # 콘텐츠 가져오기, 없으면 404
    reviews = Review_tb.objects.filter(place_id=place_id).order_by('-review_date')

    if array == 'oldest':
        reviews = reviews.order_by('review_date')
    
    paginator = Paginator(reviews, 6)  # 리뷰를 6개씩 나눠서 페이지를 나눈다
    page_obj = paginator.get_page(page)  # 페이지 번호에 해당하는 리뷰 객체 가져오기

    context = {
        
        'place': place,
        'reviews': page_obj,
        'array': array,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    }
    
    return render(request, 'reviews.html', context)



