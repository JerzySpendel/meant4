build:
	docker build -t assessment .
run:
	docker run -p 8282:8282 -it assessment