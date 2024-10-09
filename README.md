# Junior Python Backend Developer Assignment - Meme Generator API

## Introduction

Welcome to the Meme Generator API assignment! This project will test your skills in building a RESTful API using Django and PostgreSQL, as well as your ability to containerize the application using Docker.

## Task Overview

Create a RESTful API for a Meme Generator service using Django and PostgreSQL. This service will allow users to create, retrieve, and rate memes. The entire application should be containerized using Docker for easy deployment and testing. No need to deploy - only local development.


## Requirements

1. Backend:

   - Use Django and Django Rest Framework to create the backend.
   - Implement a PostgreSQL database to store data.

2. Models:

   - User: Use Django's built-in User model.
   - MemeTemplate: id, name, image_url, default_top_text, default_bottom_text
   - Meme: id, template (ForeignKey to MemeTemplate), top_text, bottom_text, created_by (ForeignKey to User), created_at
   - Rating: id, meme (ForeignKey to Meme), user (ForeignKey to User), score (1-5), created_at

3. API Endpoints:

   *** Use mixins for theses endpoints ***
   - GET /api/templates/ - List all meme templates
   - GET /api/memes/ - List all memes (with pagination)
   - POST /api/memes/ - Create a new meme
   - GET /api/memes/<id>/ - Retrieve a specific meme

   - POST /api/memes/<id>/rate/ - Rate a meme
   - GET /api/memes/random/ - Get a random meme
   - GET /api/memes/top/ - Get top 10 rated memes


4. Business Logic:
   - Meme creation:
     - Users can create memes using existing templates.
     - If top_text or bottom_text is not provided, use the template's default text.
   - Meme rating:
     - Users can rate memes from 1 to 5.
     - A user can only rate a meme once, but they can update their rating.
   - Random meme:
     - Implement an efficient method to fetch a random meme.
   - Top memes:
     - Calculate the average rating for memes and return the top 10.

5. Authentication:
   - Implement token authentication for the API.

6. Testing:
   - Write unit tests for API views using built-in Django test system.
   - Aim for maximum test coverage.

7. Version Control:
   - Use Git for version control.
   - Create a GitHub repository for the project.
   - Make meaningful commits with clear commit messages.

8. Docker:
   - Containerize the entire application (Django app and PostgreSQL database) using Docker-Compose.
   - Create a docker-compose.yml file to orchestrate the services.
   - Ensure the application can be started with a single command.

9. Bonus (Optional):
   - Implement a simple meme generation feature:
     - Use Pillow (Python Imaging Library) to add text to the template image.
     - Return the URL of the generated meme image.
   - Create a '/api/memes/surprise-me/' endpoint that returns a meme with random text from a list of funny phrases.
   - Usage of Swagger


## Code Structure

Here's a basic structure to help you get started:

### 1. Models

```python
from django.db import models
from django.contrib.auth.models import User

class MemeTemplate(models.Model):
    name = models.CharField(max_length=100)
    image_url = models.URLField()
    default_top_text = models.CharField(max_length=100, blank=True)
    default_bottom_text = models.CharField(max_length=100, blank=True)

class Meme(models.Model):
    template = models.ForeignKey(MemeTemplate, on_delete=models.CASCADE)
    top_text = models.CharField(max_length=100)
    bottom_text = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Rating(models.Model):
    meme = models.ForeignKey(Meme, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('meme', 'user')
```


## Submission Instructions

1. Create a new GitHub repository for your project.
2. Implement the Meme Generator API according to the requirements.
3. Create a Dockerfile for your Django application.
4. Create a docker-compose.yml file that includes both your Django application and a PostgreSQL database.
5. Include a README.md file in your repository with:
   - Project overview
   - How to run the project using Docker (it should be a single command)
   - API documentation (a simple list of endpoints with their functions is sufficient)
   - Any additional notes or explanations about your implementation
6. Make sure your code is well-commented and follows Python and Django best practices.
7. Commit your changes regularly with clear and concise commit messages.
8. Once you're finished, send us the link to your GitHub repository.

## Running the Project

Your project should be able to run with a single command, such as:

```
docker-compose up
```

This command should:

- Build the Docker image for your Django application
- Start the PostgreSQL database
- Apply migrations
- Create Super User
- Start the Django development server

Make sure to test this thoroughly before submission.

## Evaluation Criteria

Your submission will be evaluated based on:

- Correct implementation of Django models and REST API
- Quality of business logic implementation
- Proper use of PostgreSQL database
- Code quality, organization, and adherence to Python/Django best practices
- Completeness and correctness of unit tests and built in django tests
- Proper use of Git (commit history, meaningful commits)
- Error handling and edge case management
- Correct Docker setup and ease of running the project
- Creativity in implementing the bonus features (if attempted)

Good luck, and have fun building your Meme Generator API!
