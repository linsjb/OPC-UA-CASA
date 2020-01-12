SERVER_CONTAINER_NAME := opc-server
SERVER_FILE_SOURCE := ${CURDIR}/server/src
SERVER_FILE_TARGET := /usr/opc/src
SERVER_IMAGE_NAME := freeopcua_debian_server

CLIENT_CONTAINER_NAME := opc-client
CLIENT_FILE_SOURCE := ${CURDIR}/client/src
CLIENT_FILE_TARGET := opc-client
CLIENT_IMG := {$SERVER_IMAGE_NAME}

build-server-image:
	docker build -t ${SERVER_IMAGE_NAME} -f Dockerfile ${CURDIR}/server

build-server-container:
	@docker run -it -d \
		--name ${SERVER_CONTAINER_NAME} \
		-p 4880:4881 \
		--mount type=bind,source=${SERVER_FILE_SOURCE},\target=/${SERVER_FILE_TARGET} \
		--network opc-ua-casa_default \
		${SERVER_IMAGE_NAME}

	@echo "${SERVER_CONTAINER_NAME} container created"
	@docker ps

start-server:
	@docker start ${SERVER_CONTAINER_NAME}
	@echo "${SERVER_CONTAINER_NAME} container started"
	@docker ps

stop-server:
	@docker stop ${SERVER_CONTAINER_NAME}
	@echo "${SERVER_CONTAINER_NAME} container stopped"
	@docker ps

enter-server:
	@docker exec -ti ${SERVER_CONTAINER_NAME} /bin/zsh

build-client-container:
	@docker run -it -d \
		--name ${CLIENT_CONTAINER_NAME} \
		--mount type=bind,source=${CLIENT_FILE_SOURCE},target=/${CLIENT_FILE_TARGET} \
		${CLIENT_IMG}

	@echo "${CLIENT_CONTAINER_NAME} docker container created"
	@docker ps

start-client:
	@docker start ${CLIENT_CONTAINER_NAME}
	@echo "${CLIENT_CONTAINER_NAME} container started"
	@docker ps

stop-client:
	@docker stop ${CLIENT_CONTAINER_NAME}
	@echo "${CLIENT_CONTAINER_NAME} container stopped"
	@docker ps

enter-client:
	@docker exec -ti ${CLIENT_CONTAINER_NAME} /bin/zsh