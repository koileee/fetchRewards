# fetchRewards
fetching rewards backend service

## To run the app

Move into the directory
`cd fetchRewards`

Build docker image from Dockerfile
`docker build -t fetchapp .`

Run the app
`docker run -p 5000:5000 fetchapp`

Go to `http://127.0.0.1:5000/receipts/process` with receipt payload to retrieve an id
Go to `http://127.0.0.1:5000/receipts/<receipt_id>/points` to retrieve the points

## Alternatively, you can build the docker image from dockerhub

this is the image hosted on [dockerHub](https://hub.docker.com/repository/docker/taroleee/fetchapp/general)

`docker pull taroleee/fetchapp:test`

`docker run -p 5000:5000 taroleee/fetchapp:test`
