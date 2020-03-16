### build components:
docker-compose build

### Run the server
docker-compose up -d

### ssh into docker
docker exec -ti image_name bash

tailing docker logs docker logs -f image_name

#### After running docker up command, check port 3000 if the app is running