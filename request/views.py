from django.shortcuts import render, redirect
from .models import Request
from django.utils import timezone
import socket

def board_list(request):
    requests = Request.objects.all().order_by('-request_time')
    return render(request, 'board_list.html', {'requests': requests})

def board_create(request):
    if request.method == "POST":
        request_text = request.POST.get('request_text')
        request_ip = get_client_ip(request)
        new_request = Request(request_text=request_text, request_ip=request_ip, request_time=timezone.now())
        new_request.save()
        return redirect('board_list')
    return render(request, 'board_create.html')

def get_client_ip(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip = ip_address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

from django.shortcuts import get_object_or_404

def board_delete(request, request_id):
    # 해당 요청을 데이터베이스에서 가져옴
    board_request = get_object_or_404(Request, pk=request_id)

    # 만약 IP 주소가 같다면 삭제
    if board_request.request_ip == get_client_ip(request):
        board_request.delete()
        return redirect('board_list')
    else:
        # 권한이 없을 경우 에러 페이지로 이동
        return render(request, 'no_permission.html')