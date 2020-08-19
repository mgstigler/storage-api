docker:
	docker build --tag hundred-acre/storage-api:latest .

run: docker	
	docker run -p 5000:5000 --env-file .env hundred-acre/storage-api

requirements:
	pip3 install --no-cache-dir -r requirements.txt