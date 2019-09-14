# flaskSaas

Forked form alectrocute's fork of [Max Halford's](https://github.com/MaxHalford) [flask-boilerplate](https://github.com/MaxHalford/flask-boilerplate). Added 3 ML models attempting to predict Disney's stock price. Added as well matplotlib graphs rendered in flask.

## Setup

### Vanilla

- Install the requirements and setup the development environment.

	`make install && make dev`

- Create the database.

	`python manage.py initdb`

- Run the application.

	`python manage.py runserver`

- Navigate to `localhost:5000`.

trainmodel2.py contails the code for training the three models using sklearn
