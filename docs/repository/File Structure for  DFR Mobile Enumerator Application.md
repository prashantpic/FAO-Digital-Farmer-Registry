# Specification

# 1. Files

- **Path:** pubspec.yaml  
**Description:** Flutter project's manifest file, defining dependencies, assets, fonts, and project metadata. Essential for managing project setup and build configurations.  
**Template:** Flutter Project Configuration  
**Dependancy Level:** 0  
**Name:** pubspec  
**Type:** Configuration  
**Relative Path:** ../pubspec.yaml  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Project Dependency Management
    - Asset Declaration
    - Flutter SDK Version Constraint
    
**Requirement Ids:**
    
    - REQ-4-001
    - REQ-4-004
    
**Purpose:** To declare project dependencies (e.g., sqflite, dio, flutter_bloc, sqlcipher_flutter_libs, geolocator, mobile_scanner, flutter_secure_storage), assets, and configure project settings.  
**Logic Description:** Specifies library versions for all third-party packages. Lists paths to assets like images, fonts, and localization files. Defines Flutter SDK constraints and project name/description. Ensure it includes dependencies for SQLite, SQLCipher, REST client, BLoC, GPS, QR scanner, and secure storage.  
**Documentation:**
    
    - **Summary:** Defines project metadata, dependencies (sqflite, SQLCipher, Dio, flutter_bloc, etc.), and asset paths for the DFR Mobile App. Essential for Flutter's build system.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** Configuration
    
- **Path:** android/app/build.gradle  
**Description:** Android-specific build configuration file. Defines Android SDK versions, application ID, dependencies, and build variants for the Android part of the Flutter application.  
**Template:** Gradle Build Script  
**Dependancy Level:** 0  
**Name:** build.gradle  
**Type:** Configuration  
**Relative Path:** ../android/app/build.gradle  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Android Build Configuration
    - SDK Version Management
    
**Requirement Ids:**
    
    - REQ-4-001
    
**Purpose:** To configure Android-specific build settings, including min SDK version (API 26 for Android 8.0 Oreo), target SDK version, and application ID.  
**Logic Description:** Sets `minSdkVersion` to 26. Configures `defaultConfig` with application ID, target SDK version. Includes dependencies required for SQLCipher native libraries if necessary.  
**Documentation:**
    
    - **Summary:** Manages Android build settings, ensuring compatibility with Android 8.0 (API 26) and above.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** PlatformConfiguration
    
- **Path:** android/app/src/main/AndroidManifest.xml  
**Description:** Core manifest file for the Android application. Declares application components, permissions (e.g., internet, location, camera), and other essential metadata.  
**Template:** Android Manifest XML  
**Dependancy Level:** 0  
**Name:** AndroidManifest.xml  
**Type:** Configuration  
**Relative Path:** ../android/app/src/main/AndroidManifest.xml  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    
**Implemented Features:**
    
    - Android App Permissions
    - Application Component Declaration
    
**Requirement Ids:**
    
    - REQ-PCA-006
    - REQ-4-001
    
**Purpose:** To declare necessary permissions for network access (for sync), location (GPS capture), camera (QR scanning), and define application components.  
**Logic Description:** Includes `<uses-permission>` tags for `android.permission.INTERNET`, `android.permission.ACCESS_FINE_LOCATION`, `android.permission.CAMERA`. Defines the main application class and activities as per Flutter project structure.  
**Documentation:**
    
    - **Summary:** Defines Android application permissions (Internet, Location, Camera) and core components.
    
**Namespace:**   
**Metadata:**
    
    - **Category:** PlatformConfiguration
    
- **Path:** lib/main.dart  
**Description:** The main entry point for the Flutter application. Initializes essential services, dependency injection, and runs the root application widget.  
**Template:** Dart Application Entry Point  
**Dependancy Level:** 0  
**Name:** main  
**Type:** EntryPoint  
**Relative Path:** main.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    
**Methods:**
    
    - **Name:** main  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** public|static|async  
    
**Implemented Features:**
    
    - App Initialization
    - Dependency Injection Setup
    
**Requirement Ids:**
    
    - REQ-4-001
    
**Purpose:** To initialize the Flutter application, set up dependency injection (e.g., GetIt), initialize localization, and launch the main `App` widget.  
**Logic Description:** Calls `WidgetsFlutterBinding.ensureInitialized()`. Sets up any global error handling. Initializes dependency injection container (e.g., GetIt). Calls `runApp()` with the main `App` widget.  
**Documentation:**
    
    - **Summary:** Main entry point of the DFR Mobile App. Initializes essential services and runs the root `App` widget.
    
**Namespace:** com.fao.dfr.mobile  
**Metadata:**
    
    - **Category:** Application
    
- **Path:** lib/app.dart  
**Description:** The root widget of the Flutter application. Sets up MaterialApp, theme, localization, and initial navigation.  
**Template:** Flutter Root Widget  
**Dependancy Level:** 1  
**Name:** App  
**Type:** Widget  
**Relative Path:** app.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    - MVC
    
**Members:**
    
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** public|override  
    
**Implemented Features:**
    
    - App Theme Configuration
    - Localization Setup
    - Root Navigation
    
**Requirement Ids:**
    
    - REQ-4-002
    
**Purpose:** To define the root `MaterialApp` widget, configure global theme, set up localization delegates, and manage initial routing or navigation stack.  
**Logic Description:** Returns a `MaterialApp` widget. Configures `theme` using `AppTheme`. Sets up `localizationsDelegates` and `supportedLocales`. Defines initial routes or uses a router like GoRouter for navigation.  
**Documentation:**
    
    - **Summary:** Root Flutter widget defining the `MaterialApp`, theme, localization, and navigation for the DFR Mobile App.
    
**Namespace:** com.fao.dfr.mobile  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/core/theme/app_theme.dart  
**Description:** Defines the application's visual theme, including color schemes, typography, and component styling, adhering to Material Design guidelines.  
**Template:** Dart Class Template  
**Dependancy Level:** 0  
**Name:** AppTheme  
**Type:** Theme  
**Relative Path:** core/theme/app_theme.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** lightTheme  
**Type:** ThemeData  
**Attributes:** public|static  
    - **Name:** darkTheme  
**Type:** ThemeData  
**Attributes:** public|static  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Material Design Theming
    - Color Palette Definition
    - Typography Styles
    
**Requirement Ids:**
    
    - REQ-4-002
    
**Purpose:** To provide consistent styling across the application. Defines primary colors, accent colors, text styles, button themes, input decoration themes, etc.  
**Logic Description:** Contains static methods or constants returning `ThemeData` objects for light and dark themes. Defines `ColorScheme`, `TextTheme`, and styles for common widgets to ensure a user-friendly interface optimized for field data collection and adhering to Material Design.  
**Documentation:**
    
    - **Summary:** Provides centralized theme definitions (colors, typography, component styles) for the DFR Mobile App.
    
**Namespace:** com.fao.dfr.mobile.core.theme  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/core/database/database_helper.dart  
**Description:** Manages the local SQLite database, including schema creation, versioning, and providing a database instance. Integrates SQLCipher for encryption.  
**Template:** Dart Class Template  
**Dependancy Level:** 1  
**Name:** DatabaseHelper  
**Type:** DatabaseHelper  
**Relative Path:** core/database/database_helper.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    - Singleton
    
**Members:**
    
    - **Name:** _database  
**Type:** Database?  
**Attributes:** private|static  
    - **Name:** dbName  
**Type:** String  
**Attributes:** private|static|final  
    - **Name:** dbVersion  
**Type:** int  
**Attributes:** private|static|final  
    
**Methods:**
    
    - **Name:** database  
**Parameters:**
    
    
**Return Type:** Future<Database>  
**Attributes:** public|async  
    - **Name:** _initDatabase  
**Parameters:**
    
    - String encryptionKey
    
**Return Type:** Future<Database>  
**Attributes:** private|async  
    - **Name:** _onCreate  
**Parameters:**
    
    - Database db
    - int version
    
**Return Type:** Future<void>  
**Attributes:** private|async  
    - **Name:** _onUpgrade  
**Parameters:**
    
    - Database db
    - int oldVersion
    - int newVersion
    
**Return Type:** Future<void>  
**Attributes:** private|async  
    - **Name:** close  
**Parameters:**
    
    
**Return Type:** Future<void>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Local SQLite Database Management
    - Schema Creation & Migration
    - SQLCipher Integration for Encryption
    
**Requirement Ids:**
    
    - REQ-4-003
    - REQ-4-004
    
**Purpose:** To provide a singleton instance of the encrypted SQLite database. Handles database initialization, schema creation for all local tables (Farmer, Plot, FormDefinition, FormSubmission, etc.), and schema migrations if needed.  
**Logic Description:** Uses `sqflite` and `sqlcipher_flutter_libs`. The `_initDatabase` method opens the database with an encryption key (fetched from secure storage). `_onCreate` executes `CREATE TABLE` statements for all entities needed for offline operation. `_onUpgrade` handles schema changes between versions. Provides access to the `Database` object for DAOs.  
**Documentation:**
    
    - **Summary:** Manages the encrypted local SQLite database using SQLCipher for offline data storage.
    
**Namespace:** com.fao.dfr.mobile.core.database  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** lib/core/database/encryption_service.dart  
**Description:** Manages the retrieval and provision of the encryption key for SQLCipher, typically by interacting with Secure Storage.  
**Template:** Dart Class Template  
**Dependancy Level:** 1  
**Name:** EncryptionService  
**Type:** Service  
**Relative Path:** core/database/encryption_service.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _secureStorageService  
**Type:** SecureStorageService  
**Attributes:** private|final  
    
**Methods:**
    
    - **Name:** getDatabaseEncryptionKey  
**Parameters:**
    
    
**Return Type:** Future<String>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Database Encryption Key Management
    
**Requirement Ids:**
    
    - REQ-4-004
    
**Purpose:** To securely retrieve or generate and store the encryption key used by SQLCipher to encrypt the local database.  
**Logic Description:** Interacts with `SecureStorageService` to read an existing encryption key or generate a new one if not found and store it securely. This key is then provided to `DatabaseHelper` for initializing SQLCipher.  
**Documentation:**
    
    - **Summary:** Provides the encryption key for the local SQLCipher database, fetching it from secure storage.
    
**Namespace:** com.fao.dfr.mobile.core.database  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** lib/core/security/secure_storage_service.dart  
**Description:** A wrapper around flutter_secure_storage to securely store sensitive data like encryption keys using platform-provided mechanisms (Android Keystore).  
**Template:** Dart Class Template  
**Dependancy Level:** 0  
**Name:** SecureStorageService  
**Type:** Service  
**Relative Path:** core/security/secure_storage_service.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _storage  
**Type:** FlutterSecureStorage  
**Attributes:** private|final  
    
**Methods:**
    
    - **Name:** write  
**Parameters:**
    
    - String key
    - String value
    
**Return Type:** Future<void>  
**Attributes:** public|async  
    - **Name:** read  
**Parameters:**
    
    - String key
    
**Return Type:** Future<String?>  
**Attributes:** public|async  
    - **Name:** delete  
**Parameters:**
    
    - String key
    
**Return Type:** Future<void>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Secure Data Storage
    - Encryption Key Persistence
    
**Requirement Ids:**
    
    - REQ-4-004
    
**Purpose:** To provide a secure mechanism for storing the database encryption key and potentially other sensitive app data, leveraging platform keystore capabilities.  
**Logic Description:** Uses the `flutter_secure_storage` plugin to interact with Android Keystore (or iOS Keychain). Provides methods to write, read, and delete key-value pairs securely.  
**Documentation:**
    
    - **Summary:** Provides secure storage for sensitive data like encryption keys using `flutter_secure_storage`.
    
**Namespace:** com.fao.dfr.mobile.core.security  
**Metadata:**
    
    - **Category:** Security
    
- **Path:** lib/core/network/api_client.dart  
**Description:** Sets up and configures the HTTP client (e.g., Dio) for making requests to the DFR backend API. Handles base URL, headers, interceptors.  
**Template:** Dart Class Template  
**Dependancy Level:** 1  
**Name:** ApiClient  
**Type:** NetworkClient  
**Relative Path:** core/network/api_client.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** dio  
**Type:** Dio  
**Attributes:** public|final  
    
**Methods:**
    
    - **Name:** ApiClient  
**Parameters:**
    
    - String baseUrl
    
**Return Type:**   
**Attributes:** public  
    - **Name:** addAuthInterceptor  
**Parameters:**
    
    - Interceptor interceptor
    
**Return Type:** void  
**Attributes:** public  
    
**Implemented Features:**
    
    - HTTP Client Configuration
    - API Base URL Setup
    - Request Interception (e.g., for auth tokens)
    
**Requirement Ids:**
    
    - REQ-4-006
    
**Purpose:** To provide a configured instance of an HTTP client (Dio) for all API communications. Sets base URL from app config, and allows adding interceptors for logging, authentication tokens, etc.  
**Logic Description:** Initializes a `Dio` instance with `BaseOptions` (baseUrl, connectTimeout, receiveTimeout). Includes methods to add interceptors dynamically (e.g., an `AuthInterceptor` to add JWT tokens to headers).  
**Documentation:**
    
    - **Summary:** Configures and provides the Dio HTTP client for API communication with the DFR backend.
    
**Namespace:** com.fao.dfr.mobile.core.network  
**Metadata:**
    
    - **Category:** Network
    
- **Path:** lib/core/network/dfr_api_service.dart  
**Description:** Defines the abstract interface or concrete implementation for interacting with DFR backend REST APIs related to synchronization and data exchange.  
**Template:** Dart Class Template  
**Dependancy Level:** 2  
**Name:** DfrApiService  
**Type:** ApiService  
**Relative Path:** core/network/dfr_api_service.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _apiClient  
**Type:** ApiClient  
**Attributes:** private|final  
    
**Methods:**
    
    - **Name:** syncFarmerData  
**Parameters:**
    
    - List<FarmerModel> farmersToSync
    
**Return Type:** Future<SyncResponseModel>  
**Attributes:** public|async  
    - **Name:** syncFormSubmissions  
**Parameters:**
    
    - List<FormSubmissionModel> submissionsToSync
    
**Return Type:** Future<SyncResponseModel>  
**Attributes:** public|async  
    - **Name:** getFormDefinitions  
**Parameters:**
    
    
**Return Type:** Future<List<FormDefinitionModel>>  
**Attributes:** public|async  
    - **Name:** getUpdatedFarmerData  
**Parameters:**
    
    - String lastSyncTimestamp
    
**Return Type:** Future<List<FarmerModel>>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - API Endpoint Definitions for Sync
    - Data Serialization/Deserialization for API
    
**Requirement Ids:**
    
    - REQ-PCA-006
    - REQ-4-006
    
**Purpose:** To abstract the communication with specific DFR backend API endpoints used for bi-directional data synchronization. Handles request building and response parsing.  
**Logic Description:** Uses the `ApiClient` to make HTTP requests (POST, GET) to defined backend API routes for syncing farmer data, form submissions, and fetching form definitions and updated records. Handles JSON serialization/deserialization.  
**Documentation:**
    
    - **Summary:** Provides methods to interact with DFR backend APIs for data synchronization.
    
**Namespace:** com.fao.dfr.mobile.core.network  
**Metadata:**
    
    - **Category:** Network
    
- **Path:** lib/features/farmer_registration/data/datasources/farmer_local_datasource.dart  
**Description:** Data Access Object (DAO) for Farmer entities, providing CRUD operations on the local SQLite database.  
**Template:** Dart Class Template  
**Dependancy Level:** 2  
**Name:** FarmerLocalDatasource  
**Type:** LocalDatasource  
**Relative Path:** features/farmer_registration/data/datasources/farmer_local_datasource.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    - DAO
    
**Members:**
    
    - **Name:** _dbHelper  
**Type:** DatabaseHelper  
**Attributes:** private|final  
    
**Methods:**
    
    - **Name:** createFarmer  
**Parameters:**
    
    - FarmerModel farmer
    
**Return Type:** Future<int>  
**Attributes:** public|async  
    - **Name:** getFarmerById  
**Parameters:**
    
    - String id
    
**Return Type:** Future<FarmerModel?>  
**Attributes:** public|async  
    - **Name:** getAllFarmers  
**Parameters:**
    
    
**Return Type:** Future<List<FarmerModel>>  
**Attributes:** public|async  
    - **Name:** updateFarmer  
**Parameters:**
    
    - FarmerModel farmer
    
**Return Type:** Future<int>  
**Attributes:** public|async  
    - **Name:** deleteFarmer  
**Parameters:**
    
    - String id
    
**Return Type:** Future<int>  
**Attributes:** public|async  
    - **Name:** getPendingSyncFarmers  
**Parameters:**
    
    
**Return Type:** Future<List<FarmerModel>>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Local CRUD for Farmer Data
    - Offline Farmer Data Storage
    
**Requirement Ids:**
    
    - REQ-4-003
    
**Purpose:** To manage persistence of farmer data in the local SQLite database, enabling offline creation, reading, updating, and deletion of farmer records.  
**Logic Description:** Uses the `DatabaseHelper` to get a database instance. Implements SQL queries (INSERT, SELECT, UPDATE, DELETE) for the `Farmer` table. Maps between `FarmerModel` objects and database records.  
**Documentation:**
    
    - **Summary:** Handles local database operations (CRUD) for farmer records, supporting offline functionality.
    
**Namespace:** com.fao.dfr.mobile.features.farmer_registration.data.datasources  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** lib/features/farmer_registration/data/models/farmer_model.dart  
**Description:** Data Transfer Object (DTO) / Model representing a Farmer, used for local storage and API communication. Includes (de)serialization logic.  
**Template:** Dart Class Template  
**Dependancy Level:** 0  
**Name:** FarmerModel  
**Type:** Model  
**Relative Path:** features/farmer_registration/data/models/farmer_model.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** id  
**Type:** String  
**Attributes:** public|final  
    - **Name:** uid  
**Type:** String  
**Attributes:** public|final  
    - **Name:** fullName  
**Type:** String  
**Attributes:** public|final  
    - **Name:** dateOfBirth  
**Type:** String?  
**Attributes:** public|final  
    - **Name:** sex  
**Type:** String?  
**Attributes:** public|final  
    - **Name:** contactPhone  
**Type:** String  
**Attributes:** public|final  
    - **Name:** nationalIdType  
**Type:** String?  
**Attributes:** public|final  
    - **Name:** nationalIdNumber  
**Type:** String?  
**Attributes:** public|final  
    - **Name:** status  
**Type:** String  
**Attributes:** public|final  
    - **Name:** syncStatus  
**Type:** String  
**Attributes:** public|final  
    - **Name:** syncAttemptTimestamp  
**Type:** int?  
**Attributes:** public|final  
    
**Methods:**
    
    - **Name:** FarmerModel.fromJson  
**Parameters:**
    
    - Map<String, dynamic> json
    
**Return Type:** FarmerModel  
**Attributes:** public|factory  
    - **Name:** toJson  
**Parameters:**
    
    
**Return Type:** Map<String, dynamic>  
**Attributes:** public  
    - **Name:** FarmerModel.fromEntity  
**Parameters:**
    
    - FarmerEntity entity
    
**Return Type:** FarmerModel  
**Attributes:** public|factory  
    - **Name:** toEntity  
**Parameters:**
    
    
**Return Type:** FarmerEntity  
**Attributes:** public  
    
**Implemented Features:**
    
    - Farmer Data Structure
    - JSON Serialization/Deserialization
    
**Requirement Ids:**
    
    - REQ-4-003
    - REQ-4-006
    
**Purpose:** To define the structure for farmer data handled by the application, enabling conversion to/from JSON for API interactions and to/from database maps for local storage.  
**Logic Description:** Defines fields like id, uid, fullName, dateOfBirth, sex, contactPhone, nationalId related fields, status, and syncStatus. Implements `fromJson` and `toJson` methods for API communication. May include methods for conversion to/from domain entities and database maps.  
**Documentation:**
    
    - **Summary:** Data model for farmer information, used for API communication and local persistence.
    
**Namespace:** com.fao.dfr.mobile.features.farmer_registration.data.models  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** lib/features/farmer_registration/domain/entities/farmer_entity.dart  
**Description:** Domain entity representing a Farmer. Contains core business attributes and logic, independent of data sources or UI.  
**Template:** Dart Class Template  
**Dependancy Level:** 0  
**Name:** FarmerEntity  
**Type:** Entity  
**Relative Path:** features/farmer_registration/domain/entities/farmer_entity.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    - DDD Entity
    
**Members:**
    
    - **Name:** id  
**Type:** String  
**Attributes:** public|final  
    - **Name:** uid  
**Type:** String  
**Attributes:** public|final  
    - **Name:** fullName  
**Type:** String  
**Attributes:** public|final  
    - **Name:** contactPhone  
**Type:** String  
**Attributes:** public|final  
    
**Methods:**
    
    
**Implemented Features:**
    
    - Farmer Business Object Definition
    
**Requirement Ids:**
    
    - REQ-4-003
    
**Purpose:** To represent the core business concept of a farmer within the application's domain layer.  
**Logic Description:** Plain Dart object (POJO/PODO) with final fields representing essential farmer attributes. May include simple validation logic or business methods if applicable to the entity itself.  
**Documentation:**
    
    - **Summary:** Domain entity for Farmer, representing core farmer attributes.
    
**Namespace:** com.fao.dfr.mobile.features.farmer_registration.domain.entities  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** lib/features/farmer_registration/domain/repositories/farmer_repository.dart  
**Description:** Abstract interface defining the contract for farmer data operations, decoupling domain logic from data source implementations.  
**Template:** Dart Abstract Class Template  
**Dependancy Level:** 0  
**Name:** FarmerRepository  
**Type:** RepositoryInterface  
**Relative Path:** features/farmer_registration/domain/repositories/farmer_repository.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    
**Methods:**
    
    - **Name:** registerFarmer  
**Parameters:**
    
    - FarmerEntity farmer
    
**Return Type:** Future<Either<Failure, void>>  
**Attributes:** public|abstract  
    - **Name:** getFarmer  
**Parameters:**
    
    - String farmerId
    
**Return Type:** Future<Either<Failure, FarmerEntity>>  
**Attributes:** public|abstract  
    - **Name:** getAllLocalFarmers  
**Parameters:**
    
    
**Return Type:** Future<Either<Failure, List<FarmerEntity>>>  
**Attributes:** public|abstract  
    - **Name:** getFarmersToSync  
**Parameters:**
    
    
**Return Type:** Future<Either<Failure, List<FarmerEntity>>>  
**Attributes:** public|abstract  
    
**Implemented Features:**
    
    - Farmer Data Operations Contract
    
**Requirement Ids:**
    
    - REQ-4-003
    - REQ-4-006
    
**Purpose:** To define a clear contract for accessing and managing farmer data, abstracting away the specific data sources (local DB or remote API).  
**Logic Description:** Abstract class with methods for creating, retrieving, updating, and deleting farmer data, as well as methods specific to synchronization needs (e.g., fetching pending records). Uses `Either` for error handling.  
**Documentation:**
    
    - **Summary:** Defines the contract for farmer data operations, used by domain use cases.
    
**Namespace:** com.fao.dfr.mobile.features.farmer_registration.domain.repositories  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** lib/features/farmer_registration/data/repositories/farmer_repository_impl.dart  
**Description:** Implementation of the FarmerRepository interface, coordinating data from local and remote datasources.  
**Template:** Dart Class Template  
**Dependancy Level:** 3  
**Name:** FarmerRepositoryImpl  
**Type:** RepositoryImplementation  
**Relative Path:** features/farmer_registration/data/repositories/farmer_repository_impl.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** _localDatasource  
**Type:** FarmerLocalDatasource  
**Attributes:** private|final  
    - **Name:** _remoteDatasource  
**Type:** FarmerRemoteDatasource  
**Attributes:** private|final  
    - **Name:** _connectivityService  
**Type:** ConnectivityService  
**Attributes:** private|final  
    
**Methods:**
    
    - **Name:** registerFarmer  
**Parameters:**
    
    - FarmerEntity farmer
    
**Return Type:** Future<Either<Failure, void>>  
**Attributes:** public|override|async  
    - **Name:** getFarmer  
**Parameters:**
    
    - String farmerId
    
**Return Type:** Future<Either<Failure, FarmerEntity>>  
**Attributes:** public|override|async  
    - **Name:** getAllLocalFarmers  
**Parameters:**
    
    
**Return Type:** Future<Either<Failure, List<FarmerEntity>>>  
**Attributes:** public|override|async  
    - **Name:** getFarmersToSync  
**Parameters:**
    
    
**Return Type:** Future<Either<Failure, List<FarmerEntity>>>  
**Attributes:** public|override|async  
    
**Implemented Features:**
    
    - Farmer Data Source Coordination
    - Offline/Online Data Strategy for Farmers
    
**Requirement Ids:**
    
    - REQ-4-003
    - REQ-4-006
    
**Purpose:** To implement the `FarmerRepository` contract, deciding whether to fetch data from/save data to local storage or remote API based on connectivity and sync status.  
**Logic Description:** Implements methods defined in `FarmerRepository`. For write operations (registerFarmer), it saves to local DB first and marks for sync. For read operations, it might check local first, then remote if online. Handles conversion between `FarmerEntity` and `FarmerModel`.  
**Documentation:**
    
    - **Summary:** Implements farmer data operations, managing local and remote data sources.
    
**Namespace:** com.fao.dfr.mobile.features.farmer_registration.data.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** lib/features/farmer_registration/presentation/screens/farmer_registration_screen.dart  
**Description:** UI screen for capturing farmer registration details. Includes form fields, validation, and interaction with BLoC for state management.  
**Template:** Flutter Widget Template (StatefulWidget)  
**Dependancy Level:** 3  
**Name:** FarmerRegistrationScreen  
**Type:** Screen  
**Relative Path:** features/farmer_registration/presentation/screens/farmer_registration_screen.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    - BLoC
    
**Members:**
    
    - **Name:** _formKey  
**Type:** GlobalKey<FormState>  
**Attributes:** private|final  
    
**Methods:**
    
    - **Name:** build  
**Parameters:**
    
    - BuildContext context
    
**Return Type:** Widget  
**Attributes:** public|override  
    - **Name:** _onSubmit  
**Parameters:**
    
    
**Return Type:** void  
**Attributes:** private  
    
**Implemented Features:**
    
    - Farmer Registration UI Form
    - Input Validation Display
    - Interaction with FarmerRegistrationBloc
    
**Requirement Ids:**
    
    - REQ-4-002
    - REQ-4-003
    
**Purpose:** To provide a user-friendly interface for enumerators to enter farmer details. Handles form state, validation, and submission to the BLoC for processing.  
**Logic Description:** Builds a `Form` widget with `TextFormField`s for farmer name, contact, DOB, etc. Uses `BlocBuilder` or `BlocListener` to react to `FarmerRegistrationState` changes (e.g., show loading, success, error messages). On submit, validates form and dispatches an event to `FarmerRegistrationBloc`.  
**Documentation:**
    
    - **Summary:** UI screen for farmer registration, enabling data capture and submission.
    
**Namespace:** com.fao.dfr.mobile.features.farmer_registration.presentation.screens  
**Metadata:**
    
    - **Category:** Presentation
    
- **Path:** lib/features/sync/domain/usecases/synchronize_data_usecase.dart  
**Description:** Coordinates the bi-directional data synchronization process between the mobile app and the DFR backend API.  
**Template:** Dart Class Template  
**Dependancy Level:** 1  
**Name:** SynchronizeDataUsecase  
**Type:** Usecase  
**Relative Path:** features/sync/domain/usecases/synchronize_data_usecase.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _syncRepository  
**Type:** SyncRepository  
**Attributes:** private|final  
    - **Name:** _farmerRepository  
**Type:** FarmerRepository  
**Attributes:** private|final  
    
**Methods:**
    
    - **Name:** call  
**Parameters:**
    
    - SyncParams params
    
**Return Type:** Future<Either<Failure, SyncResult>>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Bi-directional Data Synchronization Logic
    - Conflict Resolution Trigger
    
**Requirement Ids:**
    
    - REQ-PCA-006
    - REQ-4-006
    
**Purpose:** To manage the overall data synchronization flow. Fetches pending local changes, sends them to the server, fetches server updates, and applies them locally. Handles conflict resolution strategy.  
**Logic Description:** Fetches pending farmer records and form submissions from local repositories. Calls `SyncRepository` to push these changes to the backend. Fetches updated data (farmers, form definitions) from the backend. Updates local database with server changes. Implements logic for conflict resolution (e.g., last-write-wins or flagging for manual review).  
**Documentation:**
    
    - **Summary:** Orchestrates the bi-directional data synchronization process with the backend.
    
**Namespace:** com.fao.dfr.mobile.features.sync.domain.usecases  
**Metadata:**
    
    - **Category:** Domain
    
- **Path:** lib/features/sync/data/repositories/sync_repository_impl.dart  
**Description:** Implementation of SyncRepository, handles communication with backend sync endpoints.  
**Template:** Dart Class Template  
**Dependancy Level:** 3  
**Name:** SyncRepositoryImpl  
**Type:** RepositoryImplementation  
**Relative Path:** features/sync/data/repositories/sync_repository_impl.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    - RepositoryPattern
    
**Members:**
    
    - **Name:** _remoteDatasource  
**Type:** SyncRemoteDatasource  
**Attributes:** private|final  
    - **Name:** _localFarmerDs  
**Type:** FarmerLocalDatasource  
**Attributes:** private|final  
    - **Name:** _localFormDs  
**Type:** DynamicFormLocalDatasource  
**Attributes:** private|final  
    
**Methods:**
    
    - **Name:** pushLocalChanges  
**Parameters:**
    
    - List<FarmerModel> farmers
    - List<FormSubmissionModel> forms
    
**Return Type:** Future<Either<Failure, SyncPushResult>>  
**Attributes:** public|async  
    - **Name:** pullServerUpdates  
**Parameters:**
    
    - String lastSyncTimestamp
    
**Return Type:** Future<Either<Failure, SyncPullResult>>  
**Attributes:** public|async  
    
**Implemented Features:**
    
    - Push Local Data to Server
    - Pull Remote Data from Server
    
**Requirement Ids:**
    
    - REQ-PCA-006
    - REQ-4-006
    
**Purpose:** To manage the actual API calls for pushing local data modifications to the server and pulling server-side updates to the mobile device.  
**Logic Description:** Interacts with `SyncRemoteDatasource` (which uses `DfrApiService`). Collects pending data from local datasources (farmer, forms). Batches data and sends it to the server. Fetches new form definitions and updated records from the server. Updates local records based on server response and handles conflicts or errors.  
**Documentation:**
    
    - **Summary:** Implements data synchronization logic by interacting with backend API for push/pull operations.
    
**Namespace:** com.fao.dfr.mobile.features.sync.data.repositories  
**Metadata:**
    
    - **Category:** DataAccess
    
- **Path:** lib/core/utils/connectivity_service.dart  
**Description:** Provides information about the device's network connectivity status (online/offline).  
**Template:** Dart Class Template  
**Dependancy Level:** 0  
**Name:** ConnectivityService  
**Type:** Service  
**Relative Path:** core/utils/connectivity_service.dart  
**Repository Id:** DFR_MOBILE_APP  
**Pattern Ids:**
    
    
**Members:**
    
    - **Name:** _connectivity  
**Type:** Connectivity  
**Attributes:** private|final  
    
**Methods:**
    
    - **Name:** isConnected  
**Parameters:**
    
    
**Return Type:** Future<bool>  
**Attributes:** public|async  
    - **Name:** onConnectivityChanged  
**Parameters:**
    
    
**Return Type:** Stream<ConnectivityResult>  
**Attributes:** public  
    
**Implemented Features:**
    
    - Network Status Detection
    
**Requirement Ids:**
    
    - REQ-PCA-006
    - REQ-4-003
    
**Purpose:** To allow the application to check current network status and react to connectivity changes, crucial for offline-first behavior and sync scheduling.  
**Logic Description:** Uses the `connectivity_plus` plugin to check for active internet connection (Wi-Fi, Mobile Data). Provides a stream to listen for connectivity changes.  
**Documentation:**
    
    - **Summary:** Monitors and reports device network connectivity status.
    
**Namespace:** com.fao.dfr.mobile.core.utils  
**Metadata:**
    
    - **Category:** Utility
    


---

# 2. Configuration

- **Feature Toggles:**
  
  - enableDarkTheme
  - enableLocalDeDuplicationCheck
  
- **Database Configs:**
  
  - DB_NAME
  - DB_VERSION
  - DB_ENCRYPTION_KEY_ALIAS
  
- **Api Configs:**
  
  - BASE_API_URL
  - API_TIMEOUT_SECONDS
  


---

