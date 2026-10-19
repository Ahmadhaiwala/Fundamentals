# PostgreSQL Index Types — Mental Models & Practical Guide

> Understanding **why** PostgreSQL has different index types, not just memorizing their names.

---

## 1. What Is an Index?

An index is a separate data structure that helps PostgreSQL find rows without scanning the entire table.

Without an index:

```text
Query
  ↓
Scan row 1
Scan row 2
Scan row 3
...
Scan row 1,000,000
```

With an appropriate index:

```text
Query
  ↓
Index
  ↓
Find relevant rows
  ↓
Fetch rows
```

The important idea:

> **Indexes optimize specific access patterns.**

An index isn't automatically "better" just because it exists.

Indexes also have costs:

* Additional disk space
* Additional memory/cache usage
* Slower `INSERT`
* Slower `UPDATE` of indexed columns
* Slower `DELETE`
* Maintenance overhead

Therefore:

> **Index based on query patterns, not blindly on columns.**

---

# 2. PostgreSQL Index Access Methods

PostgreSQL supports multiple index types.

The major ones to understand are:

```text
B-tree
Hash
GIN
GiST
BRIN
```

---

# 3. B-tree

## What it means

B-tree = **Balanced Tree**

It maintains data in an ordered structure.

Conceptually:

```text
                [50]
               /    \
            [25]     [75]
           /   \     /   \
        [10] [40] [60] [90]
```

The exact internal implementation is more sophisticated than this diagram, but this is a useful mental model.

## What B-tree is good at

B-tree is the general-purpose index.

It supports operations such as:

```sql
=
<
>
<=
>=
BETWEEN
ORDER BY
```

Example:

```sql
CREATE INDEX idx_users_age
ON users(age);
```

Useful queries:

```sql
SELECT *
FROM users
WHERE age = 20;
```

```sql
SELECT *
FROM users
WHERE age > 20;
```

```sql
SELECT *
FROM users
WHERE age BETWEEN 20 AND 30;
```

```sql
SELECT *
FROM users
ORDER BY age;
```

## Important

B-tree is PostgreSQL's **default index type**.

Therefore:

```sql
CREATE INDEX idx_email
ON users(email);
```

normally means:

```sql
CREATE INDEX idx_email
ON users USING btree(email);
```

You usually don't need to explicitly write `USING btree`.

## Mental model

> **B-tree = ordered general-purpose index**

---

# 4. Hash

Hash indexes use a hashing structure.

The programming analogy is a `HashMap` / dictionary.

Conceptually:

```text
email
  ↓
hash(email)
  ↓
bucket
  ↓
row
```

Hash indexes are primarily useful for **equality comparisons**:

```sql
WHERE email = 'ahmad@example.com'
```

Example:

```sql
CREATE INDEX idx_users_email
ON users USING hash(email);
```

## Limitation

Hash indexes are not designed for ordered operations.

For example:

```sql
WHERE age > 20
```

or:

```sql
ORDER BY age
```

are not what hash indexes are designed for.

B-tree can handle equality **and** ordering/ranges, making B-tree the much more common choice.

## Important misconception

Do NOT think:

```text
Small data → Hash
Medium data → B-tree
Large data → BRIN
```

That's not how index selection works.

Instead:

```text
What operation does my query need?
            ↓
Choose the appropriate index type
```

Hash can be used on large tables too.

## Mental model

> **Hash = fast equality-oriented lookup**

---

# 5. GIN

GIN = **Generalized Inverted Index**

The key idea is an **inverted index**.

Imagine documents:

```text
Post 1 → React, PostgreSQL, Ahmedabad
Post 2 → Python, PostgreSQL, Surat
Post 3 → React, Docker, Ahmedabad
```

GIN can conceptually organize this as:

```text
React       → Post 1, Post 3
PostgreSQL  → Post 1, Post 2
Ahmedabad   → Post 1, Post 3
Python      → Post 2
Docker      → Post 3
```

Instead of:

```text
document → contents
```

we can efficiently answer:

```text
term/value → documents containing it
```

## Common uses

GIN is especially useful for:

### Arrays

```sql
skills text[]
```

Searching for values inside arrays.

### JSONB

```sql
metadata jsonb
```

Searching inside JSONB structures.

### Full-text search

PostgreSQL's text-search functionality can use GIN indexes.

## Important

GIN is **not simply "the text index."**

Its broader idea is:

> **GIN is excellent when one row contains multiple searchable values.**

## Mental model

> **GIN = inverted index for multi-valued/searchable data**

---

# 6. GiST

GiST = **Generalized Search Tree**

GiST is designed for data where normal ordering isn't enough and queries involve more specialized relationships.

One important example is **geospatial data**.

With PostGIS, GiST indexes can support spatial queries.

Imagine:

```text
          Restaurant
              ●

       ┌─────────────┐
       │             │
       │    ● Me     │
       │             │
       └─────────────┘
```

A query might ask:

```text
Find places within 5 km of me.
```

This isn't simply:

```sql
latitude > X
```

It's a spatial relationship.

PostGIS can use GiST indexes for operations such as:

```text
ST_DWithin
ST_Intersects
ST_Contains
```

GiST can also be useful for:

* Geometric data
* Range types
* Spatial relationships
* Specialized operator classes
* Certain nearest-neighbor queries

## Important misconception

GiST is not:

> "The latitude/longitude index."

Rather:

> **GiST is a generalized search structure that is particularly useful for spatial and other specialized data types.**

## Mental model

> **GiST = generalized index for complex relationships**

---

# 7. BRIN

BRIN = **Block Range INdex**

This one is fundamentally different from the others.

The key idea:

> **BRIN stores summaries of ranges of physical table blocks rather than precise entries for every row.**

Imagine a huge table:

```text
100 million rows
```

Suppose rows were inserted mostly in chronological order:

```text
Block 1
Jan 1
Jan 1
Jan 2
Jan 2

Block 2
Jan 2
Jan 3
Jan 3

Block 3
Jan 3
Jan 4
Jan 5

...
```

BRIN can store summaries such as:

```text
Block range     Minimum       Maximum

1–10            Jan 1         Jan 5
11–20           Jan 5         Jan 10
21–30           Jan 10        Jan 15
...
```

Now suppose:

```sql
SELECT *
FROM events
WHERE created_at = '2026-09-01';
```

PostgreSQL can inspect the BRIN summaries:

```text
Block 1–10       Jan 1–5       ❌
Block 11–20      Jan 5–10      ❌
...
Block 900–910    Aug 29–Sep 3  ✅
```

It can then inspect those relevant blocks.

---

# 8. Why BRIN Is So Small

A B-tree may maintain index information at a much more granular level.

BRIN instead summarizes ranges:

```text
Rows
 ↓
Blocks
 ↓
Block ranges
 ↓
Summary
```

Therefore a BRIN index can be **extremely small** compared with a B-tree for a huge table.

The tradeoff:

```text
B-tree
→ precise

BRIN
→ approximate/block-level
```

BRIN helps PostgreSQL identify **where it is worth looking**, after which PostgreSQL may scan the relevant blocks.

## When BRIN shines

BRIN works particularly well when:

1. The table is very large.
2. The indexed column has a strong correlation with physical row order.

Classic example:

```sql
created_at
```

when rows are mostly inserted chronologically.

## Mental model

> **BRIN = cheap summaries of physical regions of a huge table**

---

# 9. Comparing the Major Index Types

| Index  | Main idea               | Good for                                   |
| ------ | ----------------------- | ------------------------------------------ |
| B-tree | Ordered tree            | Equality, ranges, sorting                  |
| Hash   | Hash buckets            | Equality                                   |
| GIN    | Inverted index          | JSONB, arrays, full-text                   |
| GiST   | Generalized search tree | Spatial, ranges, specialized relationships |
| BRIN   | Block-range summaries   | Huge naturally ordered tables              |

---

# 10. The Most Important Mental Model

Do NOT think:

```text
Small data
    ↓
Hash

Medium data
    ↓
B-tree

Large data
    ↓
BRIN
```

Instead think:

```text
                     What does my query need?
                              │
             ┌────────────────┼────────────────┐
             │                │                │
          Equality         Ordering       Multi-valued /
             │             / ranges          search
             │                │                │
           Hash            B-tree             GIN
             │
             │
             └──────────── B-tree can
                         also handle =


                  Specialized relationships
                           │
                          GiST


                  Huge + physically ordered
                           │
                          BRIN
```

The **query workload** determines the index strategy.

---

# 11. Examples From a Real Application

Suppose NeedNow has:

```sql
users
requests
services
```

## Normal user lookup

```sql
SELECT *
FROM users
WHERE email = 'user@example.com';
```

Likely:

```text
B-tree
```

---

## Find recent requests

```sql
SELECT *
FROM requests
WHERE created_at >= now() - interval '7 days'
ORDER BY created_at DESC;
```

Likely:

```text
B-tree
```

---

## Search JSONB metadata

```sql
SELECT *
FROM services
WHERE metadata @> '{"category": "plumbing"}';
```

Potentially:

```text
GIN
```

---

## Search array contents

```sql
SELECT *
FROM services
WHERE skills @> ARRAY['plumbing'];
```

Potentially:

```text
GIN
```

---

## Find nearby providers

With PostGIS:

```text
Find service providers within 5 km
```

Potentially:

```text
GiST
```

---

## Massive event table

Imagine:

```text
500 million events
```

with:

```sql
created_at
```

mostly increasing with insertion order.

Potentially:

```text
BRIN
```

---

# 12. Indexes Are Not Free

Every index introduces cost.

If you have:

```text
users
 ├── email index
 ├── created_at index
 ├── name index
 ├── phone index
 └── status index
```

then inserting a user requires PostgreSQL to maintain those indexes too.

Conceptually:

```text
INSERT user
     │
     ├── update table
     ├── update email index
     ├── update created_at index
     ├── update name index
     ├── update phone index
     └── update status index
```

Therefore:

> **Don't index everything.**

Indexes should exist because they support meaningful query patterns.

---

# 13. Production-Level Thinking

When designing a database, don't ask:

> "Which columns should I index?"

Ask:

> "What queries will my application execute frequently?"

Then consider:

```text
1. What does the query filter by?
2. What operators does it use?
3. Does it need ordering?
4. Does it search inside JSONB/arrays?
5. Is the data spatial?
6. Is the table enormous?
7. Is the indexed value correlated with physical row order?
8. What is the read/write tradeoff?
```

---

# 14. Final Mental Cheat Sheet

```text
B-tree
    ↓
Default / general purpose
=, <, >, <=, >=
BETWEEN
ORDER BY


Hash
    ↓
Equality-focused
=


GIN
    ↓
Inverted index
JSONB
Arrays
Full-text search


GiST
    ↓
Generalized relationships
Spatial
Ranges
Specialized operators


BRIN
    ↓
Huge tables
Physical block summaries
Best when data correlates with physical row order
```

---

## The Core Lesson

> **Index types are different data structures optimized for different query patterns.**

The goal of database engineering isn't:

```text
"I know all five index types."
```

It's:

```text
"I understand my workload well enough
to choose the right index."
```

That distinction is where **SQL knowledge starts turning into database engineering knowledge.**
