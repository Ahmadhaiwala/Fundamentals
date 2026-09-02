# Ride-Sharing System — Database Schema

## 1. Customer

Stores information about customers using the platform.

```text
Customer
--------
customer_id PK
name
email
address
phone
```

### Relationship

```text
Customer 1 ───── N Ride
```

A customer can request multiple rides, while each ride belongs to one customer.

---

## 2. Driver

Stores information about drivers.

```text
Driver
------
driver_id PK
name
email
address
phone
license_number
```

### Relationships

```text
Driver 1 ───── N Vehicle
Driver 1 ───── N DriverAssignment
```

A driver can have multiple vehicles and can be assigned to multiple rides over time.

---

## 3. Vehicle

Stores vehicles belonging to drivers.

```text
Vehicle
-------
vehicle_id PK
driver_id FK → Driver.driver_id
vehicle_number
model
type
```

### Relationship

```text
Driver 1 ───── N Vehicle
```

Each vehicle belongs to one driver.

---

## 4. Ride

Represents a customer's ride request.

```text
Ride
----
ride_id PK
customer_id FK → Customer.customer_id
pickup_location
destination
requested_at
status
```

### Possible statuses

```text
requested
accepted
started
completed
cancelled
```

### Relationship

```text
Customer 1 ───── N Ride
```

A ride can exist before a driver is assigned.

---

## 5. DriverAssignment

Represents the assignment of a driver to a ride.

```text
DriverAssignment
----------------
assignment_id PK
ride_id FK → Ride.ride_id
driver_id FK → Driver.driver_id
assigned_at
```

### Relationships

```text
Ride 1 ───── 1 DriverAssignment
Driver 1 ───── N DriverAssignment
```

`DriverAssignment` is kept as a separate entity because driver assignment is a meaningful event and has its own information such as `assigned_at`.

If the system only allows one driver to ever be assigned to a ride, `ride_id` should also have a `UNIQUE` constraint.

---

## 6. Fare

Stores the final fare charged for a ride.

```text
Fare
----
fare_id PK
ride_id FK → Ride.ride_id
amount
```

### Relationship

```text
Ride 1 ───── 1 Fare
```

The fare is stored separately so the final amount remains historically correct even if the platform's pricing changes later.

`ride_id` should be `UNIQUE` if each ride can have only one final fare.

---

## 7. Rating

Stores ratings given after a completed ride.

```text
Rating
------
rating_id PK
ride_id FK → Ride.ride_id
rater_type
rating
```

### `rater_type`

```text
CUSTOMER
DRIVER
```

This allows the system to distinguish:

```text
Customer → Driver
Driver → Customer
```

### Relationship

```text
Ride 1 ───── N Rating
```

A ride can have at most:

```text
1 customer rating
1 driver rating
```

Therefore, a uniqueness constraint should be applied to:

```text
UNIQUE(ride_id, rater_type)
```

The rating should also satisfy:

```text
rating >= 1
rating <= 5
```

---

# Complete Schema

```text
Customer
--------
customer_id PK
name
email
address
phone


Driver
------
driver_id PK
name
email
address
phone
license_number


Vehicle
-------
vehicle_id PK
driver_id FK → Driver.driver_id
vehicle_number
model
type


Ride
----
ride_id PK
customer_id FK → Customer.customer_id
pickup_location
destination
requested_at
status


DriverAssignment
----------------
assignment_id PK
ride_id FK → Ride.ride_id
driver_id FK → Driver.driver_id
assigned_at


Fare
----
fare_id PK
ride_id FK → Ride.ride_id
amount


Rating
------
rating_id PK
ride_id FK → Ride.ride_id
rater_type
rating
```

---

# Entity Relationship Overview

```text
                    ┌──────────────┐
                    │   Customer   │
                    └──────┬───────┘
                           │
                           │ 1:N
                           │
                    ┌──────▼───────┐
                    │     Ride     │
                    └──────┬───────┘
                           │
             ┌─────────────┼──────────────┐
             │             │              │
             │ 1:1         │ 1:1          │ 1:N
             ▼             ▼              ▼
      ┌────────────┐ ┌────────────┐ ┌────────────┐
      │    Fare    │ │  Driver    │ │  Rating    │
      │            │ │ Assignment │ │            │
      └────────────┘ └─────┬──────┘ └────────────┘
                            │
                            │ N:1
                            ▼
                     ┌──────────────┐
                     │    Driver    │
                     └──────┬───────┘
                            │
                            │ 1:N
                            ▼
                     ┌──────────────┐
                     │   Vehicle    │
                     └──────────────┘
```

---

# Important Constraints

### Customer

```text
email UNIQUE
phone UNIQUE
```

### Driver

```text
email UNIQUE
phone UNIQUE
license_number UNIQUE
```

### Vehicle

```text
vehicle_number UNIQUE
```

### Driver Assignment

If only one driver can ultimately be assigned to a ride:

```text
UNIQUE(ride_id)
```

### Fare

If each ride has only one final fare:

```text
UNIQUE(ride_id)
```

### Rating

Only one rating from each party per ride:

```text
UNIQUE(ride_id, rater_type)
```

Rating must be:

```text
1 <= rating <= 5
```

---

# Design Decisions

## Why is DriverAssignment a separate entity?

Instead of:

```text
Ride
----
ride_id
customer_id
driver_id
...
```

we model:

```text
Ride
Driver
DriverAssignment
```

because assignment is an event/relationship that has its own attribute:

```text
assigned_at
```

This also leaves room for future requirements such as:

```text
accepted_at
rejected_at
assignment_status
```

---

## Why is Fare separate from Ride?

The ride represents the actual trip/request.

The fare represents the financial result of that trip.

Keeping the final fare allows historical data to remain correct even when the platform changes its pricing rules.

---

## Why is Rating separate?

Rating is not simply an attribute of a ride because a ride can produce two different ratings:

```text
Customer → Driver
Driver → Customer
```

Therefore, ratings are modeled as separate records.

---

# Core Relationships

```text
Customer 1 ───── N Ride

Driver 1 ───── N Vehicle

Ride 1 ───── 1 DriverAssignment

Driver 1 ───── N DriverAssignment

Ride 1 ───── 1 Fare

Ride 1 ───── N Rating
```

This schema represents the core ride-sharing system without introducing unnecessary tables for features that were not part of the requirements.
