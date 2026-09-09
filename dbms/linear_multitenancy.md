# Linear Multitenancy

**Linear multitenancy** (often referred to in software architecture as **siloed multitenancy** or **database-per-tenant architecture**) is a design pattern where each customer (tenant) gets their own dedicated, isolated resources within a single system application. 

Instead of mixing data in a shared database, resources are cloned or partitioned linearly as new tenants are added.

---

## Core Architectures: Linear vs. Pooled

To understand linear multitenancy, it helps to compare it to the traditional pooled model:

| Dimension | **Linear Multitenancy (Siloed)** | **Pooled Multitenancy (Shared)** |
| :--- | :--- | :--- |
| **Data Isolation** | **Maximum**. Separate databases or compute instances per tenant. | **Logical**. Shared database; separated by a `tenant_id` column. |
| **Noisy Neighbors** | **Eliminated**. One tenant's heavy usage won't slow down others. | **High Risk**. One tenant can consume shared database resources. |
| **Scaling Mechanism** | **Horizontal**. Add more database instances linearly. | **Vertical / Sharding**. Scale up the core shared infrastructure. |
| **Cost Efficiency** | **Lower**. Higher baseline cost due to idle, dedicated resources. | **Higher**. Maximum utilization of shared resources. |
| **Maintenance** | **Complex**. Schema updates must be run across *N* databases. | **Simple**. Update a single centralized database schema. |

---

## Key Benefits

* **Strict Data Security & Compliance:** Crucial for enterprise SaaS, healthcare (HIPAA), or finance, where customers forbid their data from physically sitting next to a competitor's data.
* **Simplified Deletion & Backups:** If a tenant leaves, you can drop their specific database or archive it without touching any other customer's data.
* **Customization Potential:** It is easier to run custom database migrations or tweaks for high-value VIP enterprise tenants.

## The Trade-offs

* **The "Infrastructure Tax":** You pay for the compute and storage overhead of every single instance, even if a tenant is inactive.
* **Management Complexity:** As you scale to thousands of tenants, running migrations, collecting global analytics, and monitoring infrastructure requires advanced DevOps automation (like Kubernetes or automated Terraform scripting).
