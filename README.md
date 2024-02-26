## How to run instructions

Docker is required to run the solution. In order to run the server you need to build the image and run the container.

    make build
    make run

Building the image may take a moment as it will download the `face_recognition` Python library which weight is significant.
Once the server is running the app should be accessible on port 8282 on host.

To connect to the websocket use the following URL:

`ws://localhost:8282/faces`

You can also take a look at the API documentation at `http://localhost:8282/docs`

To run tests:

    make test

### Additional notes on implementation choices

#### Web framework

The choices that I considered were Django and FastAPI.
The advantages of Django that I could see:

* Django's file systems classes and easier file management

Advantages of FastAPI

* Less boilerplate code
* Everything is async and doesn't require a dedicated tool for background tasks / queues.
* Easy to implement websockets

Given that, I chose FastAPI.


#### Package manager

Tools such as `poetry` / `pmd` / `pipenv` when used together with Docker almost always require a multi-stage build to do it correctly.
I decided for a basic `pip` and `requirements.txt` that works and doesn't require a lengthy Dockerfile configuration.


#### Tests

A few integration tests were added to test the HTTP API.