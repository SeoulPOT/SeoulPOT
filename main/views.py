from django.shortcuts import render
from datetime import datetime
from django.views.decorators.http import require_http_methods
import logging
from django.http import JsonResponse

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