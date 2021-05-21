remove:
	@docker rm eyo -f
build:
	@docker build -t eyo:v1 .
run:
	@docker run -dp 8080:5000 --name eyo eyo:v1
bash:
	@docker exec -it eyo /bin/bash

all:
	@make remove
	@make build
	@make run
	@make bash
