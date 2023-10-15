start-env:
	docker-compose -f docker-compose.yaml up -d --build

stop-env:
	docker-compose -f docker-compose.yaml down --volumes
