build:
	docker build -t assessment .
run:
	docker run -p 8282:8282 -it assessment
test:
	docker run -it -e PYTHONPATH=/code assessment pytest