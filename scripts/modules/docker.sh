docker_status(){

docker info >/dev/null 2>&1

}

running_containers(){

docker ps \
--format "table {{.Names}}\t{{.Status}}"

}

stopped_containers(){

docker ps -a \
--filter status=exited \
--format "table {{.Names}}\t{{.Status}}"

}

