````markdown
# Backend Engineering + DBMS Roadmap

The goal is not to memorize frameworks or DBMS definitions.

The goal is to understand:

> **What is actually happening inside a production backend when a request arrives?**

I will study **Backend Engineering + DBMS in parallel**, connecting theory with real PostgreSQL/FastAPI behavior.

---

# 🧠 Overall Mental Model

```text
                    CLIENT
                      │
                      ▼
                  HTTP Request
                      │
                      ▼
                ASGI / Uvicorn
                      │
                      ▼
                   FastAPI
                      │
              ┌───────┴────────┐
              │                │
         Middleware         Routing
              │                │
              └───────┬────────┘
                      ▼
                 Validation
                      │
                      ▼
               Service Layer
                      │
                      ▼
              Database Layer
                      │
                      ▼
              Connection Pool
                      │
                      ▼
                PostgreSQL
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
      Planner       MVCC          WAL
        │             │             │
        ▼             ▼             ▼
     Index/Heap    Locks/Txns    Durability
        │
        ▼
     Buffers
````

DBMS theory runs alongside this entire stack.

---

# 📚 TRACK 1 — DBMS

## Phase 1 — Schedules & Serializability

### 1. Conflict Identification

Understand:

```text
Same data item?
        +
Different transactions?
        +
At least one WRITE?
        ↓
      CONFLICT
```

Rules:

```text
R-R → No conflict
R-W → Conflict
W-R → Conflict
W-W → Conflict
```

---

### 2. Conflict Serializability

Learn to:

* Identify conflicts
* Build precedence graphs
* Find edges between transactions
* Detect cycles
* Determine serializability
* Find equivalent serial order

Mental model:

```text
Operations
    ↓
Conflicts
    ↓
Precedence Graph
    ↓
Cycle?
 ┌──┴──┐
YES    NO
 ↓      ↓
Not     Conflict
CSR     Serializable
```

---

### 3. More Conflict Serializability Problems

Progress through:

* Simple schedules
* Multiple data items
* Multiple transactions
* Multiple edges
* Tricky interleavings

Do problems instead of memorizing rules.

---

### 4. View Serializability

Understand:

* Read-from relationships
* Initial reads
* Final writes
* View equivalence
* Difference between conflict and view serializability

---

# Phase 2 — Recoverability

## 5. Recoverable Schedules

Understand:

```text
T2 reads data written by T1
        ↓
T2 should not commit
before T1 commits
```

---

## 6. Cascading Rollback

Understand how:

```text
T1 writes
 ↓
T2 reads T1's uncommitted value
 ↓
T1 aborts
 ↓
T2 must rollback
```

---

## 7. Cascadeless Schedules

Understand how schedules avoid reading uncommitted data.

---

## 8. Strict Schedules

Understand how strictness prevents problematic reads/writes of data written by uncommitted transactions.

Mental progression:

```text
Serializability
      ↓
Can execution be considered safe?
      ↓
Recoverability
      ↓
Can we recover after failure?
      ↓
Cascadeless
      ↓
Can we avoid cascading rollback?
      ↓
Strict
      ↓
Can we make recovery even safer?
```

---

# Phase 3 — Concurrency Control

## 9. Locks

Understand:

* Why locks exist
* Shared locks
* Exclusive locks
* Lock compatibility
* What operations need which locks

---

## 10. Two-Phase Locking

Understand:

```text
Growing Phase
    ↓
Acquire locks
    ↓
Shrinking Phase
    ↓
Release locks
```

---

## 11. Strict 2PL

Understand why holding write locks until commit/abort helps with recovery and concurrency.

---

## 12. Deadlocks

Understand:

```text
T1 locks A
T2 locks B

T1 waits for B
T2 waits for A

        ↓

      DEADLOCK
```

Learn:

* Wait-for graph
* Cycle detection
* Deadlock prevention
* Deadlock avoidance
* Consistent lock ordering

---

# Phase 4 — Functional Dependencies & Normalization

## 13. Functional Dependencies

Learn:

```text
A → B
```

and understand what it actually means.

---

## 14. Attribute Closure

Practice:

```text
F+
```

and determine which attributes can be derived from a given set.

---

## 15. Candidate Keys

Practice finding:

* Superkeys
* Candidate keys
* Prime attributes

---

## 16. Minimal / Canonical Cover

Learn how to reduce a set of functional dependencies.

---

## 17. Normalization

Progress through:

```text
1NF
 ↓
2NF
 ↓
3NF
 ↓
BCNF
```

Focus on **why** each decomposition is necessary.

---

## 18. Decomposition

Practice:

* Lossless join
* Dependency preservation

---

# Phase 5 — Indexing & DB Internals

## 19. B/B+ Trees

Understand:

* Tree structure
* Search
* Insertion
* Deletion
* Splitting
* Why databases use B+ Trees

---

## 20. Index Searching

Connect theory to PostgreSQL:

```text
SQL Query
    ↓
Planner
    ↓
Index Scan?
Bitmap Scan?
Seq Scan?
    ↓
Heap
    ↓
Pages
    ↓
Buffers
```

---

## 21. Clustered vs Non-Clustered Concepts

Understand the physical implications of indexes and table layout.

---

## 22. Hash Indexing

Understand when hashing makes sense compared with tree-based indexes.

---

# 🐘 PostgreSQL Knowledge Already Covered

These concepts have already been explored practically:

* Heap
* Pages
* Buffers
* Shared buffer cache
* Sequential scans
* Index scans
* Bitmap scans
* Planner
* Cost estimates
* Cardinality estimates
* PostgreSQL statistics
* Stale statistics
* `EXPLAIN`
* `EXPLAIN ANALYZE`
* `BUFFERS`
* Index maintenance
* Composite indexes
* MVCC
* `xmin`
* `xmax`
* `ctid`
* Snapshots
* READ COMMITTED
* REPEATABLE READ
* Concurrent updates
* Row locking
* Atomic updates
* Deadlocks
* WAL
* Crash recovery
* VACUUM
* Autovacuum
* Connection pooling
* Migrations
* Backup / restore
* Point-in-Time Recovery

---

# 🚀 TRACK 2 — BACKEND ENGINEERING

I already know basic backend development, so this track does **not** restart from:

```python
@app.get("/")
```

The goal is to go deeper into production behavior.

---

# Level 1 — HTTP & Networking Fundamentals

Start here.

## Learn

### HTTP

* Request structure
* Response structure
* Headers
* Status codes
* Cookies
* Sessions
* Keep-alive
* HTTP/1.1
* HTTP/2 basics
* HTTP/3 / QUIC conceptually

Understand:

```text
Client
  ↓
DNS
  ↓
TCP
  ↓
TLS
  ↓
HTTP
  ↓
Backend
```

The goal is to understand what FastAPI actually sits on top of.

---

# Level 2 — ASGI & FastAPI Internals

Go deeper than simply using FastAPI.

Understand:

```text
Request
   ↓
ASGI Server
   ↓
FastAPI
   ↓
Middleware
   ↓
Routing
   ↓
Dependencies
   ↓
Validation
   ↓
Endpoint
   ↓
Business Logic
   ↓
Database
```

## Topics

* ASGI
* Uvicorn
* Request lifecycle
* Middleware
* Dependency Injection
* Pydantic
* Validation
* Response models
* Exception handling
* Background tasks
* Async vs Sync
* `asyncio`
* Blocking vs non-blocking I/O

---

# Level 3 — Backend Application Architecture

Move from:

```text
Route
  ↓
SQL
```

towards understanding:

```text
HTTP
  ↓
Router / Controller
  ↓
Validation
  ↓
Service
  ↓
Repository / DB Layer
  ↓
PostgreSQL
```

## Topics

* Routers / Controllers
* Services
* Repositories
* DTOs / Schemas
* Business logic
* Dependency Injection
* Configuration
* Environment variables
* Error handling
* Logging

The goal is not to blindly follow "Clean Architecture".

Understand **why each boundary exists**.

---

# Level 4 — Database Integration

This is where PostgreSQL + DBMS knowledge becomes backend engineering.

Understand:

```text
HTTP Request
      ↓
Connection Pool
      ↓
Transaction
      ↓
SQL
      ↓
PostgreSQL
      ↓
Planner
      ↓
Index / Heap
      ↓
MVCC
      ↓
Locks
      ↓
WAL
      ↓
COMMIT
```

## Topics

* Connection pooling
* Pool sizing
* Transactions
* Transaction boundaries
* Isolation levels
* Race conditions
* Atomic queries
* Optimistic locking
* Pessimistic locking
* N+1 queries
* Query performance
* Index design
* `EXPLAIN`
* Query timeouts
* Retry behavior

---

# Level 5 — Authentication & Security

Go beyond simply knowing JWT.

Understand:

```text
Login
  ↓
Verify Credentials
  ↓
Create Session / Token
  ↓
Client
  ↓
Request
  ↓
Authentication
  ↓
Authorization
  ↓
Resource
```

## Topics

* Password hashing
* Sessions
* JWT
* Access tokens
* Refresh tokens
* Token rotation
* Token revocation
* Cookies
* CSRF
* CORS
* XSS
* SQL Injection
* Rate limiting
* Authorization
* RBAC
* Secrets management

---

# Level 6 — Reliability & Failure Handling

This is where backend starts becoming production-oriented.

## Learn

* Retries
* Timeouts
* Idempotency
* Race conditions
* Duplicate requests
* Graceful failure
* Transactions
* Distributed failure
* Circuit breakers
* Queues
* Background workers

Example:

```text
Client
  │
  │ POST /payment
  ▼
Backend
  │
  ├── Payment succeeds
  │
  └── Response is lost
          ↓
      Client retries
          ↓
      Payment AGAIN ❌
```

Question:

> How should the backend make the operation safe to retry?

This is the type of engineering problem to solve.

---

# Level 7 — Testing

Understand testing at different levels:

```text
Unit Tests
    ↓
Service Tests
    ↓
Integration Tests
    ↓
Database Tests
    ↓
API Tests
    ↓
End-to-End Tests
```

## Topics

* Unit testing
* Integration testing
* API testing
* Database testing
* Test databases
* Fixtures
* Mocking
* Dependency overrides
* Transactions in tests
* End-to-end testing

---

# Level 8 — Observability

Learn how to answer:

> "Why is this endpoint slow?"

Instead of guessing.

Understand:

```text
Logs
  +
Metrics
  +
Traces
  ↓
Observability
```

Example:

```text
Request ID: abc123

POST /orders
    ↓
Service: 40ms
    ↓
Database: 380ms
    ↓
Redis: 5ms
    ↓
Response: 430ms
```

Topics:

* Structured logging
* Request IDs
* Metrics
* Latency
* Error rates
* Tracing
* Health checks
* Monitoring

---

# Level 9 — Docker & Deployment

Understand:

```text
Application
     ↓
Docker
     ↓
Container
     ↓
Reverse Proxy
     ↓
Cloud / VPS
     ↓
Database
```

## Topics

* Docker
* Docker Compose
* Environment configuration
* Production builds
* Reverse proxy
* HTTPS
* Process management
* Health checks
* Graceful shutdown
* Database migrations during deployment

---

# Level 10 — System Design

Only after understanding the previous layers.

Start asking:

```text
How would I build this for:

10 users?
      ↓
10,000 users?
      ↓
1 million users?
```

## Topics

* Caching
* Redis
* Queues
* Message brokers
* Load balancing
* Horizontal scaling
* Database replication
* Read replicas
* Partitioning
* Rate limiting
* Distributed systems
* Consistency
* Eventual consistency

---

# 🔥 How To Study Both Tracks

Do **not** do:

```text
DBMS
 ↓
Finish everything
 ↓
FastAPI
 ↓
Finish everything
```

Instead:

```text
                BACKEND
                   │
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
      HTTP                  DBMS
        │                     │
      ASGI             Serializability
        │                     │
    FastAPI              Recovery
        │                     │
   Architecture              2PL
        │                     │
        └──────────┬──────────┘
                   │
                   ▼
             PostgreSQL
                   │
             Transactions
                   │
             Concurrency
                   │
             Connection Pool
                   │
                   ▼
              Real Backend
```

The important part is **connecting the concepts**.

---

# 🧩 Example Of The Learning Style

### DBMS

Problem:

```text
T1 locks A
T2 locks B
T1 wants B
T2 wants A
```

Solve the deadlock theoretically.

Then ask:

> How could my backend actually create this?

Then:

```text
FastAPI Request A
       ↓
Transaction A
       ↓
UPDATE account 1
       ↓
locks row 1

FastAPI Request B
       ↓
Transaction B
       ↓
UPDATE account 2
       ↓
locks row 2
```

Then both try to access the other's row.

Now DBMS theory becomes a real backend problem.

---

# 🎯 Exact Starting Point

## DBMS

Continue from:

```text
Conflict Serializability
        ↓
View Serializability
        ↓
Recoverability
        ↓
Cascadeless / Strict
        ↓
Locks
        ↓
2PL
        ↓
Deadlocks
        ↓
Normalization
        ↓
B+ Trees / Indexing
```

## Backend

Start from:

```text
HTTP
  ↓
ASGI
  ↓
FastAPI Request Lifecycle
  ↓
Middleware
  ↓
Dependency Injection
  ↓
Async / Sync
  ↓
Application Architecture
  ↓
Database Integration
```

Do **not** restart basic FastAPI.

---

# 🧠 Final Goal

The ultimate mental model should become:

```text
                CLIENT
                  │
                  ▼
                 HTTP
                  │
                  ▼
             ASGI / Server
                  │
                  ▼
               FastAPI
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   Middleware            Routing
        │                   │
        └─────────┬─────────┘
                  ▼
             Validation
                  │
                  ▼
              Service
                  │
                  ▼
          Connection Pool
                  │
                  ▼
             Transaction
                  │
                  ▼
             PostgreSQL
                  │
       ┌──────────┼──────────┐
       ▼          ▼          ▼
    Planner      MVCC       WAL
       │          │          │
       ▼          ▼          ▼
    Indexes     Locks     Durability
       │
       ▼
      Heap
       │
       ▼
     Pages
       │
       ▼
    Buffers
       │
       ▼
      Disk
```

And alongside it:

```text
DBMS THEORY
    │
    ├── Serializability
    ├── Recoverability
    ├── 2PL
    ├── Deadlocks
    ├── Functional Dependencies
    ├── Normalization
    └── B+ Trees
```

### Core principle

> **Don't memorize the stack. Understand the behavior of the system at every layer.**

That is the transition from:

**"I know FastAPI and PostgreSQL"**

to:

**"I understand what my backend is actually doing in production."**

```
```
