# Ticket-System

## User types

* Customer: create, read, update and delete his own Ticket
* Developer: create, read, update and delete all tickets
* Admin : create, read, update and delete all tickets + can update User roles

## Tech Stack

* UI/UX Design: Figma
* Frontend: Vue.js + HTML/CSS
* Backend: Python (fast-api)
* DB: postgresql (containerized)


## Structure

* Login/ Register
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

-----------------------------------------------------------------------------------------------------------------------
***********************************************************************************************************************
-----------------------------------------------------------------------------------------------------------------------

# frontend

## Project setup
```
yarn install
```
### Install Vue CLI
```
yarn install -g @vue/cli@5.0.8   
```
### Lints and fixes files
```
yarn lint
```
### Install Axios
```
yarn add axios
```
### Compiles and minifies for production
```
yarn build
```
### Compiles and hot-reloads for development
```
yarn run serve
```
->  http://localhost:8080/

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

### Login & Register
When you register you will be assigned with the user type admin.
This is done automatically in the login() function so that you can fully test the web application with all rights.
Normally every newly registered user is created with the user_type customer.





