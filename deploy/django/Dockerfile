FROM python:3.12.3-bullseye

# Установка переменных окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN mkdir /app/media
RUN mkdir /app/logs

# Установка зависимостей приложения
COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов приложения
COPY ./stalker_op22_cyclic_quest_wiki /app/stalker_op22_cyclic_quest_wiki
COPY ./stalker_op22_cyclic_quest_wiki_proj /app/stalker_op22_cyclic_quest_wiki_proj
COPY ./manage.py /app/manage.py
COPY ./deploy/settings.py /app/stalker_op22_cyclic_quest_wiki_proj/settings.py
COPY ./deploy/update.sh /app/update.sh
COPY ./data /app/data

RUN chmod +x /app/update.sh
# Запуск приложения
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stalker_op22_cyclic_quest_wiki_proj.wsgi:application"]
