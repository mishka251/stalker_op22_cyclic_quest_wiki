docker image rm mishka251/stalker_op22_cyclic_quest_wiki-django:v0.1.0
docker image rm mishka251/stalker_op22_cyclic_quest_wiki-nginx:v0.1.0

docker image build -f ./deploy/django/Dockerfile -t mishka251/stalker_op22_cyclic_quest_wiki-django:v0.1.0 .
docker image build -f ./deploy/nginx/Dockerfile -t mishka251/stalker_op22_cyclic_quest_wiki-nginx:v0.1.0 .
