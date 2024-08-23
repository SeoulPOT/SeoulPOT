
from django.db import models

class Code_tb(models.Model):
    code = models.CharField(max_length=15, primary_key=True)
    code_name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'code_tb'

class Place_tb(models.Model):
    place_id = models.IntegerField(primary_key=True)
    place_name = models.CharField(max_length=200)
    place_address = models.CharField(max_length=2000)
    place_phone = models.CharField(max_length=15)
    place_review_num = models.IntegerField()
    place_operating_hours = models.CharField(max_length=200)
    place_entrance_fee = models.IntegerField(default=0)
    place_desc = models.CharField(max_length=2000)
    place_url = models.CharField(max_length=300)
    place_feature = models.CharField(max_length=200)
    place_keyword_cd = models.CharField(max_length=200)
    place_category_cd = models.CharField(max_length=100)
    place_tag_cd = models.CharField(max_length=200)
    # img_path = models.CharField(max_length=2000)
    
    
    def __str__(self) -> str:
        return self.place_name

    class Meta:
        db_table = 'place_tb' # 실제 연동할 데이터 테이블이름을 지정

class Review_tb(models.Model):
    review_id = models.IntegerField(primary_key=True)
    place_id = models.ForeignKey(Place_tb, on_delete=models.CASCADE, db_column='place_id')
    review_text = models.TextField()  # 리뷰 내용
    review_photo = models.CharField(max_length=2000)
    review_date = models.DateField()  # 리뷰 날짜
    review_sentiment = models.BooleanField()
    review_advertising = models.BooleanField()
    review_with_tag_cd = models.CharField(max_length=255)  # 리뷰 태그 (예: "#with,#daily,#특징")
    review_daily_tag_cd = models.CharField(max_length=255)
    

    def __str__(self):
        return f'Review for {self.place}'

    class Meta:
        db_table = 'review_tb'  # 실제 연동할 데이터 테이블이름을 지정
    

    
