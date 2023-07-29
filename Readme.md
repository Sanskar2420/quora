# Quora Project

## Overview
Quora is a social media platform that allows users to ask questions, answer questions, follow other users, and interact with the community through likes and comments. This project implements a simplified version of Quora with basic features like adding questions, answering questions, adding tags, liking/disliking questions and answers, commenting, and user authentication.

## Features
- **User registration and login:** Users can register and log in to the platform using their credentials.
- **Add a new question:** Authenticated users can add new questions to the platform with associated tags.
- **Answer questions:** Authenticated users can provide answers to questions.
- **Like/Dislike questions and answers:** Users can like or dislike questions and answers.
- **Comments:** Users can comment on questions and answers.
- **View all questions and answers:** All users can view all questions and answers on the platform.

## Project Setup
To set up the Quora project, follow the steps below:

- Clone the repository to your local machine using 
```
git clone <repository_url>
```

- Navigate to the project directory using 
```
cd <path of quora folder>
```
- Install Requirements
```
pip install -r requirements.txt
```

## Database & Migrations
The Quora project uses an SQLite database, which is included by default in Django.
- Applying Migrations
```
python manage.py makemigrations
python manage.py migrate
```

## Running the Project
To run the Quora project locally, execute the following command:
```
python manage.py runserver
```

## Packages Used
- **asgiref:** Django uses ASGI for running asynchronous views and handling WebSocket connections. The asgiref package is used by Django's channels library, which extends Django to support real-time features and WebSockets.

- **Django:** Django package is the core of web application. It provides the necessary structure, tools, and conventions to build the various functionalities and components of Quora-like platform.

- **python-dotenv:** It's used .env files to store sensitive or configuration-specific data (e.g. secret keys) separately from the code. This package allows to access these variables in Django settings and other parts of the project.

- **sqlparse:** sqlparse is used by Django's ORM to generate and format SQL queries for various database operations. It helps developers to inspect and debug SQL queries executed by Django.

## Layerwise Structure Explanation
The project is organized into three Django applications: quora, questions, and users.

- **quora:** The main application that contains project-level configurations.
- **questions:** This app handles functionalities related to questions, answers, tags, likes, and comments.
- **users:** This app manages user-related functionalities such as registration, login, profile, etc.