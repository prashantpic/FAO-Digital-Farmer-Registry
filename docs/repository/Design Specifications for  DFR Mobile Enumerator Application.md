# DFR Mobile Enumerator Application - Software Design Specification

## 1. Introduction

### 1.1 Purpose
This document provides the detailed software design specification for the DFR (Digital Farmer Registry) Mobile Enumerator Application. This application is an Android-based mobile solution developed using Flutter/Dart, designed for enumerators to register farmers, collect household and plot data, manage dynamic forms, and synchronize data with the DFR backend. It prioritizes offline-first functionality with secure local data storage.

This SDS will guide the development of the mobile application, detailing its architecture, components, data management, UI/UX considerations, and integration points.

### 1.2 Scope
The scope of this document covers the design and implementation of the DFR Mobile Enumerator Application, including:
-   User authentication and session management.
-   Farmer, household, and plot registration and management (CRUD operations).
-   Dynamic form rendering, data capture, and submission.
-   Offline data storage with AES-256 encryption using SQLCipher.
-   Secure management of encryption keys.
-   Bi-directional data synchronization with the DFR backend API, including conflict resolution.
-   GPS location capture for plots.
-   QR code scanning for farmer identification.
-   Multilingual support.
-   App update checks and enforcement mechanisms.
-   Local logging and basic troubleshooting information.
-   Adherence to specified performance and security requirements.

### 1.3 Definitions, Acronyms, and Abbreviations
-   **DFR**: Digital Farmer Registry
-   **API**: Application Programming Interface
-   **SDK**: Software Development Kit
-   **UI**: User Interface
-   **UX**: User Experience
-   **CRUD**: Create, Read, Update, Delete
-   **GPS**: Global Positioning System
-   **QR**: Quick Response (code)
-   **SQLite**: Relational database management system contained in a C library.
-   **SQLCipher**: An open-source extension to SQLite that provides transparent 256-bit AES encryption of database files.
-   **JWT**: JSON Web Token
-   **BLoC**: Business Logic Component (a state management pattern for Flutter)
-   **Cubit**: A simpler subset of BLoC.
-   **DAO**: Data Access Object
-   **DTO**: Data Transfer Object
-   **MDM**: Mobile Device Management
-   **APK**: Android Package Kit
-   **MASVS**: Mobile Application Security Verification Standard
-   **SLA**: Service Level Agreement
-   **TOT**: Train-the-Trainer
-   **SOP**: Standard Operating Procedure
-   **OTP**: One-Time Password
-   **PII**: Personally Identifiable Information
-   **SemVer**: Semantic Versioning

### 1.4 References
-   Project Requirements Document (SRS_DFR_Platform_WP_ABCDE_vX.X.docx - specifically sections REQ-PCA-006, REQ-3-*, REQ-4-*, REQ-DIO-012, REQ-LMS-*, REQ-SADG-*)
-   DFR System Architecture Document
-   DFR API Gateway Specification (OpenAPI v3.x)
-   Local Mobile Database Design (`databaseDesign.json`)
-   Sequence Diagrams (e.g., SD-DFR-012)

## 2. System Overview

The DFR Mobile Enumerator Application is a key component of the DFR platform, enabling field data collection by enumerators. It operates with an offline-first approach, storing data locally in an encrypted SQLite database and synchronizing with the central DFR backend (Odoo) via RESTful APIs when network connectivity is available.

**Key Features:**
-   Secure Enumerator Login
-   Farmer Registration & Profile Management
-   Household & Household Member Management
-   Farm & Plot Management (including GPS capture)
-   Dynamic Form Rendering & Data Collection
-   Offline Data Storage & Operations
-   Bi-directional Data Synchronization with Conflict Resolution
-   QR Code Scanning for Farmer Lookup
-   Multilingual User Interface
-   App Update Management

**Technology Stack:**
-   **Framework:** Flutter 3.22.2
-   **Language:** Dart 3.4.3
-   **Target Platform:** Android (Min SDK API 26 - Android 8.0, Target SDK API 34)
-   **Local Database:** SQLite 3.45.3 with SQLCipher 4.5.6 (AES-256 encryption)
-   **State Management:** `flutter_bloc` (BLoC/Cubit)
-   **HTTP Client:** `dio`
-   **Secure Storage:** `flutter_secure_storage`
-   **GPS:** `geolocator`
-   **QR Scanner:** `mobile_scanner`
-   **Connectivity:** `connectivity_plus`

## 3. System Architecture

The mobile application follows a Layered Architecture, promoting separation of concerns, testability, and maintainability.

### 3.1 Layers
1.  **Presentation Layer (`mobile_presentation`):**
    *   **Responsibility:** Handles all UI and user interaction. Consists of Widgets (Screens, UI components), and manages UI state presentation logic using BLoC/Cubit.
    *   **Components:** Screens, Widgets, BLoC/Cubit event/state classes.
    *   **Technologies:** Flutter Widgets, `flutter_bloc`.

2.  **Application Logic / Domain Layer (`mobile_application_logic`):**
    *   **Responsibility:** Contains the core business logic, use cases (interactors), and domain entities. It orchestrates data flow between the presentation and data layers and is independent of UI and data sources.
    *   **Components:** Usecases/Interactors, Domain Entities, Repository Interfaces.
    *   **Technologies:** Dart.

3.  **Data Layer (`mobile_data`):**
    *   **Responsibility:** Manages data persistence (local and remote). Implements repository interfaces defined in the domain layer. Handles data fetching, storage, synchronization, and communication with the backend API.
    *   **Components:** Repository Implementations, Local Datasources (DAOs for SQLite), Remote Datasources (API service clients), Data Models (DTOs).
    *   **Technologies:** `sqflite`, `sqlcipher_flutter_libs`, `dio`, Dart.

4.  **Cross-Cutting Services Layer (`mobile_cross_cutting_services`):**
    *   **Responsibility:** Provides common utilities and services used across different layers, such as GPS location, QR code scanning, logging, network connectivity checks, secure key management, and app update checks.
    *   **Components:** GPS Service, QR Scanner Service, Logging Service, Secure Storage Service, Connectivity Service, App Update Service.
    *   **Technologies:** `geolocator`, `mobile_scanner`, `logger` (or similar), `flutter_secure_storage`, `connectivity_plus`.

### 3.2 Architectural Patterns
-   **Layered Architecture:** As described above.
-   **BLoC/Cubit:** For state management in the Presentation Layer.
-   **Repository Pattern:** To abstract data sources from the domain layer.
-   **Dependency Injection:** To manage dependencies between layers and components (e.g., using `get_it`).
-   **Offline-First:** Core design principle ensuring functionality without network.
-   **Singleton:** For services like `DatabaseHelper`, `ApiClient` where a single instance is desired.

## 4. Data Design

### 4.1 Local Database Design (SQLite with SQLCipher)
The local database schema is defined in the `databaseDesign.json` provided as input. Key tables include:
-   `Farmer`: Stores farmer profile information.
-   `Household`: Stores household information.
-   `HouseholdMember`: Stores household member details.
-   `Farm`: Stores farm information.
-   `Plot`: Stores plot details, including GPS coordinates.
-   `AdministrativeArea`: Stores relevant administrative area hierarchy for offline use.
-   `DynamicForm`: Stores definitions of dynamic forms synced from the server.
-   `FormField`: Stores field definitions for each dynamic form.
-   `FormSubmission`: Stores locally saved submissions of dynamic forms.
-   `FormResponse`: Stores individual responses for each field in a form submission.
-   `User`: Stores basic information about the logged-in enumerator.
-   `SyncQueueItem`: Tracks local data changes pending synchronization with the server.

**Key Schema Considerations:**
-   **Primary Keys:** Server-side UUIDs will be stored as `TEXT` for entities synced from the server. Locally generated IDs (e.g., for `FormSubmission` before sync) might be local UUIDs or integers.
-   **Foreign Keys:** Enforced to maintain relational integrity.
-   **Synchronization Fields:** Each syncable table (e.g., Farmer, Plot, FormSubmission, FormResponse) will include:
    -   `syncStatus` (TEXT): e.g., 'Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error'.
    -   `syncAttemptTimestamp` (INTEGER): Unix timestamp of the last sync attempt.
    -   `isDeleted` (BOOLEAN): For soft deletes.
    -   `serverId` (TEXT, nullable): Stores the server's ID for a record once synced.
-   **Encryption:** The entire SQLite database file will be encrypted using SQLCipher with AES-256. The encryption key will be managed by `EncryptionService` and stored via `SecureStorageService`.

Refer to `databaseDesign.json` for detailed table structures, attributes, types, constraints, and indexes.

### 4.2 Data Models (DTOs)
For each entity in the local database and for API communication, corresponding Dart model classes (DTOs) will be created. These models will include:
-   Fields matching the entity attributes.
-   `fromJson(Map<String, dynamic> json)` factory constructor for deserializing data from API responses or local storage.
-   `toJson() -> Map<String, dynamic>` method for serializing data for API requests or local storage.
-   Potentially `fromEntity(Entity entity)` and `toEntity() -> Entity` methods for mapping between data models and domain entities.

Examples: `FarmerModel`, `PlotModel`, `FormDefinitionModel`, `FormSubmissionModel`.

### 4.3 Domain Entities
Pure Dart classes representing core business concepts, independent of specific data representation.
Examples: `FarmerEntity`, `PlotEntity`, `FormEntity`.

## 5. Module and Component Design

This section details the design of key files and components as outlined in the `file_structure_json`.

### 5.1 Core Application (`lib/`, `lib/core/`)

#### 5.1.1 `pubspec.yaml`
-   **Purpose:** Project manifest; declares dependencies, assets, and Flutter configuration.
-   **Logic:**
    -   Specify project `name`, `description`, `version` (adhering to SemVer REQ-CM-003).
    -   Define `environment: sdk: '>=3.4.3 <4.0.0'` and `flutter: '>=3.22.2'`.
    -   **Dependencies:**
        -   `flutter_bloc`: For state management.
        -   `dio`: For HTTP API communication.
        -   `sqflite`: SQLite plugin.
        -   `sqlcipher_flutter_libs`: SQLCipher native libraries. (Note: `sqflite_sqlcipher` might be the actual Flutter package that combines `sqflite` with SQLCipher support or direct use of `sqflite` with custom SQLCipher bindings if `sqlcipher_flutter_libs` only provides libs). Verify the exact Flutter SQLCipher package. Assuming `sqflite` can be opened with SQLCipher parameters if native libs are present and correctly linked.
        -   `geolocator`: For GPS location services.
        -   `mobile_scanner`: For QR code scanning.
        -   `flutter_secure_storage`: For secure storage of encryption keys.
        -   `connectivity_plus`: For network connectivity checks.
        -   `path_provider`: For getting filesystem paths.
        -   `uuid`: For generating local UUIDs.
        -   `intl`: For internationalization and localization (date/number formatting).
        -   `get_it`: For dependency injection.
        -   `dartz`: For functional programming constructs like `Either`.
        -   `equatable`: For value equality in models and entities.
    -   **Dev Dependencies:**
        -   `build_runner`: For code generation.
        -   `mockito`: For testing.
        -   `bloc_test`: For testing BLoCs.
    -   Declare assets (images, fonts, localization files in `assets/i18n/`).
    -   Enable `uses-material-design: true`.
-   **Requirements Met:** REQ-4-001, REQ-4-004, project setup.

#### 5.1.2 `android/app/build.gradle`
-   **Purpose:** Android-specific build configuration.
-   **Logic:**
    -   `minSdkVersion 26`
    -   `targetSdkVersion 34` (or latest stable)
    -   `compileSdkVersion 34` (or latest stable)
    -   `applicationId "com.fao.dfr.mobile"`
    -   Ensure necessary configurations for SQLCipher if required at this level (e.g., specific ProGuard rules if minification is enabled, or native library loading).
-   **Requirements Met:** REQ-4-001.

#### 5.1.3 `android/app/src/main/AndroidManifest.xml`
-   **Purpose:** Android app manifest, declares permissions and components.
-   **Logic:**
    -   `<uses-permission android:name="android.permission.INTERNET" />` (REQ-PCA-006, REQ-4-006 for sync)
    -   `<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />` (REQ-PCA-006, REQ-4-009 for GPS)
    -   `<uses-permission android:name="android.permission.CAMERA" />` (REQ-PCA-006, REQ-4-008 for QR scan)
    -   `<uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />` (For connectivity checks)
    -   Define application activities, services as per Flutter setup.
    -   If using `flutter_local_notifications` or FCM for push, declare relevant permissions and services.
-   **Requirements Met:** REQ-PCA-006, REQ-4-001.

#### 5.1.4 `lib/main.dart`
-   **Purpose:** Application entry point.
-   **`main()` method:**
    -   `WidgetsFlutterBinding.ensureInitialized();`
    -   Initialize global error handling (e.g., `PlatformDispatcher.instance.onError`).
    -   Initialize dependency injection (e.g., using `get_it` to register services like `DatabaseHelper`, `ApiClient`, repositories, BLoCs).
    -   Initialize localization services.
    -   `runApp(const App());`
-   **Requirements Met:** REQ-4-001.

#### 5.1.5 `lib/app.dart`
-   **Purpose:** Root application widget.
-   **`App` class (StatelessWidget or StatefulWidget for dynamic theme/locale):**
    -   **`build(BuildContext context)` method:**
        -   Returns `MaterialApp`.
        -   `theme: AppTheme.lightTheme` (or dynamically set).
        -   `darkTheme: AppTheme.darkTheme` (if dark mode is supported by REQ-CONF-001 FeatureToggle `enableDarkTheme`).
        -   `localizationsDelegates`: Setup for `AppLocalizations` (custom) and `GlobalMaterialLocalizations`, `GlobalWidgetsLocalizations`.
        -   `supportedLocales`: List of supported locales (e.g., `[Locale('en', ''), Locale('fr', '')]`).
        -   `localeResolutionCallback` or `localeListResolutionCallback`.
        -   `initialRoute` or `routerDelegate` using a router package (e.g., GoRouter) for navigation.
        -   `builder`: To wrap child widgets with common providers if needed (e.g., `ConnectivityProvider`).
-   **Requirements Met:** REQ-4-002 (Theme, Localization setup).

#### 5.1.6 `lib/core/theme/app_theme.dart`
-   **`AppTheme` class:**
    -   `static ThemeData get lightTheme`: Defines light theme properties (colors, typography, input decorations, button styles) adhering to Material Design and DFR branding (REQ-4-002).
        -   `colorScheme`: `ColorScheme.fromSeed(seedColor: DFRColors.primary)`.
        -   `textTheme`: Define various text styles.
        -   `inputDecorationTheme`: Consistent styling for text fields.
        -   `elevatedButtonTheme`, `textButtonTheme`.
    -   `static ThemeData get darkTheme` (if `enableDarkTheme` is true): Defines dark theme properties.
-   **Requirements Met:** REQ-4-002.

#### 5.1.7 `lib/core/database/database_helper.dart`
-   **`DatabaseHelper` class (Singleton):**
    -   `static final DatabaseHelper _instance = DatabaseHelper._internal();`
    -   `factory DatabaseHelper() => _instance;`
    -   `DatabaseHelper._internal();`
    -   `static Database? _database;`
    -   `static const String _dbName = 'dfr_mobile.db';` (configurable via REQ-CONF-002 `DB_NAME`)
    -   `static const int _dbVersion = 1;` (configurable via REQ-CONF-002 `DB_VERSION`)
    -   **`Future<Database> get database async`:**
        -   If `_database` is null, initialize it by calling `_initDatabase()`.
        -   Return `_database`.
    -   **`Future<Database> _initDatabase() async`:**
        -   Get database path using `path_provider`.
        -   Retrieve encryption key from `EncryptionService`.
        -   Open the database using `sqflite.openDatabase()` with SQLCipher options:
            dart
            // Pseudocode for opening with SQLCipher
            // Note: Actual sqflite API might differ for SQLCipher integration.
            // Typically, you might pass password to openDatabase options
            // or use a specific `openCipheredDatabase` method if provided by a wrapper package.
            // For sqlcipher_flutter_libs, it might involve setting a PRAGMA key before operations.
            // This step requires careful verification with the chosen SQLCipher Flutter package.
            // Example:
            // await db.rawQuery("PRAGMA key = '$encryptionKey';"); // After opening plain
            // await db.rawQuery("PRAGMA cipher_page_size = 4096;"); // Example cipher config
            // Or
            // path_to_db = join(await getDatabasesPath(), _dbName);
            // return await openDatabase(
            //     path_to_db,
            //     version: _dbVersion,
            //     onCreate: _onCreate,
            //     onUpgrade: _onUpgrade,
            //     singleInstance: true,
            //     readOnly: false,
            //     options: OpenDatabaseOptions(
            //       password: encryptionKey, // This is conceptual for SQLCipher
            //     )
            // );
            // More likely, using sqflite_sqlcipher or a similar package:
            // return await openDatabaseWithCipher(
            //   path,
            //   password: encryptionKey,
            //   version: _dbVersion,
            //   onCreate: _onCreate,
            //   onUpgrade: _onUpgrade,
            // );
            // Research for `sqflite_sqlcipher` or `sqflite` with `sqlcipher_flutter_libs`:
            // The common approach is to open a standard SQLite database and then issue PRAGMA commands.
            // Or, if using a dedicated package like `sqflite_sqlcipher`, it would have a direct method.
            // Assuming `sqlcipher_flutter_libs` provides the native libs and `sqflite` can leverage them
            // by opening a normally named DB and then immediately setting the key.
            
            Let's assume a helper function or package exists or needs to be created for `openEncryptedDatabase`.
            dart
            final String path = join(await getDatabasesPath(), _dbName);
            final String encryptionKey = await getIt<EncryptionService>().getDatabaseEncryptionKey();
            // This is a conceptual call. The actual method depends on the SQLCipher Flutter package.
            // E.g., if using a package like `sqlite_framework` or a custom native bridge.
            // For `sqflite` with `sqlcipher_flutter_libs` typically one would open the database
            // and then execute `PRAGMA key = 'your_key';`.
            // Or a package like `sqflite_sqlcipher` might provide `openDatabase(path, password: key, ...)`
            
            // Tentative approach based on common patterns:
            var db = await openDatabase(path, version: _dbVersion, onCreate: _onCreate, onUpgrade: _onUpgrade);
            await db.rawQuery("PRAGMA key = '$encryptionKey';"); 
            // Test if encryption works by trying to open it with a different key or without a key
            // Also, check if data is indeed encrypted by inspecting the DB file.
            await db.rawQuery("PRAGMA kdf_iter = '256000';"); // Example security hardening
            await db.rawQuery("PRAGMA cipher_page_size = 4096;");
            await db.rawQuery("PRAGMA cipher_hmac_algorithm = HMAC_SHA512;");
            await db.rawQuery("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA512;");

            // After setting the key, verify a simple query works.
            try {
                await db.getVersion(); // This might fail if key is wrong or not set.
                                   // The first operation on an encrypted DB needs the key.
            } catch (e) {
                // Handle error if key is wrong or db is corrupted
                throw Exception("Failed to open/verify encrypted database: $e");
            }
            return db;
            
    -   **`Future<void> _onCreate(Database db, int version) async`:**
        -   Execute `CREATE TABLE` statements for all tables defined in `databaseDesign.json`.
        -   Example: `await db.execute(FarmerTable.createTableQuery);`
    -   **`Future<void> _onUpgrade(Database db, int oldVersion, int newVersion) async`:**
        -   Implement schema migration logic if `newVersion > oldVersion`.
    -   **`Future<void> close() async`:**
        -   `await _database?.close(); _database = null;`
-   **Requirements Met:** REQ-4-003, REQ-4-004 (partially, key management is in EncryptionService).

#### 5.1.8 `lib/core/database/encryption_service.dart`
-   **`EncryptionService` class:**
    -   `final SecureStorageService _secureStorageService;` (injected)
    -   `static const String _dbEncryptionKeyAlias = 'dfr_db_encryption_key';` (from REQ-CONF-002)
    -   **`Future<String> getDatabaseEncryptionKey() async`:**
        -   Try to read key from `_secureStorageService.read(key: _dbEncryptionKeyAlias)`.
        -   If key exists, return it.
        -   If not, generate a new strong random key (e.g., 32 bytes, Base64 encoded).
            dart
            // import 'dart:math';
            // import 'dart:convert';
            // final random = Random.secure();
            // final keyBytes = List<int>.generate(32, (i) => random.nextInt(256));
            // final newKey = base64UrlEncode(keyBytes);
            
        -   Store the new key using `_secureStorageService.write(key: _dbEncryptionKeyAlias, value: newKey)`.
        -   Return the new key.
-   **Requirements Met:** REQ-4-004 (Key management).

#### 5.1.9 `lib/core/security/secure_storage_service.dart`
-   **`SecureStorageService` class:**
    -   `final FlutterSecureStorage _storage = const FlutterSecureStorage();`
    -   **`Future<void> write({required String key, required String value}) async`:**
        -   `await _storage.write(key: key, value: value, aOptions: _getAndroidOptions());`
    -   **`Future<String?> read({required String key}) async`:**
        -   `return await _storage.read(key: key, aOptions: _getAndroidOptions());`
    -   **`Future<void> delete({required String key}) async`:**
        -   `await _storage.delete(key: key, aOptions: _getAndroidOptions());`
    -   **`AndroidOptions _getAndroidOptions() => const AndroidOptions(encryptedSharedPreferences: true);`** (Ensures usage of Android Keystore-backed storage if available)
-   **Requirements Met:** REQ-4-004 (Secure key persistence).

#### 5.1.10 `lib/core/network/api_client.dart`
-   **`ApiClient` class:**
    -   `final Dio dio;`
    -   **`ApiClient({required String baseUrl, String? authToken})` constructor:**
        -   Initializes `dio` with `BaseOptions(baseUrl: baseUrl, connectTimeout: Duration(seconds: 30), receiveTimeout: Duration(seconds: 60))`. (Timeout values from REQ-CONF-003)
        -   Adds default interceptors (e.g., `LogInterceptor` for debugging).
        -   If `authToken` is provided, adds an `AuthInterceptor` (see below).
    -   **`void addAuthInterceptor(String token)`:**
        -   Adds or replaces an `InterceptorsWrapper` to inject the `Authorization: Bearer $token` header.
    -   **`void removeAuthInterceptor()`:**
        -   Removes the auth interceptor.
-   **`AuthInterceptor` (can be a separate file or inner class):**
    -   Extends `Interceptor`.
    -   `onRequest(RequestOptions options, RequestInterceptorHandler handler)`: Adds auth token to headers.
-   **Requirements Met:** REQ-4-006 (HTTP client setup).

#### 5.1.11 `lib/core/network/dfr_api_service.dart`
-   **`DfrApiService` class:**
    -   `final ApiClient _apiClient;` (injected)
    -   Base URL for API is configured in `ApiClient` from REQ-CONF-003 `BASE_API_URL`.
    -   **`Future<List<FarmerModel>> getUpdatedFarmerData(String lastSyncTimestamp) async` (REQ-API-005):**
        -   Makes GET request to `/api/v1/farmers/updates?since=$lastSyncTimestamp`.
        -   Parses JSON response into `List<FarmerModel>`.
    -   **`Future<SyncFarmerResponseModel> syncFarmerData(List<FarmerModel> farmersToSync) async` (REQ-API-005):**
        -   Makes POST request to `/api/v1/farmers/sync` with `farmersToSync` in body.
        -   Parses JSON response into `SyncFarmerResponseModel` (containing created/updated/conflicted farmer IDs and potentially full updated farmer objects from server).
    -   **`Future<List<FormDefinitionModel>> getFormDefinitions() async` (REQ-API-005):**
        -   Makes GET request to `/api/v1/forms/definitions`.
        -   Parses JSON response into `List<FormDefinitionModel>`.
    -   **`Future<SyncFormResponseModel> syncFormSubmissions(List<FormSubmissionModel> submissionsToSync) async` (REQ-API-005):**
        -   Makes POST request to `/api/v1/forms/submissions/sync` with `submissionsToSync`.
        -   Parses JSON response into `SyncFormResponseModel`.
    -   **`Future<AppVersionInfoModel> checkAppVersion() async` (Supports REQ-4-013, SD-DFR-012):**
        -   Makes GET request to `/api/v1/app/version`.
        -   Response includes `latestVersion`, `minRequiredVersion`, `updateUrl`, `isCriticalUpdate`.
    -   **`Future<FarmerModel?> lookupFarmerByUid(String uid) async` (REQ-API-004):**
        -   GET `/api/v1/farmers/lookup?uid=$uid`.
    -   **`Future<List<FarmerModel>> lookupFarmer(Map<String, String> queryParams) async` (REQ-API-004):**
        -   GET `/api/v1/farmers/lookup` with query parameters.
    -   Error handling: Wrap Dio calls in try-catch, convert DioErrors to custom `NetworkFailure`.
-   **Requirements Met:** REQ-PCA-006, REQ-4-006, REQ-API-004, REQ-API-005.

#### 5.1.12 `lib/core/utils/connectivity_service.dart`
-   **`ConnectivityService` class:**
    -   `final Connectivity _connectivity = Connectivity();`
    -   **`Future<bool> isConnected() async`:**
        -   `final result = await _connectivity.checkConnectivity();`
        -   `return result.contains(ConnectivityResult.mobile) || result.contains(ConnectivityResult.wifi);`
    -   **`Stream<List<ConnectivityResult>> get onConnectivityChanged => _connectivity.onConnectivityChanged;`**
-   **Requirements Met:** REQ-PCA-006, REQ-4-003 (supports offline-first decisions).

#### 5.1.13 `lib/core/config/app_config.dart`
-   **`AppConfig` class (Singleton or loaded via DI):**
    -   Stores configurations: `BASE_API_URL`, `API_TIMEOUT_SECONDS` (from REQ-CONF-003).
    -   Feature Toggles: `enableDarkTheme`, `enableLocalDeDuplicationCheck` (from REQ-CONF-001).
    -   Can be loaded from environment variables (using `flutter_dotenv` or similar) or compiled-in defaults.
    -   `static Future<void> load() async { ... }`
    -   `static String get baseApiUrl => _instance._baseApiUrl;`
-   **Purpose:** Centralized access to application configurations.

#### 5.1.14 `lib/core/error/failures.dart`
-   **Abstract `Failure` class:** (extends `Equatable`)
-   **Concrete Failure classes:**
    -   `ServerFailure extends Failure { final String message; }`
    -   `CacheFailure extends Failure { final String message; }`
    -   `NetworkFailure extends Failure { final String message; }`
    -   `ValidationFailure extends Failure { final Map<String, String> fieldErrors; }`
    -   `PermissionFailure extends Failure { final String message; }`
    -   `SyncConflictFailure extends Failure { final List<ConflictInfo> conflicts; }`
-   **Purpose:** Standardized error/failure representation across the app, used with `Either`.

#### 5.1.15 `lib/core/localization/app_localizations.dart` and `assets/i18n/`
-   **`AppLocalizations` class:** Manages localized strings using Flutter's internationalization system.
    -   `static AppLocalizations? of(BuildContext context)`
    -   `static const LocalizationsDelegate<AppLocalizations> delegate`
    -   Methods for each translatable string: `String get appTitle;`, `String get registerFarmer;` etc.
-   **`assets/i18n/en.json`, `assets/i18n/fr.json` (etc.):** JSON files containing key-value pairs for translations.
    -   Loaded by `AppLocalizations`.
-   **Purpose:** To provide multilingual support for all UI text.
-   **Requirements Met:** REQ-LMS-001, REQ-LMS-003.

### 5.2 Feature: Farmer Registration (`lib/features/farmer_registration/`)

#### 5.2.1 Data Layer
##### `datasources/farmer_local_datasource.dart`
-   **`FarmerLocalDatasource` abstract class / `FarmerLocalDatasourceImpl` class:**
    -   `final DatabaseHelper _dbHelper;`
    -   `Future<String> createFarmer(FarmerModel farmer);` (returns local ID)
    -   `Future<FarmerModel?> getFarmerById(String id);`
    -   `Future<FarmerModel?> getFarmerByServerId(String serverId);`
    -   `Future<FarmerModel?> getFarmerByUid(String uid);` (REQ-4-008)
    -   `Future<List<FarmerModel>> getAllFarmers();`
    -   `Future<List<FarmerModel>> searchFarmersByName(String nameQuery);` (REQ-4-008)
    -   `Future<int> updateFarmer(FarmerModel farmer);`
    -   `Future<void> updateFarmerSyncStatus(String localId, String serverId, String syncStatus);`
    -   `Future<int> deleteFarmer(String id);` (soft delete: set `isDeleted=true`, `syncStatus='PendingDelete'`)
    -   `Future<List<FarmerModel>> getFarmersBySyncStatus(List<String> statuses);` (e.g., PendingCreate, PendingUpdate)
-   **Logic:** Interacts with `DatabaseHelper` to perform SQL operations on the `Farmer` table and related tables like `Plot`, `HouseholdMember` within the same transaction if needed. Maps data to/from `FarmerModel`.
-   **Requirements Met:** REQ-4-003, REQ-FHR-017 (local search part).

##### `datasources/plot_local_datasource.dart` (Similar structure for Plot CRUD)
##### `datasources/household_local_datasource.dart` (Similar for Household, HouseholdMember)

##### `models/farmer_model.dart`
-   **`FarmerModel` class:**
    -   Fields: `id` (local UUID), `serverId` (String?, nullable server UUID), `uid`, `fullName`, `dateOfBirth` (String, ISO8601), `sex`, `contactPhone`, `nationalIdType`, `nationalIdNumber`, `status` (from server), `adminAreaId` (String?, FK to local `AdministrativeArea`), `consentStatus`, `consentVersion`, `consentDate`.
    -   `syncStatus` (String), `syncAttemptTimestamp` (int?), `isDeleted` (bool).
    -   `List<PlotModel> plots;`
    -   `List<HouseholdMemberModel> householdMembers;` (if household is directly tied to farmer, or this is part of a `HouseholdModel` linked to farmer)
    -   `factory FarmerModel.fromJson(Map<String, dynamic> json)`
    -   `Map<String, dynamic> toJson()`
    -   `factory FarmerModel.fromDb(Map<String, dynamic> dbMap)`
    -   `Map<String, dynamic> toDbMap()`
    -   `FarmerEntity toEntity()`
    -   `static FarmerModel fromEntity(FarmerEntity entity)`
-   **Requirements Met:** REQ-FHR-003, REQ-FHR-004, REQ-FHR-005, REQ-FHR-006, REQ-FHR-007, REQ-FHR-018, local data representation.

##### `models/plot_model.dart`, `models/household_model.dart`, `models/household_member_model.dart`
-   Similar structure to `FarmerModel` for their respective entities and fields as per `databaseDesign.json` and SRS requirements.

##### `repositories/farmer_repository_impl.dart`
-   **`FarmerRepositoryImpl` class (implements `FarmerRepository`):**
    -   `final FarmerLocalDatasource _localDatasource;`
    -   `final ConnectivityService _connectivityService;`
    -   **`Future<Either<Failure, FarmerEntity>> getFarmer(String farmerId) async;`**
        -   Try local. If not found and online, could try remote (though typically sync brings data down).
    -   **`Future<Either<Failure, void>> registerOrUpdateFarmer(FarmerEntity farmer) async;`**
        -   Convert `FarmerEntity` to `FarmerModel`.
        -   If `farmer.id` suggests existing, update in `_localDatasource`, set `syncStatus = 'PendingUpdate'`.
        -   Else, create in `_localDatasource`, set `syncStatus = 'PendingCreate'`.
        -   Handle plots and household members transactionally.
    -   **`Future<Either<Failure, List<FarmerEntity>>> getAllLocalFarmers() async;`**
    -   **`Future<Either<Failure, List<FarmerEntity>>> getFarmersToSync() async;`**
        -   Fetch farmers with `syncStatus` in `['PendingCreate', 'PendingUpdate', 'PendingDelete']`.
    -   **`Future<Either<Failure, List<FarmerEntity>>> searchLocalFarmers(String query) async;` (REQ-FHR-017)**
    -   **`Future<Either<Failure, void>> markFarmerAsSynced(String localId, String serverId, FarmerModel serverFarmerData) async;`**
        -   Update local farmer with `serverId` and `syncStatus = 'Synced'`, potentially merging server data based on conflict resolution.
    -   **`Future<Either<Failure, void>> markFarmerSyncFailed(String localId, String errorMessage) async;`**
        -   Update local farmer `syncStatus = 'Error'`, store `errorMessage`.
-   **Logic:** Coordinates between local storage. Actual API calls for sync are handled by a dedicated Sync feature/repository. This repository focuses on preparing data for sync and processing results of sync for farmer entities.
-   **Requirements Met:** REQ-4-003, REQ-4-006 (preparation/consumption of sync data).

#### 5.2.2 Domain Layer
##### `entities/farmer_entity.dart`
-   **`FarmerEntity` class (extends `Equatable`):**
    -   Fields: `id` (String - can be local or server ID depending on context), `uid` (String), `fullName` (String), `dateOfBirth` (DateTime?), `sex` (String?), `contactPhone` (String), `nationalIdType` (String?), `nationalIdNumber` (String?), `status` (String), `adminAreaId` (String?), `plots` (List<PlotEntity>), `householdMembers` (List<HouseholdMemberEntity>), `consentStatus` (String?), `consentVersion` (String?), `consentDate` (DateTime?).
-   **Requirements Met:** Core data representation.

##### `entities/plot_entity.dart`, `entities/household_entity.dart`, `entities/household_member_entity.dart`
-   Similar `Entity` classes for related concepts. `PlotEntity` includes `latitude`, `longitude`, `polygonCoordinates` (String, GeoJSON?).

##### `repositories/farmer_repository.dart` (Interface)
-   **`FarmerRepository` abstract class:**
    -   `Future<Either<Failure, FarmerEntity>> getFarmer(String farmerId);`
    -   `Future<Either<Failure, void>> registerOrUpdateFarmer(FarmerEntity farmer);`
    -   `Future<Either<Failure, List<FarmerEntity>>> getAllLocalFarmers();`
    -   `Future<Either<Failure, List<FarmerEntity>>> getFarmersToSync();`
    -   `Future<Either<Failure, List<FarmerEntity>>> searchLocalFarmers(String query);`
    -   `Future<Either<Failure, void>> markFarmerAsSynced(String localId, String serverId, FarmerEntity serverFarmerData);`
    -   `Future<Either<Failure, void>> markFarmerSyncFailed(String localId, String errorMessage);`
    -   `Future<Either<Failure, void>> deleteFarmer(String farmerId);` (soft delete)
-   **Requirements Met:** Decouples domain from data implementation.

##### `usecases/register_farmer_usecase.dart`
-   **`RegisterFarmerUsecase` class:**
    -   `final FarmerRepository _repository;`
    -   `Future<Either<Failure, void>> call(FarmerEntity farmer) async { return await _repository.registerOrUpdateFarmer(farmer); }`
##### `usecases/get_farmer_details_usecase.dart`
##### `usecases/get_all_local_farmers_usecase.dart`
##### `usecases/search_local_farmers_usecase.dart`

#### 5.2.3 Presentation Layer
##### `bloc/farmer_registration_bloc/farmer_registration_event.dart`
-   `abstract class FarmerRegistrationEvent extends Equatable {}`
-   `class SubmitFarmerRegistration extends FarmerRegistrationEvent { final FarmerEntity farmer; ... }`
-   `class LoadFarmerForEdit extends FarmerRegistrationEvent { final String farmerId; ... }`

##### `bloc/farmer_registration_bloc/farmer_registration_state.dart`
-   `abstract class FarmerRegistrationState extends Equatable {}`
-   `class FarmerRegistrationInitial extends FarmerRegistrationState {}`
-   `class FarmerRegistrationLoading extends FarmerRegistrationState {}`
-   `class FarmerRegistrationSuccess extends FarmerRegistrationState { final String message; ... }`
-   `class FarmerRegistrationFailure extends FarmerRegistrationState { final String error; ... }`
-   `class FarmerLoadedForEdit extends FarmerRegistrationState { final FarmerEntity farmer; ... }`

##### `bloc/farmer_registration_bloc/farmer_registration_bloc.dart`
-   **`FarmerRegistrationBloc extends Bloc<FarmerRegistrationEvent, FarmerRegistrationState>`:**
    -   `final RegisterFarmerUsecase _registerFarmerUsecase;`
    -   `final GetFarmerDetailsUsecase _getFarmerDetailsUsecase;`
    -   Handles `SubmitFarmerRegistration` event by calling `_registerFarmerUsecase`.
    -   Handles `LoadFarmerForEdit` by calling `_getFarmerDetailsUsecase`.
    -   Emits states accordingly.

##### `screens/farmer_registration_screen.dart`
-   **`FarmerRegistrationScreen` (StatefulWidget):**
    -   Uses `Form` widget with `TextFormField`, `DropdownButtonFormField`, custom `DatePickerField`, `LocationPickerField` (for plots).
    -   Manages `TextEditingController`s for each field.
    -   Implements validation logic (e.g., required fields, phone format). REQ-4-002 (client-side validation).
    -   Uses `BlocProvider` to provide `FarmerRegistrationBloc`.
    -   Uses `BlocListener` to show snackbars/dialogs for success/failure.
    -   Uses `BlocBuilder` to update UI based on state (e.g., prefill form for editing).
    -   On submit, collects data into a `FarmerEntity` and dispatches `SubmitFarmerRegistration`.
    -   Integrates GPS capture for plot location (REQ-4-009).
    -   Plot management (add/edit/remove plots associated with farmer).
    -   Household member management.
-   **Requirements Met:** REQ-4-002, REQ-4-003, REQ-FHR-001 to REQ-FHR-007, REQ-FHR-018.

##### `screens/farmer_list_screen.dart`
-   Displays list of locally stored farmers.
-   Allows searching/filtering.
-   Navigation to `FarmerRegistrationScreen` for new registration or editing.
-   Option to initiate sync (could be global).

##### `widgets/plot_input_widget.dart`, `widgets/household_member_widget.dart`, `widgets/custom_text_field.dart`
-   Reusable widgets for complex input sections.

### 5.3 Feature: Dynamic Forms (`lib/features/dynamic_forms/`)
Structure similar to Farmer Registration:
#### Data Layer
-   `datasources/dynamic_form_local_datasource.dart`: CRUD for `DynamicFormModel`, `FormFieldModel`.
-   `datasources/form_submission_local_datasource.dart`: CRUD for `FormSubmissionModel`, `FormResponseModel`.
-   `models/form_definition_model.dart`, `models/form_field_model.dart`.
-   `models/form_submission_model.dart`, `models/form_response_model.dart`.
-   `repositories/dynamic_form_repository_impl.dart`.

#### Domain Layer
-   `entities/form_definition_entity.dart`, `entities/form_field_entity.dart`.
-   `entities/form_submission_entity.dart`, `entities/form_response_entity.dart`.
-   `repositories/dynamic_form_repository.dart` (Interface).
-   `usecases/get_form_definition_usecase.dart`.
-   `usecases/submit_form_usecase.dart`.
-   `usecases/get_pending_form_submissions_usecase.dart`.

#### Presentation Layer
-   `bloc/dynamic_form_bloc/`: BLoC for fetching form definitions and managing submission state.
-   `screens/dynamic_form_screen.dart`: Renders the dynamic form based on `FormDefinitionEntity`.
    -   Dynamically creates widgets based on `FormFieldEntity.fieldType` (text, number, date, select, GPS, image REQ-3-001).
    -   Implements client-side validation based on `FormFieldEntity.validationRules` (REQ-3-002).
    -   Implements conditional logic (`show/hide` fields) based on `FormFieldEntity.conditionalLogic` (REQ-3-003).
    -   Handles localization of labels, instructions from synced form definitions (REQ-3-006, REQ-4-010).
    -   Links submission to farmer (`farmerId`) (REQ-3-008, REQ-3-013).
    -   Saves submission locally via BLoC and usecase.
-   `screens/form_list_screen.dart`: Lists available dynamic forms for a selected farmer.
-   `widgets/dynamic_field_widget_factory.dart`: A factory to return appropriate Flutter widget based on field type.
-   **Requirements Met:** REQ-3-001, REQ-3-002, REQ-3-003, REQ-3-006, REQ-3-007, REQ-3-008, REQ-3-013, REQ-4-003.

### 5.4 Feature: Data Synchronization (`lib/features/sync/`)

#### Data Layer
-   `datasources/sync_remote_datasource.dart`:
    -   `final DfrApiService _apiService;`
    -   `Future<SyncFarmerResponseModel> pushFarmers(List<FarmerModel> farmers);`
    -   `Future<List<FarmerModel>> pullFarmers(String lastSyncTimestamp);`
    -   `Future<SyncFormResponseModel> pushFormSubmissions(List<FormSubmissionModel> submissions);`
    -   `Future<List<FormDefinitionModel>> pullFormDefinitions();`
-   `repositories/sync_repository_impl.dart`:
    -   `final SyncRemoteDatasource _remoteDatasource;`
    -   `final FarmerLocalDatasource _farmerLocalDs;`
    -   `final DynamicFormLocalDatasource _dynamicFormLocalDs;`
    -   `final FormSubmissionLocalDatasource _formSubmissionLocalDs;`
    -   `final ConnectivityService _connectivity;`
    -   **`Future<Either<Failure, SyncResult>> synchronizeAllData() async`:**
        -   Checks connectivity.
        -   **Push Phase:**
            -   Fetch pending `FarmerModel`s, `FormSubmissionModel`s from local datasources.
            -   Call `_remoteDatasource.pushFarmers()`, `_remoteDatasource.pushFormSubmissions()`.
            -   Process responses: update local `syncStatus`, `serverId`, handle conflicts/errors.
                -   Conflict strategy (REQ-4-007): e.g., server wins: update local record with server version. Client wins: re-push with conflict flag. Manual: mark as 'Conflict' for server-side resolution. (To be finalized, for now, assume server data is truth for updates, or a simple timestamp based last-write-wins).
        -   **Pull Phase:**
            -   Get last successful sync timestamp.
            -   Call `_remoteDatasource.pullFarmers()`, `_remoteDatasource.pullFormDefinitions()`.
            -   Process responses:
                -   For new/updated farmers: create/update in `_farmerLocalDs`.
                -   For new/updated form definitions: create/update in `_dynamicFormLocalDs`.
        -   Store new last successful sync timestamp.
        -   Return `SyncResult` (success, conflicts, errors).

#### Domain Layer
-   `entities/sync_result_entity.dart`: Contains summary of sync operation.
-   `repositories/sync_repository.dart` (Interface).
-   `usecases/synchronize_data_usecase.dart`:
    -   `final SyncRepository _syncRepository;`
    -   `Future<Either<Failure, SyncResult>> call() async { return await _syncRepository.synchronizeAllData(); }`

#### Presentation Layer
-   `bloc/sync_bloc/`: BLoC for managing sync state (Idle, Syncing, Success, Failure).
-   `widgets/sync_button_widget.dart` or `screens/sync_status_screen.dart`: UI to trigger sync and display status/progress.

-   **Requirements Met:** REQ-PCA-006, REQ-4-006, REQ-4-007, REQ-4-014 (sync performance part).

### 5.5 Feature: Authentication/User Session (`lib/features/auth/`)
-   **Data Layer:**
    -   `datasources/auth_remote_datasource.dart`: Calls Odoo API for login (e.g., standard Odoo `/web/session/authenticate` or custom JWT endpoint).
    -   `datasources/user_local_datasource.dart`: Stores logged-in user details locally (e.g., `UserModel` with username, role, token, assigned area ID).
    -   `repositories/auth_repository_impl.dart`.
-   **Domain Layer:**
    -   `entities/user_entity.dart`.
    -   `repositories/auth_repository.dart` (Interface for login, logout, getCurrentUser, saveSession, clearSession).
    -   `usecases/login_usecase.dart`, `logout_usecase.dart`, `get_current_user_usecase.dart`.
-   **Presentation Layer:**
    -   `bloc/auth_bloc/`: Manages authentication state (Authenticated, Unauthenticated).
    -   `screens/login_screen.dart`: UI for username/password input.
-   **Logic:**
    -   On login, `AuthRepository` calls remote datasource.
    -   On success, saves session (token, user details) using `SecureStorageService` (for token) and `UserLocalDatasource` (for user profile details).
    -   `ApiClient` is updated with the auth token.
    -   On logout, clears session and token.
    -   `AuthBloc` controls navigation based on auth state (e.g., to LoginScreen or HomeScreen).
-   **Requirements Met:** Secure Login, session management.

### 5.6 Feature: Settings & App Management (`lib/features/settings/`)
-   **Presentation Layer:**
    -   `screens/settings_screen.dart`:
        -   UI to toggle language (REQ-4-010, REQ-LMS-003).
        -   Display app version.
        -   "Check for Updates" button (triggers AppUpdateService REQ-4-013).
        -   View local logs (REQ-4-011).
        -   Logout button.
        -   Option to clear local data (with warning).
-   **Cross-Cutting: `lib/core/services/app_update_service.dart`**
    -   `final DfrApiService _apiService;`
    -   `Future<AppUpdateInfo> checkForUpdate() async`: Calls `_apiService.checkAppVersion()`.
    -   `void promptUserToUpdate(AppUpdateInfo info)`: Shows dialog.
    -   `bool isCriticalUpdate(AppUpdateInfo info)`: Logic based on `isCriticalUpdate` flag.
    -   `Future<bool> canProceedWithoutUpdate()`: Checks current version against min required version. If critical and outdated, return false.
    -   Handles logic for SD-DFR-012.
-   **Requirements Met:** REQ-4-010, REQ-4-011, REQ-4-013.

### 5.7 Platform Services Integration (`lib/core/platform_services/`)

#### `gps_service.dart`
-   **`GpsService` class:**
    -   Uses `geolocator` plugin.
    -   `Future<Position?>getCurrentPosition() async;` (handles permissions).
    -   `Stream<Position> getPositionStream() async*;`
-   **Purpose:** Abstract GPS location fetching.
-   **Requirements Met:** REQ-4-009.

#### `qr_scanner_service.dart`
-   **`QrScannerService` class:**
    -   Uses `mobile_scanner` plugin.
    -   `Future<String?>scanQrCode(BuildContext context) async;` (navigates to a scanner screen/widget, returns scanned string).
-   **Purpose:** Abstract QR code scanning.
-   **Requirements Met:** REQ-4-008.

#### `logging_service.dart`
-   **`LoggingService` class:**
    -   Uses a logging package like `logger`.
    -   Methods: `debug()`, `info()`, `warning()`, `error()`.
    -   Can be configured to write to console and/or a local file (for REQ-4-011).
    -   Local file logs should be managed (e.g., rotation, size limits).
-   **Purpose:** Centralized logging.
-   **Requirements Met:** REQ-4-011.

## 6. User Interface (UI) and User Experience (UX) Design

-   **Responsiveness:** UI must adapt to various Android smartphone and tablet screen sizes (REQ-4-002). Use Flutter's layout widgets effectively (Expanded, Flexible, MediaQuery).
-   **Material Design:** Adhere to Android Material Design guidelines for components, navigation, and interactions (REQ-4-002). Use `ThemeData` extensively.
-   **Clarity & Simplicity:** Clear icons, simple language, logical workflows, suitable for enumerators with varying literacy levels (REQ-4-002).
-   **Offline Indicators:** Clearly indicate when the app is offline and when data is pending sync.
-   **Performance:** UI responsiveness < 1 second for typical interactions (REQ-4-014). Optimize widget builds, use `const` widgets where possible.
-   **Accessibility (WCAG considerations for future if portal elements were in-app):** While WCAG is more for web, general accessibility principles (sufficient contrast, touch target sizes, text scalability) should be considered.
-   **Navigation:** Consistent and intuitive navigation (e.g., BottomNavigationBar, AppBar actions, Drawer). Consider `GoRouter` for named routes and deep linking if needed.
-   **Error Handling:** User-friendly error messages and guidance.
-   **Input Validation:** Real-time validation feedback on forms.

## 7. Security Design

-   **Local Data Encryption:** SQLite database encrypted with SQLCipher (AES-256) (REQ-4-004).
-   **Encryption Key Management:** Encryption key stored securely using `flutter_secure_storage` (leveraging Android Keystore) (REQ-4-004).
-   **API Communication:** All communication with the backend API over HTTPS/TLS 1.2+ (REQ-4-015). `ApiClient` configured for HTTPS.
-   **Authentication:** User login required. Session token (JWT from backend) securely stored and sent with API requests.
-   **Input Validation:** Both client-side (in forms) and server-side (by backend API) validation.
-   **Dependency Management:** Regularly scan and update third-party libraries (REQ-4-015, REQ-DIO-023). An SBOM will be maintained centrally for the project.
-   **OWASP MASVS:** Development practices should consider relevant MASVS guidelines (e.g., secure coding, data storage, network communication).
-   **Permissions:** Request only necessary Android permissions.

## 8. Data Synchronization Design

-   **Bi-directional:** Data flows from mobile to server and server to mobile (REQ-4-006).
-   **Mechanism:**
    1.  **Push Local Changes:**
        -   Collect records from local DB with `syncStatus` = 'PendingCreate', 'PendingUpdate', 'PendingDelete'.
        -   Batch these records and send to respective backend API sync endpoints (e.g., `/api/v1/farmers/sync`, `/api/v1/forms/submissions/sync`).
        -   Backend processes changes, performs de-duplication, validation.
        -   Backend returns results: success, failures with errors, conflict information.
        -   Mobile app updates local `syncStatus`, `serverId` (for new records), `syncAttemptTimestamp`, and error messages. If successful, `isDeleted` records are physically removed locally (or kept as tombstone if needed for longer).
    2.  **Pull Server Changes:**
        -   Mobile app requests updates from server since last successful sync timestamp (or full dataset on first sync / if forced).
        -   Endpoints: `/api/v1/farmers/updates`, `/api/v1/forms/definitions`.
        -   Server returns new/updated farmer records and form definitions.
        -   Mobile app updates/inserts these into local DB, overwriting local data if server version is newer (based on conflict resolution strategy).
-   **Conflict Resolution (REQ-4-007):**
    -   Strategy to be finalized (e.g., Last-Write-Wins based on server timestamp, Server-Wins, or flagging for manual resolution on Odoo backend).
    -   For initial implementation, a simple "Server Wins" strategy for conflicts on records updated both locally and on the server between syncs could be used: if a record pulled from the server has a more recent modification timestamp than the local "pending update" record, the server version overwrites the local changes, and the local `syncStatus` is set to 'Synced'. If local changes are more critical and need review, the record could be marked 'Conflict' and the specific conflicting fields noted for server-side administrative review. The `syncAttemptTimestamp` and server-provided record timestamps are crucial here.
-   **Resilience (REQ-4-006):**
    -   **Network Interruptions:** Sync operations should be resumable or idempotent. If a batch fails, it should be re-attempted. Store `syncAttemptTimestamp` and retry failed items.
    -   **Idempotency:** Server API endpoints should handle re-submission of the same data without creating duplicates (e.g., using local client-generated UUIDs that become the server's primary key for new records, or by checking for existing serverId for updates).
-   **Queue Management:** The `SyncQueueItem` table can be used to manage individual operations if a more granular sync queue is needed beyond just checking `syncStatus` on main entity tables. For simplicity, relying on `syncStatus` on entity tables is preferred initially.
-   **Trigger:** Sync can be manual (user-initiated button) or automatic (periodic background task if connectivity allows, or on app resume).

## 9. App Update and Version Management

-   **Distribution Strategy (REQ-DIO-012):** MDM or private app store preferred. If manual APK, safeguards are needed.
-   **Version Check (SD-DFR-012, REQ-4-013):**
    -   On app start and/or before manual sync, app calls `/api/v1/app/version` endpoint.
    -   API returns `latestVersion`, `minRequiredVersion`, `updateUrl`, `isCriticalUpdate`.
    -   App compares its current version.
    -   If `currentVersion < minRequiredVersion` or `isCriticalUpdate` is true for a newer version:
        -   Prompt user to update.
        -   If critical, block further data entry/sync until updated.
        -   Provide link/instructions to update (via MDM, store, or `updateUrl`).
    -   Backend API should also refuse sync from critically outdated app versions (REQ-PCA-019).
-   **Schema Compatibility (REQ-PCA-019):** Pre-synchronization check for critical schema incompatibilities handled by the version check. If a schema change occurred server-side that requires a mobile app update, the `minRequiredVersion` on the server would be bumped, forcing clients to update.

## 10. Configuration Management
-   **Feature Toggles (REQ-CONF-001):** `enableDarkTheme`, `enableLocalDeDuplicationCheck`.
    -   Managed via `AppConfig` service, potentially loaded from a configuration file bundled with the app or fetched from a non-critical server endpoint (if dynamic toggles are needed post-deployment, though initial scope suggests compile-time or bundled config).
-   **Database Configs (REQ-CONF-002):** `DB_NAME`, `DB_VERSION`, `DB_ENCRYPTION_KEY_ALIAS`.
    -   `DB_NAME`, `DB_VERSION` used in `DatabaseHelper`.
    -   `DB_ENCRYPTION_KEY_ALIAS` used in `EncryptionService`.
-   **API Configs (REQ-CONF-003):** `BASE_API_URL`, `API_TIMEOUT_SECONDS`.
    -   Used in `ApiClient` and `DfrApiService`.
-   **Access:** Configurations will be accessed via a dedicated `AppConfig` service/singleton, loaded during app initialization.

## 11. Error Handling and Logging
-   **Error Handling:**
    -   Use `Either<Failure, SuccessType>` from `dartz` for usecase return types to explicitly handle success and failure paths.
    -   Custom `Failure` types (ServerFailure, CacheFailure, NetworkFailure, etc.) as defined in `lib/core/error/failures.dart`.
    -   UI layer (BLoCs/Screens) will react to these failures to show appropriate user-friendly messages.
-   **Logging (REQ-4-011):**
    -   `LoggingService` (`lib/core/platform_services/logging_service.dart`) using `logger` package.
    -   Log levels: DEBUG, INFO, WARNING, ERROR.
    -   Log key events: app start, login, sync start/end/success/failure, errors, significant user actions.
    -   Logs viewable within the app (e.g., in a debug/settings screen).
    -   Optional: mechanism to export/share logs for troubleshooting.
    -   Optional: sync critical error logs to server (requires API endpoint).

## 12. Testing Strategy
-   **Unit Tests:** For individual functions, methods, BLoCs/Cubits, Usecases, Models (serialization/deserialization). Use `mockito` for mocking dependencies. (`flutter_test`, `bloc_test`)
-   **Widget Tests:** For UI widgets in isolation. (`flutter_test`)
-   **Integration Tests:** Test interactions between layers (e.g., BLoC -> Usecase -> Repository -> Datasource). Test full feature flows like farmer registration, form submission, local DB operations. (`flutter_test`, `integration_test` package).
-   **E2E Tests (if feasible):** For critical user flows across the entire app. (`flutter_driver` or `patrol`).
-   **Manual Testing:** On target Android devices/emulators (various OS versions API 26+ and screen sizes) for UI/UX, performance, offline capabilities, sync resilience, GPS, QR scanning.
-   **Security Testing:** Adherence to OWASP MASVS, checks for data leakage, secure storage verification.
-   **Performance Testing:** UI responsiveness, sync times with target data volumes (REQ-4-014).

## 13. Performance Considerations
-   **UI Responsiveness (REQ-4-014):** Target < 1 second for typical interactions. Achieved by:
    -   Optimizing widget builds (`const` widgets, `ValueListenableBuilder` where appropriate).
    -   Efficient state management (rebuild only necessary widgets).
    -   Performing long-running operations (DB access, API calls) asynchronously off the UI thread.
-   **Sync Performance (REQ-4-014):** Target 500 records < 2 mins on simulated 3G. Achieved by:
    -   Batching data for API calls.
    -   Optimizing JSON serialization/deserialization.
    -   Efficient local DB queries (proper indexing as per `databaseDesign.json`).
    -   Delta-syncing (only changed data).
-   **Local DB Performance (REQ-4-005):** Optimize for up to 5000 farmer profiles.
    -   Use database transactions for multiple related operations.
    -   Efficient queries and indexing.
    -   Paginate lists if displaying very large local datasets.
-   **App Startup Time:** Minimize by deferring non-critical initializations.

## 14. Deployment
-   **Target Platform:** Android API Level 26 (Android 8.0) and above (REQ-4-001).
-   **Distribution (REQ-DIO-012):** Via MDM, private app store, or manual APK distribution with safeguards.
-   **Builds:** Generate release APKs/AppBundles signed with a production keystore.
-   **CI/CD Pipeline (REQ-DIO-011):** To automate builds, tests, and deployments (details covered in central DFR documentation).

## 15. Dependencies on Other Repositories
-   **DFR_MOD_API_GATEWAY:** The mobile app will consume REST APIs provided by this Odoo module for:
    -   User authentication.
    -   Bi-directional data synchronization (farmer data, dynamic form definitions, dynamic form submissions).
    -   Farmer lookup.
    -   App version checking.

This SDS provides a comprehensive guide for developing the DFR Mobile Enumerator Application. Specific implementation details for each class and method will be further elaborated during the coding phase, adhering to these design principles.