Yes bro. **Level 2 is essentially complete.** 🔥

The important thing is that you didn't just memorize PostgreSQL commands—you built the mental model of **what PostgreSQL is doing underneath your backend queries**.

# PostgreSQL — Level 2 Complete Overview

## 1. How PostgreSQL Finds Data

We started with:

```text
SELECT *
FROM orders
WHERE user_id = 5000;
```

And learned that PostgreSQL doesn't simply "use the index."

It goes roughly:

```text
SQL
 ↓
Parser / Analyzer
 ↓
Planner
 ↓
Choose execution strategy
 ↓
Executor
 ↓
Heap / Index
 ↓
Buffers
 ↓
Rows
```

The planner estimates different strategies and chooses what it thinks is cheapest.

---

# 2. Heap

The **heap is where the actual table rows live**.

Think:

```text
Table
 ↓
Heap
 ↓
Pages
 ↓
Rows
```

An index doesn't contain the complete table.

It helps PostgreSQL find **where the relevant table rows are**.

```text
Index
 ↓
"Matching row is around here"
 ↓
Heap
 ↓
Actual row
```

---

# 3. Pages & Buffers

PostgreSQL works with data in **pages/blocks**, rather than thinking about individual rows as the fundamental disk I/O unit.

Conceptually:

```text
Disk
 ↓
Database pages
 ↓
Shared buffers
 ↓
PostgreSQL works on data
```

So:

```text
shared hit
```

means the required page was already in PostgreSQL's shared buffer cache.

```text
shared read
```

means PostgreSQL had to read the page into the buffer cache.

This gave us an important physical mental model:

```text
row
 ↓
page
 ↓
buffer
 ↓
CPU works with it
```

---

# 4. Sequential Scan

If PostgreSQL needs most/all of a table:

```text
Seq Scan
```

can be better than using an index.

Example:

```sql
SELECT *
FROM orders;
```

There is no point doing:

```text
index
 ↓
find row 1
 ↓
heap
 ↓
find row 2
 ↓
heap
 ↓
...
```

when we need basically everything.

Instead:

```text
heap page 1
 ↓
heap page 2
 ↓
heap page 3
 ↓
...
```

That's a sequential scan.

### Key lesson

> **An index isn't automatically faster.**

It depends on how much data PostgreSQL needs and what the planner estimates.

---

# 5. Index Scan vs Bitmap Scan

We saw:

```text
Bitmap Index Scan
        ↓
Bitmap Heap Scan
```

The index finds matching tuple locations.

Then PostgreSQL groups the required heap pages and fetches them efficiently.

Conceptually:

```text
Index
 ↓
matching locations
 ↓
group required pages
 ↓
Heap
 ↓
rows
```

This is useful when there are enough matching rows that a simple index scan would involve lots of scattered heap accesses.

---

# 6. Planner & Cost

The planner asks:

> "What execution strategy is likely to be cheapest?"

It considers things such as:

```text
estimated number of rows
estimated page accesses
indexes
selectivity
table statistics
```

And produces something like:

```text
Seq Scan
cost = ...

Bitmap Scan
cost = ...

Index Scan
cost = ...
```

The cost isn't milliseconds.

It's a **planner cost unit used for comparing strategies**.

---

# 7. Statistics

PostgreSQL maintains statistics about the data.

For example:

```text
How many distinct values?
How common are certain values?
How is the data distributed?
```

The planner uses this information to estimate:

```text
How many rows will this query probably return?
```

Example:

```sql
WHERE user_id = 5000
```

Planner might estimate:

```text
100 rows
```

---

# 8. Stale Statistics

We deliberately inserted a huge number of rows with:

```text
user_id = 5000
```

without refreshing statistics.

PostgreSQL thought:

```text
Estimated: ~110 rows
Actual:     ~100,094 rows
```

That's roughly a **910× estimation error**.

The important chain was:

```text
Data changes
 ↓
statistics don't immediately reflect everything
 ↓
planner has inaccurate information
 ↓
planner makes inaccurate estimates
 ↓
potentially chooses a bad execution plan
 ↓
query can become expensive
```

Then:

```text
ANALYZE
```

refreshes planner statistics.

---

# 9. Index Maintenance

We learned something very important:

> An index isn't free.

When you insert:

```text
INSERT
```

PostgreSQL has to maintain relevant indexes.

Similarly, updates/deletes can require index maintenance.

Therefore:

```text
More indexes
     ↓
Faster potential reads
     ↓
More storage
     ↓
More work during writes
```

So production isn't:

> "Put an index on everything."

It's:

> **Index according to real query patterns.**

---

# 10. Composite Indexes

We introduced:

```sql
CREATE INDEX idx_user_status
ON orders(user_id, status);
```

The ordering matters.

A composite index:

```text
(user_id, status)
```

is naturally useful for queries involving:

```text
user_id
```

and:

```text
user_id + status
```

but isn't equivalent to having:

```text
(status, user_id)
```

because index column ordering affects how PostgreSQL can navigate the index.

The important production question is:

> **What queries do I actually need to optimize?**

---

# 11. MVCC

This was one of the biggest concepts.

PostgreSQL generally doesn't simply overwrite a row in place for every UPDATE.

Conceptually:

```text
Before

id = 1
value = 100
```

UPDATE:

```sql
UPDATE mvcc_demo
SET value = 200
WHERE id = 1;
```

Conceptually becomes:

```text
old version
value = 100

      ↓

new version
value = 200
```

Different transactions can see different versions depending on visibility rules.

---

# 12. xmin / xmax / ctid

We inspected:

```sql
SELECT xmin, xmax, ctid, id, value
FROM mvcc_demo;
```

Mental model:

```text
xmin
 ↓
transaction that created this tuple version

xmax
 ↓
transaction that made this version obsolete
```

And:

```text
ctid
 ↓
physical tuple location
```

We saw the `ctid` change after an UPDATE, which helped demonstrate that a new physical tuple version was created.

---

# 13. Snapshots

This distinction was extremely important:

```text
Connection ≠ Transaction ≠ Snapshot
```

### Connection

A communication channel/session with PostgreSQL.

### Transaction

A unit of database work:

```sql
BEGIN;

...

COMMIT;
```

### Snapshot

The visibility information used to determine:

> "Which row versions can this transaction see?"

A snapshot is **not a copy of the database**.

---

# 14. READ COMMITTED

Under PostgreSQL's default:

```text
READ COMMITTED
```

each statement gets its own view/snapshot.

So:

```text
Transaction A

SELECT → sees 100

Transaction B
UPDATE → 200
COMMIT

Transaction A

SELECT → can now see 200
```

The second SELECT is a new statement and can therefore see newer committed data.

---

# 15. REPEATABLE READ

With:

```text
REPEATABLE READ
```

the transaction maintains a consistent transaction-level view.

Conceptually:

```text
Transaction A
     ↓
snapshot
     ↓
SELECT → 100

Transaction B
     ↓
UPDATE → 200
     ↓
COMMIT

Transaction A
     ↓
SELECT
     ↓
still sees its consistent view
```

This is where the difference between **statement-level and transaction-level visibility** became important.

---

# 16. Row Locking & Concurrent Updates

Suppose:

```text
balance = 100
```

Transaction A:

```sql
UPDATE account
SET amount = amount - 100
WHERE id = 1;
```

Transaction B simultaneously tries to modify the **same row**.

PostgreSQL doesn't simply let both conflicting writes blindly proceed.

Conceptually:

```text
A
 ↓
modifies row
 ↓
holds conflicting lock

B
 ↓
tries same row
 ↓
WAIT
```

Then:

```text
A COMMIT
 ↓
B wakes up
 ↓
continues according to PostgreSQL's concurrency rules
```

Important distinction:

> The **row operation is blocked**, not the entire database.

Other unrelated rows can continue being processed.

---

# 17. Atomic Updates

We saw why this is dangerous:

```sql
SELECT amount
FROM account
WHERE id = 1;

-- application checks amount

UPDATE account
SET amount = amount - 100
WHERE id = 1;
```

Between the SELECT and UPDATE, another transaction can change the balance.

Better:

```sql
UPDATE account
SET amount = amount - 100
WHERE id = 1
  AND amount >= 100;
```

Then check the affected-row count.

```text
1 row updated → withdrawal succeeded

0 rows updated → condition wasn't satisfied
```

This pushes the critical invariant into **one atomic database operation**.

---

# 18. Deadlocks

Normal waiting:

```text
A → locks row 1
B → wants row 1
B waits
A commits
B continues
```

That's fine.

Deadlock:

```text
A → locks row 1
A → wants row 2
       ↑
       │
B → locks row 2
B → wants row 1
```

Now:

```text
A waits for B
B waits for A
```

Circular dependency.

PostgreSQL detects the deadlock and aborts one transaction so the other can continue.

### Prevention

Acquire resources in a consistent order.

For example:

```text
Always lock smaller account ID first.
```

---

# 19. WAL

This was another major piece.

When PostgreSQL changes data:

```text
UPDATE
 ↓
data page becomes dirty
 ↓
WAL record generated
 ↓
WAL made durable according to durability settings
 ↓
COMMIT
```

The actual table page doesn't necessarily need to be immediately written to disk at COMMIT.

That's important because doing so for every transaction would be expensive.

Instead:

```text
WAL
 ↓
durable record of changes
```

allows PostgreSQL to recover after a crash.

---

# 20. Crash Recovery

Suppose:

```text
UPDATE
 ↓
COMMIT
 ↓
server suddenly crashes
```

After restart:

```text
PostgreSQL
 ↓
reads WAL
 ↓
recovery
 ↓
reconstructs required state
```

That's **crash recovery**.

---

# 21. VACUUM

Because of MVCC:

```text
UPDATE
 ↓
new tuple version
 ↓
old tuple eventually becomes dead
```

Those dead tuples cannot just accumulate forever.

VACUUM helps clean up obsolete tuple versions and make their space reusable.

```text
UPDATE
 ↓
old version
 ↓
dead tuple
 ↓
VACUUM
 ↓
space becomes reusable
```

Important distinction:

```text
VACUUM
=
cleanup/reuse space

ANALYZE
=
refresh planner statistics
```

And:

```text
autovacuum
```

automates maintenance based on table activity.

---

# 22. Long-Running Transactions

This connected directly to MVCC + VACUUM.

If an old transaction remains open:

```text
old transaction
       ↓
still needs an older visibility horizon
       ↓
some old row versions cannot yet be cleaned
       ↓
dead tuples accumulate
       ↓
bloat
```

So a backend engineer should care about long-running transactions.

---

# 23. Connection Pooling

Creating a fresh database connection for every HTTP request is inefficient.

Instead:

```text
HTTP request
     ↓
connection pool
     ↓
borrow connection
     ↓
execute DB work
     ↓
return connection
```

The pool also acts as a concurrency boundary.

Too many database connections can actually hurt performance.

```text
More connections
≠
More performance
```

---

# 24. Migrations

We cleared up an important misconception here.

### Schema

Current database structure.

```text
users
├── id
├── name
├── email
└── phone
```

### Schema Version

A label describing the current structural state.

### Migration

The change required to move between structural states.

Example:

```text
001_create_users
002_add_phone
003_add_phone_index
004_make_phone_required
```

A migration is **not another database**.

It is essentially:

> **Versioned, controlled SQL/schema changes.**

---

# 25. Production Schema Evolution

Instead of suddenly doing:

```sql
ALTER TABLE users
ADD phone TEXT NOT NULL;
```

we might do:

```text
Migration 1
    ↓
Add nullable phone

Application update
    ↓
Start writing phone

Backfill
    ↓
Populate existing records

Verification
    ↓
Check no NULL values

Migration 2
    ↓
Make phone NOT NULL
```

The sophistication isn't the SQL itself.

The sophistication is:

```text
How do we safely evolve a live database
without breaking existing data/application instances?
```

---

# 26. Backup

A backup provides a **recoverable database state**.

Think:

```text
Database
   ↓
Backup
   ↓
saved recoverable state
```

It is not:

```text
WAL
```

and it is not:

```text
migration
```

---

# 27. Restore

Restore means:

> **Reconstructing a database from a backup/recovery source.**

Conceptually:

```text
Backup
   ↓
Restore
   ↓
Recovered database
```

The backup doesn't magically fix bad data.

If you backed up a database containing bad data:

```text
bad data
   ↓
backup
   ↓
restore
   ↓
bad data
```

Therefore, recovery often relies on a **known-good backup**.

---

# 28. Backup + WAL

This gives us:

```text
Backup
   +
WAL history
   ↓
Recovery
```

The backup provides the starting point.

WAL provides subsequent changes.

This enables the concept of:

```text
Point-in-Time Recovery
```

For example:

```text
10:00
Good state
 ↓
Backup

11:00
Bug introduced

11:05
Bad UPDATE

11:30
Problem discovered
```

Potentially recover toward:

```text
10:59
```

rather than recovering the bad changes.

---

# 29. Crash Recovery vs Restore

Don't mix these.

### Crash Recovery

```text
Server crashes
 ↓
PostgreSQL restarts
 ↓
WAL recovery
```

### Restore

```text
Backup/recovery source
 ↓
reconstruct database
 ↓
recovered system
```

---

# The Complete Level 2 Mental Model

This is the thing I really want you to retain—not individual commands:

```text
                         PostgreSQL
                              │
                         SQL Request
                              │
                              ↓
                         Query Planner
                              │
                  ┌───────────┴───────────┐
                  ↓                       ↓
             Statistics               Query Shape
                  │                       │
                  └───────────┬───────────┘
                              ↓
                       Execution Plan
                              │
                    ┌─────────┴─────────┐
                    ↓                   ↓
                  Index               Heap
                    │                   │
                    └─────────┬─────────┘
                              ↓
                           Pages
                              ↓
                          Buffers
                              ↓
                           Rows
                              │
                       ┌──────┴──────┐
                       ↓             ↓
                     MVCC         Locks
                       │             │
                       └──────┬──────┘
                              ↓
                         Transactions
                              ↓
                             WAL
                              ↓
                            Disk
                              │
                    ┌─────────┴─────────┐
                    ↓                   ↓
               Crash Recovery        Backup
                                        ↓
                                     Restore
                                        ↓
                                      PITR
```

And above all of this:

```text
Application
     ↓
Connection Pool
     ↓
PostgreSQL
```

---

# ✅ Level 2 Status

### Completed

* ✅ Heap / pages
* ✅ Buffers / cache
* ✅ Sequential scans
* ✅ Index scans
* ✅ Bitmap scans
* ✅ Planner
* ✅ Cost estimates
* ✅ Statistics
* ✅ Stale statistics
* ✅ Index maintenance
* ✅ Composite-index fundamentals
* ✅ MVCC
* ✅ Row versions
* ✅ `xmin` / `xmax` / `ctid`
* ✅ Snapshots
* ✅ READ COMMITTED
* ✅ REPEATABLE READ
* ✅ Concurrent updates
* ✅ Row locking
* ✅ Atomic updates
* ✅ Deadlocks
* ✅ WAL
* ✅ Crash recovery
* ✅ VACUUM
* ✅ Autovacuum
* ✅ Long-running transaction implications
* ✅ Connection pooling
* ✅ Migrations
* ✅ Production schema evolution
* ✅ Backup
* ✅ Restore
* ✅ Backup + WAL / PITR concept

### One thing I would **not** do

Don't now spend another week trying to memorize every PostgreSQL feature.

You've reached the point where the useful next step is:

> **Take this mental model and use it to debug a production-like backend problem.**

That's where Level 2 actually becomes solid.

For example, I'll give you a backend situation like:

```text
"API became slow after deployment.
CPU is normal.
Database connections are near the limit.
One query suddenly went from 20ms → 8 seconds."
```

And **you investigate it like an engineer**, using everything we've learned rather than me telling you which concept to use.

That would be the natural **Level 2 final boss** before moving forward.
