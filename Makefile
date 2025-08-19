db_up:
	podman run -d \
		--name octopus-database \
		--network host \
	    -e POSTGRES_PASSWORD=octopus \
        -e POSTGRES_USER=octopus \
        -e POSTGRES_DB=octopus \
	    -p 5432:5432 \
		docker.io/postgres:latest

run_etl:
	uv run -m octopus_exercise.etl.run

run_app:
	uv run fastapi dev octopus_exercise/main.py

test:
	uv run pytest
