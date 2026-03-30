# Database Directory

This folder is designated for database-related files, documentation, and backup exports. 

## File Structure Explanation

* `schema.sql` → **Database schema:** Contains the DDL (Data Definition Language) queries to create the tables, relationships, and constraints required for the ERP system.
* `seed_data.sql` → **Sample data:** Contains the DML (Data Manipulation Language) queries to insert initial dummy data (vendors, products, sample purchase orders) to bootstrap and test the application quickly.
* `export.sql` → **Full database dump:** Contains a complete backup of the database structure and all inserted records. (Generated manually, see instructions below).

---

## Instructions: Creating `export.sql`

To fulfill the assignment requirements, you must generate a full database export file.

### What is `export.sql`?
It is a complete SQL dump of your PostgreSQL database containing all tables, constraints, sequences, and the active data currently in the database.

### Why is it needed?
It allows evaluators, instructors, or other developers to completely restore the database perfectly on their local machines without running the application or manually inserting data.

### How to generate it
Run the following command in your terminal. Ensure that your PostgreSQL server is running and you have access to the `pg_dump` utility.

```bash
pg_dump -U postgres -d erp_db > export.sql
```
*(Note: If you are using Docker, you can run `docker exec -t <container_name_or_id> pg_dump -U erp_user -d erp_db > export.sql`)*

### Where to place the file
Once generated, `export.sql` should be placed in the root of the repository (or inside this `database/` folder, depending on the exact submission instruction) so it is included in your GitHub repository and assignment submission.
