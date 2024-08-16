from django.db import models

class Request(models.Model):
    request_id = models.AutoField(primary_key=True)
    request_text = models.TextField()  # 게시물 내용
    request_time = models.DateTimeField(auto_now_add=True)  # 게시물 작성 시간
    request_ip = models.CharField(max_length=50)  # 작성자 IP 주소

    class Meta:
        db_table = 'request_tb'
    
    def __str__(self):
        return f"Request {self.request_id}"
