# PostgreSQL Connection Pooling — README

## 1. The Problem

A backend application may receive many requests:

```text
Request 1 → database
Request 2 → database
Request 3 → database
...
Request 1000 → database
```

A naive approach would create a new PostgreSQL connection for every request:

```text
HTTP request
    ↓
create DB connection
    ↓
execute query
    ↓
close connection
```

Creating connections has overhead, and PostgreSQL cannot efficiently handle unlimited concurrent connections.

---

# 2. Connection Pool

A **connection pool** maintains a limited number of reusable PostgreSQL connections.

```text
              Connection Pool
        ┌────────────────────────┐
        │ Connection 1           │
        │ Connection 2           │
        │ Connection 3           │
        │ Connection 4           │
        │ Connection 5           │
        └────────────────────────┘
                   │
                   ▼
              PostgreSQL
```

Instead of creating a connection for every request:

```text
Request
   ↓
get connection from pool
   ↓
execute database work
   ↓
release connection
   ↓
connection becomes available again
```

---

# 3. Connection ≠ Transaction

These are different concepts.

```text
CONNECTION
     ↓
can contain a
     ↓
TRANSACTION
     ↓
has visibility/snapshot behavior
```

A connection can exist without an active transaction.

Example:

```text
Connection #2
     ↓
BEGIN
     ↓
queries
     ↓
COMMIT
     ↓
connection returned to pool
```

Later:

```text
Another request
     ↓
gets Connection #2
```

The connection is reused, but the previous transaction should already be finished.

---

# 4. What Happens When the Pool Is Full?

Suppose:

```text
Pool size = 10
```

and all ten connections are currently being used:

```text
Request 1  → Connection 1
Request 2  → Connection 2
...
Request 10 → Connection 10
```

Then:

```text
Request 11
    ↓
no connection available
    ↓
wait
    ↓
connection is returned
    ↓
Request 11 gets connection
```

So the pool effectively places a limit on how much database work can happen concurrently through that application instance.

---

# 5. Why Not Use Hundreds of Connections?

More connections do **not** automatically mean better performance.

For example:

```text
500 connections
      ↓
500 concurrent queries
      ↓
CPU / memory / I/O contention
      ↓
PostgreSQL becomes overloaded
```

The goal is:

> Have enough connections to keep useful database work flowing without overwhelming PostgreSQL.

---

# 6. Connection Pool as a Resource Queue

Think of the pool as a limited resource:

```text
              HTTP Requests
                    │
          ┌─────────┴─────────┐
          ▼                   ▼
     DB required          No DB needed
          │
          ▼
   Connection Pool
          │
     ┌────┴────┐
     ▼         ▼
available    full
     │         │
     ▼         ▼
execute      wait
     │         │
     └────┬────┘
          ▼
       release
```

This is why connection pooling is not merely an optimization.

It is also a way of **controlling database concurrency**.

---

# 7. Connection Pool + Transactions

A common backend flow is:

```text
HTTP Request
     ↓
get connection
     ↓
BEGIN
     ↓
SQL queries
     ↓
COMMIT / ROLLBACK
     ↓
release connection
```

If something fails:

```text
BEGIN
   ↓
query
   ↓
❌ error
   ↓
ROLLBACK
   ↓
release connection
```

The important idea is that a connection should not be returned to the pool while it is accidentally carrying an unfinished transaction or undesirable session state.

---

# 8. Why This Matters in Real Backends

Suppose your application has:

```text
10,000 HTTP requests
```

but only:

```text
20 database connections
```

That does **not** mean only 20 HTTP requests can exist.

Instead:

```text
10,000 HTTP requests
        │
        ├── requests that don't currently need DB
        │
        └── requests needing DB
                     │
                     ▼
                Connection Pool
                     │
                     ▼
              limited DB concurrency
```

Requests requiring database access may wait when all connections are busy.

---

# 9. Complete System Mental Model

We've now connected the application layer to PostgreSQL:

```text
HTTP Request
     ↓
Connection Pool
     ↓
PostgreSQL Connection
     ↓
Transaction
     ↓
SQL
     ↓
Planner
     ↓
Index / Heap
     ↓
Buffers
     ↓
MVCC
     ↓
WAL
     ↓
COMMIT
```

After changes:

```text
MVCC
  ↓
old tuple versions
  ↓
dead tuples
  ↓
VACUUM / Autovacuum
```

---

# 🔥 Core Mental Model

Don't memorize:

> "Connection pooling means reusing database connections."

Instead remember the problem:

```text
Creating connections has overhead
            +
PostgreSQL cannot efficiently handle unlimited
concurrent database work
            ↓
       CONNECTION POOL
            ↓
limited reusable connections
            ↓
requests share them
            ↓
database concurrency is controlled
```

### One-line summary

> **A connection pool keeps a controlled number of PostgreSQL connections alive and lets many application requests reuse them instead of creating a new database connection for every request.**
