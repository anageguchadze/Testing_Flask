# Testing_Flask

A simple Flask-based REST API for managing authors and books, including authentication and pagination. This project includes automated tests using pytest.

🚀 Features
Manage Authors & Books: Create, retrieve, and delete authors and their books.
Authentication: Secure book creation with a token-based authentication mechanism.
Pagination: List authors with pagination support.
Testing: Includes unit tests for API endpoints and database relationships.

🛠️ Installation & Setup
1️⃣ Clone the repository
git clone https://github.com/anageguchadze/Testing_Flask.git
cd Testing_Flask

2️⃣ Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Run the Flask application
python app.py
By default, the API will be available at http://127.0.0.1:5000/.

📌 API Endpoints
✅ List Authors
GET /api/authors

Query Parameters:
nationality (optional) – Filter authors by nationality.
page (optional) – Pagination page number.
per_page (optional) – Number of authors per page.

Response Example:
{
  "results": [
    {"id": 1, "name": "J.K. Rowling", "nationality": "British"}
  ],
  "next": "/api/authors/?page=2&per_page=10"
}

✅ Create a Book (Requires Authentication)
POST /api/books

Headers:
{
  "Authorization": "Token secret"
}

Request Body:
{
  "title": "Harry Potter and the Prisoner of Azkaban",
  "publication_date": "1999-07-08"
}

Response Example:
{
  "id": 1,
  "title": "Harry Potter and the Prisoner of Azkaban",
  "publication_date": "1999-07-08"
}

🧪 Running Tests
Run the test suite using pytest:
pytest

📜 License
This project is licensed under the MIT License.