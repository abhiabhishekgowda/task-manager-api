# Task Manager API

A backend project built with FastAPI to learn API development, CRUD operations, and database integration.

## Project Goal

Build a complete Task Manager API that allows users to:

* Create Tasks
* View Tasks
* Update Tasks
* Delete Tasks
* Store Data Permanently
* Work with a Database

## Features Completed

### Week 1

* FastAPI Setup
* Uvicorn Server Setup
* GET Endpoints
* POST Endpoints
* PUT Endpoints
* DELETE Endpoints
* Path Parameters
* JSON Responses
* In-Memory Task Storage Using Python Lists

## Example Task Structure

```json
{
    "id": 1,
    "title": "Study FastAPI",
    "completed": false
}
```

## Current Tech Stack

* Python
* FastAPI
* Uvicorn

## Current API Endpoints

| Method | Endpoint    | Description      |
| ------ | ----------- | ---------------- |
| GET    | /           | Home Route       |
| GET    | /tasks      | View All Tasks   |
| GET    | /tasks/{id} | View Single Task |
| POST   | /tasks      | Create Task      |
| PUT    | /tasks/{id} | Update Task      |
| DELETE | /tasks/{id} | Delete Task      |

## Upcoming Features (Week 2)

* SQLite Database
* Database CRUD Operations
* Persistent Data Storage
* SQL Basics
* Python OOP Basics

## Learning Journey

This project is part of my backend engineering learning roadmap. The goal is to build strong backend fundamentals before moving into advanced software engineering and AI systems.

## Author

Abhishek
