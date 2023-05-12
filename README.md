# NDBI040 Virtuoso

## Run the examples

Requires docker.

1. clone the repository
2. `docker compose up`
3. (different terminal) `docker exec -it ndbi040-python-1 bash`
4. (inside the newly opened bash) `python generate_data.py`
5. (to run the queries) `python benchmark_queries.py`
