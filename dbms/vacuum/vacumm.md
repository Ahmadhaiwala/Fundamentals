# PostgreSQL WAL & VACUUM — README

## 1. WAL — Write-Ahead Logging

### What problem does WAL solve?

Imagine:

```text
UPDATE account
SET balance = 500
WHERE id = 1;

COMMIT;
```

The database tells us:

```text
COMMIT successful
```

Then the server suddenly loses power.

PostgreSQL still needs to guarantee that the committed change can be recovered.

The problem is that the actual table data may still be sitting in PostgreSQL's memory buffers and may **not yet have been written to the physical data file**.

---

## Core Idea

**WAL = Write-Ahead Log**

Before PostgreSQL relies on a changed data page being safely stored, it records the change in a durable log.

Conceptually:

```text
UPDATE
   ↓
modify data page in memory
   ↓
create WAL record
   ↓
WAL is flushed durably
   ↓
COMMIT can be acknowledged
   ↓
data page can be written later
```

The important rule is:

> **The log describing a change must reach durable storage before the corresponding changed data page is allowed to be considered safely persisted.**

---

## Why not immediately write the table page?

Suppose an UPDATE changes one row inside an 8 KB page.

If PostgreSQL immediately had to write that data page to disk for every change:

```text
UPDATE
 ↓
write table page to storage
 ↓
UPDATE
 ↓
write table page
 ↓
UPDATE
 ↓
write table page
```

That would create a lot of expensive storage I/O.

Instead:

```text
UPDATE
 ↓
modify buffer
 ↓
write WAL
 ↓
continue
 ↓
flush data pages later
```

This allows PostgreSQL to batch data-page writes efficiently.

---

## WAL is not a database backup

Don't think:

```text
WAL = copy of database
```

Think:

```text
Database files
    ↓
actual table/index data

WAL
    ↓
durable record of changes
```

WAL allows PostgreSQL to recover the database after a crash.

---

## Crash Recovery

Imagine:

```text
UPDATE
   ↓
data page changed in memory
   ↓
WAL safely persisted
   ↓
COMMIT
   ↓
💥 POWER FAILURE
```

The data page may not have reached the main database file yet.

When PostgreSQL starts again:

```text
PostgreSQL starts
       ↓
recovery
       ↓
read WAL
       ↓
reconstruct/replay required changes
       ↓
database reaches a consistent state
```

This is why WAL is fundamental to PostgreSQL durability.

---

# 2. VACUUM

## Why does VACUUM exist?

PostgreSQL uses **MVCC**.

An UPDATE doesn't simply overwrite the old tuple.

Conceptually:

```text
Before:

┌──────────────┐
│ id = 1       │
│ value = 100  │
└──────────────┘
```

After:

```text
┌──────────────┐
│ id = 1       │
│ value = 100  │ ← old version
└──────────────┘

┌──────────────┐
│ id = 1       │
│ value = 200  │ ← new version
└──────────────┘
```

The old version eventually becomes a **dead tuple**.

---

## Dead Tuple

A dead tuple is an old row version that is no longer needed by any transaction that could still need to see it.

Example:

```text
UPDATE
   ↓
new tuple created
   ↓
old tuple becomes obsolete
   ↓
eventually becomes dead
```

If this happens continuously:

```text
UPDATE
 ↓
dead tuple

UPDATE
 ↓
dead tuple

UPDATE
 ↓
dead tuple

UPDATE
 ↓
dead tuple
```

the table can accumulate lots of useless row versions.

---

# What VACUUM does

VACUUM finds tuple versions that are no longer needed and makes their space available for reuse.

Conceptually:

```text
Before:

┌─────────────────────┐
│ live tuple          │
│ dead tuple          │
│ dead tuple          │
│ live tuple          │
│ dead tuple          │
└─────────────────────┘
```

After VACUUM:

```text
┌─────────────────────┐
│ live tuple          │
│ reusable space      │
│ reusable space      │
│ live tuple          │
│ reusable space      │
└─────────────────────┘
```

---

## Important: VACUUM doesn't simply "delete rows"

The better mental model is:

> **VACUUM cleans up obsolete tuple versions and makes their storage space reusable.**

This distinction matters.

---

# Does VACUUM shrink the table?

Usually, ordinary VACUUM does **not** mean:

```text
100 MB table
     ↓
50 MB file
```

Instead:

```text
100 MB table

[DATA][DEAD][DEAD][DATA][DEAD]

        VACUUM

[DATA][FREE][FREE][DATA][FREE]
```

The space can be reused by future operations.

`VACUUM FULL` is a different, much more invasive operation that can physically rewrite the table and reclaim disk space, with significant locking/performance implications.

---

# Autovacuum

You obviously don't want your application doing:

```sql
VACUUM orders;
```

after every UPDATE. 😂

PostgreSQL has **autovacuum**.

Conceptually:

```text
Application
     ↓
INSERT / UPDATE / DELETE
     ↓
dead tuples accumulate
     ↓
autovacuum notices
     ↓
VACUUM runs
     ↓
obsolete tuples cleaned
     ↓
space becomes reusable
```

This is an essential part of normal PostgreSQL maintenance.

---

# Long-Running Transactions

Here's where MVCC and VACUUM connect.

Suppose:

```text
Transaction A
BEGIN
```

Then another transaction modifies a row:

```text
Transaction B
UPDATE row
COMMIT
```

But A remains open for a long time.

Conceptually:

```text
old version
     ↑
     │
Transaction A may still need
this version for visibility
```

Therefore PostgreSQL may not be able to clean every old version immediately.

So:

```text
long transaction
      ↓
old versions remain relevant
      ↓
VACUUM cannot clean everything
      ↓
dead tuples accumulate
      ↓
bloat can increase
```

This is one reason unnecessarily long transactions can be problematic in production.

---

# The Bigger PostgreSQL Picture

Now connect the concepts:

```text
                     PostgreSQL
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
        MVCC            WAL          Planner
          │              │              │
          │              │              ├── Statistics
          │              │              ├── Index
          │              │              └── Scan
          │              │
          ▼              ▼
    Row versions      Durability
          │
          ▼
    Dead tuples
          │
          ▼
       VACUUM
          │
          ▼
    Reusable space
```

---

# The Two Mental Models

### WAL

Ask:

> **"What happens if PostgreSQL crashes right now?"**

```text
Change
  ↓
WAL
  ↓
durability
  ↓
recovery after crash
```

### VACUUM

Ask:

> **"What happens to all those old MVCC versions?"**

```text
UPDATE / DELETE
       ↓
old versions
       ↓
dead tuples
       ↓
VACUUM
       ↓
space becomes reusable
```

---

# 🔥 Final System Model

When you execute:

```sql
UPDATE orders
SET amount = 500
WHERE id = 10;
```

don't imagine merely:

```text
500 replaces 300
```

Imagine:

```text
                         UPDATE
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
            WAL                           MVCC
             │                             │
      durable change                 new tuple version
             │                             │
             │                       old version
             │                             │
             │                             ▼
             │                       dead tuple
             │                             │
             │                             ▼
             │                          VACUUM
             │                             │
             ▼                             ▼
         crash recovery             reusable space
```

That's the **system-level PostgreSQL mental model** we're building.
