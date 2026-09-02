# Banking System — Database Schema Design

## Problem Statement

Design a basic banking database system that supports customers, bank accounts, beneficiaries, transactions, and money transfers.

The goal is to model the system based on the business requirements rather than starting with normalization rules.

---

# Requirements

## 1. Customers

A customer can have multiple bank accounts.

Store:

* Customer ID
* Name
* Email
* Phone
* Address

---

## 2. Accounts

Each customer can have one or more bank accounts.

Each account has:

* Account ID
* Account number
* Account type
* Current balance
* Customer who owns the account

Account types:

```text
savings
current
```

---

## 3. Beneficiaries

A customer can save beneficiaries for frequently used transfers.

A beneficiary has:

* Beneficiary ID
* Name
* Bank account number
* Customer who added the beneficiary

A beneficiary does **not necessarily have to be a customer of this bank**.

---

## 4. Transactions

An account can have many transactions.

A transaction can be:

```text
deposit
withdrawal
transfer
```

Each transaction stores:

* Transaction ID
* Account
* Type
* Amount
* Timestamp
* Status

Possible statuses:

```text
pending
completed
failed
```

---

## 5. Transfers

A customer can transfer money from one bank account to another.

The system must know:

* Source account
* Destination account
* Transaction associated with the transfer

The destination account may belong to a completely different customer.

---

## 6. Historical Accuracy

Completed financial records must remain historically accurate.

For example, if a transfer was completed for `$500`, that amount must remain `$500` even if pricing or account information changes later.

A foreign key such as `customer_id` gives access to the customer's **current** information. It does not automatically preserve what that customer's information looked like when the transaction occurred.

If historical customer information itself is required, appropriate snapshot fields or history tables would need to be introduced.

---

## 7. Important Business Rules

* Transaction amount must be greater than `0`.
* Account balance must never become negative.
* Account numbers must be unique.
* A transaction must belong to an account.
* A transfer must have both a source and destination account.
* A source account should not be the same as its destination account.
* Transaction status must be valid.
* Account type must be valid.

---

# Final Schema

## Customer

```text
Customer
--------
customer_id PK
name
email
phone
address
```

---

## Account

```text
Account
-------
account_id PK
account_number UNIQUE
account_type
balance
customer_id FK → Customer.customer_id
```

### Relationship

```text
Customer 1 ───── N Account
```

One customer can own multiple accounts.

---

## Beneficiary

```text
Beneficiary
-----------
beneficiary_id PK
customer_id FK → Customer.customer_id
name
bank_account_number
```

### Relationship

```text
Customer 1 ───── N Beneficiary
```

A customer can save multiple beneficiaries.

The beneficiary is represented using a bank account number rather than a `customer_id` because the beneficiary may not be a customer of this bank.

---

## Transaction

```text
Transaction
-----------
transaction_id PK
account_id FK → Account.account_id
type
amount
timestamp
status
```

### Relationship

```text
Account 1 ───── N Transaction
```

An account can have many transactions.

---

## Transfer

```text
Transfer
--------
transfer_id PK
transaction_id FK → Transaction.transaction_id
source_account_id FK → Account.account_id
destination_account_id FK → Account.account_id
```

### Relationships

```text
Account 1 ───── N Transfer
          source

Account 1 ───── N Transfer
          destination
```

The same `Account` entity participates in the relationship twice:

```text
source_account_id
destination_account_id
```

---

# Complete Schema

```text
Customer
--------
customer_id PK
name
email
phone
address


Account
-------
account_id PK
account_number UNIQUE
account_type
balance
customer_id FK


Beneficiary
-----------
beneficiary_id PK
customer_id FK
name
bank_account_number


Transaction
-----------
transaction_id PK
account_id FK
type
amount
timestamp
status


Transfer
--------
transfer_id PK
transaction_id FK
source_account_id FK
destination_account_id FK
```

---

# Entity Relationships

```text
Customer
   │
   ├─────────────── 1:N ──────────────> Account
   │
   └─────────────── 1:N ──────────────> Beneficiary


Account
   │
   └─────────────── 1:N ──────────────> Transaction


Account
   │
   ├─────────────── 1:N ──────────────> Transfer (source)
   │
   └─────────────── 1:N ──────────────> Transfer (destination)
```

---

# Important Design Decisions

## 1. Why isn't Beneficiary connected to another Customer?

A first instinct might be:

```text
Beneficiary
-----------
beneficiary_id
host_customer_id
beneficiary_customer_id
```

This assumes every beneficiary is a customer in our banking system.

That assumption is not in the requirements.

Instead:

```text
Beneficiary
-----------
beneficiary_id
customer_id
name
bank_account_number
```

This allows the beneficiary to belong to another bank.

---

## 2. Why does Transfer use accounts instead of customers?

Money moves between **accounts**, not directly between customers.

Incorrect:

```text
Customer A → Customer B
```

Correct:

```text
Account A → Account B
```

This matters because one customer can own multiple accounts.

For example:

```text
Customer A
   │
   ├── Savings Account
   └── Current Account
```

A transfer needs to identify exactly which account sends and receives the money.

---

## 3. Why is DriverAssignment-like modeling useful here?

A transfer represents a meaningful financial event.

It contains information about:

```text
source account
destination account
transaction
```

Therefore, it is more than just a simple foreign-key relationship between two accounts.

---

## 4. Current Data vs Historical Data

Suppose:

```text
Customer
customer_id = 10
name = Ahmad
```

A transaction occurs.

Later:

```text
name = Ahmad Haiwala
```

Querying:

```text
Transaction → Account → Customer
```

will return the customer's **current name**.

It will not tell you what the name was when the transaction happened.

Therefore:

> A foreign key preserves identity, not historical state.

If the business requires historical snapshots, additional fields/history tables are required.

---

# Important Constraints

### Account

```text
account_number UNIQUE

account_type IN ('savings', 'current')

balance >= 0
```

### Transaction

```text
amount > 0

type IN ('deposit', 'withdrawal', 'transfer')

status IN ('pending', 'completed', 'failed')
```

### Transfer

```text
source_account_id != destination_account_id
```

A transfer must have both:

```text
source_account_id
destination_account_id
```

---

# Core Schema-Design Lessons

### 1. Money moves between accounts, not customers.

### 2. A foreign key does not preserve historical values.

### 3. Don't assume every referenced person is another entity in your system.

### 4. Separate concepts when they represent different facts.

```text
Transaction ≠ Transfer
Account ≠ Customer
Beneficiary ≠ Customer
```

### 5. Ask what a row actually represents.

For example:

```text
Account
```

represents a bank account.

```text
Transaction
```

represents a financial event.

```text
Transfer
```

represents money moving from one account to another.

That distinction is more important than simply counting how many tables the schema contains.
