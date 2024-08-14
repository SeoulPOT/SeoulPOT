from django.shortcuts import render
from datetime import datetime
from django.views.decorators.http import require_http_methods
import logging
from django.http import JsonResponse
from .models import district_tb

# Create your views here.

# 로깅 설정
logger = logging.getLogger(__name__)

# get method만 받음
@require_http_methods(["GET"])
def get_sever_time(request):
    try:
        context = {
            "now_time" : datetime.now().isoformat()
        }
        return render(request, 'main/main.html', context)
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        return JsonResponse({
            "error": "internal_server_error",
            "message": "An unexpected error occurred on the server."
        }, status=500)

@require_http_methods(["GET"])
def get_districts(request):
    try:

        # 해당 언어에 맞게 구별 정보를 불러옴 (예시로 한국어로만 처리)
        districts = district_tb.objects.all()
        response_data = { #확인필요
            "districts": [
                {
                    "district_id": district.id,
                    "district_name": district.district_name,
                    "district_img": district.district_img,
                    "district_desc": district.district_desc
                }
                for district in districts
            ]
        }
        return JsonResponse(response_data)
    
    except Exception as e:
        logger.error(f"Error fetching districts: {str(e)}")
        return JsonResponse({
            "error": "bad_request",
            "message": "The request is required and must be a valid language code."
        }, status=400)
