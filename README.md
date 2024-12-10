# Document Service

The **Document Service** is a backend service responsible for managing documents in the real-time collaborative document editor. It supports document CRUD operations, version history, and integration with other services in a microservices architecture.

## Features

- **CRUD Operations**: Create, Read, Update, Delete documents.
- **Version History**: Track changes to documents over time and provide rollback functionality.
- **Real-time Collaboration**: Integration with WebSocket service to allow real-time collaboration on documents (handled by the WebSocket service).
- **Integration with Auth Service**: Ensures that document operations are secure, with user authentication and authorization handled by the Auth service.

## Technologies

- **FastAPI**: The web framework used for building the REST API.
- **MongoDB**: Document-based NoSQL database for storing document data.
- **Poetry**: Dependency management tool for Python, used to handle project dependencies.
- **Docker**: Containerization of the application to ensure it runs consistently across environments.

## Requirements

- Python 3.8+
- MongoDB (for local development or use a remote MongoDB instance)
- Poetry (for managing Python dependencies)
- Docker (for containerization)

## Installation

### 1. Clone the repository

```bash
git clone git remote add origin https://github.com/Michael233ctrl/document_service.git
cd document_service
