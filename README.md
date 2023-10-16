# Ticket System API

**Ticket System API** provides functionality for managing tickets in a ticket system. Tickets are the primary elements in the system and can have comments associated with them.



## Getting Started

Ticket System API requires Python 3.11 or later

### 1. Install requirements

```zsh
pip install -r requirements.txt
```

### 2. ENV

Create and populate your .env according to the structure of the .env-example file.

### 3. Migrations

Initialize migrations on your database

```zsh
flask db upgrade
```

### 4. Run uWSGI

```zsh
uwsgi app.ini
```

---

## API Reference

To reduce time costs, it was decided to create a postman collection as an API reference  
[PostmanCollection](tickets_api.postman_collection.json)  
Specify the correct `serverurl` in the Postman Environment

## Available Ticket Statuses:
* open
* anwered
* waiting_answer
* closed

## About Redis

**Redis** is used for tickets with a `closed` status:
- Update *ticket status* to `closed`;
- Get `closed` ticket by ID.


## Testing

Before running tests, **make sure** that you have correctly specified the connection parameters to your test database in the `.env` file

To start testing, run the following command in the root directory of the project.

```
pytest
```
