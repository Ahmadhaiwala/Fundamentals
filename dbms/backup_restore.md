# PostgreSQL Backup & Restore

## 1. The Core Idea

A backup is a **saved, recoverable representation of a database state**.

It is NOT:

* WAL
* a migration
* a live database
* automatically a guarantee that the data is correct

Think:

```text
Database
   ↓
Backup
   ↓
Saved recoverable state
```

Later:

```text
Backup
   ↓
Restore
   ↓
Recovered database
```

---

# 2. Why Do We Need Backups?

WAL primarily protects PostgreSQL from **physical failures such as crashes**.

But logical problems can also happen.

For example:

```text
Application bug
      ↓
UPDATE users
SET balance = 0;
      ↓
COMMIT;
```

The transaction may be completely valid from PostgreSQL's perspective.

```text
Constraints ✓
Transaction ✓
WAL ✓
COMMIT ✓
```

But the business data is wrong.

WAL faithfully records the change.

A backup gives us a way to recover from situations where the database's logical state itself has become bad.

---

# 3. Backup Is Not Automatically a "Known-Good" Point

This is important.

Suppose the database already contains bad data:

```text
Database
   ↓
bad data
   ↓
Backup
```

Then:

```text
Backup
   ↓
Restore
   ↓
bad data
```

The backup preserves the state that existed when it was created.

Therefore, recovery usually relies on a **known-good backup** and, when configured, WAL history.

---

# 4. What Does Restore Mean?

Restore means:

> **Reconstructing database state from a backup.**

Suppose the original database is:

```text
users

id | name | balance
-------------------
1  | A    | 500
2  | B    | 900
```

A backup is created.

Later:

```text
id | name | balance
-------------------
1  | A    | 0
2  | B    | 0
```

We can restore from the earlier backup:

```text
Backup
   ↓
Restore
   ↓
users

id | name | balance
-------------------
1  | A    | 500
2  | B    | 900
```

The restored database is reconstructed from the saved backup state.

---

# 5. Restore Does Not Necessarily Mean "Fix the Existing Database"

A useful mental model is:

```text
Broken database
      X

Backup
  ↓
Restore
  ↓
Recovered database
```

The recovered database can then be verified before the application is pointed at it.

The exact operational procedure depends on the backup/recovery setup.

---

# 6. Backup vs WAL

These solve different problems.

```text
Backup
   =
recoverable starting state

WAL
   =
record of database changes
```

For example:

```text
Monday
   ↓
Backup
   ↓
Tuesday
   ↓
transactions
   ↓
Wednesday
   ↓
more transactions
```

The backup gives us a starting point.

WAL can contain the changes that happened after that backup.

---

# 7. Backup + WAL

Conceptually:

```text
Backup
   +
WAL history
   ↓
Recovery
```

This allows PostgreSQL to potentially reconstruct the database to a particular point in time.

This is the foundation of:

> **Point-in-Time Recovery (PITR)**

---

# 8. Point-in-Time Recovery

Imagine:

```text
10:00 ── database is good
         ↑
       backup

11:00 ── buggy deployment

11:05 ── bad UPDATE

11:30 ── problem discovered
```

We don't necessarily want to recover to 11:30 because that could include the bad changes.

Instead, we may want:

```text
Backup
   ↓
WAL
   ↓
Replay changes
   ↓
Stop at 10:59
   ↓
Recovered database
```

Conceptually:

```text
GOOD STATE
   ↓
Backup
   ↓
changes
   ↓
changes
   ↓
BAD CHANGE
   ↓
STOP RECOVERY HERE
```

This is why the combination of **backup + WAL** is powerful.

---

# 9. Backup Does Not Prevent Bad Data

Backups are a **recovery mechanism**, not a validation mechanism.

Prevention:

```text
Constraints
Transactions
Locks
Application validation
```

Recovery:

```text
Backup
WAL
Restore
Point-in-Time Recovery
```

Think:

```text
          DATABASE SAFETY
                │
       ┌────────┴────────┐
       ↓                 ↓
   Prevention          Recovery
       │                 │
       ↓                 ↓
 Constraints          Backup
 Transactions         WAL
 MVCC                 Restore
 Locks                PITR
```

---

# 10. Crash Recovery vs Restore

These are different.

## Crash Recovery

PostgreSQL crashes:

```text
Database
   ↓
Server crashes
   ↓
PostgreSQL restarts
   ↓
WAL recovery
   ↓
Database becomes consistent
```

This happens as part of PostgreSQL's normal crash-recovery mechanism.

---

## Restore

You deliberately recover/rebuild database state:

```text
Backup
   ↓
Restore
   ↓
Recovered database
```

This can be needed because of:

* accidental data deletion
* bad application deployment
* incorrect bulk update
* corrupted/lost infrastructure
* other serious operational failures

---

# 11. The Most Important Distinction

Don't think:

```text
WAL = backup
```

Instead:

```text
Backup
    ↓
"I have a recoverable database state."

WAL
    ↓
"I have the history of changes needed for recovery."
```

Together:

```text
Backup
   +
WAL
   ↓
Recover database
to a desired point in time
```

---

# 12. Final Mental Model

The full PostgreSQL safety model we've learned:

```text
Constraints
    ↓
Prevent invalid states


Transactions / MVCC / Locks
    ↓
Control concurrent changes


WAL
    ↓
Protect durability during crashes


Backup
    ↓
Provide a recoverable database state


Restore
    ↓
Reconstruct database from backup


Backup + WAL
    ↓
Potential Point-in-Time Recovery
```

The key sentence to remember:

> **A backup gives you a recoverable starting state; restore reconstructs a database from that state; WAL can provide the changes after the backup, allowing recovery toward a specific point in time.**
