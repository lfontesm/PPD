#!/usr/bin/env bash

function log_in_container(){
	sleep 10
	docker exec -it ppd sh

	echo Finishing up containers...

	docker stop ppd rabbitmq
	exit 0
}

function start_up_containers() {
	docker-compose up >/dev/null &
	echo Waiting for rabbitmq host...
	if [[ $? -eq 0 ]]; then
		while true; do
			nc -z localhost 5672
			if [[ $? -eq 0 ]]; then
				echo -e "Host is up, setting up containers...\n"
				log_in_container
			fi
		done
	fi
}

# Check if cmd was executed as root
if [[ $EUID -ne 0 ]]; then
	echo pls exec as rooteh mah frend
	#exit
fi

# Start up the containers
if ! dockercomposeloc="$(type -p docker-compose)" || [[ -z $dockercomposeloc ]]; then
	echo install dis dood
else
	if [[ -a messages.log ]]; then
		rm messages.log
	fi
	start_up_containers
fi

#docker-compose up --build


