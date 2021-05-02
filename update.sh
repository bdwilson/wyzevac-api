docker stop wyzevac-api
docker rm wyzevac-api
docker rmi -f wyzevac-api
./build.sh
./run.sh
docker image prune
