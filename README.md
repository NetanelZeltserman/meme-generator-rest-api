# Meme Generator API

## Project Overview

A RESTful API for a Meme Generator built using Django and PostgreSQL. It allows users to perform CRUD operations on memes. Docker is used for easy deployment and testing.

## Highlights
Design Patterns: Factory, Service, Repository
- Exceptions Factory, for consistent errors handling – handles view exceptions
- Image generation service with inheritence from a base service, using Pillow for image processing
- Meme repository for database operations

CI pipeline (bonus)
- PostgreSQL db instance as service
- Run migrations & tests on every push

Image generation (bonus)
- Service for generating images that inherits from a base service
- Pillow for image processing

Seed data (bonus)
- Meme templates
- Funny phrases for the surprise me feature

Swagger & ReDoc support (bonus)
- Add Swagger & ReDoc UI for interactive API exploration
- Include raw JSON schema file download endpoint for API specification

Auto. Camel case transformer (bonus)
- for API serialization in API responses

Serializers
- Input validation
- Model creation & update
- Output representation

Testing
- Integration – calls URL, checks response
- Unit – tests induvidual code components


## How to Run the Project

To run the project, Docker and Docker Compose are required.
Run the following command in the root directory of the project:
```
docker compose up --build
```

This command will:
- Build the Docker image for the Django application
- Start the PostgreSQL database
- Make & apply migrations
- Seed the database with test data for convenience
- Create a superuser (username: admin, password: admin)
- Start the Django development server

The API will be available at `http://localhost:8000`.

## API Documentation

Here's a list of available endpoints and their functions:

- `GET /api/schema/` - OpenAPI JSON schema
- `GET /api/schema/redoc/` - Redoc for API documentation
- `GET /api/schema/swagger-ui/` - Swagger UI for API documentation

- `POST /api/login/` - Get user's access and refresh tokens by username & password
- `POST /api/token/refresh/` - Refresh user's access token by refresh token

- `GET /api/templates/` - List all meme templates

- `GET /api/memes/` - List all memes (with pagination)
- `POST /api/memes/` - Create a new meme
- `GET /api/memes/<id>/` - Retrieve a specific meme
- `POST /api/memes/<id>/rate/` - Rate a meme
- `GET /api/memes/random/` - Get a random meme
- `GET /api/memes/top/` - Get top 10 rated memes
- `GET /api/memes/surprise-me/` - Get a meme with random text from a list of funny phrases (includes image URL)
- `GET /api/memes/surprise-me/<template_id>/` - Get a meme with random text from a list of funny phrases, related to a specific template (includes image URL)

## Additional Notes

1. Authentication:
   - The API uses JWT tokens for authentication.
   - To obtain a token, use the `/api/login/` endpoint.
   - Include the token as a `Bearer` token in the Authorization header for ALL requests (excluding `/api/login/` and `/api/token/refresh/`).

2. Meme Creation:
   - When creating a meme, if top_text or bottom_text is not provided, the template's default text will be used.

3. Meme Rating:
   - Users can rate memes from 1 to 5.
   - A user can only rate a meme once, but they can update their rating (using the same endpoint and method).

4. Random Meme:
   - The `/api/memes/random/` endpoint efficiently fetches a random meme from the database.

5. Top Memes:
   - The `/api/memes/top/` endpoint calculates the average rating for memes and returns the top 10.

6. Surprise Me Feature:
   - Includes image generation in two endpoints:
    - The `/api/memes/surprise-me/` endpoint generates a meme with random text from a predefined list of funny phrases.
    - The `/api/memes/surprise-me/<template_id>/` endpoint generates a meme with random text from a predefined list of funny phrases, related to a specific template.

7. Image Generation:
   - The application uses Pillow to add text to template images when generating memes.

8. Swagger & Redoc Documentation:
   - API documentation is available through Swagger UI at `/api/schema/swagger-ui/`.
   - API documentation is also available through Redoc at `/api/schema/redoc/`.

9. Testing:
   - Includes both unit & integration tests

10. Error Handling:
    - Uses exceptions factory for consistent error responses across the API
