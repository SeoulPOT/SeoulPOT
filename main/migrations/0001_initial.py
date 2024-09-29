# Generated by Django 5.1.1 on 2024-09-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CodeTb',
            fields=[
                ('code', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('kor_code_name', models.CharField(max_length=255)),
                ('eng_code_name', models.CharField(max_length=255)),
                ('code_desc', models.TextField(blank=True, null=True)),
                ('parent_code', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'code_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DistrictTb',
            fields=[
                ('district_id', models.AutoField(primary_key=True, serialize=False)),
                ('kor_district_name', models.CharField(max_length=255)),
                ('eng_district_name', models.CharField(max_length=255)),
                ('kor_district_desc', models.TextField(blank=True, null=True)),
                ('eng_district_desc', models.TextField(blank=True, null=True)),
                ('district_lat', models.FloatField(blank=True, null=True)),
                ('district_lon', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'district_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='LogTb',
            fields=[
                ('log_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_ip', models.CharField(blank=True, max_length=50, null=True)),
                ('session_id', models.CharField(blank=True, max_length=255, null=True)),
                ('page_url', models.CharField(blank=True, max_length=255, null=True)),
                ('click_timestamp', models.DateTimeField(blank=True, null=True)),
                ('button_id', models.CharField(blank=True, max_length=50, null=True)),
                ('additional_info', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'log_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PlaceTb',
            fields=[
                ('place_id', models.AutoField(primary_key=True, serialize=False)),
                ('place_name', models.CharField(max_length=255)),
                ('place_address', models.CharField(blank=True, max_length=255, null=True)),
                ('place_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('place_operating_hours', models.CharField(blank=True, max_length=255, null=True)),
                ('place_entrance_fee', models.CharField(blank=True, max_length=50, null=True)),
                ('place_desc', models.CharField(blank=True, max_length=255, null=True)),
                ('place_url', models.CharField(blank=True, max_length=255, null=True)),
                ('place_review_num', models.IntegerField(blank=True, null=True)),
                ('place_pos_review_num', models.IntegerField(blank=True, null=True)),
                ('place_neg_review_num', models.IntegerField(blank=True, null=True)),
                ('place_ad_review_num', models.IntegerField(blank=True, null=True)),
                ('place_feature', models.TextField(blank=True, null=True)),
                ('place_thema_cd', models.CharField(blank=True, max_length=50, null=True)),
                ('place_category_cd', models.CharField(blank=True, max_length=50, null=True)),
                ('place_tag_cd', models.CharField(blank=True, max_length=50, null=True)),
                ('place_lat', models.FloatField(blank=True, null=True)),
                ('place_lon', models.FloatField(blank=True, null=True)),
                ('place_review_num_real', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'place_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='RequestTb',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('request_text', models.TextField(blank=True, null=True)),
                ('request_time', models.DateTimeField(blank=True, null=True)),
                ('request_ip', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'request_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewTb',
            fields=[
                ('review_id', models.AutoField(primary_key=True, serialize=False)),
                ('kor_review_text', models.TextField(blank=True, null=True)),
                ('eng_review_text', models.TextField(blank=True, null=True)),
                ('review_photo', models.TextField(blank=True, null=True)),
                ('review_date', models.DateField(blank=True, null=True)),
                ('review_sentiment', models.IntegerField(blank=True, null=True)),
                ('review_advertising', models.IntegerField(blank=True, null=True)),
                ('similar_review', models.TextField(blank=True, null=True)),
                ('review_with_tag_cd', models.CharField(blank=True, max_length=50, null=True)),
                ('review_daily_tag_cd', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'review_tb',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='ReviewTbTemp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('place_name', models.TextField(blank=True, null=True)),
                ('place_address', models.TextField(blank=True, null=True)),
                ('kor_review_text', models.TextField(blank=True, null=True)),
                ('eng_review_text', models.TextField(blank=True, null=True)),
                ('review_photo', models.TextField(blank=True, null=True)),
                ('review_date', models.DateField(blank=True, null=True)),
                ('review_sentiment', models.IntegerField(blank=True, null=True)),
                ('review_advertising', models.IntegerField(blank=True, null=True)),
                ('similar_review', models.TextField(blank=True, null=True)),
                ('review_with_tag_cd', models.CharField(blank=True, max_length=50, null=True)),
                ('review_daily_tag_cd', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'review_tb_temp',
                'managed': False,
            },
        ),
    ]
