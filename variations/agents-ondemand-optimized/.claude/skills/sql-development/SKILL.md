---
name: sql-development
description: SQL development best practices, query optimization, schema design, and database patterns for relational databases.
---

## SQL Development

### Schema Design
- Use singular table names: `user`, `order`, `product` (not `users`, `orders`)
- Every table must have a primary key — prefer `id BIGINT AUTO_INCREMENT`
- Use foreign keys to enforce referential integrity
- Add indexes on columns used in WHERE, JOIN, and ORDER BY clauses
- Use `NOT NULL` by default — only allow NULL when absence of a value is meaningful

### Naming Conventions
- **snake_case** for table and column names: `user_account`, `created_at`
- Prefix foreign keys with the referenced table: `user_id`, `order_id`
- Prefix boolean columns with `is_` or `has_`: `is_active`, `has_verified_email`
- Name indexes descriptively: `idx_user_email`, `idx_order_created_at`

### Query Best Practices
```sql
-- Always specify columns, never SELECT *
SELECT u.id, u.name, u.email
FROM user u
WHERE u.is_active = TRUE
ORDER BY u.created_at DESC
LIMIT 20 OFFSET 0;

-- Use JOINs explicitly, never implicit joins in WHERE
SELECT o.id, o.total, u.name
FROM order o
INNER JOIN user u ON u.id = o.user_id
WHERE o.status = 'completed';

-- Use parameterized queries to prevent SQL injection
-- NEVER concatenate user input into SQL strings
```

### Index Strategy
- Create indexes for columns in WHERE clauses used frequently
- Use composite indexes for multi-column queries (leftmost prefix rule)
- Don't over-index — each index slows down writes
- Use `EXPLAIN` to verify query plans and index usage
- Consider covering indexes for frequently-run queries

### Stored Procedures
```sql
CREATE PROCEDURE GetUserOrders(
    @UserId BIGINT,
    @Status VARCHAR(20) = NULL
)
AS
BEGIN
    SELECT o.id, o.total, o.created_at
    FROM [order] o
    WHERE o.user_id = @UserId
      AND (@Status IS NULL OR o.status = @Status)
    ORDER BY o.created_at DESC;
END;
```

### Migrations
- Use sequential, timestamped migration files: `001_create_user_table.sql`
- Every migration must be reversible — include both UP and DOWN scripts
- Never modify a migration that has been applied to production
- Test migrations against a copy of production data before deploying

### Transaction Management
```sql
BEGIN TRANSACTION;
    UPDATE account SET balance = balance - 100 WHERE id = 1;
    UPDATE account SET balance = balance + 100 WHERE id = 2;

    IF @@ERROR <> 0
        ROLLBACK;
    ELSE
        COMMIT;
```

### Performance Optimization
- Use `EXPLAIN ANALYZE` (PostgreSQL) or `SET STATISTICS IO ON` (SQL Server) to profile queries
- Avoid `SELECT *` — only fetch columns you need
- Use `EXISTS` instead of `IN` for subqueries with large result sets
- Batch large INSERT/UPDATE operations to avoid lock contention
- Use connection pooling in application code
- Consider read replicas for read-heavy workloads

### Common Anti-Patterns to Avoid
- **N+1 queries**: Use JOINs or batch fetching instead of looping queries
- **Missing indexes**: Profile slow queries and add targeted indexes
- **Over-normalization**: Denormalize for read performance when appropriate
- **Implicit type conversion**: Ensure WHERE clause types match column types
- **Large transactions**: Keep transactions as short as possible
- **No foreign keys**: Always use FKs unless you have a specific reason not to (e.g., partitioning)

### Data Types
- Use `VARCHAR(n)` for variable-length strings, `CHAR(n)` for fixed-length
- Use `DECIMAL(p,s)` for money/financial values, never `FLOAT`
- Use `TIMESTAMP WITH TIME ZONE` for dates (PostgreSQL) or `DATETIMEOFFSET` (SQL Server)
- Use `BOOLEAN` or `BIT` for true/false values
- Use `UUID`/`UNIQUEIDENTIFIER` for distributed IDs
