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