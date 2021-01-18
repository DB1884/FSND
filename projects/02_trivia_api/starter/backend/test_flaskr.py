import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:postgres@{}/{}".format(
            "localhost:5432", self.database_name
        )
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_successful_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["categories"]))

    def test_method_not_allowed_categories(self):
        res = self.client().post("/categories")
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 405)

    def test_get_category(self):
        res = self.client().get("/categories/3")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["category"]["id"], 3)

    def test_category_does_not_exist(self):
        res = self.client().get("/categories/50")
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)

    def test_get_paginated_questions_all(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_category"], None)

    def test_get_paginated_questions_all_invalid_page(self):
        res = self.client().get("/questions?page=5")
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)

    def test_get_paginated_questions_category(self):
        res = self.client().get("/categories/1/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_category"]["type"], "Science")
        self.assertEqual(data["total_questions"], 3)

    def test_get_paginated_questions_category_invalid_page(self):
        res = self.client().get("/categories/1/questions?page=2")
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)

    def test_delete_question(self):
        res = self.client().delete("/questions/16")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_question_does_not_exist(self):
        res = self.client().delete("/question/50")
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 404)

    def test_add_question(self):
        res = self.client().post(
            "/questions",
            json={
                "question": "Does this work?",
                "answer": "Yes",
                "difficulty": "1",
                "category": "4"
            }
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_add_question_missing_data(self):
        res = self.client().post(
            "/questions",
            json={
                "question": "Does this work?",
                "answer": "",
                "difficulty": "1",
                "category": "1"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 400)

    def test_add_question_invalid_data(self):
        res = self.client().post(
            "/questions",
            json={
                "question": "Does this work?",
                "answer": "No",
                "difficulty": "1",
                "category": "12"
            }
        )
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 422)

    def test_search_questions(self):
        res = self.client().post(
            "/questions/search",
            json={"searchTerm": "What"}
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["total_questions"], 8)
        self.assertEqual(data["current_category"], None)

    def test_search_questions_empty_search(self):
        res = self.client().post("/questions/search", json={"searchTerm": ""})
        data = json.loads(res.data)
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 422)

    def test_play_quiz_all(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [],
            "quiz_category": {"type": "click", "id": 0}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_play_quiz_category_and_previous_questions(self):
        res = self.client().post("/quizzes", json={
            "previous_questions": [20, 21],
            "quiz_category": {"type": "Science", "id": 1}
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertNotIn(data["question"]["id"], [20, 21])
        self.assertEqual(data["question"]["category"], 1)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
