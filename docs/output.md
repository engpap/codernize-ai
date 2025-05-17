# Kitchensink Jakarta EE Quickstart Documentation

## Overview
The Kitchensink Jakarta EE quickstart application demonstrates the integration of multiple Jakarta EE technologies, including CDI, JSF, EJB, JPA, Bean Validation, JAX-RS, and Arquillian. This documentation serves as a comprehensive guide covering project structure, key classes, configuration files, REST endpoints, testing strategies, and deployment instructions.

### Purpose
Showcases all features of Jakarta EE in a single project, including data validation, RESTful services, and testing.

### Main Technologies Covered
- CDI (Contexts and Dependency Injection)
- JSF (JavaServer Faces)
- EJB (Enterprise JavaBeans)
- JPA (Java Persistence API)
- Bean Validation
- JAX-RS (Java API for RESTful Web Services)
- Arquillian (Testing framework)

## Content Structure
1. **Introduction**
2. **Application Components**
   - Web Pages
   - Entities and Repositories
   - Services and Controllers
   - REST Endpoints
3. **Testing**
4. **Deployment & Run**
5. **Usage Notes**
6. **Key Classes and Files**
7. **Additional Resources**
8. **External Resources**

## Application Components

### Web Pages
- **`default.xhtml`**: Template with common layout elements (head, sidebar, footer).
- **`index.xhtml`**: Main page with member registration form and REST endpoint links.

### Entities and Repositories
- **`Member.java`**: JPA entity with validation constraints.
- **`MemberRepository.java`**: Handles database interactions using JPA Criteria API.
- **`MemberListProducer.java`**: Produces ordered list of members, updates on entity changes.

### Services and Controllers
- **`MemberRegistration.java`**: Manages member creation, uses EJB for transactions.
- **`Resources.java`**: Provides resource producers for CDI, such as EntityManager and Logger.
- **`MemberController.java`**: JSF controller for user interactions.

### REST Endpoints
- **`JaxRsActivator.java`**: Activates JAX-RS without XML configuration.
- **`MemberResourceRESTService.java`**: Exposes member data via REST, supports JSON marshalling.

## Testing
- Arquillian-based integration tests with **`MemberRegistrationTest.java`**.
- Configuration via **`arquillian.xml`**.

## Deployment & Run
Instructions for deploying and running the application on a server.

## Usage Notes
- The documentation includes commands and links to open files in an IDE for detailed code exploration.
- Emphasizes the use of CDI resource producers for consistent resource injection.
- Demonstrates validation, RESTful service exposure, and testing within a Jakarta EE environment.
- Provides deployment and testing instructions, including Arquillian configuration.

## Key Classes and Files
- **`Member.java`**: Defines the member entity with validation constraints and JAXB annotations.
- **`MemberRepository.java`**: Manages persistence operations for members.
- **`MemberListProducer.java`**: Produces a list of members, updates upon entity changes.
- **`MemberRegistration.java`**: Handles member registration with transaction management.
- **`Resources.java`**: CDI resource producer for EntityManager, Logger, FacesContext.
- **`MemberController.java`**: JSF backing bean for member management.
- **`JaxRsActivator.java`**: Configures JAX-RS application path.
- **`MemberResourceRESTService.java`**: Implements RESTful endpoints for member data.
- **`arquillian.xml`**: Configures deployment for Arquillian tests.
- **`pom.xml`**: Maven configuration for container selection and dependencies.

## Additional Resources
- Links to Arquillian project page and configuration guides.
- Guidance for creating custom projects from the archetype.

## External Resources
- [Red Hat JBoss EAP Documentation](https://access.redhat.com/documentation/en/red-hat-jboss-enterprise-application-platform/)
- [Arquillian Project Page](http://www.jboss.org/arquillian)

---

## Overview of `pom.xml` for Kitchensink Quickstart

### General Information
- **Project Name:** Quickstart: kitchensink
- **Type:** WAR (Web Application)
- **Description:** Starter Jakarta EE web application for JBoss EAP
- **Version:** 8.0.0.GA
- **Parent:** `jboss-eap-quickstart-parent` (version 6.0.0.redhat-00001)

### Licensing
- **License:** Apache License 2.0

### Properties
- **Server BOM Version:** 8.0.0.GA-redhat-00009
- **EAP Maven Plugin Version:** 1.0.0.Final-redhat-00014

### Repositories
- **JBoss Public Maven Repository**
- **Red Hat GA Maven Repository**

### Dependency Management
- Imports BOM: `org.jboss.bom:jboss-eap-ee-with-tools` (version specified by property)

### Dependencies
- **APIs (provided scope):**
  - Jakarta EE APIs (CDI, JPA, EJB, JSF, JAX-RS, JAXB)
  - Jakarta Activation and Annotations
- **Testing (test scope):**
  - JUnit
  - Arquillian (JUnit container, protocol)
  - JSON API and Parsson
- **Tools and Processors:**
  - Hibernate JPA Metamodel Generator
  - Hibernate Validator and Annotation Processor

### Profiles
- **arq-remote:** For remote Arquillian testing on JBoss EAP
- **openshift:** For building on OpenShift with specific layers and feature packs

### Build Plugins
- Configurations for Maven Failsafe Plugin (for integration tests)
- EAP Maven Plugin (for OpenShift deployment)

---

## Overview of `README.adoc` for Kitchensink Quickstart

This document provides comprehensive guidance for deploying and testing the Kitchensink quickstart application across various environments, including local servers and OpenShift.

### Content Summary

#### Project Description
- Demonstrates a web-enabled database application using JSF, CDI, EJB, JPA, and Bean Validation.
- Designed for {javaVersion} and {productNameFull} with deployment instructions.

#### Configuration Attributes
- Product-specific settings for JBoss EAP, WildFly, and OpenShift.
- Versioning, repository URLs, Helm charts, and quickstart download links.
- Environment-specific variables for OpenShift S2I, Helm, and domain configurations.

#### Deployment Instructions
- Building and running on a standalone server with configurable profiles.
- Starting the server with appropriate arguments.
- Building, deploying, and undeploying the application via Maven commands.
- Access URL and server log considerations.

#### Testing Procedures
- Running Arquillian integration tests locally and on OpenShift.
- Environment variables for test configuration.
- SSL considerations for OpenShift testing.

#### Additional Resources
- Links to product documentation, configuration guides, development guides, and Helm charts.
- Instructions for deploying via Helm and OpenShift CLI.
- Notes on production considerations, database setup, and performance.

#### Special Notes
- Deprecated datasource configuration files.
- Usage of specific profiles for OpenShift provisioning.
- Customization options for deployment and testing.

---

## Helm Chart Configuration

### Build Settings
- **URI:** URL to the Git repository containing the quickstarts.
- **Reference:** Branch or tag (`8.0.x`) for the build.
- **Context Directory:** `kitchensink`.

### Deployment Settings
- **Replicas:** Number of pod replicas to deploy (`1`).

### Configuration: Test DataSource (`test-ds.xml`)
- Defines an unmanaged, in-memory H2 datasource for testing purposes.
- JNDI Name: `java:jboss/datasources/KitchensinkQuickstartTestDS`
- Connection URL: `jdbc:h2:mem:kitchensink-quickstart-test;DB_CLOSE_DELAY=-1`
- Driver: `h2`
- Security Credentials: username `sa`, password `sa`
- Usage: Intended for proofs of concept and testing only, not for production.

---

## Arquillian Configuration

Defines the setup for Arquillian testing environment:
- **Namespaces and Schema**: Specifies XML namespace and schema location.
- **Commented Options**: Export of test archives for inspection, custom JBoss EAP home configuration.
- **Container Setup**: Uses a container with qualifier "jboss", marked as default.

### Persistence Configuration
- Defines a JPA persistence unit named **"primary"** using an unmanaged, in-memory H2 datasource for testing.
- Includes Hibernate-specific properties:
  - **`hibernate.hbm2ddl.auto`** set to **`create-drop`**.
  - **`hibernate.show_sql`** set to **`false`**.

---

## RemoteMemberRegistrationIT Class

### Purpose
Integration test for remote member registration API.

### Key Methods
- `getHTTPEndpoint()`: Constructs the URI for the REST endpoint.
- `getServerHost()`: Retrieves server host configuration.
- `testRegister()`: Tests member registration by sending a POST request.

---

## MemberRegistrationIT Test Class

### Key Components
- **Deployment Method (`createTestArchive`)**: Configures the test deployment archive.
- **Injected Dependencies**: `MemberRegistration`, `Logger`.
- **Test Method (`testRegister`)**: Tests member registration and asserts ID generation.

---

## import.sql Configuration

This file contains SQL statements for seeding the database with initial data.

### Key Elements
- **Insert Statements**: Adds a sample member.
- **Licensing and Copyright**: License information and legal notices.

---

## beans.xml Configuration

- **Purpose**: Marker file to enable CDI (Contexts and Dependency Injection).
- **Schema**: Defines Java EE namespace and schema location.
- **Bean Discovery Mode**: Set to `"all"`.

---

## Faces Configuration Overview

- **File Location**: `/WEB-INF/faces-config.xml`
- **Purpose**: Configures JavaServer Faces (JSF) settings for the application.
- **Main Components**: Namespace declarations, JSF version, activation, navigation rules, managed beans.

---

## Data Source Configuration

Defines an unmanaged in-memory H2 database datasource for testing purposes.

### Key Elements
- **JNDI Name**: `java:jboss/datasources/KitchensinkQuickstartDS`
- **Pool Name**: `kitchensink-quickstart`
- **Enabled**: `true`
- **Connection URL**: In-memory H2 database.
- **Driver**: `h2`
- **Security Credentials**: Username `sa`, password `sa`.

---

## Resources Class

The `Resources` class provides CDI producers for Jakarta EE resources.

### Public Methods
- **`produceLog(InjectionPoint injectionPoint)`**: Produces a `Logger` instance.
- **CDI Producers**: Provides an `EntityManager` instance for database operations.

---

## MemberController

### Overview
Manages the registration process for members within the application.

### Annotations
- `@Model`, `@Inject`, `@Produces`, `@Named`.

### Fields
- `facesContext`, `memberRegistration`, `newMember`.

### Lifecycle Methods
- `@PostConstruct initNewMember()`: Initializes a new `Member` instance.

### Public Methods
- `register()`: Handles the registration process.

---

## Member Class

The `Member` class represents a data model for storing member information.

### Class Overview
- **Annotations**: `@Entity`, `@XmlRootElement`, `@Table`.

### Fields
- `id`, `name`, `email`, `phoneNumber`.

### Methods
- Getters and Setters for each field.

---

## MemberRegistration Class

The `MemberRegistration` class provides business logic for registering new members.

### Class Declaration
- **@Stateless**: Indicates a stateless session bean.

### Dependencies
- **Logger**, **EntityManager**, **Event**.

### Public Methods
- **register(Member member)**: Registers a new member.

---

## MemberListProducer Class

The `MemberListProducer` class manages a list of `Member` entities.

### Class Overview
- **Scope**: `@RequestScoped`.

### Public Methods
- **`getMembers()`**: Provides access to the list of members.
- **`onMemberListChanged(Member member)`**: Observes member change events.

---

## MemberRepository

The `MemberRepository` class provides data access methods for `Member` entities.

### Class Overview
- **Scope**: `@ApplicationScoped`.

### Public Methods
- **`findById(Long id)`**: Retrieves a `Member` entity by ID.
- **`findByEmail(String email)`**: Finds a `Member` by email.
- **`findAllOrderedByName()`**: Retrieves all `Member` entities ordered by name.

---

## JaxRsActivator

### Overview
Configures the base URI path for JAX-RS resources.

### Class Signature
- **Class Name**: `JaxRsActivator`
- **Annotations**: `@ApplicationPath("/rest")`.

---

## MemberResourceRESTService

This class provides a RESTful API for managing members.

### Class Declaration
- **Path**: `/members`.

### Public Methods
- **listAllMembers**: Retrieves a list of all members.
- **lookupMemberById**: Retrieves a member by ID.
- **createMember**: Creates a new member.

### Private Methods
- **validateMember**: Validates the member object.
- **createViolationResponse**: Constructs a response detailing validation errors.
- **emailAlreadyExists**: Checks if a member with the given email exists.