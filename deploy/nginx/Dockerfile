FROM nginx:1.25.5-alpine
COPY ./deploy/nginx/stalker_op22_cyclic_quest_wiki.conf /etc/nginx/conf.d/stalker_op22_cyclic_quest_wiki.conf
RUN mkdir /nginx_data
COPY ./deploy/nginx/robots.txt  /nginx_data/robots.txt
COPY ./deploy/nginx/favicon.ico  /nginx_data/favicon.ico
