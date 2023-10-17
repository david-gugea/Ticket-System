# Ticket-System

## User types

* Customer: read only
* Developer: create read update
* Admin : create read update delete

## Tech Stack

* UI/UX Design: Figma
* Frontend: Vue
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
python -m venv .venv
.\.venv\Scripts\activate
```

Install necessary libraries and frameworks

```bash
pip install "fastapi[all]" sqlalchemy
```