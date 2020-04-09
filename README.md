
## Branch Naming

| Type        | Description           |
| ------------- |:-------------:|
| feat      | Feature I'm adding or expanding |
| bug      | Bug fix or experiment      |
| hotfix | Quick patch on a ceertain release      |
| junk | Throwaway branch created to experiment      |

*branch/type-of-branch/short-desc*

# Pulling the latest updated
$ git pull origin development

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

$ docker exec -ti fares_db_1 bash

$ python manage.py migrate users

$ python manage.py migrate facility

$ python manage.py migrate

### Controlling Admin Page

$ python manage.py createsuperuser

### Controlling Cashier Page

1. Create Cashier Profile
2. Under Top_Up Page - Cashier can see Users Registered
3. Change values to update balances.

