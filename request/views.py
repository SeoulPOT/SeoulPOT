from django.shortcuts import render, redirect
from main.models import RequestTb
from django.utils import timezone
import socket

def board_list(request, lang):
    requests = RequestTb.objects.all().order_by('-request_time')

    context = {
        'requests': requests,
        'lang' : lang
    }
    return render(request, 'request/board_list.html', context)

def board_create(request, lang):
    if request.method == "POST":
        request_text = request.POST.get('request_text')
        request_ip = get_client_ip(request)
        new_request = RequestTb(request_text=request_text, request_ip=request_ip, request_time=timezone.now())
        new_request.save()
        return redirect('main')
    
    context = {
        'lang' : lang
    }

    return render(request, 'request/board_create.html', context)

def get_client_ip(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if ip_address:
        ip = ip_address.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

from django.shortcuts import get_object_or_404

def board_delete(request, request_id, lang):
    # 해당 요청을 데이터베이스에서 가져옴
    board_request = get_object_or_404(RequestTb, pk=request_id)

    # 만약 IP 주소가 같다면 삭제
    if board_request.request_ip == get_client_ip(request):
        board_request.delete()
        return redirect('board_list')
    else:
        # 권한이 없을 경우 에러 페이지로 이동
        return render(request, 'request/no_permission.html')
