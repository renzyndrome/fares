
## Branch Naming

| Type        | Description           |
| ------------- |:-------------:|
| feat      | Feature I'm adding or expanding |
| bug      | Bug fix or experiment      |
| hotfix | Quick patch on a ceertain release      |
| junk | Throwaway branch created to experiment      |

*branch/type-of-branch/short-desc*


### build components:
docker-compose build

### Run the server
docker-compose up -d

### ssh into docker
docker exec -ti image_name bash

tailing docker logs docker logs -f image_name

#### After running docker up command, check port 3000 if the app is running

### Rebuilding
$ docker-compose stop

$ docker-compose rm -f

$ docker-compose build

$ docker-compose up -d

$ docker-compose exec web_1 bash

$ python manage.py migrate