FROM python:3.12 AS python-build

RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    gcc
    
RUN pip install mysqlclient

FROM python:3.12-slim
COPY --from=python-build /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
RUN apt-get update && apt-get install -y libmariadb3 nginx

# 파이썬 모듈 설치 
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Nginx
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
