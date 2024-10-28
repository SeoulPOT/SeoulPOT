# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class CodeTb(models.Model):
    code = models.CharField(primary_key=True, max_length=50)
    kor_code_name = models.CharField(max_length=255)
    eng_code_name = models.CharField(max_length=255)
    code_desc = models.TextField(blank=True, null=True)
    parent_code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "code_tb"


class DistrictTb(models.Model):
    district_id = models.AutoField(primary_key=True)
    kor_district_name = models.CharField(max_length=255)
    eng_district_name = models.CharField(max_length=255)
    kor_district_desc = models.TextField(blank=True, null=True)
    eng_district_desc = models.TextField(blank=True, null=True)
    district_lat = models.FloatField(blank=True, null=True)
    district_lon = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "district_tb"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class LogTb(models.Model):
    log_id = models.AutoField(primary_key=True)
    user_ip = models.CharField(max_length=50, blank=True, null=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)
    page_url = models.CharField(max_length=255, blank=True, null=True)
    click_timestamp = models.DateTimeField(blank=True, null=True)
    button_id = models.CharField(max_length=50, blank=True, null=True)
    additional_info = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "log_tb"


class PlaceTb(models.Model):
    place_id = models.AutoField(primary_key=True)
    district = models.ForeignKey(DistrictTb, models.DO_NOTHING, blank=True, null=True)
    place_name = models.CharField(max_length=255)
    place_address = models.CharField(max_length=255, blank=True, null=True)
    place_phone = models.CharField(max_length=50, blank=True, null=True)
    place_operating_hours = models.CharField(max_length=255, blank=True, null=True)
    place_desc = models.CharField(max_length=255, blank=True, null=True)
    place_url = models.CharField(max_length=255, blank=True, null=True)
    place_review_num = models.IntegerField(blank=True, null=True)
    place_pos_review_num = models.IntegerField(blank=True, null=True)
    place_neg_review_num = models.IntegerField(blank=True, null=True)
    place_ad_review_num = models.IntegerField(blank=True, null=True)
    place_thema_cd = models.CharField(max_length=50, blank=True, null=True)
    place_category_cd = models.CharField(max_length=50, blank=True, null=True)
    place_tag_cd = models.CharField(max_length=50, blank=True, null=True)
    place_lat = models.FloatField(blank=True, null=True)
    place_lon = models.FloatField(blank=True, null=True)
    place_subway_station = models.CharField(max_length=100, blank=True, null=True)
    place_distance = models.CharField(max_length=100, blank=True, null=True)
    kor_ai_review_text = models.TextField(blank=True, null=True)
    eng_ai_review_text = models.TextField(blank=True, null=True)
    # place_review_num = models.Intege
    # rField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "place_tb"


class RequestTb(models.Model):
    request_id = models.AutoField(primary_key=True)
    request_text = models.TextField(blank=True, null=True)
    request_time = models.DateTimeField(blank=True, null=True)
    request_ip = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "request_tb"


class ReviewTb(models.Model):
    review_id = models.AutoField(primary_key=True)
    place = models.ForeignKey(PlaceTb, models.DO_NOTHING, blank=True, null=True)
    kor_review_text = models.TextField(blank=True, null=True)
    eng_review_text = models.TextField(blank=True, null=True)
    review_photo = models.TextField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    review_sentiment = models.IntegerField(blank=True, null=True)
    review_advertising = models.IntegerField(blank=True, null=True)
    similar_review = models.TextField(blank=True, null=True)
    review_with_tag_cd = models.CharField(max_length=50, blank=True, null=True)
    review_daily_tag_cd = models.CharField(max_length=50, blank=True, null=True)
    has_photo = models.BooleanField(blank=False)

    class Meta:
        managed = False
        db_table = "review_tb"


class ReviewTbTemp(models.Model):
    place_name = models.TextField(blank=True, null=True)
    place_address = models.TextField(blank=True, null=True)
    kor_review_text = models.TextField(blank=True, null=True)
    eng_review_text = models.TextField(blank=True, null=True)
    review_photo = models.TextField(blank=True, null=True)
    review_date = models.DateField(blank=True, null=True)
    review_sentiment = models.IntegerField(blank=True, null=True)
    review_advertising = models.IntegerField(blank=True, null=True)
    similar_review = models.TextField(blank=True, null=True)
    review_with_tag_cd = models.CharField(max_length=50, blank=True, null=True)
    review_daily_tag_cd = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "review_tb_temp"
