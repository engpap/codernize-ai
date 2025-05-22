# CDI + JSF + EJB + JTA + Bean Validation + JAX-RS + Arquillian: Kitchensink Quickstart Documentation

## Overview
This quickstart demonstrates the integration of multiple Jakarta EE technologies, including CDI, JSF, EJB, JTA, Bean Validation, JAX-RS, and Arquillian, within a sample application called "kitchensink." It provides a comprehensive starting point for developing Jakarta EE applications.

## Key Components
- **Title:** CDI + JSF + EJB + JTA + Bean Validation + JAX-RS + Arquillian: Kitchensink quickstart
- **Category:** Business Logic

## Application Structure

### The Kitchensink Example
- Demonstrates various Jakarta EE technologies via a member registration database accessible through JSF and JAX-RS.
- Deployment descriptors:
  - `beans.xml` and `faces-config.xml` in `WEB-INF/`.
  - `persistence.xml` and `import.sql` in `WEB-INF/classes/META-INF/`.

### JSF Views
- **default.xhtml:** Template with common header, sidebar, and footer.
- **index.xhtml:** Main page with member registration form and REST endpoint links.
  - Utilizes Bean Validation for data validation.
  - Displays REST endpoint URLs for registered members.

### Entity Class
- **Member.java:** JPA entity representing a member.
  - Annotated with `@Entity` and `@XmlRootElement`.
  - Constraints applied via Bean Validation annotations such as `@Size`, `@Pattern`, `@Email`, `@Digits`, `@NotNull`.

### Persistence Layer
- **MemberRepository.java:** Handles database interactions.
  - Application-scoped singleton.
  - Uses JPA Criteria API to query members by ID or email, and to retrieve lists of members.

### Business Logic
- **MemberListProducer.java:** Produces a list of members ordered by name.
  - Request-scoped bean.
  - Observes member changes to refresh the list.
- **MemberRegistration.java:** Manages member creation.
  - Stateless EJB with transaction management.
  - Sends events upon member updates.

### Resource Management
- **Resources.java:** Provides resource producers.
  - CDI producer for `EntityManager`.
  - CDI producer for `Logger`.
  - Producer for `FacesContext`.
  - Links to Red Hat documentation for datasource configuration.

### JSF Controller
- **MemberController.java:** Facilitates interaction between JSF pages and business logic.
  - Uses `@Model` stereotype (`@Named` + `@RequestScoped`).
  - Injects `FacesContext`, `MemberRegistration`, and `Member`.
  - Handles member registration and user feedback.

## RESTful Services
- **JaxRsActivator.java:** Activates JAX-RS with `@ApplicationPath`.
- **MemberResourceRESTService.java:** Provides REST endpoints under `rest/members`.
  - Request-scoped CDI bean.
  - Injects `MemberRepository`, `MemberRegistration`, and Validator.
  - Endpoints:
    - `listAllMembers()`: Retrieves all members as JSON.
    - `lookupMemberById()`: Retrieves a member by ID.
    - `createMember()`: Creates a new member with validation.
  - Validates member data before persistence.
  - Marshals responses to JSON automatically.

## Deployment and Testing

### Run and Deploy
- Right-click project → Run As → Run on Server.
- Uses `org.jboss.tools.project.examples.cheatsheet.actions.RunOnServer`.

### Arquillian Testing
- Integrates Arquillian for in-container testing.
- **Start Arquillian Tests:**
  - Use Maven profile `arq-remote`.
  - Run JUnit tests to execute integration tests inside JBoss EAP.
- **MemberRegistrationTest.java:**
  - Annotated with `@RunWith(Arquillian.class)`.
  - Defines deployment archive with relevant classes, `persistence.xml`, `beans.xml`, and test datasource.
  - Contains test methods for member creation and validation.

### Arquillian Configuration
- **arquillian.xml:** Configures deployment settings and container specifics.
- **pom.xml:** Manages container profiles and dependencies for Arquillian.

### Additional Resources
- Arquillian project page: [http://www.jboss.org/arquillian](http://www.jboss.org/arquillian)
- Red Hat JBoss documentation: [https://access.redhat.com/documentation/en/red-hat-jboss-enterprise-application-platform/](https://access.redhat.com/documentation/en/red-hat-jboss-enterprise-application-platform/)

## Creating Your Own Application
- Generate a new project from the Maven archetype used for this example.
- Use the Red Hat Central plugin in Eclipse to start a new Jakarta EE Web Project with customizations.

# Maven Project Configuration

## Basic Information
- **Artifact ID:** kitchensink
- **Version:** 8.0.0.GA
- **Packaging:** WAR
- **Description:** Starter Jakarta EE web application for JBoss EAP

## Parent and Licensing
- **Parent:** org.jboss.eap.quickstarts:jboss-eap-quickstart-parent:6.0.0.redhat-00001
- **License:** Apache License 2.0

## Properties
- **Server BOM Version:** 8.0.0.GA-redhat-00009
- **EAP Maven Plugin Version:** 1.0.0.Final-redhat-00014

## Repositories
- **JBoss Public Maven Repository**
- **Red Hat GA Maven Repository**

## Plugin Repositories
- **JBoss Public Maven Repository**
- **Red Hat GA Maven Repository**

## Dependency Management
- **Imports:** `org.jboss.bom:jboss-eap-ee-with-tools` BOM

## Dependencies Overview
- **API Dependencies (provided scope):**
  - Jakarta EE APIs (CDI, JPA, EJB, JSF, JAX-RS, Common Annotations)
- **Testing Dependencies:**
  - JUnit
  - Arquillian (JUnit container, protocol)
  - JSON and parsing libraries
- **Tools and Implementation:**
  - Hibernate JPA Metamodel Generator
  - Hibernate Validator and Validation API
  - Jakarta Activation API
  - Jakarta XML Binding API

## Profiles
### arq-remote
- **Purpose:** Run tests in a remote JBoss EAP instance
- **Includes:** `org.wildfly.arquillian:wildfly-arquillian-container-remote`
- **Build Plugins:** Maven Failsafe Plugin for integration testing

### openshift
- **Purpose:** Package application for OpenShift deployment
- **Plugins:** EAP Maven Plugin with specified channels, feature packs, and layers
- **Output:** `ROOT.war` file

# Additional Notes

- Deprecated datasource configuration files are used for convenience but are unsupported in production.
- The documentation emphasizes environment setup, deployment commands, and testing procedures for both local and cloud environments.

# Overview of `README.adoc` for Kitchensink Quickstart

This document provides comprehensive guidance for deploying and testing the Kitchensink quickstart application across different environments, including local servers, OpenShift, and Helm charts. It covers:

- **Project Description**  
  Demonstrates a web-enabled database application using Java EE technologies (JSF, CDI, EJB, JPA, Bean Validation).

- **Configuration and Environment Setup**  
  Details product-specific attributes for JBoss EAP, EAP XP, and WildFly, including versioning, repository URLs, and platform-specific settings.

- **System Requirements**  
  Lists prerequisites such as Java SDK 11+, Maven 3.6.0+, and optional database configurations.

- **Server Management**  
  Instructions for starting, stopping, and configuring standalone servers with various profiles (default, full, ha, microprofile, custom).

- **Build and Deployment**  
  Guidelines for building, deploying, and undeploying the application using Maven commands and archive configurations.

- **Testing Procedures**  
  Explains how to run Arquillian integration tests locally and on OpenShift, including environment setup and SSL considerations.

- **OpenShift and Helm Integration**  
  Provides steps for building, deploying, and managing the application on OpenShift with Helm charts, including prerequisites, Helm repository setup, and route access.

- **Additional Resources**  
  Links to official documentation, guides, and related tools such as CodeReady Studio and OpenShift.

This structured overview facilitates understanding of deployment workflows, environment configurations, and testing strategies for the Kitchensink quickstart.

## Overview

The `kitchensink` quickstart showcases a comprehensive Java web application using {javaVersion} and {productNameFull}. It integrates multiple technologies including CDI, JSF, JPA, EJB, JAX-RS, and Bean Validation, with a focus on database access and enterprise Java development.

## Key Features

- Deployable Maven 3 project with WAR packaging
- Demonstrates creating a compliant {javaVersion} application
- Includes persistence unit and sample database transactions

## Building and Deployment

- Instructions for building and deploying on a {productName} server distribution
- Access URL: `http://localhost:8080/{artifactId}/`
- Server log notes on deprecated features

## Testing and Management

- Guidance on running Arquillian integration tests
- Procedures for undeploying the application
- Additional build and run options for different environments (e.g., OpenShift, provisioned servers)

## Additional Resources

- System requirements
- Development shortcuts
- Use of {jbossHomeName} in configurations

# Utilities: Checkstyle Result Summary

- **File Path:** `/Users/dre/dev/jboss-eap-quickstarts/kitchensink/target/checkstyle-result.xml`
- **Category:** Utilities
- **Description:**  
  An empty Checkstyle report indicating no style violations detected.  
- **Key Elements:**  
  - XML version and encoding declaration  
  - `<checkstyle>` root element with version attribute (8.5)

# Checkstyle Configuration

This file defines the Checkstyle rules for code quality enforcement in the project.

## Main Components
- **Checker Module:** The root module managing all checks.
- **FileTabCharacter:** Ensures no tab characters are used.
- **RegexpSingleline:** Detects trailing spaces at line ends.
- **TreeWalker:** Contains core coding style and quality checks, including:
  - Import management (`AvoidStarImport`, `RedundantImport`, `UnusedImports`, `IllegalImport`)
  - Modifier order and redundancy (`ModifierOrder`, `RedundantModifier`)
  - Block formatting (`LeftCurly`)
  - Common coding problems (`EmptyStatement`, `IllegalInstantiation`)
  - Miscellaneous rules (`UpperEll`, `PackageAnnotation`, `ArrayTypeStyle`, `SuppressWarningsHolder`)
  - Warnings suppression (`SuppressWarnings`, `SuppressWarningsFilter`)
- **SuppressionFilter:** Applies external suppression rules from specified XML.
- **SuppressWarningsFilter:** Handles suppression annotations in code.

This configuration helps maintain consistent coding standards and suppresses specific warnings as needed.

# Configuration Overview

This file defines an unmanaged datasource for testing purposes in JBoss EAP.

## Key Elements
- **Datasource JNDI Name:** `java:jboss/datasources/KitchensinkQuickstartTestDS`
- **Pool Name:** `kitchensink-quickstart-test`
- **Enabled:** `true`
- **Connection URL:** In-memory H2 database (`jdbc:h2:mem:kitchensink-quickstart-test`)
- **Driver:** `h2`
- **Security Credentials:** Username `sa`, Password `sa`

## Usage
- Bound into JNDI for lookup in `META-INF/test-persistence.xml`.
- Intended for proofs of concept or testing only, not for production use.

# Arquillian Configuration

Defines the setup for Arquillian testing with JBoss EAP:

- **Namespaces and Schema**: Uses specific XML namespaces and schema location for validation.
- **Test Archive Export**: Optional configuration (commented out) to export test archives for inspection.
- **Container Configuration**:
  - **Qualifier**: "jboss"
  - **Default**: true
  - **JBoss EAP Location**:
    - Uses `JBOSS_HOME` environment variable by default.
    - Optional property (commented out) to specify custom `jbossHome` path.

# test-persistence.xml

## Overview
This XML configuration file defines persistence settings for a Java application using JPA (Java Persistence API). It specifies the persistence unit, data source, and Hibernate properties.

## Main Components

### Persistence Element
- **version**: Specifies the version of the persistence configuration, set to `"2.0"`.
- **xmlns**: Namespace for JPA persistence schema.
- **xsi:schemaLocation**: Location of the XML schema for validation.

### Persistence Unit
- **name**: Identifier for the persistence unit, set to `"primary"`.

### Data Source Configuration
- **jta-data-source**: Specifies the JTA data source used for database interactions.
  - Value: `java:jboss/datasources/KitchensinkQuickstartTestDS`
  - Note: Uses an unmanaged, in-memory H2 database for testing purposes. Production should use a managed data source.

### Properties
- **hibernate.hbm2ddl.auto**: Set to `"create-drop"` to automatically create and drop database schemas during testing.
- **hibernate.show_sql**: Set to `"false"` to disable SQL statement logging.

## Usage Notes
- Designed for testing environments with an in-memory database.
- Production applications should modify the data source and Hibernate properties accordingly.

# Persistence Import Script

This SQL script is used for seeding the database with initial data.  
**Key features include:**  
- **Insert Statement:** Adds a record to the `Member` table with fields for `id`, `name`, `email`, and `phone_number`.  
- **Usage:** Executed to initialize or populate the database during setup or testing.

# Persistence Configuration

Defines the persistence unit for the application with the following key elements:

- **Persistence Namespace and Schema**: Uses Jakarta Persistence 3.0 schema.
- **Persistence Unit Name**: `primary`.
- **Data Source**: Managed JTA data source `java:jboss/datasources/KitchensinkQuickstartDS`.
- **Properties**:
  - Hibernate auto schema generation set to `create-drop`.
  - SQL logging disabled (`show_sql = false`).

## Configuration Details

- **Artifact ID:** `kitchensink`
- **Group ID:** `org.jboss.eap.quickstarts`
- **Version:** `8.0.0.GA`

# Checkstyle Results Documentation

## Overview
Provides the results of Checkstyle analysis using the `wildfly-checkstyle/checkstyle.xml` ruleset, specifically version 8.5.

## Main Sections
- **Summary**: Displays total files, info messages, warnings, and errors detected.
- **Files**: Lists individual files with associated issue counts.
- **Rules**: Details categories, specific rules, violations, and severity levels.
- **Details**: Additional in-depth information about the checkstyle analysis.

## Additional Information
- Last published date: 2025-05-18
- Project version: 8.0.0.GA
- External link to Checkstyle: [Checkstyle](http://checkstyle.sourceforge.net/)

# Index Page Overview

- **Purpose:** Serves as the entry point redirecting users to the main application.
- **Main Functionality:** Automatically redirects to `index.jsf` upon page load.
- **Technical Details:** Implements a meta refresh tag for redirection.
- **Legal & Licensing:** Contains licensing information for JBoss and Red Hat.

# Index.xhtml Overview

This XHTML file serves as the main user interface for the JBoss Kitchen Sink application, demonstrating Jakarta EE features.

## Structure and Components

- **Template**: Extends `default.xhtml` layout.
- **Content Section**:
  - Welcome message.
  - Deployment confirmation.

## Member Registration Form

- **Form ID**: `reg`
- **Fields**:
  - Name (`#{newMember.name}`)
  - Email (`#{newMember.email}`)
  - Phone Number (`#{newMember.phoneNumber}`)
- **Validation**: Enforces annotation-based constraints.
- **Actions**:
  - Register button triggers `#{memberController.register}`.
  - Displays validation messages.

## Members List

- **Conditional Rendering**:
  - Shows message if no members registered.
  - Displays data table if members exist.
- **Data Table**:
  - Columns: Id, Name, Email, Phone Number, REST URL.
  - REST URL links for individual members and all members.
- **Footer**:
  - Provides link to REST endpoint for all members.

# beans.xml Configuration

- **Purpose:** Marker file to enable Contexts and Dependency Injection (CDI)
- **Namespace:** Java EE namespace for beans configuration
- **Schema:** References to beans schema for validation
- **Bean Discovery Mode:** Set to `all` to include all beans for CDI
- **Additional Info:** Contains licensing and copyright comments

# Faces Configuration (`faces-config.xml`)

## Purpose
- Activates the JavaServer Faces (JSF) servlet.
- Serves as the main configuration file for JSF applications.

## Key Elements
- **Namespace declarations**:
  - Default namespace for Java EE 4.0.
  - Schema location for validation.
- **Version**: 4.0

## Customization
- Placeholder for defining navigation rules.
- Encourages use of CDI for managed beans via `@Named`.

## Notes
- Optional file; only needed for additional configuration beyond defaults.

# Data Source Configuration

Defines an unmanaged in-memory H2 database datasource for testing purposes.

## Key Elements
- **JNDI Name:** `java:jboss/datasources/KitchensinkQuickstartDS`
- **Pool Name:** `kitchensink-quickstart`
- **Enabled:** `true`
- **Connection URL:** `jdbc:h2:mem:kitchensink-quickstart;DB_CLOSE_ON_EXIT=FALSE;DB_CLOSE_DELAY=-1`
- **Driver:** `h2`
- **Security Credentials:** username `sa`, password `sa`

## Usage
- Referenced in `META-INF/persistence.xml` for database connectivity.
- Intended solely for testing or proof-of-concept environments; not suitable for production.

# Persistence Import Script

This SQL script is used for seeding initial data into the database.  
**Key features include:**  
- Insertion of sample data into the `Member` table  
- Defines fields such as `id`, `name`, `email`, and `phone_number`.  
- Facilitates database setup during application deployment.

# Persistence Configuration

Defines the JPA persistence unit for the application.

## Key Elements
- **Persistence Unit Name:** `primary`
- **Data Source:** `java:jboss/datasources/KitchensinkQuickstartDS`
- **Properties:**
  - Hibernate schema management: `create-drop`
  - SQL logging: disabled (`show_sql` = false)

## Schema
- Uses Jakarta Persistence (JPA) 3.0 schema
- XML namespace and schema location specified for validation

# index.html Overview

- **Purpose:** Serves as a plain HTML entry point redirecting to the JSF application.
- **Key Features:**
  - Contains licensing and copyright information.
  - Implements an automatic redirect to `index.jsf` using a meta refresh tag.
- **Public Interface:** Minimal, primarily the redirect mechanism for app initialization.

# Index.xhtml Overview

This file defines the main user interface for the JBoss Quickstart application using Facelets templating.

## Structure and Components

- **Template**: Extends `/WEB-INF/templates/default.xhtml`.
- **Content Section**:
  - Welcome message and deployment confirmation.
  - **Member Registration Form**:
    - Input fields for Name, Email, and Phone Number.
    - Validation messages for each input.
    - Register button triggering `memberController.register`.
  - **Members List**:
    - Conditional display: shows "No registered members" if empty.
    - Data table listing member details:
      - ID, Name, Email, Phone Number.
      - REST URL link for each member.
    - Footer with URL for all members REST endpoint.

## Key Features

- Utilizes Jakarta Faces components (`h:form`, `h:dataTable`, `h:commandButton`, etc.).
- Implements validation and messaging.
- Dynamic rendering based on data availability.
- Links to RESTful services for member data.

# beans.xml Configuration

- **Purpose:** Marker file to enable Contexts and Dependency Injection (CDI)
- **Root Element:** `<beans>`
- **Namespaces:**
  - Java EE namespace (`http://xmlns.jcp.org/xml/ns/javaee`)
  - XML Schema Instance namespace
- **Attributes:**
  - `bean-discovery-mode="all"`: Specifies CDI bean discovery mode as 'all'
- **Comments:**
  - Licensing information and purpose of the file

# `faces-config.xml` Overview

- **Purpose:** Configures JavaServer Faces (JSF) settings for the application.
- **Namespaces and Schema:**
  - Uses `http://xmlns.jcp.org/xml/ns/javaee` namespace.
  - Schema location points to Jakarta EE 4.0.
- **Main Elements:**
  - `<faces-config>`: Root element specifying version 4.0.
  - Comments indicate:
    - Activation of the JSF Servlet.
    - Placeholder for navigation rules.
    - Recommendation to use CDI for managed beans.
- **Additional Notes:**
  - Not required if no extra configuration is needed.

## Data Source Configuration

Defines an unmanaged, in-memory H2 datasource for testing purposes.

### Key Elements
- **JNDI Name:** `java:jboss/datasources/KitchensinkQuickstartDS`
- **Pool Name:** `kitchensink-quickstart`
- **Enabled:** `true`
- **Connection URL:** `jdbc:h2:mem:kitchensink-quickstart;DB_CLOSE_ON_EXIT=FALSE;DB_CLOSE_DELAY=-1`
- **Driver:** `h2`
- **Security Credentials:** username `sa`, password `sa`

### Notes
- Used for testing or proof of concept only.
- Not suitable for production environments.

# Default XHTML Template

This file defines the main layout for the web application using JSF Facelets.

## Structure
- **Head Section**
  - Sets page title (`kitchensink`)
  - Includes meta tags for character encoding
  - Links to external stylesheet (`css/screen.css`)
- **Body Section**
  - Container `<div>` with ID `container`
    - **Branding**
      - Logo image (`resources/gfx/rhjb_eap_logo.png`)
    - **Content Area**
      - `<ui:insert>` named "content" for dynamic content insertion
    - **Aside Section**
      - Links to documentation and product information about Red Hat JBoss EAP
    - **Footer**
      - Notes project origin from a Maven archetype by JBoss

# Resources.java

## Overview
The `Resources` class provides CDI (Contexts and Dependency Injection) producers for Jakarta EE resources, enabling injection of persistence contexts and loggers into application components.

## Package
`org.jboss.as.quickstarts.kitchensink.util`

## Public API

### Fields

- `EntityManager em`
  - **Annotations:** `@Produces`, `@PersistenceContext`
  - **Description:** Produces an `EntityManager` instance linked to the persistence context, allowing injection into other CDI-managed beans.

### Methods

- `Logger produceLog(InjectionPoint injectionPoint)`
  - **Annotations:** `@Produces`
  - **Parameters:** 
    - `InjectionPoint injectionPoint` – provides metadata about the injection point.
  - **Returns:** 
    - `Logger` – a logger instance named after the class where injection occurs.
  - **Description:** Produces a `Logger` object for injection, facilitating logging with context-specific naming.

## Usage
- Enables injection of `EntityManager` and `Logger` into CDI-managed beans.
- Example injection:
  ```java
  @Inject
  private EntityManager em;

  @Inject
  private Logger log;
  ```

# MemberController

The `MemberController` class manages the registration process for members within the application. It is a request-scoped bean with an EL name, facilitating interaction with the user interface.

## Annotations

- `@Model`: Combines `@Named` and `@RequestScoped`, making this bean accessible in EL expressions and scoped to a single HTTP request.

## Injected Dependencies

- `FacesContext`: Provides context for JSF (JavaServer Faces) operations, such as adding messages.
- `MemberRegistration`: Service responsible for handling member registration logic.

## Produced Properties

- `newMember`: A `Member` instance representing the member being registered, available for injection and EL expressions.

## Lifecycle Methods

- `@PostConstruct initNewMember()`: Initializes `newMember` as a new `Member` object when the bean is constructed.

## Public Methods

- `register()`: Handles the registration process.
  - Calls `memberRegistration.register(newMember)` to perform registration.
  - Adds a success message to the FacesContext upon successful registration.
  - Reinitializes `newMember` for potential subsequent registrations.
  - Handles exceptions by retrieving the root error message and adding an error message to FacesContext.

## Private Methods

- `getRootErrorMessage(Exception e)`: Extracts the root cause message from an exception.
  - Recursively traverses the exception cause chain.
  - Returns the localized message of the deepest cause or a default error message if none is available.

# Member Class

The `Member` class is a data model representing a member entity within the application. It is designed for persistence in a relational database and includes validation constraints for its fields.

## Class Overview

- **Package:** `org.jboss.as.quickstarts.kitchensink.model`
- **Annotations:**
  - `@Entity` — Marks the class as a JPA entity.
  - `@XmlRootElement` — Enables XML serialization.
  - `@Table` — Specifies table constraints, including a unique constraint on the `email` column.
- **Implements:** `Serializable` — Allows instances to be serialized.

## Key Attributes

### `id`
- **Type:** `Long`
- **Annotations:**
  - `@Id` — Denotes primary key.
  - `@GeneratedValue` — Specifies auto-generation of the ID.

### `name`
- **Type:** `String`
- **Validation Constraints:**
  - `@NotNull` — Cannot be null.
  - `@Size(min=1, max=25)` — Length must be between 1 and 25 characters.
  - `@Pattern(regexp = "[^0-9]*", message = "Must not contain numbers")` — Must not contain numeric characters.

### `email`
- **Type:** `String`
- **Validation Constraints:**
  - `@NotNull` — Cannot be null.
  - `@NotEmpty` — Cannot be empty.
  - `@Email` — Must be a valid email format.
- **Database Constraint:** Unique email addresses (`@Table(uniqueConstraints = ...)`).

### `phoneNumber`
- **Type:** `String`
- **Validation Constraints:**
  - `@NotNull` — Cannot be null.
  - `@Size(min=10, max=12)` — Length must be between 10 and 12 characters.
  - `@Digits(fraction=0, integer=12)` — Must be numeric with up to 12 digits.
- **Column Name:** `phone_number`

## Accessor Methods

- **Getters and Setters:**
  - `getId()`, `setId(Long id)`
  - `getName()`, `setName(String name)`
  - `getEmail()`, `setEmail(String email)`
  - `getPhoneNumber()`, `setPhoneNumber(String phoneNumber)`

# MemberRegistration Class

The `MemberRegistration` class handles the business logic related to registering new members within the application.

## Class Overview

- **Package:** `org.jboss.as.quickstarts.kitchensink.service`
- **Annotations:** `@Stateless`
  - Indicates that this is a stateless session bean, which manages business logic without maintaining conversational state.

## Dependencies

- **Logger (`log`)**
  - Injected for logging informational messages.
- **EntityManager (`em`)**
  - Injected for performing persistence operations on entities.
- **Event (`memberEventSrc`)**
  - Injected event source for firing events related to `Member` entities.

## Public Methods

### `register(Member member)`

- **Purpose:** Registers a new member by persisting the member entity and firing a registration event.
- **Parameters:** 
  - `member` - The `Member` entity to be registered.
- **Throws:** 
  - `Exception` - Propagates any exceptions that occur during registration.
- **Behavior:**
  - Logs the registration process.
  - Persists the `Member` entity to the database.
  - Fires an event to notify other components of the new registration.

## MemberListProducer

### Class Overview
`MemberListProducer` is a request-scoped CDI (Contexts and Dependency Injection) bean responsible for producing a list of `Member` entities for use in the application's presentation layer. It observes changes to `Member` entities and updates the list accordingly.

### Annotations
- `@RequestScoped`: Defines the bean's lifecycle to be tied to an HTTP request.
- `@Produces`: Indicates that the method produces a bean that can be injected or referenced in EL expressions.
- `@Named`: Makes the produced list accessible via Expression Language (EL) with the default name `members`.
- `@PostConstruct`: Marks the method to be executed after dependency injection is complete, initializing the members list.
- `@Observes`: Listens for events of type `Member` to trigger updates to the list.
- `@Inject`: Injects dependencies, specifically the `MemberRepository`.

### Public Methods
- `getMembers()`: Returns the current list of `Member` objects for UI rendering.
- `onMemberListChanged(Member member)`: Observes `Member` change events and refreshes the list when a change occurs.
- `retrieveAllMembersOrderedByName()`: Retrieves all `Member` entities from the repository, ordered by name, and updates the internal list.

### Dependencies
- `MemberRepository`: Injected repository used to fetch `Member` data from the data source.

### Lifecycle
- Initialization occurs after construction via `@PostConstruct`, loading all members ordered by name.
- List updates are triggered by observing `Member` change events, ensuring the UI reflects the latest data.

# MemberRepository

The `MemberRepository` class provides data access methods for `Member` entities within the application. It is designed with application scope and utilizes dependency injection for entity management.

## Class Overview

- **Package:** `org.jboss.as.quickstarts.kitchensink.data`
- **Scope:** ApplicationScoped
- **Dependencies:**
  - `EntityManager` for persistence operations
  - JPA Criteria API for building type-safe queries
  - `Member` entity class

## Public Methods

### `findById(Long id)`
- **Description:** Retrieves a `Member` entity by its unique identifier.
- **Parameters:**
  - `id` (Long): The primary key of the member.
- **Returns:** `Member` object matching the provided ID.

### `findByEmail(String email)`
- **Description:** Finds a `Member` entity based on the email address.
- **Parameters:**
  - `email` (String): The email address to search for.
- **Returns:** `Member` object with the specified email.
- **Notes:** Utilizes JPA Criteria API for constructing the query, with a commented-out alternative for type-safe criteria queries.

### `findAllOrderedByName()`
- **Description:** Retrieves a list of all `Member` entities ordered alphabetically by name.
- **Returns:** `List<Member>` sorted by name.
- **Notes:** Uses JPA Criteria API to define ordering, with an alternative commented out for type-safe criteria queries.

## Usage Notes

- The class relies on dependency injection to obtain the `EntityManager`.
- Queries are constructed using JPA Criteria API for flexibility and type safety.
- The class is intended for use within Java EE or Jakarta EE applications with container-managed persistence context.

# JaxRsActivator Class

- **Purpose:** Activates JAX-RS in the application using the "no XML" approach.
- **Annotations:**
  - `@ApplicationPath("/rest")`: Sets the base URI for REST resources.
- **Inheritance:** Extends `jakarta.ws.rs.core.Application`.
- **Implementation Details:** Empty class body, serving as a configuration point for JAX-RS activation.

# MemberResourceRESTService

This class provides a RESTful web service for managing members, including listing, retrieving, and creating member records.

## Class Declaration
- **Path**: `/members`
- **Scope**: RequestScoped
- **Purpose**: Handles HTTP requests related to member entities.

## Dependencies
- **Logger**: Injected for logging purposes.
- **Validator**: Bean validation for member data.
- **MemberRepository**: Data access layer for member entities.
- **MemberRegistration**: Service for registering new members.

## Public Methods

### listAllMembers
- **HTTP Method**: GET
- **Produces**: `application/json`
- **Description**: Retrieves a list of all members ordered by name.

### lookupMemberById
- **HTTP Method**: GET
- **Path**: `/{id}`
- **Path Parameter**: `id` (numeric)
- **Produces**: `application/json`
- **Description**: Retrieves a member by their unique ID. Throws a 404 error if not found.

### createMember
- **HTTP Method**: POST
- **Consumes**: `application/json`
- **Produces**: `application/json`
- **Description**: Creates a new member record. Performs validation and handles potential errors, returning appropriate HTTP responses.

## Private Methods

### validateMember
- **Purpose**: Validates a member object using bean validation and checks for email uniqueness.
- **Throws**:
  - `ConstraintViolationException` for validation errors.
  - `ValidationException` if email already exists.

### createViolationResponse
- **Purpose**: Constructs a bad request response containing validation error details.
- **Input**: Set of constraint violations.
- **Output**: Response builder with error details.

### emailAlreadyExists
- **Purpose**: Checks if a member with the given email is already registered.
- **Input**: Email address.
- **Output**: Boolean indicating existence.