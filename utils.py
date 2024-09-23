from  main.models import LogTb
from datetime import datetime
import pytz

def SaveLog(request):

    kst = pytz.timezone('Asia/Seoul')

    user_ip = request.META.get('REMOTE_ADDR')
    button_id = request.GET.get('button_id')
    add_info = request.GET.get('add_info')
    session_id = request.GET.get('session_id')
    page_url = request.path
    
    log_entry = LogTb(user_ip=user_ip, page_url=page_url, button_id=button_id, additional_info=add_info, session_id=session_id, click_timestamp=datetime.now(kst))
    log_entry.save()