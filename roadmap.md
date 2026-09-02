# Ahmad × GPT — Backend Engineering Roadmap

## Purpose

This README is the persistent roadmap for my software-engineering learning journey with GPT.

The goal is not to memorize technologies or solve isolated problems.

The goal is to become capable of:

> **Understanding requirements → designing systems → implementing them → debugging them → testing them → deploying them.**

GPT should teach me through practical reasoning, implementation, debugging, and progressively harder real-world problems.

---

# Current Level

I am a CSE engineering student with experience in:

* Python
* Data Structures & Algorithms
* SQL
* LeetCode SQL
* Git/GitHub
* Basic backend/project development
* Open-source contribution attempts
* Existing personal projects

I have recently completed a focused phase on **relational database/schema design**.

---

# Completed: Schema Design

I have practiced schema design through multiple realistic systems:

1. University Course Registration
2. E-commerce
3. Food Delivery
4. Hotel Booking
5. Ride Sharing
6. Banking
7. Hospital Management
8. Social Media Platform

The purpose was not simply normalization.

I learned to reason from requirements.

## Concepts Covered

### Entity identification

Ask:

> Does this thing exist independently?

### Row meaning

Always ask:

> **What does one row represent?**

### Relationships

* 1:1
* 1:N
* M:N
* Self-referencing

### Associative entities

Used when:

* an M:N relationship exists
* a relationship has attributes
* an event/association must be stored

Examples:

```text
Enrollment
OrderItem
PrescriptionItem
Follow
PostLike
PostShare
```

### Recursive relationships

Example:

```text
Comment
  ↓
parent_comment_id
  ↓
Comment
```

Used for unlimited-depth structures.

### Historical data

Understand the difference between:

```text
Current state
```

and:

```text
Historical fact
```

Example:

```text
OrderItem.unit_price
```

must preserve the price actually paid even if the product's current price changes.

### Events

Understand when an event itself needs to become a table.

Examples:

```text
Payment
Transaction
Assignment
Booking
Enrollment
PostShare
```

### Constraints

Covered:

* PRIMARY KEY
* FOREIGN KEY
* UNIQUE
* NOT NULL
* CHECK
* composite keys
* business constraints
* deletion behavior

### Temporal constraints

Example:

Hotel rooms cannot have overlapping bookings.

### Redundancy

Learned to avoid storing information that can already be derived through relationships.

Example:

If:

```text
Doctor → Department
```

then an Appointment generally doesn't also need:

```text
Appointment → Department
```

unless there is a specific historical/business reason.

---

# Important Schema Principle

The main mental model I should continue using:

> **Requirements first → entities → relationships → cardinality → attributes → constraints → historical requirements → implementation.**

Normalization is a validation tool, not the starting point.

---

# Current Decision

## STOP doing endless schema challenges.

The important schema-design patterns have been covered sufficiently.

Future projects may still require schema design, but schema design should now be **part of building applications**, rather than the entire learning exercise.

---

# NEXT PHASE

# Phase 1 — Real PostgreSQL

Goal:

Move from:

> "I can write SQL."

to:

> "I understand how a real relational database behaves."

Topics:

* PostgreSQL setup
* CREATE TABLE
* INSERT / UPDATE / DELETE
* PK / FK
* UNIQUE
* CHECK
* NOT NULL
* DEFAULT
* ON DELETE
* indexes
* composite indexes
* transactions
* ACID
* isolation basics
* `EXPLAIN`
* `EXPLAIN ANALYZE`

Learning style:

Do not dump theory on me.

Prefer:

```text
Concept
↓
Small example
↓
I attempt it
↓
You review/debug it
↓
Real-world application
```

---

# Phase 2 — Real SQL

I already practice SQL through LeetCode.

Now expand into practical database querying.

Topics:

* JOINs
* GROUP BY
* HAVING
* subqueries
* CTEs
* CASE
* EXISTS
* UNION
* window functions
* aggregation
* pagination
* filtering/sorting
* query optimization

Focus on:

> **Why would I use this here?**

rather than memorizing syntax.

---

# Phase 3 — FastAPI

Use Python + FastAPI to build actual backend services.

Learn:

* HTTP
* REST
* endpoints
* request/response
* JSON
* status codes
* path parameters
* query parameters
* request bodies
* Pydantic
* validation
* dependency injection
* error handling
* middleware

Architecture:

```text
Client
  ↓
API Router
  ↓
Service / Business Logic
  ↓
Database Layer
  ↓
PostgreSQL
```

Understand why each layer exists.

---

# Phase 4 — Database + Backend

Connect FastAPI to PostgreSQL.

Build real functionality:

```text
POST /users
GET /users
GET /users/{id}
POST /orders
GET /orders/{id}
PATCH /orders/{id}
```

Learn:

* CRUD
* database transactions
* connection management
* ORM
* raw SQL
* migrations
* validation
* business logic

Important:

Do not just teach me how to make endpoints.

Teach me what happens from:

```text
HTTP request
↓
Python code
↓
SQL
↓
PostgreSQL
↓
response
```

---

# Phase 5 — Authentication & Authorization

Learn:

### Authentication

> Who are you?

Topics:

* password hashing
* login
* access tokens
* JWT
* refresh tokens
* sessions

### Authorization

> What are you allowed to do?

Topics:

* roles
* permissions
* protected endpoints
* resource ownership

Example:

```text
Customer → own orders
Admin → all orders
```

---

# Phase 6 — Backend Engineering

Learn how real applications are structured.

Topics:

* validation
* error handling
* logging
* configuration
* environment variables
* `.env`
* service layer
* repository/data-access layer
* clean project structure
* dependency management

Goal:

Understand why production code isn't just one giant Python file.

---

# Phase 7 — Testing

Learn:

### Unit testing

Test individual pieces.

### Integration testing

Test:

```text
Backend → Database
```

### API testing

Test complete endpoints.

Learn to think:

> "What can break?"

rather than only:

> "Does the happy path work?"

---

# Phase 8 — Git & Open Source

Continue improving Git skills.

Important commands:

```text
clone
add
commit
push
pull
fetch
branch
switch
merge
rebase
remote
```

Understand:

```text
Fork
↓
Clone
↓
Branch
↓
Modify
↓
Test
↓
Commit
↓
Push
↓
Pull Request
↓
Review
↓
Merge
```

I have already started exploring open-source contribution, including working with repositories such as `supabase/supabase-py`.

Goal:

Become comfortable working inside someone else's codebase.

---

# Phase 9 — Docker

Learn:

* images
* containers
* Dockerfile
* volumes
* networks
* Docker Compose

Eventually run:

```text
FastAPI container
       +
PostgreSQL container
```

with Docker Compose.

---

# Phase 10 — Deployment

Learn the basics of taking an application from:

```text
localhost
```

to:

```text
Internet
```

Topics:

* Linux basics
* processes
* ports
* environment variables
* server deployment
* reverse proxy
* HTTPS
* CI/CD
* cloud basics

The goal is understanding, not becoming a DevOps specialist.

---

# Phase 11 — System Design

Only after gaining practical backend experience.

Learn:

* load balancing
* caching
* Redis
* queues
* background jobs
* rate limiting
* pagination
* database replication
* scaling
* consistency
* horizontal scaling
* distributed systems basics

Approach:

Do not memorize architecture diagrams.

Instead ask:

> **What breaks when this application grows?**

---

# Phase 12 — Serious Projects

Build fewer projects, but make them substantially better.

## Project 1

Production-style backend:

```text
Python
FastAPI
PostgreSQL
Authentication
Testing
Docker
```

## Project 2

Improve my existing **NeedNow** project.

Use the complete engineering workflow:

```text
Requirements
↓
Architecture
↓
Schema
↓
API
↓
Business logic
↓
Authentication
↓
Testing
↓
Docker
↓
Deployment
```

## Project 3

Continue contributing to open source.

---

# Parallel Track — DSA

DSA continues alongside backend development.

Do not stop DSA.

But don't let DSA consume the entire engineering journey.

Current approach:

```text
DSA
+
SQL
+
Backend
+
Projects
+
Open Source
```

---

# GPT's Teaching Rules

GPT should follow these principles when teaching me.

## 1. Don't overwhelm me

Introduce concepts progressively.

If something is advanced, explain the prerequisite first.

---

## 2. Prefer reasoning over memorization

Don't just tell me:

> "Use a transaction."

Explain:

> **What problem does the transaction solve?**

---

## 3. Let me attempt things

For practical problems:

```text
Give requirements
↓
Let me design/implement
↓
Review my attempt
↓
Attack edge cases
↓
Improve it
```

Don't immediately give the perfect solution unless I ask for it.

---

## 4. Explain the "why"

For every important technology or pattern, answer:

```text
What is it?
Why does it exist?
What problem does it solve?
When should I use it?
When shouldn't I use it?
```

---

## 5. Connect everything

Don't teach technologies as isolated topics.

Show:

```text
Database
   ↓
SQL
   ↓
Backend
   ↓
API
   ↓
Authentication
   ↓
Testing
   ↓
Docker
   ↓
Deployment
   ↓
System Design
```

---

## 6. Use realistic scenarios

Prefer problems like:

> "Build the backend for a food delivery service."

over:

> "Create a CRUD API for books."

unless the simple example is specifically useful for learning a concept.

---

## 7. Challenge my assumptions

If I propose something questionable, don't just agree.

Tell me:

> "This works, but here's what breaks."

Then demonstrate the edge case.

---

## 8. Don't hide complexity

If something is genuinely complicated, say so.

Break it down instead of pretending it's simple.

---

# Current Position

```text
DSA                         ████████░░
SQL                         ████████░░
Schema Design               █████████░
PostgreSQL                  ██░░░░░░░░
Backend                     ███░░░░░░░
Authentication              █░░░░░░░░░
Testing                     █░░░░░░░░░
Docker                      █░░░░░░░░░
Deployment                  █░░░░░░░░░
System Design               █░░░░░░░░░
Open Source                 ██░░░░░░░░
```

These are rough learning-stage indicators, not formal assessments.

---

# Immediate Next Step

When starting the next session, **do not give me another schema challenge.**

Start with:

# PostgreSQL — From SQL Knowledge to Real Database Engineering

Begin practically.

First establish what I already know, then teach the missing PostgreSQL concepts without repeating basic SQL unnecessarily.

The first progression should be approximately:

```text
PostgreSQL
↓
Create a real database
↓
Implement a schema
↓
Constraints
↓
Queries
↓
Transactions
↓
Indexes
↓
EXPLAIN
```

Then transition naturally into:

```text
FastAPI
↓
PostgreSQL integration
↓
Real backend
```

---

# Final Goal

The end goal is not:

> "I know Python, SQL, FastAPI, Docker, and system design."

The end goal is:

> **Give me a real software requirement and I can reason about it, design it, implement it, debug it, test it, and explain my technical decisions.**

That is the skill we are building.
