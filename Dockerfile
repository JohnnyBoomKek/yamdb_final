# создать образ на основе базового слоя python (там будет ОС и интерпретатор Python)
FROM python:3.8.5

# создать директорию /code
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r /code/requirements.txt
COPY . /code
#Если я убираю это строчку докер все поднимает и все работает, однако тесты 
#Яндекса валятся и задание не принимается. Если убираю эту строчку из докеркомпоз
#Падает база данных с ошибками. Такие дела.
CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000