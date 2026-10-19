# PostgreSQL MVCC & Transaction Concurrency

## Overview

PostgreSQL does **not simply overwrite rows in place** when updates happen.

Instead, it uses **MVCC (Multi-Version Concurrency Control)** to maintain multiple versions of rows and decide which version each transaction is allowed to see.

The goal is to understand PostgreSQL from the perspective of:

> **"If I were PostgreSQL, what would I do when multiple transactions interact with the same data?"**

---

# 1. MVCC — Multiple Versions of a Row

Consider:

```text
account
┌────┬────────┐
│ id │ amount │
├────┼────────┤
│ 1  │ 100    │
└────┴────────┘
```

When an update happens:

```sql
UPDATE account
SET amount = 200
WHERE id = 1;
```

PostgreSQL conceptually creates a **new row version** rather than simply destroying the old version.

```text
Old version                 New version

amount = 100                amount = 200
     │                           │
     └── old version             └── new version
```

The old version can remain in the heap until PostgreSQL determines that it is no longer needed and cleans it up.

---

# 2. `xmin`, `xmax`, and `ctid`

PostgreSQL tuples contain transaction-related metadata.

Useful values for understanding MVCC:

### `xmin`

Transaction that created the row version.

```text
xmin = 987
```

means that transaction `987` created that tuple version.

### `xmax`

Transaction that made the tuple version obsolete.

```text
xmax = 0
```

generally means the current tuple has not been marked obsolete by a deleting/updating transaction.

### `ctid`

Physical location of the tuple inside the table.

Example:

```text
ctid = (0,2)
```

It can change when a row is updated because a new physical tuple version may be created.

---

# 3. MVCC Experiment

```sql
CREATE TABLE mvcc_demo (
    id INT PRIMARY KEY,
    value INT
);

INSERT INTO mvcc_demo VALUES (1, 100);

SELECT xmin, xmax, ctid, id, value
FROM mvcc_demo;
```

Then:

```sql
UPDATE mvcc_demo
SET value = 200
WHERE id = 1;

SELECT xmin, xmax, ctid, id, value
FROM mvcc_demo;
```

The important observation is that the physical tuple information can change after the update.

Mental model:

```text
Logical row
     │
     ├── version 1 → value = 100
     │
     └── version 2 → value = 200
```

---

# 4. Snapshot

A snapshot is **NOT a copy of the database**.

It is information PostgreSQL uses to determine:

> **Which row versions are visible to this transaction/statement?**

Think:

```text
Heap
 │
 ├── row version 1
 ├── row version 2
 └── row version 3
          │
          ▼
      Snapshot
          │
          ▼
"Which version am I allowed to see?"
```

---

# 5. Connection ≠ Transaction ≠ Snapshot

These are different concepts.

```text
CONNECTION
     ↓
TRANSACTION
     ↓
SNAPSHOT / VISIBILITY
     ↓
ROW VERSIONS
```

### Connection

A connection is the communication channel between the application/client and PostgreSQL.

### Transaction

A transaction is a unit of database work:

```sql
BEGIN;

-- statements

COMMIT;
```

`BEGIN` starts a **transaction**, not a new connection.

### Snapshot

A snapshot determines what data is visible according to the transaction's isolation rules.

---

# 6. READ COMMITTED

PostgreSQL's default isolation level is:

```text
READ COMMITTED
```

The important mental model:

> **Each statement gets a fresh snapshot.**

Example:

```text
Initial amount = 100
```

Transaction A:

```sql
BEGIN;

SELECT amount;
-- 100
```

Transaction B:

```sql
UPDATE account
SET amount = 200
WHERE id = 1;

COMMIT;
```

A executes another statement:

```sql
SELECT amount;
```

It can now see:

```text
200
```

Because the second statement gets a newer snapshot.

```text
Transaction A

SELECT #1
   ↓
Snapshot #1
   ↓
100

B changes data
   ↓
B COMMIT

SELECT #2
   ↓
Snapshot #2
   ↓
200
```

---

# 7. REPEATABLE READ

With:

```sql
SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;
```

the transaction gets a consistent view for its reads.

Example:

```text
Initial:
amount = 100
```

A:

```sql
BEGIN;

SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

SELECT amount;
-- 100
```

B:

```sql
UPDATE account
SET amount = 200
WHERE id = 1;

COMMIT;
```

A reads again:

```sql
SELECT amount;
```

A can continue seeing:

```text
100
```

even though the current database state is:

```text
200
```

Mental model:

```text
Actual database          A's transaction view

amount = 200             amount = 100
                              │
                              │
                         consistent view
```

---

# 8. REPEATABLE READ + Concurrent UPDATE

This is an important behavior.

Initial:

```text
amount = 100
```

A:

```sql
BEGIN;

SET TRANSACTION ISOLATION LEVEL REPEATABLE READ;

SELECT amount;
-- 100
```

Then B:

```sql
UPDATE account
SET amount = 200
WHERE id = 1;

COMMIT;
```

Now A tries:

```sql
UPDATE account
SET amount = amount + 50
WHERE id = 1;
```

PostgreSQL can reject A's update with a **serialization failure** because the row A is trying to modify was concurrently changed after A's snapshot.

It does **not** simply do:

```text
200 + 50 = 250
```

Mental model:

```text
A's snapshot
amount = 100

        ↓

B changes row

100 → 200
        ↓
B COMMIT

        ↓

A tries to UPDATE
        ↓
PostgreSQL detects concurrent change
        ↓
Serialization failure ❌
```

---

# 9. Concurrent Updates and Row Locking

Consider:

```text
amount = 100
```

Transaction A:

```sql
BEGIN;

UPDATE account
SET amount = amount - 100
WHERE id = 1;
```

A has modified the row and has the necessary conflicting lock state.

Transaction B then tries:

```sql
BEGIN;

UPDATE account
SET amount = amount - 100
WHERE id = 1;
```

B cannot blindly modify the same row simultaneously.

Instead:

```text
A
│
├── modifying row 1
│
└── transaction still open
          │
          ▼
       row conflict
          │
          ▼
B ────── WAIT ⏳
```

After A commits:

```text
A → COMMIT
      ↓
B wakes up
      ↓
continues according to
transaction/isolation rules
```

The important distinction:

> **It isn't the UPDATE statement itself that is "locked." The conflicting row modification requires coordination.**

---

# 10. MVCC vs Row Locking

These solve different problems.

### MVCC

Answers:

> **Which row version should I see?**

```text
Old version
     │
New version
     │
     ▼
visibility rules
```

### Row locking

Answers:

> **Can conflicting transactions modify the same row simultaneously?**

```text
A modifies row
      ↓
B wants same row
      ↓
WAIT
```

Together:

```text
MVCC
 ↓
visibility

Row locking
 ↓
conflicting writers coordinate
```

---

# 11. Constraints Still Apply

Suppose:

```sql
CHECK (amount >= 0)
```

Starting balance:

```text
100
```

A:

```text
100 → 0
```

B tries to withdraw another 100.

B waits for A's conflicting modification.

After A commits:

```text
Current amount = 0
```

B attempts:

```text
0 - 100 = -100
```

Then:

```text
CHECK(amount >= 0)
        ↓
    -100 >= 0
        ↓
       FALSE
        ↓
      ERROR ❌
```

So concurrency involves multiple mechanisms:

```text
MVCC
  ↓
row versions / visibility

Locking
  ↓
conflicting writers wait

Constraints
  ↓
invalid state rejected
```

---

# 12. Atomic Database Operations

A dangerous backend pattern is:

```sql
SELECT amount
FROM account
WHERE id = 1;
```

Then application code:

```python
if amount >= 100:
    UPDATE ...
```

Two requests can race:

```text
A                         B

SELECT → 100
                          SELECT → 100

100 >= 100 ✔
                          100 >= 100 ✔

UPDATE
                          UPDATE
```

Instead, put the condition and modification together:

```sql
UPDATE account
SET amount = amount - 100
WHERE id = 1
  AND amount >= 100;
```

Then check the affected row count.

```text
1 row affected
    ↓
withdrawal succeeded

0 rows affected
    ↓
insufficient balance / row didn't match
```

This removes the application-level race between the `SELECT` and `UPDATE`.

---

# 13. SERIALIZABLE

The strongest commonly used isolation level we are studying:

```text
SERIALIZABLE
```

The goal:

> Concurrent transactions should behave as though they executed in some serial order.

It does **not necessarily mean PostgreSQL literally executes one transaction at a time**.

Instead, PostgreSQL detects dangerous concurrent interactions and may abort a transaction.

```text
A ──────────────┐
                │
        dangerous interaction
                │
B ──────────────┘
                ↓
      serialization failure ❌
                ↓
       application retries
```

---

# 14. Isolation Levels — Mental Model

```text
READ COMMITTED
    ↓
Each statement gets a fresh snapshot.

REPEATABLE READ
    ↓
Transaction maintains a consistent view.
Concurrent modifications can cause
serialization failures.

SERIALIZABLE
    ↓
Concurrent execution must be equivalent
to some serial execution.
Unsafe transaction may be aborted.
```

---

# 15. The PostgreSQL System Model

The overall mental model we've built:

```text
Application
     │
     ▼
Connection
     │
     ▼
Transaction
     │
     ▼
SQL statement
     │
     ▼
MVCC visibility
     │
     ├── Which row versions are visible?
     │
     ▼
Find target row
     │
     ▼
Conflicting writer?
     │
     ├── YES → WAIT
     │
     └── NO  → proceed
     │
     ▼
Create/update row version
     │
     ▼
Constraints
     │
     ▼
COMMIT / ROLLBACK
     │
     ▼
Visibility to other transactions
```

---

# Key Takeaways

* **MVCC** allows PostgreSQL to maintain multiple versions of rows.
* An `UPDATE` can result in a new physical tuple version.
* `xmin`, `xmax`, and `ctid` help expose the underlying tuple behavior.
* A **snapshot is visibility information, not a database copy**.
* `BEGIN` starts a transaction; it does not create a connection.
* **READ COMMITTED** gets a fresh snapshot for each statement.
* **REPEATABLE READ** provides a consistent transaction view.
* **SERIALIZABLE** provides the strongest concurrency guarantee by preventing unsafe transaction interleavings.
* MVCC and locking are **different mechanisms**.
* Conflicting writers can **wait for each other**.
* Constraints remain the final integrity boundary.
* Putting a condition and state change into one SQL operation can eliminate application-level race conditions.

---

## Mental Picture to Remember

```text
                 PostgreSQL
                     │
              ┌──────┴──────┐
              │             │
             MVCC         LOCKING
              │             │
       "What can I see?"   "Can I modify?"
              │             │
              └──────┬──────┘
                     │
                TRANSACTION
                     │
                ISOLATION
                     │
              "How consistent
               must my view be?"
                     │
                     ▼
              COMMIT / ROLLBACK
```

**Next:** Deadlocks → how PostgreSQL handles transactions that are waiting on each other.
