```dart
import 'package:sqflite/sqflite.dart';
import 'package:uuid/uuid.dart';
import 'package:dfr_mobile/core/database/database_helper.dart';
import 'package:dfr_mobile/features/farmer_registration/data/models/farmer_model.dart';
import 'package:dfr_mobile/core/constants/db_constants.dart';

/// Abstract class defining the contract for local data operations on Farmer entities.
///
/// This interface provides methods for CRUD (Create, Read, Update, Delete) operations
/// on farmer data stored in the local SQLite database. It supports offline functionality
/// by managing farmer records locally.
/// Requirements: REQ-4-003.
abstract class FarmerLocalDatasource {
  /// Creates a new farmer record in the local database.
  ///
  /// The [farmer] model should have its `id` (local UUID) pre-populated.
  /// Returns the local ID (UUID string) of the newly created farmer.
  Future<String> createFarmer(FarmerModel farmer);

  /// Retrieves a farmer record by its local ID.
  ///
  /// Returns the [FarmerModel] if found, otherwise null.
  Future<FarmerModel?> getFarmerById(String id);

  /// Retrieves a farmer record by its server ID.
  ///
  /// Returns the [FarmerModel] if found, otherwise null.
  Future<FarmerModel?> getFarmerByServerId(String serverId);

  /// Retrieves a farmer record by its UID (Farmer Unique Identifier).
  ///
  /// Corresponds to REQ-4-008 for local lookup by UID.
  /// Returns the [FarmerModel] if found, otherwise null.
  Future<FarmerModel?> getFarmerByUid(String uid);

  /// Retrieves all farmer records stored locally.
  Future<List<FarmerModel>> getAllFarmers();

  /// Searches for farmers by name in the local database.
  ///
  /// Corresponds to REQ-FHR-017 (local search part).
  /// The [nameQuery] is used to filter farmers whose `fullName` contains the query.
  Future<List<FarmerModel>> searchFarmersByName(String nameQuery);

  /// Updates an existing farmer record in the local database.
  ///
  /// Uses the `id` field of the [farmer] model to identify the record to update.
  /// Returns the number of rows affected (typically 1 if successful, 0 if not found).
  Future<int> updateFarmer(FarmerModel farmer);

  /// Updates the synchronization status and server ID of a local farmer record.
  ///
  /// This is typically called after a successful sync operation.
  Future<void> updateFarmerSyncStatus(
      String localId, String? serverId, String syncStatus, int? syncAttemptTimestamp);

  /// Marks a farmer record for deletion (soft delete).
  ///
  /// Sets `isDeleted` to true and `syncStatus` to 'PendingDelete'.
  /// The [id] is the local ID of the farmer to delete.
  /// Returns the number of rows affected.
  Future<int> deleteFarmer(String id);

  /// Retrieves farmers based on their synchronization status.
  ///
  /// Useful for fetching records that are pending creation, update, or deletion.
  Future<List<FarmerModel>> getFarmersBySyncStatus(List<String> statuses);

  /// Retrieves farmers that are pending synchronization (Create, Update, Delete).
  ///
  /// This is a convenience method calling [getFarmersBySyncStatus].
  Future<List<FarmerModel>> getPendingSyncFarmers();
}

/// Implementation of [FarmerLocalDatasource] using SQLite.
///
/// This class handles all direct interactions with the local SQLite database
/// for Farmer entities, using the [DatabaseHelper] to obtain a database instance.
class FarmerLocalDatasourceImpl implements FarmerLocalDatasource {
  final DatabaseHelper _dbHelper;
  final Uuid _uuid;

  /// Constructs a [FarmerLocalDatasourceImpl].
  ///
  /// Requires a [DatabaseHelper] for database access and a [Uuid] generator.
  FarmerLocalDatasourceImpl(this._dbHelper, this._uuid);

  @override
  Future<String> createFarmer(FarmerModel farmer) async {
    final db = await _dbHelper.database;
    // Ensure farmer has a local ID if not already set by usecase/repo
    final farmerWithId = farmer.id.isEmpty
        ? farmer.copyWith(id: _uuid.v4())
        : farmer;

    await db.insert(
      DbConstants.farmerTable,
      farmerWithId.toDbMap(),
      conflictAlgorithm: ConflictAlgorithm.replace,
    );
    return farmerWithId.id;
  }

  @override
  Future<FarmerModel?> getFarmerById(String id) async {
    final db = await _dbHelper.database;
    final List<Map<String, dynamic>> maps = await db.query(
      DbConstants.farmerTable,
      where: '${DbConstants.farmerColId} = ?',
      whereArgs: [id],
    );

    if (maps.isNotEmpty) {
      return FarmerModel.fromDbMap(maps.first);
    } else {
      return null;
    }
  }

  @override
  Future<FarmerModel?> getFarmerByServerId(String serverId) async {
    final db = await _dbHelper.database;
    final List<Map<String, dynamic>> maps = await db.query(
      DbConstants.farmerTable,
      where: '${DbConstants.farmerColServerId} = ?',
      whereArgs: [serverId],
    );

    if (maps.isNotEmpty) {
      return FarmerModel.fromDbMap(maps.first);
    } else {
      return null;
    }
  }

  @override
  Future<FarmerModel?> getFarmerByUid(String uid) async {
    final db = await _dbHelper.database;
    final List<Map<String, dynamic>> maps = await db.query(
      DbConstants.farmerTable,
      where: '${DbConstants.farmerColUid} = ? AND ${DbConstants.farmerColIsDeleted} = 0',
      whereArgs: [uid],
    );

    if (maps.isNotEmpty) {
      return FarmerModel.fromDbMap(maps.first);
    } else {
      return null;
    }
  }

  @override
  Future<List<FarmerModel>> getAllFarmers() async {
    final db = await _dbHelper.database;
    final List<Map<String, dynamic>> maps = await db.query(
      DbConstants.farmerTable,
      where: '${DbConstants.farmerColIsDeleted} = 0', // Exclude soft-deleted farmers
      orderBy: '${DbConstants.farmerColFullName} ASC',
    );
    return maps.map((map) => FarmerModel.fromDbMap(map)).toList();
  }

  @override
  Future<List<FarmerModel>> searchFarmersByName(String nameQuery) async {
    final db = await _dbHelper.database;
    final List<Map<String, dynamic>> maps = await db.query(
      DbConstants.farmerTable,
      where: '${DbConstants.farmerColFullName} LIKE ? AND ${DbConstants.farmerColIsDeleted} = 0',
      whereArgs: ['%$nameQuery%'],
      orderBy: '${DbConstants.farmerColFullName} ASC',
    );
    return maps.map((map) => FarmerModel.fromDbMap(map)).toList();
  }

  @override
  Future<int> updateFarmer(FarmerModel farmer) async {
    final db = await _dbHelper.database;
    return await db.update(
      DbConstants.farmerTable,
      farmer.toDbMap(),
      where: '${DbConstants.farmerColId} = ?',
      whereArgs: [farmer.id],
    );
  }

  @override
  Future<void> updateFarmerSyncStatus(
      String localId, String? serverId, String syncStatus, int? syncAttemptTimestamp) async {
    final db = await _dbHelper.database;
    Map<String, dynamic> valuesToUpdate = {
      DbConstants.farmerColSyncStatus: syncStatus,
      DbConstants.farmerColSyncAttemptTimestamp: syncAttemptTimestamp ?? DateTime.now().millisecondsSinceEpoch,
    };
    if (serverId != null) {
      valuesToUpdate[DbConstants.farmerColServerId] = serverId;
    }
    // If status is 'Synced' and it was 'PendingDelete', we might physically delete or keep tombstone.
    // For now, just update status. Actual deletion logic post-sync is in repository/usecase.
     if (syncStatus == SyncStatus.synced.name && serverId != null) {
        // If an item was marked PendingDelete and now is confirmed Synced (meaning server acknowledged deletion)
        // we can consider physically deleting it. However, the current SDS suggests soft deletes persist until a cleanup process.
        // For 'PendingCreate' or 'PendingUpdate' that become 'Synced', serverId is crucial.
    }


    await db.update(
      DbConstants.farmerTable,
      valuesToUpdate,
      where: '${DbConstants.farmerColId} = ?',
      whereArgs: [localId],
    );
  }


  @override
  Future<int> deleteFarmer(String id) async {
    final db = await _dbHelper.database;
    return await db.update(
      DbConstants.farmerTable,
      {
        DbConstants.farmerColIsDeleted: 1, // true
        DbConstants.farmerColSyncStatus: SyncStatus.pendingDelete.name,
        DbConstants.farmerColSyncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
      },
      where: '${DbConstants.farmerColId} = ?',
      whereArgs: [id],
    );
  }

  @override
  Future<List<FarmerModel>> getFarmersBySyncStatus(
      List<String> statuses) async {
    final db = await _dbHelper.database;
    // Creates a string of placeholders '(?, ?, ?)' for the IN clause
    final placeholders = List.filled(statuses.length, '?').join(',');
    final List<Map<String, dynamic>> maps = await db.query(
      DbConstants.farmerTable,
      where: '${DbConstants.farmerColSyncStatus} IN ($placeholders)',
      whereArgs: statuses,
    );
    return maps.map((map) => FarmerModel.fromDbMap(map)).toList();
  }
  
  @override
  Future<List<FarmerModel>> getPendingSyncFarmers() async {
    return getFarmersBySyncStatus([
      SyncStatus.pendingCreate.name,
      SyncStatus.pendingUpdate.name,
      SyncStatus.pendingDelete.name,
    ]);
  }
}

```