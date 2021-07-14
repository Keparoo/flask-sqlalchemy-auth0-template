# Title Of Project

Project description

---

## Features
- Bullet points of features


## API URL 
- **Deployed App URL:** https://deployed_url.herokuapp.com/
- **Localhost base URL:**  is http://127.0.0.1:5000/
---  
## Getting Started

### Installation and Database Setup

Clone the repo by running 

```bash
git clone https://github.com/Keparoo/name_of_repository.git
```
#### Key Dependencies

- [Python 3.8.5](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python) This project was developed using Python 3.8.5 and the project will not run with versions of Python below 3.6.

#### Virtual Enviornment

It is recommended to work within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

```bash
python3 -m venv venv
```

Activate the virtual environment:

```bash
. venv/bin/activate
```

#### Installing Python Dependencies

Once the virtual environment is setup and running, install the required dependencies by navigating to the project directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages in the `requirements.txt` file.

---

## Database Setup

The project uses **PostgreSQL** databases.
- Create two databases: One for **testing** and one for **development**
```bash
createdb <database_name>
```
- Generate database tables from the migration files included by executing: 
  `python manage.py db upgrade`
- Add starter data by executing:
  `python manage.py seed`

- Set the `DATABASE_URL` and `TEST_DATABASE_URL` in `.env` file to match the names of your development and testing databases.

## Running the Server
Switch to the project directory and ensure that the virtual environment is running.

#### To run the **development** server, execute:  

```bash
source setup.sh
flask run
```
--- 

## Environment Variables  
Create a `.env` file matching the template provided in the `.env.example` file. All environmental variables must be populated with the appropriate `auth0` constants and `PostgreSQL` database URLs in order for the application to function.  

---
## Authentication and Authorization
Authentication is implemented in the form of RBAC (Role Based Access Control) using [Auth0](https://auth0.com/)
#### Roles & Permissions
- List of Roles & Permissions  

The following is the formula for the URL that will open the **auth0** login page and after login return a JWT for the **auth0** account:  
  `AUTH0_BASE_URL + 'authorize?audience=' + AUTH0_AUDIENCE + '&response_type=token&client_id=' + AUTH0_CLIENT_ID + '&redirect_uri=' + AUTH0_CALLBACK_URL`

To create an authorization system matching the API see the docs at [Auth0](https://auth0.com/docs/api/management/v2)  
- Create an **auth0** account
- In the **auth0 dashboard** create a single page application
    - Add the following URLs to the Allowed Callback URLs:  
        1. http://127.0.0.1:5000/callback  
        2. https://name-of-app.herokuapp.com/callback
    - Add the following URLs to the Allowed Logout URLs:  
        1. http://127.0.0.1:5000/ 
        2. https://name-of-app.herokuapp.com/
        3. http://127.0.0.1:5000/login
        4. https://name-of-app.herokuapp.com/login
- Create an API
    - Turn on `Enable RBAC` and `Add Permissions in the Access Token`
- Add authorized users
- Create roles for the users
- Create and assign permissions to the roles
- Update the `AUTH0_DOMAIN`, `API_AUDIENCE`, `AUTH0_CLIENT_ID`, `AUTH0_CLIENT_SECRET`, and `AUTH0_CALLBACK_URL` constants in the `.env` file
---
## Testing

Replace the JWT tokens in `test_app.py` with ones generated on the website. JWT tokens expire 24 hours from generation.

For testing locally, stop the development server and reset the database.
The following resets the database and runs the test suite:

```bash
source setup_test.sh
```

Two Postman collections are also included for further testing.
- `name-of-collection-local.postman_collection.json`
- `name-of-collection-deployed.postman_collection.json`

To use them install [Postman](https://www.postman.com/downloads/) locally and import the 2 collections. In order for them to work properly, update the Bearer Tokens in each collection with tokens generated from the website. See the Authorization section.

---
## Deployment

This project is deployed to [Heroku](https://heroku.com). To Deploy your own version:
- You must have Git installed and your project must be tracked in a repository
- Install Heroku locally: https://devcenter.heroku.com/articles/heroku-cli
- Create your heroku app:
```bash
heroku create <name_of_app>
```
- Add `heroku` as a Git remote and push your project to `Heroku` (Change `main` to the name of the appropriate git brach if it differs, i.e. `master`)
```bash
git remote add heroku <heroku_git_url>
git push heroku main
```
- Create a postgres database in Heroku:
```bash
heroku addons:create heroku-postgresql:hobby-dev --app <name_of_app>
```
- go to settings on the [Heroku dashboard](https://dashboard.heroku.com/) for the app you've built and click on `Show Environment Variables`. You will need to set environmental variables for each variable found in the `.env.example` file.

- Once your app is deployed, run migrations by running:
```bash
heroku run python manage.py db upgrade --app <name_of_app>
```
- To see the Heroku logs for debugging:
```bash
heroku logs --tail
```
- To reset the Heroku database:
```bash
heroku run python manage.py db downgrade --app <name_of_app>
heroku run python manage.py db upgrade --app <name_of_app>
heroku run python manage.py seed --app <name_of_app>
```
---

## API

In order to use the API, users need to be authenticated. JWT tokens can be generated by logging in with the provided credentials on the hosted site.

### Endpoints

- Note: any `curl` commands used must include an authorization header as all endpoints require authorization to use:  
`curl -H "Authorization: Bearer <JWT_ACCESS_TOKEN>"`

#### GET /movies

- General:

  - Returns a list of all the movies in database.
  - Request arguments: None
  - Roles authorized : Casting Assistant, Casting Director, Executive Producer
  - Required permission: `get:movies`

- Sample: `curl http://127.0.0.1:5000/movies`

```json
{
    "movies": [
        {
            "id": 1,
            "release_date": "Fri, 19 Jan 2018 05:00:00 GMT",
            "title": "Call Me By Your Name"
        },
        {
            "id": 2,
            "release_date": "Wed, 30 Sep 2020 05:00:00 GMT",
            "title": "The Boys in the Band"
        }
        ],
    "success": true
}
```

#### GET /movies/\<int:id>

- General:

  - Returns the specific movie matching the provided id.
  - Request arguments: id (The ID of the movie)
  - Roles authorized : Casting Assistant, Casting Director, Executive Producer
  - Required permission: `get:movies`
  - Returns a 404 if movie is not in database

- Sample: `curl http://127.0.0.1:5000/movies/1`

```json
{
  "movie": {
    "id": 1,
    "release_date": "Fri, 19 Jan 2018 05:00:00 GMT",
    "title": "Call Me By Your Name"
  },
  "success": true
}
```

#### POST /movies

- General:

  - Creates a new movie with the provided parameters.
  - Request arguments: None
  - Roles authorized : Executive Producer
  - Required permission: `post:movies`
  - All fields must be populated:
  - Request Body: 
  ```json
    {
        "title": "The Boys in the Band",
        "release_date": "2020-09-30"
    }
  ```

- Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Content-Type: application/json" -d '{ "title": "The Boys in the Band", "release_date": "2020-09-30" }'`

```json
{
  "movie": {
    "id": 3,
    "release_date": "Wed, 30 Sep 2020 05:00:00 GMT",
    "title": "The Boys in the Band"
  },
  "success": true
}
```

#### PATCH /movies/\<int:id>

- General:

  - Updates a movie with the provided parameters.
  - Request Arguments: id (The ID of the movie to update)
  - Roles authorized : Casting Director, Executive Producer
  - Required permission: `patch:movies`
  - Returns a 404 if movie is not in database
  - All fields must be populated
  - Request Body:
  ```json
    {
      "title": "The Boys in the Band Updated",
      "release_date": "2018-01-19"
    }
  ```
- Sample: `curl http://127.0.0.1:5000/movies/3 -X PATCH -H "Content-Type: application/json" -d '{ "title": "The Boys in the Band Updated", "release_date": "2018-01-19" }'`

```json
{
  "movie": {
    "id": 3,
    "release_date": "Fri, 19 Jan 2018 05:00:00 GMT",
    "title": "The Boys in the Band Updated"
  },
  "success": true
}
```

#### DELETE /movies/\<int:id>

- General:

  - Deletes a specific movie matching the provided movie id.
  - Request Arguments: id (The ID of the movie to delete)
  - Roles authorized : Executive Producer
  - Required permission: `delete:movie`
  - Returns a 404 if movie is not in database

- Sample: `curl http://127.0.0.1:5000/movies/3 -X DELETE`

```json
{
  "delete": 3,
  "success": true
}
```

---

## Error Handling

- 401 and 403 errors due to authorization are returned as

```json
{
  "code": "unauthorized",
  "description": "Permission not found."
}
```

Other errors are returned in the following json format:

```json
{
  "success": "False",
  "error": 404,
  "message": "resource not found"
}
```

The error codes currently returned are:

- 400 – bad request
- 401 – unauthorized
- 403 - forbidden
- 404 – resource not found
- 422 – unprocessable
- 500 – internal server error

### Author
Kep Kaeppeler is the author of this project and all documentation.