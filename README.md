# whats-cat-api
Cat breed classifier using Inceptionv3. Deployed using Tensorflow Serving and Flask, built with Docker Compose
## Dependencies
Install [docker](https://docs.docker.com/get-docker/) and [docker compose](https://docs.docker.com/compose/install/)
## Installation
1. Clone repository with `git clone https://github.com/devbcdestiller/whats-cat-api.git`
2. `cd whats-cat-api`
3. `docker-compose build`
4. `docker-compose up`
## Usage
HTTP Request: `http://localhost:5000/predict`
- Request Method: `POST`
- Request Body: `form-data`
- form-data: `{'img': *your_image*}`
