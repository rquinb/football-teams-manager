# football-teams-manager
Everything needed for managing football matches

## How to run it

In order to run it you will need docker installed

1. `cd` into project repo
1. `docker-compose up --build` to start the server
1. After build completes you should be able to visit `http://localhost:5000` in order to access main page

## How to stop the server

1. `docker-compose down`
1. In case you also would like to delete databases and files generated run `docker-compose down -v`

