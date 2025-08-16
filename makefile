new:
	docker compose run --rm site new 

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose exec site build
