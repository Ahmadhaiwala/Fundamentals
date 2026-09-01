Final schema
1. Customer
Customer
---------
customer_id PK
name
email UNIQUE
phone
2. Address

A customer can save multiple addresses.

Address
---------
address_id PK
customer_id FK
address
is_default
Customer 1 ─── N Address

The is_default requirement also means you'd eventually want a constraint/business rule ensuring a customer has at most one default address.

3. Restaurant
Restaurant
----------
restaurant_id PK
name
phone
address
4. MenuItem

A menu item belongs to exactly one restaurant.

MenuItem
---------
menu_item_id PK
restaurant_id FK
name
description
price
is_available
Restaurant 1 ─── N MenuItem

So you don't need a RestaurantMenu junction table here. The relationship is 1:N, not M:N.

5. Order

This represents the overall transaction.

Order
------
order_id PK
customer_id FK
restaurant_id FK
address_id FK
status
created_at

Relationships:

Customer   1 ─── N Order
Restaurant 1 ─── N Order
Address    1 ─── N Order

The restaurant_id is important because the requirement says one order can contain items from only one restaurant.

6. OrderItem 🔥

This is the part that was giving you the headache.

Imagine:

Order #101

Pizza     × 2
Burger    × 1
Coke      × 3

You can't keep those as columns inside Order. So you create a row for each distinct item:

OrderItem
---------
order_item_id PK
order_id FK
menu_item_id FK
quantity
unit_price

Relationship:

Order 1 ─── N OrderItem N ─── 1 MenuItem

So the data could look like:

order_item_id | menu_item | quantity
-------------------------------------
1             | Pizza     | 2
2             | Burger    | 1
3             | Coke      | 3

And here's the important part:

unit_price

is the price actually paid at the time of the order.

If Pizza costs ₹300 today and becomes ₹350 tomorrow:

MenuItem.price = ₹350
OrderItem.unit_price = ₹300

That old order must still show ₹300.

This is one of those cases where keeping a historical snapshot is intentional and correct.

7. Payment

The requirement says payment can be attempted multiple times.

Payment
--------
payment_id PK
order_id FK
amount
status
payment_time
transaction_id

So:

Order 1 ─── N Payment

For example:

Payment #1 → ₹700 → FAILED
Payment #2 → ₹700 → FAILED
Payment #3 → ₹700 → SUCCESS

That's why you shouldn't put a single payment_id inside Order.

8. Driver
Driver
-------
driver_id PK
name
phone
vehicle_number

A driver can deliver many orders over time, while an order can have at most one driver.

You could put driver_id, assigned_at, and picked_up_at directly in Order, but there's a better modeling option here.

9. Delivery

The assignment itself has meaningful information:

Which driver was assigned, when were they assigned, and when did they pick it up?

So:

Delivery
---------
delivery_id PK
order_id FK UNIQUE
driver_id FK
assigned_at
picked_up_at

Giving:

Order 1 ─── 1 Delivery N ─── 1 Driver

Delivery represents the actual delivery/driver assignment rather than treating those details as random attributes of Order.

10. Order status

You don't necessarily need another table just to represent the current status.

Your Order.status can be:

PLACED
CONFIRMED
PREPARING
READY
PICKED_UP
DELIVERED
CANCELLED
REJECTED

So:

Order.status

represents the current state.

But here's an important distinction:

If the requirement later changes to:

"We need to know when the order entered each status."

Then you'd need:

OrderStatusHistory
------------------
history_id PK
order_id FK
status
changed_at
changed_by

That's:

current state ≠ state history.

11. Restaurant Review

A customer can rate a restaurant after an order is delivered.

RestaurantReview
----------------
review_id PK
order_id FK
customer_id FK
restaurant_id FK
rating
comment
created_at

You'd want something like:

UNIQUE(customer_id, order_id)

so the same customer can't submit multiple restaurant reviews for the same order.

And your application/database logic needs to ensure the order is actually delivered before allowing the review.

12. Driver Review

Same concept, but for the driver:

DriverReview
------------
review_id PK
order_id FK
customer_id FK
driver_id FK
rating
comment
created_at

Again:

UNIQUE(customer_id, order_id)

and it should only be allowed after delivery.

🧠 Put the whole thing together
                    Customer
                   /        \
                  /          \
                 ↓            ↓
             Address         Order
                              |
              ┌───────────────┼───────────────┐
              ↓               ↓               ↓
          OrderItem        Payment          Delivery
              |                               |
              ↓                               ↓
          MenuItem                          Driver
              |
              ↓
          Restaurant

And separately:

Order ─── RestaurantReview
Order ─── DriverReview
The patterns you should take away

This one problem gave you several real schema-design patterns:

1. One-to-many
Restaurant → MenuItem
Customer → Address
Order → OrderItem
Order → Payment
2. Many-to-many resolved through an associative entity

Conceptually:

Order ↔ MenuItem

becomes:

Order → OrderItem → MenuItem

because the relationship needs quantity and unit_price.

3. Historical snapshot
OrderItem.unit_price

exists because the current MenuItem.price can change.

4. Current state vs history
Order.status

versus:

OrderStatusHistory

if you need the complete state transition history.

5. Relationship with attributes
Delivery
assigned_at
picked_up_at

The relationship itself contains meaningful data, so giving it its own entity can make the model much cleaner.

6. Business constraints

Things like:

one order → one restaurant
one order → max one driver
multiple payment attempts
review only after delivery

are part of schema design too. It's not just about deciding what tables exist.