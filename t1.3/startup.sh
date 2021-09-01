#!/usr/bin/env bash

# Start interacting with container
function log_in_container(){
	sleep 10

	# tail -f messages.log &
	docker exec -it ppd sh

	echo Finishing up containers...

	rm messages.log
	docker stop ppd rabbitmq
	exit 0
}

# Boot up containters
function start_up_containers() {
	echo "Waiting for rabbitmq host. This can take a few seconds..."
	docker-compose up --build >/dev/null & # Executes docker-compose in background
	if [[ $? -eq 0 ]]; then # Checks if cmd executed without errors
		while true; do
			nc -z localhost 5672
			if [[ $? -eq 0 ]]; then
				echo -e "Host is up, setting up containers...\n"
				log_in_container
			fi
		done
		else
			echo "Error while executing docker-compose"
			exit 1
	fi
}

# Check if cmd was executed as root
if [[ $EUID -ne 0 ]]; then
	echo "Por favor execute como root!"
	exit 1
fi
# Check if nc is installed
if ! ncat="$(type -p nc)" || [[ -z $ncat ]]; then
	echo "Por favor instale nc (netcat)"
	exit 1
fi
# Check if docker-compose is installed
if ! dockercomposeloc="$(type -p docker-compose)" || [[ -z $dockercomposeloc ]]; then
	echo "Por favor instale docker-compose"
	exit 1
else # Start routine
	if [[ ! -a messages.log ]]; then
		touch messages.log
	fi
	start_up_containers
fi
