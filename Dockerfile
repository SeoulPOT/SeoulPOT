FROM python:3.12 AS python-build

# 필요한 빌드 도구 및 라이브러리 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    gcc

# mysqlclient 설치
RUN pip install mysqlclient

FROM python:3.12-slim

# 런타임에 필요한 라이브러리 및 도구 설치
RUN apt-get update && apt-get install -y \
    libmariadb3 \
    libmariadb-dev \
    default-libmysqlclient-dev \
    gcc \
    nginx \
    && apt-get clean

# 파이썬 모듈 설치 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Nginx 설정 복사
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# Django server
RUN mkdir /app
COPY . /app
WORKDIR /app

# 환경변수 적용 
ENV SECRET_KEY 'django-insecure-msabi9_e7sw@y86fmyztm8-uni*%c$(bqv7x1zsy8!37nch@g1' 
COPY run.sh .
RUN chmod +x run.sh
CMD ["./run.sh"]

