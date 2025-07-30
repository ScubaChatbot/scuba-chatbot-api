
# ScubaTours Chatbot API

This project is a Retrieval-Augmented Generation (RAG) API built with Python (Flask) to assist ScubaTours customers in planning diving experiences, courses, and managing bookings in Colombia. The chatbot leverages OpenAI for natural language understanding and is provided with a specialized knowledge base about diving tours, courses, and services in Colombia (Providencia, San Andrés, etc).

## Main Features
- Query availability and details of diving tours in Providencia, San Andrés and Gorgona.
- Get information about Free Diving courses and requirements.
- User registration and authentication for personalized interaction.
- Ask about services included in tour packages.
- Check the status of existing bookings.
- RAG architecture: combines OpenAI LLM with a curated knowledge base on Colombian diving.

## Key Endpoints
- `POST /chat`: Main interaction with the chatbot for queries about tours, courses, and bookings.
- `POST /users/register`: Register new users.
- `POST /users/login`: User authentication.


## Database

This project uses SQLite as the database engine for user registration and authentication. The database file (`scuba_chatbot.db`) is automatically created in the project root when the API is first run. SQLite is lightweight and ideal for development and prototyping. You can easily migrate to a more robust database (e.g., PostgreSQL, MySQL) for production if needed.

User data (username and hashed password) is stored in the database and used for authentication and JWT token generation. No tokens are stored; JWTs are stateless and validated on each request.

## Local Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone <REPO_URL>
   cd scuba-chatbot-api
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the API:**
   ```bash
   python run.py
   ```

5. **Access the API:**
   - By default, it will be available at `http://localhost:5000`
   - You can test the `/chat` endpoint using Postman or cURL:
     ```bash
     curl -X POST http://localhost:5000/chat -H "Content-Type: application/json" -d '{"message": "What diving tours are available in Providencia?"}'
     ```

## User Stories
The main user stories covered by the API include:
- Querying tours and courses.
- User registration and authentication.
- Information about included services.
- Booking status verification.

For more details, see the `user-stories.md` file.
