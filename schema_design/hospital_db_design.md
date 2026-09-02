# Hospital Management System — Database Schema Design

## Problem Statement

Design a database schema for a hospital management system.

The system should support:

* Patients
* Doctors
* Departments
* Appointments
* Medical records
* Prescriptions
* Medicines
* Billing

The goal is to model the system based on its real-world requirements rather than simply applying normalization rules.

---

# Requirements

## 1. Patients

A patient can visit the hospital multiple times.

Store:

* Patient ID
* Name
* Date of birth
* Phone
* Address

---

## 2. Doctors

A doctor works in one department.

Store:

* Doctor ID
* Name
* Phone
* Email
* Specialization
* Department

A department can have multiple doctors.

---

## 3. Departments

The hospital has departments such as:

```text id="wz0g3f"
Cardiology
Neurology
Orthopedics
General Medicine
```

Store:

* Department ID
* Name

---

## 4. Appointments

A patient can have many appointments.

Each appointment is with a particular doctor.

Store:

* Appointment ID
* Patient
* Doctor
* Appointment date/time
* Status

Possible statuses:

```text id="j82q9m"
scheduled
completed
cancelled
```

---

## 5. Medical Records

When a patient visits a doctor, the doctor can create a medical record.

Store:

* Diagnosis
* Notes
* Date

Medical records are historical records and should remain associated with the original patient, doctor, and appointment.

---

## 6. Prescriptions

A prescription can contain multiple medicines.

A medicine can appear in prescriptions for many different patients.

For every medicine prescribed, store:

* Medicine
* Dosage
* Frequency
* Duration

Example:

```text id="u9t1kw"
Medicine: Paracetamol
Dosage: 500mg
Frequency: 2 times/day
Duration: 5 days
```

---

## 7. Billing

An appointment may generate a bill.

A bill contains:

* Bill ID
* Appointment
* Total amount
* Payment status

Possible payment statuses:

```text id="c0l7h1"
pending
paid
failed
```

A cancelled appointment should not generate a bill.

---

## 8. Important Hospital Rules

A doctor cannot have two appointments at the exact same time.

Other important rules include:

* A rating/amount/etc. must have valid values where applicable.
* A prescription can contain multiple medicines.
* A medicine can occur in many prescriptions.
* An appointment may or may not have a medical record.
* An appointment may or may not have a bill.
* Cancelled appointments should not generate bills.

---

# Final Schema

## Patient

```text id="e4my3s"
Patient
-------
patient_id PK
name
dob
phone
address
```

---

## Department

```text id="h6l9yc"
Department
----------
department_id PK
name
```

---

## Doctor

```text id="0e2e2a"
Doctor
------
doctor_id PK
name
email
phone
specialization
department_id FK → Department.department_id
```

### Relationship

```text id="l8u2g9"
Department 1 ───── N Doctor
```

A department can have many doctors.

Each doctor belongs to one department.

---

## Appointment

```text id="v4q1q5"
Appointment
-----------
appointment_id PK
patient_id FK → Patient.patient_id
doctor_id FK → Doctor.doctor_id
appointment_datetime
status
```

### Relationships

```text id="0exrj2"
Patient 1 ───── N Appointment

Doctor 1 ───── N Appointment
```

An appointment belongs to one patient and one doctor.

---

## MedicalRecord

```text id="t8u1iq"
MedicalRecord
-------------
record_id PK
patient_id FK → Patient.patient_id
doctor_id FK → Doctor.doctor_id
appointment_id FK → Appointment.appointment_id
diagnosis
notes
recorded_at
```

### Relationships

```text id="6fz9uq"
Patient 1 ───── N MedicalRecord

Doctor 1 ───── N MedicalRecord

Appointment 1 ───── 0/1 MedicalRecord
```

The `appointment_id` connects the medical record to the specific visit during which it was created.

---

## Prescription

```text id="c6t7yl"
Prescription
------------
prescription_id PK
record_id FK → MedicalRecord.record_id
prescribed_at
```

### Relationship

```text id="a1by0j"
MedicalRecord 1 ───── N Prescription
```

A medical record can have one or more prescriptions if the system allows multiple prescriptions.

---

## Medicine

```text id="3c1i0h"
Medicine
--------
medicine_id PK
name
```

A medicine is a reusable entity because the same medicine can appear in many prescriptions.

---

## PrescriptionItem

```text id="zj9m5y"
PrescriptionItem
----------------
prescription_id FK → Prescription.prescription_id
medicine_id FK → Medicine.medicine_id
dosage
frequency
duration
```

Primary key:

```text id="9d6zbr"
PK(prescription_id, medicine_id)
```

### Relationship

```text id="3n1j9b"
Prescription 1 ───── N PrescriptionItem

Medicine 1 ───── N PrescriptionItem
```

Therefore:

```text id="2o6h4s"
Prescription N ───── M Medicine
```

is implemented through:

```text id="p8x9mv"
PrescriptionItem
```

---

## Bill

```text id="m3o4q8"
Bill
----
bill_id PK
appointment_id FK → Appointment.appointment_id
total_amount
payment_status
```

### Relationship

```text id="0u8q4e"
Appointment 1 ───── 0/1 Bill
```

If each appointment can only generate one bill:

```text id="v2r8x1"
UNIQUE(appointment_id)
```

---

# Complete Schema

```text id="n4w7lp"
Patient
-------
patient_id PK
name
dob
phone
address


Department
----------
department_id PK
name


Doctor
------
doctor_id PK
name
email
phone
specialization
department_id FK


Appointment
-----------
appointment_id PK
patient_id FK
doctor_id FK
appointment_datetime
status


MedicalRecord
-------------
record_id PK
patient_id FK
doctor_id FK
appointment_id FK
diagnosis
notes
recorded_at


Prescription
------------
prescription_id PK
record_id FK
prescribed_at


Medicine
--------
medicine_id PK
name


PrescriptionItem
----------------
prescription_id FK
medicine_id FK
dosage
frequency
duration


Bill
----
bill_id PK
appointment_id FK
total_amount
payment_status
```

---

# Entity Relationship Overview

```text id="4q6r7w"
                         Department
                             │
                             │ 1:N
                             ▼
                          Doctor
                             │
                             │ 1:N
                             ▼
Patient ───── 1:N ────> Appointment
                             │
                             ├──────── 0/1 ─────> Bill
                             │
                             │
                             └──────── 0/1 ─────> MedicalRecord
                                                      │
                                                      │ 1:N
                                                      ▼
                                                Prescription
                                                      │
                                                      │ 1:N
                                                      ▼
                                             PrescriptionItem
                                                      ▲
                                                      │ N:1
                                                      │
                                                  Medicine
```

---

# Important Constraints

## Appointment Scheduling

A doctor cannot have two appointments at the exact same time.

Conceptually:

```text id="r6w2kq"
UNIQUE(doctor_id, appointment_datetime)
```

This prevents:

```text id="x2l4d8"
Doctor 5 | 10:00
Doctor 5 | 10:00    ❌
```

but allows:

```text id="5c8z7m"
Doctor 5 | 10:00
Doctor 5 | 11:00    ✅
```

---

## Appointment Status

```text id="n9j3qb"
status IN (
    'scheduled',
    'completed',
    'cancelled'
)
```

---

## Payment Status

```text id="4h8k1c"
payment_status IN (
    'pending',
    'paid',
    'failed'
)
```

---

## Billing

If one appointment can generate only one bill:

```text id="g5r0ty"
UNIQUE(appointment_id)
```

A cancelled appointment should not generate a bill.

This can be enforced through application logic or stricter database-level mechanisms depending on the implementation.

---

## PrescriptionItem

A medicine should not appear twice in the same prescription:

```text id="2t7x9q"
PRIMARY KEY (
    prescription_id,
    medicine_id
)
```

---

# Important Design Decisions

## 1. Why isn't Prescription just an attribute of MedicalRecord?

A prescription is a meaningful object that can contain multiple medicines.

For example:

```text id="v6m3n2"
Prescription #101

Paracetamol
Amoxicillin
Vitamin D
```

Therefore, `Prescription` deserves its own entity.

---

# 2. Why do we need PrescriptionItem?

This is the most important design decision in this problem.

We have:

```text id="b5c1r7"
Prescription N ───── M Medicine
```

A prescription can contain many medicines.

A medicine can appear in many prescriptions.

Therefore, this is an M:N relationship.

We resolve it using:

```text id="j8p2k4"
PrescriptionItem
```

But there's another important reason.

These attributes:

```text id="a0f9xs"
dosage
frequency
duration
```

describe the relationship between the prescription and the medicine.

For example:

```text id="1q5m7n"
Medicine:
Paracetamol
```

doesn't inherently have:

```text id="d4f8k2"
dosage = 500mg
frequency = 2/day
duration = 5 days
```

Those values depend on **how that medicine was prescribed**.

Therefore they belong to `PrescriptionItem`.

---

# 3. Why does MedicalRecord reference Patient, Doctor, and Appointment?

A medical record represents a historical medical event.

We want to know:

```text id="k2x8p0"
Which patient?
Which doctor?
Which appointment?
What diagnosis?
What notes?
When?
```

Therefore:

```text id="y7n4q2"
patient_id
doctor_id
appointment_id
```

are appropriate references.

---

# 4. Why does Appointment reference Doctor instead of Department?

The appointment is specifically with a **doctor**.

The department can already be found through:

```text id="r8v1c6"
Appointment
    ↓
Doctor
    ↓
Department
```

There is no need to duplicate `department_id` inside Appointment unless the requirements specifically demand it.

---

# 5. Current Data vs Historical Data

Suppose:

```text id="h7x3n1"
Patient
patient_id = 10
name = Ahmad
```

A medical record is created.

Later the patient's name changes.

The foreign key:

```text id="p4m9q2"
patient_id = 10
```

still identifies the same patient.

However, it will retrieve the patient's **current** information.

Therefore:

> A foreign key preserves identity, not historical state.

If the hospital legally or operationally needs the patient's exact demographic information as it existed when the record was created, additional snapshot/history data would be required.

---

# Core Schema-Design Lessons

## 1. Identify real-world entities

```text
Patient
Doctor
Department
Appointment
MedicalRecord
Prescription
Medicine
Bill
```

---

## 2. Identify events

Some tables represent things that happened rather than permanent objects.

Examples:

```text
Appointment
MedicalRecord
Prescription
Bill
```

Thinking in terms of events helps identify what information needs to be stored historically.

---

## 3. M:N relationships usually need an associative entity

```text
Prescription N ───── M Medicine
```

becomes:

```text
Prescription
      │
      │ 1:N
      ▼
PrescriptionItem
      ▲
      │ N:1
      │
   Medicine
```

---

## 4. Relationship attributes belong to the relationship

These:

```text
dosage
frequency
duration
```

describe how a particular medicine is used in a particular prescription.

Therefore:

```text
PrescriptionItem
```

is the correct place for them.

---

## 5. Not every relationship needs a table

For example:

```text
Department → Doctor
Patient → Appointment
Doctor → Appointment
```

can be represented using foreign keys because the relationship itself does not require additional repeated information.

---

## 6. Constraints are part of schema design

Schema design isn't only about deciding tables.

You also need to think about rules such as:

```text
UNIQUE(doctor_id, appointment_datetime)

UNIQUE(appointment_id)

rating/amount/value constraints where applicable

valid status values
```

The database should prevent invalid states whenever practical.

---

# Final Mental Model

When designing a schema, ask:

```text
1. What are the real-world entities?

2. What does each row represent?

3. What are the relationships?

4. What is the cardinality?

5. Does the relationship have its own attributes?

6. Is this an M:N relationship?

7. Is this information current state or historical state?

8. What business rules must be enforced?

9. Can the database prevent invalid states?

10. Am I storing duplicate information unnecessarily?
```

The goal is not to create as many tables as possible.

The goal is to make the database accurately represent the real-world system.
