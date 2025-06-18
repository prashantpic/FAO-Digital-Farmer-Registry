```dart
import 'dart:async';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:sqflite/sqflite.dart';
import 'package:dfr_mobile/core/database/encryption_service.dart';
import 'package:dfr_mobile/injection_container.dart'; // For getIt

// This file will contain the generated CREATE TABLE statements
import 'app_schema.dart';


/// Manages the encrypted local SQLite database using SQLCipher for offline data storage.
///
/// Handles database initialization, schema creation for all local tables
/// (Farmer, Plot, FormDefinition, FormSubmission, etc.), and schema migrations.
/// It uses SQLCipher for AES-256 encryption of the database file.
class DatabaseHelper {
  static final DatabaseHelper _instance = DatabaseHelper._internal();
  factory DatabaseHelper() => _instance;
  DatabaseHelper._internal();

  static Database? _database;

  // Configurable via REQ-CONF-002, using constants for now
  static const String _dbName = 'dfr_mobile.db';
  static const int _dbVersion = 1; 

  /// Provides access to the database instance.
  ///
  /// Initializes the database if it hasn't been already.
  Future<Database> get database async {
    if (_database != null && _database!.isOpen) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  /// Initializes the SQLite database with SQLCipher encryption.
  ///
  /// Retrieves the encryption key from [EncryptionService] and configures
  /// SQLCipher PRAGMA settings for encryption strength and parameters.
  Future<Database> _initDatabase() async {
    final documentsDirectory = await getApplicationDocumentsDirectory();
    final path = join(documentsDirectory.path, _dbName);
    
    final encryptionKey = await getIt<EncryptionService>().getDatabaseEncryptionKey();

    // Open the database (it will be created if it doesn't exist)
    final db = await openDatabase(
      path,
      version: _dbVersion,
      onCreate: _onCreate,
      onUpgrade: _onUpgrade,
      // Note: singleInstance: true is default behavior in sqflite >=2.0.0
    );

    // Apply SQLCipher PRAGMA settings for encryption
    // These need to be executed after opening and before any other operations on an encrypted DB.
    // The key pragma effectively encrypts an unencrypted DB or decrypts an encrypted one.
    await db.rawQuery("PRAGMA key = '$encryptionKey';");
    
    // Further security hardening PRAGMAs (as per SDS)
    // These should ideally be set when the database is first created or key is set.
    // Some PRAGMAs might only take effect on a new database or after rekeying.
    // For an existing encrypted database, these might need to be set after PRAGMA key.
    await db.rawQuery("PRAGMA kdf_iter = '256000';"); 
    await db.rawQuery("PRAGMA cipher_page_size = 4096;");
    await db.rawQuery("PRAGMA cipher_hmac_algorithm = HMAC_SHA512;"); // Make sure this is supported by SQLCipher version
    await db.rawQuery("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA512;"); // Make sure this is supported

    // Verify encryption is active by trying a simple operation.
    // If the key is wrong or encryption isn't set up, this might fail.
    try {
      await db.getVersion(); // A simple query to test the connection post-keying.
    } catch (e) {
      // Log error or throw a more specific exception
      // This indicates a problem with the encryption key or database corruption.
      // print('Error verifying encrypted database: $e');
      throw Exception("Failed to open/verify encrypted database: $e. Path: $path");
    }
    
    return db;
  }

  /// Called when the database is created for the first time.
  ///
  /// Executes `CREATE TABLE` statements for all entities defined in the application schema.
  Future<void> _onCreate(Database db, int version) async {
    final batch = db.batch();
    AppSchema.createTableStatements.forEach(batch.execute);
    AppSchema.createIndexStatements.forEach(batch.execute);
    await batch.commit(noResult: true);
  }

  /// Called when the database needs to be upgraded.
  ///
  /// Implements schema migration logic if `newVersion > oldVersion`.
  Future<void> _onUpgrade(Database db, int oldVersion, int newVersion) async {
    // Implement migration logic here if schema changes.
    // For example:
    // if (oldVersion < 2) {
    //   await db.execute("ALTER TABLE Farmer ADD COLUMN newField TEXT;");
    // }
    // This requires careful planning for each version increment.
    // For now, if _dbVersion is incremented, ensure _onCreate reflects the new schema
    // or migrations are added here.
  }

  /// Closes the database connection.
  Future<void> close() async {
    final db = _database;
    if (db != null && db.isOpen) {
      await db.close();
      _database = null;
    }
  }
}

// lib/core/database/app_schema.dart
// This would be a separate file, but included here for completeness of DatabaseHelper
// It should be generated based on the databaseDesign.json

class AppSchema {
  static final List<String> createTableStatements = [
    """
    CREATE TABLE Farmer (
        id TEXT PRIMARY KEY NOT NULL,
        uid VARCHAR(20) NOT NULL,
        fullName VARCHAR(100) NOT NULL,
        dateOfBirth TEXT,
        sex VARCHAR(10),
        contactPhone VARCHAR(20) NOT NULL,
        nationalIdType VARCHAR(50),
        nationalIdNumber VARCHAR(50),
        status VARCHAR(30) NOT NULL,
        syncStatus VARCHAR(20) NOT NULL DEFAULT 'Synced' CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error')),
        syncAttemptTimestamp INTEGER,
        isDeleted INTEGER NOT NULL DEFAULT 0,
        localDraftData TEXT
    )
    """,
    """
    CREATE TABLE Household (
        id TEXT PRIMARY KEY NOT NULL,
        uid VARCHAR(20) NOT NULL,
        syncStatus VARCHAR(20) NOT NULL DEFAULT 'Synced' CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error')),
        syncAttemptTimestamp INTEGER,
        isDeleted INTEGER NOT NULL DEFAULT 0
    )
    """,
    """
    CREATE TABLE HouseholdMember (
        id TEXT PRIMARY KEY NOT NULL,
        householdId TEXT NOT NULL,
        farmerId TEXT,
        relationshipToHead VARCHAR(50) NOT NULL,
        syncStatus VARCHAR(20) NOT NULL DEFAULT 'Synced' CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error')),
        syncAttemptTimestamp INTEGER,
        isDeleted INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (householdId) REFERENCES Household(id),
        FOREIGN KEY (farmerId) REFERENCES Farmer(id)
    )
    """,
    """
    CREATE TABLE Farm (
        id TEXT PRIMARY KEY NOT NULL,
        farmerId TEXT,
        householdId TEXT,
        name VARCHAR(100),
        syncStatus VARCHAR(20) NOT NULL DEFAULT 'Synced' CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error')),
        syncAttemptTimestamp INTEGER,
        isDeleted INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (farmerId) REFERENCES Farmer(id),
        FOREIGN KEY (householdId) REFERENCES Household(id)
    )
    """,
    """
    CREATE TABLE Plot (
        id TEXT PRIMARY KEY NOT NULL,
        farmId TEXT NOT NULL,
        size REAL NOT NULL,
        landTenureType VARCHAR(50) NOT NULL,
        primaryCrop VARCHAR(50),
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        ownershipDetails TEXT,
        syncStatus VARCHAR(20) NOT NULL DEFAULT 'Synced' CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error')),
        syncAttemptTimestamp INTEGER,
        isDeleted INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (farmId) REFERENCES Farm(id)
    )
    """,
    """
    CREATE TABLE AdministrativeArea (
        id TEXT PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        type VARCHAR(20) NOT NULL,
        parentId TEXT,
        FOREIGN KEY (parentId) REFERENCES AdministrativeArea(id)
    )
    """,
    """
    CREATE TABLE DynamicForm (
        id TEXT PRIMARY KEY NOT NULL,
        name VARCHAR(100) NOT NULL,
        version VARCHAR(10) NOT NULL,
        status VARCHAR(20) NOT NULL
    )
    """,
    """
    CREATE TABLE FormField (
        id TEXT PRIMARY KEY NOT NULL,
        formId TEXT NOT NULL,
        fieldType VARCHAR(20) NOT NULL,
        label TEXT NOT NULL,
        isRequired INTEGER NOT NULL,
        validationRules TEXT,
        conditionalLogic TEXT,
        "order" INTEGER NOT NULL,
        options TEXT,
        FOREIGN KEY (formId) REFERENCES DynamicForm(id)
    )
    """,
    """
    CREATE TABLE FormSubmission (
        id TEXT PRIMARY KEY NOT NULL,
        serverId TEXT,
        formId TEXT NOT NULL,
        farmerId TEXT NOT NULL,
        submissionDate INTEGER NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'Draft' CHECK (status IN ('Draft', 'PendingSync', 'Synced', 'SyncFailed')),
        syncAttemptTimestamp INTEGER,
        errorMessage TEXT,
        FOREIGN KEY (formId) REFERENCES DynamicForm(id),
        FOREIGN KEY (farmerId) REFERENCES Farmer(id)
    )
    """,
    """
    CREATE TABLE FormResponse (
        id TEXT PRIMARY KEY NOT NULL,
        serverId TEXT,
        submissionId TEXT NOT NULL,
        fieldId TEXT NOT NULL,
        value TEXT NOT NULL,
        syncStatus VARCHAR(20) NOT NULL DEFAULT 'Synced' CHECK (syncStatus IN ('Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error')),
        syncAttemptTimestamp INTEGER,
        isDeleted INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (submissionId) REFERENCES FormSubmission(id),
        FOREIGN KEY (fieldId) REFERENCES FormField(id)
    )
    """,
    """
    CREATE TABLE User (
        id TEXT PRIMARY KEY NOT NULL,
        username VARCHAR(50) NOT NULL,
        role VARCHAR(30) NOT NULL,
        assignedAreaId TEXT,
        FOREIGN KEY (assignedAreaId) REFERENCES AdministrativeArea(id)
    )
    """,
    """
    CREATE TABLE SyncQueueItem (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        entityName VARCHAR(50) NOT NULL,
        entityId TEXT NOT NULL,
        operation VARCHAR(20) NOT NULL CHECK (operation IN ('Create', 'Update', 'Delete')),
        timestamp INTEGER NOT NULL,
        status VARCHAR(20) NOT NULL DEFAULT 'Pending' CHECK (status IN ('Pending', 'Processing', 'Completed', 'Failed', 'Conflict')),
        attemptCount INTEGER NOT NULL DEFAULT 0,
        errorMessage TEXT
    )
    """
  ];

  static final List<String> createIndexStatements = [
    "CREATE INDEX IF NOT EXISTS idx_mobile_farmer_uid ON Farmer(uid)",
    "CREATE INDEX IF NOT EXISTS idx_mobile_plot_farm_id ON Plot(farmId)",
    "CREATE INDEX IF NOT EXISTS idx_mobile_plot_location ON Plot(latitude, longitude)",
    "CREATE INDEX IF NOT EXISTS idx_mobile_admin_area_parent_id ON AdministrativeArea(parentId)",
    "CREATE INDEX IF NOT EXISTS idx_mobile_formfield_form_order ON FormField(formId, \"order\")",
    "CREATE INDEX IF NOT EXISTS idx_mobile_formsubmission_farmer_form ON FormSubmission(farmerId, formId)",
    "CREATE INDEX IF NOT EXISTS idx_mobile_formresponse_submission_field ON FormResponse(submissionId, fieldId)",
    "CREATE INDEX IF NOT EXISTS idx_mobile_syncqueue_status_ts ON SyncQueueItem(status, timestamp)"
  ];
}
```