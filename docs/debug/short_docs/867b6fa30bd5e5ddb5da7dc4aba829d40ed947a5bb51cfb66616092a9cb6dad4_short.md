# MemberRepository

The `MemberRepository` class provides data access methods for `Member` entities within the application. It is designed with application scope, meaning a single instance is used throughout the application's lifecycle.

## Class Overview

- **Package:** `org.jboss.as.quickstarts.kitchensink.data`
- **Scope:** `@ApplicationScoped`
- **Dependencies:**
  - Injected `EntityManager` for persistence operations

## Public Methods

### `findById(Long id)`

- **Description:** Retrieves a `Member` entity based on its unique identifier.
- **Parameters:**
  - `id` (Long): The primary key of the `Member` to find.
- **Returns:** `Member` object matching the provided ID, or `null` if not found.

### `findByEmail(String email)`

- **Description:** Finds a `Member` entity by its email address.
- **Parameters:**
  - `email` (String): The email address to search for.
- **Returns:** `Member` object with the specified email.
- **Notes:** Utilizes JPA Criteria API to construct a type-safe query, with an example of a non-type-safe alternative commented out.

### `findAllOrderedByName()`

- **Description:** Retrieves all `Member` entities ordered alphabetically by name.
- **Returns:** `List<Member>` containing all members sorted by name.
- **Notes:** Uses JPA Criteria API to define ordering, with an example of a non-type-safe alternative commented out.

## Usage Notes

- The class relies on dependency injection for the `EntityManager`.
- Queries are constructed using JPA Criteria API for type safety and flexibility.
- The class is intended for use within Java EE or Jakarta EE environments supporting CDI and JPA.