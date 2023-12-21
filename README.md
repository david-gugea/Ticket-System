# Ticket-System

## User types

* Customer: create, read, update and delete his own Ticket
* Developer: create, read, update and delete all tickets
* Admin : create, read, update and delete all tickets + can update User roles

## Tech Stack

* UI/UX Design: Figma
* Frontend: Vue3 and js
* Backend: Python (fast-api)
* DB: postgresql (containerized)
* HTML/CSS: UI Library (~)

## Structure

* Log in/Register (+session management)
* Ticket System

## Attributes for the create/edit Page

* TICKET CREATION title, description, department, telefon
* TICKET CREATION for DB: id, date, owner (evtl. lastUpdate)

## App Database

### Table: Users

* Username - **Primary Key**
* Password 
* Type (customer, developer, admin)

## Docker

### Create network

Create a user-defined bridge network using for the ticket system using:

```bash
docker network create ticket_system_network
```

### Start docker compose

Start the container defined in docker compose using

```bash
docker-compose up -d
```

# Steps to run

## Build venv and install necessary libraries/frameworks

Build the virtual environment:

```bash
cd src/server
python -m venv .venv
.\.venv\Scripts\activate
```

Install necessary libraries and frameworks

```bash
pip install -r requirements.txt
```

## Start Server

```bash
uvicorn main:app --host 0.0.0.0 --port 8003
```

## Start containers

```docker-compose up -d```

# Database Structure

## Table User

* ID: Auto-Increment Integer PK
* Username: str
* Password: str

## Table Ticket

* ID: Auto-Increment Integer PK
* Description: str
* Date-Created: Date
* User Id: Integer

There's a 1-n Relationship between user and ticket tables.

## Credentials

### pgadmin

* email: admin@admin.com
* password: root

### pgcontainer

* username: root
* password: root