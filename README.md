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

## Environment Variables

Before running the project, copy `.env.example` to `.env` and fill in your own API keys:
```bash
cp .env.example .env
# Edit .env and add your real keys
```

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

## Running Tests

To run the test suite, use the following command from the project root:

```bash
PYTHONPATH=. pytest tests/
```

This ensures that the tests are executed with the correct module resolution.

## User Stories
The main user stories covered by the API include:
- Querying tours and courses.
- User registration and authentication.
- Information about included services.
- Booking status verification.

For more details, see the `user-stories.md` file.

## Observability

### Health Check

- **Endpoint:** `GET /health`
- **Description:** Returns `{"status": "ok"}` if the service is up and running. Useful for monitoring and orchestration systems (Kubernetes, Docker, etc).

### Metrics

- **Endpoint:** `GET /metrics`
- **Description:** Exposes Prometheus-compatible metrics using `prometheus_flask_exporter`. These metrics can be scraped by Prometheus and visualized in Grafana or similar tools.
- **Tracked Metrics:**
  - **Chat Endpoints:**
    - `chat_requests_total`: Total number of chat requests received.
    - `chat_failed_requests_total`: Total number of failed chat requests.
    - `chat_response_latency_seconds`: Histogram of chat response latency (in seconds).
  - **Authentication & Registration:**
    - `login_attempts_total`: Total number of login attempts.
    - `login_failed_total`: Total number of failed login attempts.
    - `login_success_total`: Total number of successful logins.
    - `registration_attempts_total`: Total number of registration attempts.
    - `registration_failed_total`: Total number of failed registration attempts.
    - `registration_success_total`: Total number of successful registrations.

### Logging

- **Library:** Uses Python's built-in `logging` module.
- **Log Events:**
  - **Chat Service:**
    - Initialization steps and errors for the chat service and RAG components.
    - User queries received and responses sent.
    - Errors during chat processing.
  - **Authentication & Registration:**
    - Registration and login attempts (including username).
    - Success and failure events for registration and login.
    - Warnings for missing/invalid credentials, duplicate users, and token issues.
  - **General:**
    - All logs include timestamps, log level, and module name for traceability.
- **Log Format Example:**
  ```
  2025-07-08 18:00:00,000 INFO app.services.chat: Initializing chat model...
  2025-07-08 18:00:01,000 INFO app.routes.chat: Received chat request from user 'alice': What tours are available?
  2025-07-08 18:00:01,500 ERROR app.services.chat: Failed to initialize chat service: <error details>
  ```