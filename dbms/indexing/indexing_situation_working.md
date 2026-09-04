# PostgreSQL Indexing — Complete Notes

> **Goal:** Understand indexing like PostgreSQL itself — not just memorize `CREATE INDEX`, but understand **what happens physically when a query runs and when data changes**.

---

## 1. The Big Picture

When we run:

```sql
SELECT *
FROM orders
WHERE user_id = 5000;
```

PostgreSQL has to find the rows where `user_id = 5000`.

Without an index, PostgreSQL can essentially do:

```text
Table (Heap)
   ↓
Page 1 → check rows
Page 2 → check rows
Page 3 → check rows
...
Page N → check rows
```

This is a:

```text
Sequential Scan
```

With an index:

```text
              Index
                ↓
        "user_id = 5000"
                ↓
        matching row locations
                ↓
             Heap
                ↓
        actual table rows
```

The key mental model:

> **Index = a separate structure that helps PostgreSQL locate rows in the heap.**

The index generally does **not contain the complete table row**.

---

# 2. Heap

The **heap** is where PostgreSQL stores the actual table rows.

Think:

```text
orders table
     ↓
   HEAP
     ↓
┌──────────────┐
│ Page 1       │
│ rows...      │
├──────────────┤
│ Page 2       │
│ rows...      │
├──────────────┤
│ Page 3       │
│ rows...      │
├──────────────┤
│ ...          │
└──────────────┘
```

PostgreSQL works with fixed-size database pages/blocks, commonly **8 KB**.

So conceptually:

```text
row
 ↓
page
 ↓
heap
```

The word **heap here is NOT the DSA heap data structure**.

---

# 3. Buffers

PostgreSQL doesn't constantly work directly with disk.

It loads database pages into its shared memory area:

```text
Disk
 ↓
PostgreSQL Shared Buffers
 ↓
CPU processes the page
```

A **buffer** is essentially a memory slot containing a database page PostgreSQL is working with.

For example:

```text
shared hit = 6805
```

means PostgreSQL needed 6805 pages that were **already in shared buffers**.

While:

```text
shared read = 6805
```

means PostgreSQL had to fetch those pages into memory from storage.

### Mental model

```text
Disk
  │
  │ page needed
  ↓
Shared Buffers
  │
  ↓
CPU
```

---

# 4. Sequential Scan

Suppose we have:

```sql
SELECT *
FROM orders
WHERE user_id = 5000;
```

and there is no useful index.

PostgreSQL can do:

```text
Sequential Scan
       ↓
Page 1
       ↓
Page 2
       ↓
Page 3
       ↓
...
       ↓
Page N
```

It checks the rows looking for:

```text
user_id = 5000
```

If the table has 1 million rows, potentially a huge amount of data has to be examined.

---

# 5. Creating an Index

Example:

```sql
CREATE INDEX idx_orders_user_id
ON orders(user_id);
```

Now PostgreSQL has:

```text
orders heap
     │
     │ actual rows
     │
     ↓
  HEAP


idx_orders_user_id
     │
     │ helps locate rows
     ↓
   INDEX
```

The index is a **separate database structure**.

---

# 6. Index Does NOT Automatically Mean Faster

This is extremely important.

Creating an index does **not** mean:

> "PostgreSQL will always use it."

Instead:

```text
Query
  ↓
Planner
  ↓
"What execution strategy is cheapest?"
  ↓
┌───────────────────┐
│ Sequential Scan   │
│ Index Scan        │
│ Bitmap Scan       │
│ ...               │
└───────────────────┘
  ↓
Chosen plan
```

PostgreSQL estimates the cost of different strategies and chooses one.

---

# 7. EXPLAIN

We can see PostgreSQL's planned strategy using:

```sql
EXPLAIN
SELECT *
FROM orders
WHERE user_id = 5000;
```

Important concepts:

```text
cost
rows
width
```

### `cost`

Example:

```text
cost=0.00..123.45
```

These are **planner cost units**, not milliseconds.

They represent PostgreSQL's estimate of how expensive the operation will be.

---

### `rows`

Example:

```text
rows=100
```

This means PostgreSQL estimates approximately 100 rows will be returned.

It is an **estimate**, not the actual result.

---

### `width`

Example:

```text
width=40
```

This is PostgreSQL's estimate of the average size of each output row.

---

# 8. EXPLAIN ANALYZE

To see what actually happened:

```sql
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE user_id = 5000;
```

Now PostgreSQL actually executes the query and shows things like:

```text
rows=...
actual time=...
```

So we can compare:

```text
Planner's prediction
        VS
Reality
```

Example:

```text
estimated rows = 100
actual rows    = 102
```

Great estimate.

But:

```text
estimated rows = 100
actual rows    = 100,000
```

Huge estimation error.

---

# 9. PostgreSQL Statistics

The planner needs information about the data to make good decisions.

PostgreSQL maintains statistics about columns.

For example:

```sql
SELECT *
FROM pg_stats
WHERE tablename = 'orders'
  AND attname = 'user_id';
```

Statistics can tell PostgreSQL things such as:

```text
How many distinct values exist?
Which values are common?
How frequently do they occur?
What does the distribution look like?
```

These statistics help answer:

> "If I search for `user_id = 5000`, approximately how many rows will I get?"

---

# 10. Why Statistics Matter

Suppose PostgreSQL believes:

```text
user_id = 5000
→ approximately 100 rows
```

It might choose an index-based strategy.

But suppose reality is:

```text
user_id = 5000
→ 100,000 rows
```

Now the planner's assumptions were very wrong.

That matters because:

```text
Statistics
    ↓
Row-count estimate
    ↓
Cost estimate
    ↓
Execution plan
    ↓
Actual performance
```

So statistics don't directly make the query faster.

They help PostgreSQL **choose the right strategy**.

---

# 11. Stale Statistics

We demonstrated how statistics can become inaccurate.

Initially, suppose the data is roughly:

```text
1,000,000 rows
10,000 user IDs
```

So PostgreSQL may estimate:

```text
user_id = 5000
≈ 100 rows
```

Then we inserted:

```sql
INSERT INTO orders (user_id, amount)
SELECT
    5000,
    (random() * 1000)::numeric(10,2)
FROM generate_series(1, 100000);
```

Now a huge number of new rows have:

```text
user_id = 5000
```

But if statistics haven't been refreshed yet, PostgreSQL can still believe:

```text
user_id = 5000
≈ 100 rows
```

while reality is:

```text
≈ 100,000 rows
```

This produced a huge estimation error.

### Important chain

```text
Data changes
     ↓
Statistics don't instantly know everything
     ↓
Planner uses available statistics
     ↓
Estimate may be wrong
     ↓
Potentially wrong execution plan
     ↓
Potential performance problem
```

Eventually `ANALYZE` / autovacuum mechanisms can refresh statistics.

---

# 12. Bitmap Scan

One important plan we encountered was:

```text
Bitmap Heap Scan
        ↓
Bitmap Index Scan
```

This looks complicated initially, but the idea is simple.

Suppose:

```sql
SELECT *
FROM orders
WHERE user_id = 5000;
```

PostgreSQL can first use the index:

```text
Bitmap Index Scan
       ↓
Find locations of matching rows
```

Then:

```text
Bitmap Heap Scan
       ↓
Go to the actual heap pages
       ↓
Retrieve the rows
```

Conceptually:

```text
             INDEX
               ↓
       matching row locations
               ↓
          group by pages
               ↓
             HEAP
               ↓
       retrieve actual rows
```

---

# 13. What Is a TID?

An index needs some way to tell PostgreSQL:

> "The row you're looking for is over there."

PostgreSQL internally uses a **tuple identifier (TID)** to identify a row location in the table.

Conceptually:

```text
Index
 ↓
(user_id = 5000)
 ↓
"row is around this heap location"
 ↓
Heap
 ↓
actual row
```

The exact internal representation is more detailed, but the important mental model is:

> **The index helps PostgreSQL locate the actual tuple in the heap.**

---

# 14. `Recheck Cond`

You may see:

```text
Recheck Cond: (user_id = 5000)
```

under a Bitmap Heap Scan.

This is normal.

The bitmap can sometimes represent pages **lossily** rather than storing every exact tuple location.

So PostgreSQL may need to visit the heap page and check:

```text
Does this row actually satisfy user_id = 5000?
```

Hence:

```text
Recheck Cond
```

Don't interpret it as:

> "Something went wrong."

It is part of how bitmap scans can work.

---

# 15. Heap Blocks

You may see:

```text
Heap Blocks: exact=731
```

This tells us how many heap pages were accessed using exact bitmap information.

Remember:

```text
Heap
 ↓
Pages
 ↓
Rows
```

So:

```text
Heap Blocks = 731
```

roughly means PostgreSQL needed 731 table pages for that part of the operation.

---

# 16. Why Sequential Scan Can Beat an Index

Imagine:

```text
Table = 1,000,000 rows
```

Query:

```sql
SELECT *
FROM orders;
```

We need **every row**.

Using the index would be pointless:

```text
Index
 ↓
find row
 ↓
go heap
 ↓
find row
 ↓
go heap
 ↓
...
```

Instead:

```text
Sequential Scan
 ↓
read heap pages in order
 ↓
process all rows
```

is much more sensible.

### Core principle

> **Indexes are useful when they allow PostgreSQL to avoid substantial unnecessary work.**

Not:

> "Index = always faster."

---

# 17. Cache Effect

We ran a query once and saw something like:

```text
shared read = 6805
```

Then ran it again and saw:

```text
shared hit = 6805
```

Why?

First run:

```text
Storage
 ↓
Shared Buffers
 ↓
Query
```

Second run:

```text
Shared Buffers
 ↓
Query
```

The required pages were already in memory.

Therefore:

```text
shared read
```

and

```text
shared hit
```

are useful for understanding where the data came from.

### Important

Index usage and caching are **different concepts**.

You can have:

```text
Index + cache
Index + storage reads
Sequential scan + cache
Sequential scan + storage reads
```

They are separate dimensions.

---

# 18. Composite Indexes

Now suppose our query is:

```sql
SELECT *
FROM orders
WHERE user_id = 5000
  AND status = 'paid';
```

We can create:

```sql
CREATE INDEX idx_orders_user_status
ON orders(user_id, status);
```

This is a **composite index**.

It indexes multiple columns together.

Conceptually:

```text
(user_id, status)
```

rather than:

```text
user_id
```

alone.

---

# 19. Column Order Matters

This is extremely important.

Suppose:

```sql
CREATE INDEX idx_orders_user_status
ON orders(user_id, status);
```

Think of it roughly as being organized by:

```text
user_id
    ↓
status
```

So queries involving:

```text
user_id
```

are naturally aligned with the beginning of the index.

For example:

```sql
WHERE user_id = 5000
```

is a natural use case.

And:

```sql
WHERE user_id = 5000
  AND status = 'paid'
```

is even more aligned.

But:

```sql
WHERE status = 'paid'
```

doesn't have the same direct advantage because the index starts with:

```text
user_id
```

### Mental model

For:

```text
INDEX(user_id, status)
```

think:

```text
user_id
   └── status
```

not:

```text
status
   └── user_id
```

The ordering of columns in a composite index is therefore a **query-design decision**.

---

# 20. Index Maintenance

This is one of the most important production concepts.

Suppose we have:

```text
orders table
     +
idx_user_id
     +
idx_user_status
     +
idx_amount
```

Now we execute:

```sql
INSERT INTO orders (...);
```

PostgreSQL doesn't just update the table.

It also has to maintain the relevant indexes.

Conceptually:

```text
INSERT
  │
  ├──→ Heap
  │
  ├──→ Index 1
  │
  ├──→ Index 2
  │
  └──→ Index 3
```

So yes:

> **When table data changes, indexes can also change.**

---

# 21. INSERT Cost

Suppose a table has:

```text
0 indexes
```

An insert primarily needs to modify the table storage.

With:

```text
5 indexes
```

the insert has additional index-maintenance work.

Conceptually:

```text
INSERT
 ↓
heap modification
 ↓
index 1 modification
 ↓
index 2 modification
 ↓
index 3 modification
 ↓
...
```

Therefore:

```text
More indexes
    ↓
More write work
    ↓
Potentially slower INSERT/UPDATE/DELETE
    ↓
More storage
```

---

# 22. UPDATE Cost

Suppose we have:

```sql
CREATE INDEX idx_orders_user_id
ON orders(user_id);
```

and execute:

```sql
UPDATE orders
SET user_id = 7000
WHERE id = 123;
```

The indexed value changed.

Therefore PostgreSQL has additional index-maintenance work.

Conceptually:

```text
Old row
 user_id = 5000
      ↓
UPDATE
      ↓
New row/version
 user_id = 7000

Index must reflect the change
```

This becomes even more interesting when PostgreSQL's **MVCC** behavior is considered.

That is why index maintenance naturally leads into:

> **MVCC + VACUUM**

---

# 23. DELETE Cost

Similarly:

```sql
DELETE FROM orders
WHERE id = 123;
```

affects the table and the associated index structures.

The important production idea isn't memorizing every internal operation.

It's understanding:

```text
Indexes aren't free.
```

They provide:

```text
Faster reads
```

but cost:

```text
Write work
Storage
Maintenance
```

---

# 24. The Index Tradeoff

The complete mental model:

```text
              INDEX
                │
        ┌───────┴────────┐
        ↓                ↓
      READ              WRITE
        │                │
        ↓                ↓
   potentially        additional
   much faster        maintenance
                         │
                         ↓
                    extra storage
```

So production database design isn't:

> "Add indexes everywhere."

It's:

> **Add indexes that are justified by real query patterns.**

---

# 25. The Production Question

Instead of asking:

> "How many indexes should my table have?"

Ask:

```text
What queries run frequently?
        ↓
What filters / joins / ordering do they use?
        ↓
Can an index reduce the work?
        ↓
How often does the table change?
        ↓
Is the read improvement worth the write/storage cost?
```

That's much closer to real backend/database engineering.

---

# 26. Our PostgreSQL Mental Model So Far

At this point, we have built this chain:

```text
                    SQL Query
                        │
                        ↓
                    PostgreSQL
                        │
                        ↓
                     Planner
                        │
             ┌──────────┴──────────┐
             ↓                     ↓
        Statistics             Available
             │                  Indexes
             └──────────┬──────────┘
                        ↓
                  Choose a Plan
                        │
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
       Seq Scan      Index Scan   Bitmap Scan
                                      │
                                      ↓
                                Bitmap Index
                                      │
                                      ↓
                                   Heap
                                      │
                                      ↓
                                   Pages
                                      │
                                      ↓
                                   Buffers
                                      │
                                      ↓
                                  Actual Rows
```

And when data changes:

```text
INSERT / UPDATE / DELETE
          │
          ├────────→ Heap changes
          │
          └────────→ Relevant indexes change
                         │
                         ↓
                    write overhead
```

---

# 27. Experiments We Completed

### Table

```sql
CREATE TABLE orders (
    id BIGSERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    amount NUMERIC(10,2) NOT NULL
);
```

### Large dataset

```sql
INSERT INTO orders (user_id, amount)
SELECT
    (random() * 10000)::int,
    (random() * 1000)::numeric(10,2)
FROM generate_series(1, 1000000);
```

### Basic query

```sql
SELECT *
FROM orders
WHERE user_id = 5000;
```

### Index

```sql
CREATE INDEX idx_orders_user_id
ON orders(user_id);
```

### Execution inspection

```sql
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE user_id = 5000;
```

### Buffer inspection

```sql
EXPLAIN (ANALYZE, BUFFERS)
SELECT *
FROM orders
WHERE user_id = 5000;
```

### Statistics inspection

```sql
SELECT *
FROM pg_stats
WHERE tablename = 'orders'
  AND attname = 'user_id';
```

### Deliberately stale statistics

```sql
INSERT INTO orders (user_id, amount)
SELECT
    5000,
    (random() * 1000)::numeric(10,2)
FROM generate_series(1, 100000);
```

Then:

```sql
EXPLAIN ANALYZE
SELECT *
FROM orders
WHERE user_id = 5000;
```

This demonstrated how:

```text
estimated rows ≠ actual rows
```

can become dramatically different.

---

# 28. What You Should Remember

Don't memorize 50 definitions.

Remember these **core mental models**:

### 1. Heap

```text
Heap = actual table data
```

### 2. Index

```text
Index = structure that helps locate table rows
```

### 3. Buffer

```text
Buffer = memory holding database pages
```

### 4. Planner

```text
Planner = chooses how PostgreSQL should execute the query
```

### 5. Statistics

```text
Statistics = planner's information about the data
```

### 6. EXPLAIN

```text
EXPLAIN = what PostgreSQL plans to do
```

### 7. EXPLAIN ANALYZE

```text
EXPLAIN ANALYZE = execute it + show what actually happened
```

### 8. Index ≠ automatically faster

```text
Index exists
    ↓
Planner evaluates it
    ↓
May use it
    ↓
May reject it
```

### 9. Indexes have a cost

```text
Indexes
 ↓
faster reads
 +
slower writes
 +
more storage
```

### 10. The ultimate mental model

```text
Query
 ↓
Planner
 ↓
Statistics + Cost
 ↓
Execution Plan
 ↓
Pages
 ↓
Buffers
 ↓
Heap
 ↓
Rows
```

---

# 29. Status: Indexing ✅

We have covered the important **behavioral foundation of PostgreSQL indexing**:

* [x] Heap
* [x] Pages / blocks
* [x] Shared buffers
* [x] Sequential scans
* [x] Indexes
* [x] Index vs heap
* [x] TID / row location concept
* [x] Index scans
* [x] Bitmap index scans
* [x] Bitmap heap scans
* [x] `Recheck Cond`
* [x] `EXPLAIN`
* [x] `EXPLAIN ANALYZE`
* [x] Planner cost
* [x] Row estimates
* [x] PostgreSQL statistics
* [x] Stale statistics
* [x] Cache effects
* [x] Composite indexes
* [x] Composite index column ordering
* [x] Index maintenance
* [x] INSERT/UPDATE/DELETE write overhead
* [x] Read-vs-write index tradeoff

## Next Level 2 Topic

🔥 **MVCC — Multi-Version Concurrency Control**

This is where PostgreSQL starts getting *really* interesting:

```text
UPDATE row
   ↓
Does PostgreSQL overwrite the old row?
   ↓
What happens when another transaction is reading it?
   ↓
Why can two users see different versions?
   ↓
Why does UPDATE sometimes create extra row versions?
   ↓
Why do we need VACUUM?
```

That will connect directly to the index-maintenance question you just asked.
