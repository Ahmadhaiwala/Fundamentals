# PostgreSQL Concurrency — Deadlocks

## Overview

A **deadlock** happens when two or more transactions are waiting for each other in a cycle, so none of them can make progress.

The important mental model is:

> **Waiting is normal. Circular waiting is a deadlock.**

---

# 1. Normal Lock Waiting

Suppose:

```text
account
┌────┬────────┐
│ id │ amount │
├────┼────────┤
│ 1  │ 100    │
└────┴────────┘
```

Transaction A modifies row `id = 1`:

```sql
BEGIN;

UPDATE account
SET amount = amount - 100
WHERE id = 1;
```

A has an ongoing modification involving that row.

Transaction B then tries to modify the same row:

```sql
BEGIN;

UPDATE account
SET amount = amount - 100
WHERE id = 1;
```

B cannot blindly modify the same row simultaneously.

Conceptually:

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

If A commits:

```text
A → COMMIT
      ↓
B wakes up
      ↓
B continues
```

This is **not a deadlock**.

---

# 2. What Makes a Deadlock Different?

A deadlock requires a **cycle of dependencies**.

Consider two rows:

```text
account

id = 1
id = 2
```

Transaction A:

```sql
BEGIN;

UPDATE account
SET amount = amount - 10
WHERE id = 1;
```

A now needs row `2`:

```sql
UPDATE account
SET amount = amount - 20
WHERE id = 2;
```

Meanwhile, Transaction B has already modified row `2`:

```sql
BEGIN;

UPDATE account
SET amount = amount - 20
WHERE id = 2;
```

Then B wants row `1`:

```sql
UPDATE account
SET amount = amount - 10
WHERE id = 1;
```

Now:

```text
A holds row 1
A wants row 2

B holds row 2
B wants row 1
```

Therefore:

```text
A ───── wants ─────→ B
↑                    │
│                    │
└───── wants ────────┘
```

More intuitively:

```text
A:
"I need row 2."
        ↓
"Row 2 is being held by B."
        ↓
WAIT

B:
"I need row 1."
        ↓
"Row 1 is being held by A."
        ↓
WAIT
```

Neither transaction can naturally continue.

💀 **Deadlock.**

---

# 3. How PostgreSQL Thinks About It

PostgreSQL can have many transactions waiting on one another.

Conceptually, it can represent the dependencies as a graph:

```text
Transaction A
      │
      │ waits for
      ▼
Transaction B
      │
      │ waits for
      ▼
Transaction A
```

PostgreSQL detects the cycle:

```text
A → B → A
```

and recognizes:

```text
DEADLOCK DETECTED
```

It then aborts one of the transactions.

Conceptually:

```text
A ──→ B
↑     │
└─────┘

      ↓

deadlock detected
      ↓
one transaction aborted
      ↓
other transaction can continue
```

The application receives a deadlock/serialization-related database error and should handle the failed transaction appropriately, often by retrying the whole transaction where appropriate.

---

# 4. Waiting vs Deadlock

This distinction is extremely important.

### Normal waiting

```text
A → holds row 1

B → wants row 1
     ↓
    WAIT

A → COMMIT
     ↓
B → continues
```

There is a path to completion.

### Deadlock

```text
A → holds row 1
A → wants row 2
        ↑
        │
B → holds row 2
B → wants row 1
```

Both are waiting for each other.

There is no natural path to completion.

---

# 5. Real Backend Example — Money Transfer

Imagine an API:

```text
POST /transfer
```

Transfer A:

```text
Account 1 → Account 2
```

might access rows in this order:

```text
lock account 1
lock account 2
```

At nearly the same time, another request:

```text
Account 2 → Account 1
```

might access them in the opposite order:

```text
lock account 2
lock account 1
```

Now:

```text
Transaction A

holds account 1
      ↓
wants account 2
```

while:

```text
Transaction B

holds account 2
      ↓
wants account 1
```

Result:

```text
A waits for B
B waits for A
       ↓
    DEADLOCK
```

This is a realistic backend concurrency problem.

---

# 6. Preventing Deadlocks

One important technique is:

> **Acquire resources in a consistent order.**

For example, always lock the smaller account ID first.

For:

```text
1 → 2
```

lock:

```text
1
2
```

For:

```text
2 → 1
```

also lock:

```text
1
2
```

Now:

```text
Transaction A:
lock 1
lock 2
```

Transaction B:

```text
tries lock 1
    ↓
WAIT
```

A finishes:

```text
A → COMMIT
```

Then:

```text
B → gets lock 1
B → gets lock 2
B → continues
```

No circular dependency exists.

---

# 7. Why Consistent Ordering Works

Without ordering:

```text
A: 1 → 2
B: 2 → 1
```

Potentially:

```text
A holds 1
B holds 2

A wants 2
B wants 1

       ↓

     CYCLE
```

With consistent ordering:

```text
A: 1 → 2
B: 1 → 2
```

Both attempt:

```text
1 first
2 second
```

So the second transaction may wait:

```text
A → holds 1
B → waits for 1

A → gets 2
A → commits

B → gets 1
B → gets 2
```

No cycle.

---

# 8. Deadlocks Are Not Necessarily a Database Bug

A deadlock often comes from the way an application accesses resources.

Application:

```text
Request
   ↓
Transaction
   ↓
lock resource A
   ↓
lock resource B
```

Another request:

```text
Request
   ↓
Transaction
   ↓
lock resource B
   ↓
lock resource A
```

The database is then dealing with the consequences.

PostgreSQL's job is to detect the impossible dependency and abort one transaction rather than allowing the system to wait forever.

---

# 9. Connection to MVCC

Deadlocks are part of the larger PostgreSQL concurrency system we've been studying.

```text
MVCC
 ↓
Multiple row versions
 ↓
"What version can I see?"

LOCKING
 ↓
Conflicting writers coordinate
 ↓
"Can I modify this row right now?"

ISOLATION LEVEL
 ↓
Concurrency guarantees
 ↓
"How consistent must my transaction view be?"

DEADLOCK DETECTION
 ↓
Detect impossible waiting cycles
 ↓
"Who is waiting for whom?"
```

---

# 10. Overall Mental Model

```text
                 TRANSACTION
                      │
                      ▼
                  SQL UPDATE
                      │
                      ▼
              Find target row
                      │
                      ▼
            Another writer active?
                 /          \
               NO            YES
               │              │
            proceed         WAIT
                              │
                              ▼
                     Other transaction
                         finishes?
                       /           \
                     YES            NO
                      │              │
                   continue       dependency
                                      │
                                      ▼
                              cycle detected
                                      │
                                      ▼
                                   DEADLOCK
                                      │
                                      ▼
                             abort one transaction
```

---

# Key Takeaways

* **Lock waiting is normal.**
* **Deadlock = circular waiting.**
* PostgreSQL can detect dependency cycles between transactions.
* When a deadlock is detected, PostgreSQL aborts one transaction to break the cycle.
* The surviving transaction can then continue.
* Deadlocks commonly arise when transactions acquire multiple resources in different orders.
* **Consistent lock/resource ordering** is a major prevention technique.
* Deadlocks are often caused by application transaction design rather than PostgreSQL malfunction.
* Backend applications should be prepared to handle transaction failures and retry when appropriate.

---

## 🧠 The One Picture to Remember

```text
NORMAL WAITING

A ──────→ row 1
           ↑
           │
           B waits

A finishes
    ↓
B continues
```

vs.

```text
DEADLOCK

A ──holds──→ row 1
│             ↑
│             │
wants         │
│             │
▼             │
row 2 ←──holds── B
              │
              │
              └── wants row 1

        A waits for B
        B waits for A
              ↓
           💀 DEADLOCK
```

**Next topic: WAL (Write-Ahead Logging)** — we'll move from *concurrency* to **durability** and understand what PostgreSQL actually does when you `COMMIT` and the machine suddenly loses power.
