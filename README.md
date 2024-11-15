# URL Shortener App

A simple URL shortener built with Django, which includes statistics tracking for shortened URLs.

## Features

- Shorten any URL and get a unique shortened URL.
- Retrieve the original URL from the shortened one.
- Track click statistics (click count) for each shortened URL.

## Installation

Follow the steps below to set up this project locally:

### 1. Clone the repository:

git clone [<repository_url>](https://github.com/markwagdy/urlShortener.git)
cd urlshortnerapp

### 2. Set up a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate

###3. Install dependencies:
pip3 install -r requirements.txt


### 4. Set up your environment variables:
Create a .env file in the project root and add the following configuration:

DATABASE_NAME=django_db
DATABASE_USER=mark
DATABASE_PASSWORD=mark1234
DATABASE_HOST=localhost
DATABASE_PORT=5432
CELERY_BROKER_URL=redis://localhost:6379/0

### 5. Apply migrations:
Run the Django migrations to set up the database:

python3 manage.py migrate

### 6. Run the server:

python3 manage.py runserver

### API Endpoints
  1. Shorten URL
  URL: /api/shorten/
  Method: POST
  Request Body:
  {
    "original_url": "https://example.com"
  }
  Response:
  json
  {
    "data": {
      "shortened_url": "abc123"
    }
  }
  2. Get Original URL
  URL: /api/{shortened_url}/
  Method: GET
  Response:
  json
  {
    "data": {
      "original_url": "https://example.com"
    }
  }
  3. Get URL Statistics
  URL: /api/stats/{shortened_url}/
  Method: GET
  Response:
  {
    "data": {
      "clicks": 5
    }
  }
### Running Tests
  1. Install test dependencies:
  pip3 install -r requirements-test.txt

  2. Run tests:
  You can run the tests using pytest:
  python3 -m pytest './tests.py'

  3. Use Django Database for tests:
  Make sure to use the @pytest.mark.django_db marker for database access during tests, like in the provided example tests.

Contributing
If you'd like to contribute, please fork the repository and submit a pull request. Contributions are always welcome!

License
This project is licensed under the MIT License - see the LICENSE file for details.

