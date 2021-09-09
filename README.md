## Author
Sam Moran - clicktravel-sammoran

## Description
As part of the Travelperk onboarding, an exercise in creating a Python/Django API.

## How to use it

Clone the repository:

```sh
git clone git@github.com:clicktravel-sammoran/TK-Django-Exercise.git
	cd TK-Django-Exercise
```

### Prerequisite

For the purpose of testing using enviroment variables within the excerise and also on Travis-CI, you will need to create a **.env** file at the root of your project containing the following fields subsitutated with your own values:
```sh
DB_USER=<user>
DB_PASS=<password>
DJANGO_SECRET_KEY=<secret_key>
```

```

Then you will need to build the docker image:

```sh
docker-compose build
```

Then you can run the server:

```sh
docker-compose up
```

Test the API sending your requests to the root URL `http://localhost:8000/`.
The following endpoints are available:

- Get all the recipes
  - **GET** /recipes/
- Filter recipes by name
  - **GET** /recipes/?name=`<query>`/
- Get recipe by key
  - **GET** /recipes/`<id>`/
- Create new recipe
  - **POST** /recipes/
- Edit a recipe
  - **PATCH** /recipes/`<id>`/
- Delete a recipe
  - **DELETE** /recipes/`<id>`/

## Examples

**GET** /recipes/

    [
      	{
	        'id': 1,
	        'name': 'Bangers and Mash'
	        'description': 'A hearty meal, perfect for the British winter',
	        'ingredients': [
		        {"name": 'Sausages'}, 
		        {"name": 'Potatoes'}, 
		        {"name": 'Gravy'},
        	]
		},
		{
	        'id': 2,
	        'name': 'Spaghetti Carbonara'
	        'description': 'An Italian dish',
	        'ingredients': [
		        {"name": 'Spaghetti'}, 
		        {"name": 'Egg'}, 
        	]
		}
    ]

**POST** /recipes/

    [
      	{
	        'name': 'Chicken Tikka Massala'
	        'description': 'A touch of the orient',
	        'ingredients': [
		        {"name": 'Chicken'}, 
		        {"name": 'Garlic'}, 
        	]
		}
    ]

**PATCH** /recipes/`<id>`

    [
      	{
	        'name': 'Chicken Tikka Massala'
	        'description': 'A touch of the orient',
	        'ingredients': [
		        {"name": 'Chicken'}, 
		        {"name": 'Garlic'},
		        {"name": 'Onion'}, 
        	]
		}
    ]

## Testing

Run the following command to check the tests, this will also use flake8 to ensure linting is correct:

```sh
docker-compose run --rm app sh -c "python manage.py test && flake8"
```