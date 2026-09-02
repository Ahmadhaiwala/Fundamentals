# Schema Challenge #8 — Social Media Platform

## Objective

Design a relational database schema for a small social media platform.

The goal is to practice:

* Many-to-many relationships
* Self-referencing relationships
* Recursive relationships
* Relationship attributes
* Constraints
* Deletion behavior
* Historical/event data
* Designing around actual business requirements

---

# Requirements

## 1. Users

Each user has:

* `user_id`
* `name`
* `username`
* `email`

Rules:

* `username` must be unique.
* `email` must be unique.

Relationship:

```text
User 1 ──── N Post
```

---

# 2. Posts

A user can create many posts.

Each post contains:

* `post_id`
* `user_id`
* `content`
* `created_at`
* `deleted_at`

A post can be deleted.

A deleted post must not accidentally become associated with another post's likes, comments, etc.

---

# 3. Following

A user can follow many other users.

A user can also be followed by many users.

Rules:

* A user cannot follow themselves.
* The same user cannot follow another user twice.

This is a self-referencing many-to-many relationship.

```text
User
 ├── follows ──> User
 ├── follows ──> User
 └── follows ──> User
```

Recommended table:

```text
Follow
------
follower_id
following_id
followed_at
```

Primary key:

```text
(follower_id, following_id)
```

Constraints:

```text
follower_id != following_id
```

---

# 4. Likes

Users can like posts.

Rules:

* A user can like many posts.
* A post can have many likes.
* A user cannot like the same post twice.

This is a many-to-many relationship:

```text
User N ──── M Post
```

Recommended table:

```text
PostLike
--------
user_id
post_id
liked_at
```

Primary key:

```text
(user_id, post_id)
```

---

# 5. Comments

Users can comment on posts.

Each comment contains:

* `comment_id`
* `post_id`
* `user_id`
* `content`
* `created_at`

Relationships:

```text
User 1 ──── N Comment

Post 1 ──── N Comment
```

---

# 6. Comment Replies

Users can reply to comments.

Replies can themselves have replies.

Example:

```text
Post
 │
 └── Comment A
      ├── Reply B
      │    └── Reply C
      │
      └── Reply D
```

There is no fixed maximum depth.

Therefore, the `Comment` table should reference itself:

```text
Comment
-------
comment_id PK
post_id FK
user_id FK
parent_comment_id FK → Comment.comment_id
content
created_at
```

For a top-level comment:

```text
parent_comment_id = NULL
```

For a reply:

```text
parent_comment_id = another comment_id
```

This creates a recursive relationship:

```text
Comment 1 ──── N Comment
```

---

# 7. Post Sharing

A user can share another user's post.

The system needs to know:

* Who shared the post
* Which post was shared
* When it was shared

Recommended table:

```text
PostShare
---------
share_id
user_id
post_id
shared_at
```

Relationships:

```text
User 1 ──── N PostShare

Post 1 ──── N PostShare
```

---

# Final Schema

## User

```text
User
----
user_id PK
name
username UNIQUE
email UNIQUE
```

---

## Post

```text
Post
----
post_id PK
user_id FK → User.user_id
content
created_at
deleted_at
```

`deleted_at = NULL` means the post is active.

A timestamp can also preserve when deletion occurred.

---

## Follow

```text
Follow
------
follower_id FK → User.user_id
following_id FK → User.user_id
followed_at

PK (follower_id, following_id)
```

Constraints:

```text
follower_id != following_id
```

This prevents:

```text
User A → User A
```

and the composite primary key prevents:

```text
User A → User B
User A → User B
```

---

## PostLike

```text
PostLike
--------
user_id FK → User.user_id
post_id FK → Post.post_id
liked_at

PK (user_id, post_id)
```

The composite key prevents duplicate likes.

---

## Comment

```text
Comment
-------
comment_id PK
post_id FK → Post.post_id
user_id FK → User.user_id
parent_comment_id FK → Comment.comment_id
content
created_at
```

`parent_comment_id` is nullable.

Therefore:

```text
NULL
```

means top-level comment.

While:

```text
parent_comment_id = 15
```

means this comment is a reply to comment `15`.

---

## PostShare

```text
PostShare
---------
share_id PK
user_id FK → User.user_id
post_id FK → Post.post_id
shared_at
```

---

# Relationships

```text
User
 │
 ├──────────────< Post
 │
 ├──────────────< Comment
 │
 ├──────────────< PostLike >────────────── Post
 │
 ├──────────────< PostShare >───────────── Post
 │
 └──── Follow ──────────────────────────── User
                                             │
                                             └── self relationship


Post
 │
 ├──────────────< Comment
 │                  │
 │                  └──── parent_comment_id
 │                           │
 │                           └── Comment
 │
 ├──────────────< PostLike
 │
 └──────────────< PostShare
```

---

# Important Design Decisions

## 1. Following is a table

Although "following" sounds like a relationship rather than an entity, it needs its own row because:

```text
User A follows User B
```

is something the database must store.

It also has an attribute:

```text
followed_at
```

Therefore:

```text
Follow
```

is an associative entity.

---

## 2. Likes need a junction table

Users and posts have an M:N relationship.

```text
User N ───── M Post
```

Therefore:

```text
PostLike
```

is required.

The composite primary key also naturally prevents duplicate likes.

---

## 3. Comments are recursive

A reply is still fundamentally a comment.

Instead of creating:

```text
Comment
Reply
ReplyToReply
ReplyToReplyToReply
```

we use:

```text
parent_comment_id
```

which points back to the same table.

This allows unlimited depth.

---

## 4. Don't store likes as a number on Post

Avoid:

```text
Post
----
post_id
content
like_count
```

as the source of truth.

The actual likes should be stored in:

```text
PostLike
```

The count can be calculated:

```sql
COUNT(*)
```

or maintained separately as a cache if performance eventually requires it.

---

## 5. Don't delete the post ID and reuse it

Suppose:

```text
Post 100
```

gets deleted.

Its likes/comments should never suddenly become associated with a completely new post that happens to receive ID `100`.

Primary keys should therefore be stable and not reused.

Soft deletion using:

```text
deleted_at
```

can also preserve the historical identity of the post.

---

# Core Lessons

The biggest lessons from this challenge are:

### Relationship with attributes → table

```text
Follow
PostLike
PostShare
```

### M:N → junction/associative entity

```text
User ↔ Post
```

becomes:

```text
PostLike
```

### Recursive relationship → self-reference

```text
Comment → Comment
```

using:

```text
parent_comment_id
```

### Historical/event information → store the event

```text
PostShare
followed_at
liked_at
created_at
```

### Constraints are part of schema design

Not just:

```text
PK
FK
```

but also:

```text
UNIQUE
CHECK
NOT NULL
```

and business rules.

---

# Schema Design Checklist

Before considering a schema finished, ask:

1. What does **one row represent**?
2. What are the independent entities?
3. What relationships exist?
4. What is the cardinality?
5. Is anything M:N?
6. Does a relationship have its own attributes?
7. Is anything recursive?
8. What must be unique?
9. What must never happen?
10. What happens when something is deleted?
11. Do I need historical information?
12. Am I storing current state or an event?
13. Am I duplicating information unnecessarily?
14. Can the database itself enforce the important rules?
15. Can every real-world requirement be represented by the schema?

If you can answer these consistently, you have the core schema-design skill needed to start building real applications.
