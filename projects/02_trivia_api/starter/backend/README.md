# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## Error Handling

Errors are returned by the API as JSON objects in the following format:

```
{
    "success": False,
    "error": 404,
    "message": "Not found"
}
```

The API may return one of four expected error types when requests fail:

- 400: Bad request
- 404: Not found
- 405: Method not allowed
- 422: Unprocessable entity

## Endpoints

GET /categories

- Fetches a dictionary of categories in which the keys are the category IDs and the value is the corresponding string for that category
- Request arguments: None
- Returns: An object with two keys, success and categories.
- Example request:
    `curl localhost:3000/categories`
- Example response:
    ```
    {
        "success": True,
        "categories": {
            "1" : "Science",
            "2" : "Art",
            "3" : "Geography",
            "4" : "History",
            "5" : "Entertainment",
            "6" : "Sports"
        }
    }
    ```

GET /categories/<int:category_id>

- Fetches the details of a category with a specific ID
- Request arguments: None
- Returns: An object with two keys, success, and category.
- Example request:
    `curl localhost:3000/categories/1`
- Example response:
    ```
    {
        "success": True,
        "category": {
            "id" : "1",
            "type" : "Science"
        }
    }
    ```

GET /categories/<int:category_id>/questions>

- Fetches questions within a provided category ID, the total number of questions within that category, the available categories and the current category. Paginated in groups of 10, you can include a request argument ?page to choose a page.
- Request arguments: None
- Returns: An object with five keys, success, questions, total_questions, categories and current_category.
- Example request:
    `curl localhost:3000/categories/1/questions`
- Example response:
    ```
    {
        "success": True,
        "questions": [
            {
                "answer": "The Liver",
                "category": 1,
                "difficulty": 4,
                "id": 20,
                "question": "What is the heaviest organ in the human body?"
            },
            {
                "answer": "Blood",
                "category": 1,
                "difficulty": 4,
                "id": 22,
                "question": "Hematology is a branch of medicine involving the study of what?"
            },
        ],

        "total_questions": 2
        "categories": {
            "1" : "Science",
            "2" : "Art",
            "3" : "Geography",
            "4" : "History",
            "5" : "Entertainment",
            "6" : "Sports"
        },
        "current_category": {
            "id" : "1",
            "type" : "Science"
        }
    }
    ```

GET /questions

- Fetches all questions, the total number of questions, the available categories and the current category, None in this case. Paginated in groups of 10, you can include a request argument ?page to choose a page.
- Request arguments: None
- Returns: An object with five keys, success, questions, total_questions, categories and current_category.
- Example request:
    `curl localhost:3000/questions`
- Example response:
    ```
    {
        "success": True,
        "questions": [
            {
                "answer": "Edward Scissorhands",
                "category": 5,
                "difficulty": 3,
                "id": 6,
                "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
            },
            {
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1,
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?"
            },
            {
                "answer": "Brazil",
                "category": 6,
                "difficulty": 3,
                "id": 10,
                "question": "Which is the only team to play in every soccer World Cup tournament?"
            },
            {
                "answer": "Uruguay",
                "category": 6,
                "difficulty": 4,
                "id": 11,
                "question": "Which country won the first ever soccer World Cup in 1930?"
            },
            {
                "answer": "George Washington Carver",
                "category": 4,
                "difficulty": 2,
                "id": 12,
                "question": "Who invented Peanut Butter?"
            },
            {
                "answer": "Lake Victoria",
                "category": 3,
                "difficulty": 2,
                "id": 13,
                "question": "What is the largest lake in Africa?"
            },
            {
                "answer": "The Palace of Versailles",
                "category": 3,
                "difficulty": 3,
                "id": 14,
                "question": "In which royal palace would you find the Hall of Mirrors?"
            },
            {
                "answer": "Agra",
                "category": 3,
                "difficulty": 2,
                "id": 15,
                "question": "The Taj Mahal is located in which Indian city?"
            },
            {
                "answer": "Escher",
                "category": 2,
                "difficulty": 1,
                "id": 16,
                "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
            },
            {
                "answer": "Mona Lisa",
                "category": 2,
                "difficulty": 3,
                "id": 17,
                "question": "La Giaconda is better known as what?"
            }
        ],
        "total_questions": 16
        "categories": {
            "1" : "Science",
            "2" : "Art",
            "3" : "Geography",
            "4" : "History",
            "5" : "Entertainment",
            "6" : "Sports"
        },
        "current_category": null
    }
    ```

POST /questions

- Adds a new question to the database
- Request arguments:
    ```
    {
        "question": question_string,
        "answer": answer_string,
        "category": category_int,
        "difficulty": difficulty_int,
    }
    ```
- Returns: An object with a single key, success.
- Example request:
    `curl -X POST -H "Content-Type: application/json" --data '{"question": "Why is a mouse when it spins?", "answer": "Because the higher the fewer", "category": 1, "difficulty": 1}' localhost:3000/questions/`
- Example response:
    `{"success": True}`

DELETE /questions/<int:question_id>

- Deletes a question with a specific ID from the database
- Request arguments: None
- Returns: An object with a single key, success.
- Example request:
    `curl -X DELETE localhost:3000/questions/1`
- Example response:
    `{"success": True}`

POST /questions/search>

- Fetches questions that contain a provided sub string, case insensitive. Paginated in groups of 10, you can include a request argument ?page to choose a page.
- Request arguments:
    `{"searchTerm": search_string}`
- Returns: An object with five keys, success, questions, total_questions, categories and current_category, which will always be null on this request.
- Example request:
    `curl -X POST - H "Content-Type: application/json" --data '{"searchTerm": "Who"}' localhost:3000/questions/search`
- Example response:
    ```
    {
        "success": True,
        "questions": [
            {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
            },
        ],
        "total_questions": 1
        "categories": {
            "1" : "Science",
            "2" : "Art",
            "3" : "Geography",
            "4" : "History",
            "5" : "Entertainment",
            "6" : "Sports"
        },
        "current_category": null
    }
    ```

POST /quizzes>

- Fetches a random question that has not yet been played in the current game that is within a certain category, if one is selected.
- Request arguments:
    ```
    {
        "quiz_category": category_id
        "previous_questions": list(question_ids)
    }
    ```
- Returns: An object with two keys, success, and a question if there are any valid questions remaining or None if not.
- Example request:
    `curl -X POST -H "Content-Type: application/json" --data '{"quiz_category": 1, "previous_questions": [1, 4]}' localhost:3000/quizzes`
- Example response:
    ```
    {
        "success": True,
        "question": {
            "id" : "1",
            "type" : "Science"
        }
    }
    ```


## Testing

To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```