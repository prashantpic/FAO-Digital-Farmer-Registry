```dart
import 'package:dartz/dartz.dart';
import 'package:uuid/uuid.dart';

import '../../../../core/error/failures.dart';
import '../../../../core/network/connectivity_service.dart';
import '../../../../core/utils/app_constants.dart'; // For sync status constants
import '../../domain/entities/farmer_entity.dart';
import '../../domain/entities/plot_entity.dart'; // Placeholder
import '../../domain/entities/household_member_entity.dart'; // Placeholder
import '../../domain/repositories/farmer_repository.dart';
import '../datasources/farmer_local_datasource.dart';
// import '../datasources/farmer_remote_datasource.dart'; // Not directly used as per SDS 5.2.1 for CRUD
import '../models/farmer_model.dart';
import '../models/plot_model.dart'; // Placeholder
import '../models/household_member_model.dart'; // Placeholder

// Placeholder for HouseholdModel if needed for farmer aggregation
// import '../models/household_model.dart';

/// Implementation of the [FarmerRepository] interface.
///
/// This repository coordinates farmer data operations between local storage
/// and prepares data for synchronization. It prioritizes local data for an
/// offline-first experience.
class FarmerRepositoryImpl implements FarmerRepository {
  final FarmerLocalDatasource localDatasource;
  // final FarmerRemoteDatasource remoteDatasource; // Typically, sync repository handles remote ops
  final ConnectivityService connectivityService;
  final Uuid uuid;

  FarmerRepositoryImpl({
    required this.localDatasource,
    // required this.remoteDatasource,
    required this.connectivityService,
    required this.uuid,
  });

  @override
  Future<Either<Failure, void>> registerOrUpdateFarmer(
      FarmerEntity farmer) async {
    try {
      final FarmerModel farmerModel = FarmerModel.fromEntity(farmer);
      FarmerModel modelToSave;

      if (farmer.id != null && farmer.id!.isNotEmpty && !farmer.id!.startsWith('local_')) { // Assuming local IDs are prefixed or UUIDs
        // This is an update to an existing record (potentially synced before)
        // Ensure local ID mapping is handled if farmer.id is serverId
        final existingLocalFarmer = await localDatasource.getFarmerByServerId(farmer.id!);
        if (existingLocalFarmer != null) {
           modelToSave = farmerModel.copyWith(
            id: existingLocalFarmer.id, // Use existing local ID
            serverId: farmer.id, // serverId remains the same
            syncStatus: existingLocalFarmer.syncStatus == SyncStatus.pendingCreate 
                        ? SyncStatus.pendingCreate // Keep pending create if it was never synced
                        : SyncStatus.pendingUpdate, 
            syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
          );
        } else {
          // Farmer came with a server ID but not found locally - this case should ideally be handled by sync pull.
          // For safety, creating it as a new record to be reconciled by sync.
          final localId = 'local_${uuid.v4()}';
          modelToSave = farmerModel.copyWith(
            id: localId, // new local ID
            serverId: farmer.id, // store original serverId if provided from an external source (e.g. lookup)
            syncStatus: SyncStatus.pendingCreate, // Or PendingUpdate if we are sure it's an update to a known server entity
            syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
          );
        }
      } else if (farmer.id != null && farmer.id!.startsWith('local_')) {
        // This is an update to a locally created record
         modelToSave = farmerModel.copyWith(
          syncStatus: farmerModel.syncStatus == SyncStatus.pendingCreate 
                      ? SyncStatus.pendingCreate // Keep pending create if it was never synced
                      : SyncStatus.pendingUpdate, 
          syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
        );
      }
      else {
        // This is a new farmer registration
        final localId = 'local_${uuid.v4()}';
        modelToSave = farmerModel.copyWith(
          id: localId,
          syncStatus: SyncStatus.pendingCreate,
          syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
        );
      }
      
      // Handle plots and household members transactionally if possible with local datasource
      // For simplicity, assuming local datasource handles cascading or separate calls are made.
      await localDatasource.createOrUpdateFarmer(modelToSave);

      // Save/Update Plots
      for (var plotEntity in farmer.plots) {
        final plotModel = PlotModel.fromEntity(plotEntity).copyWith(
          farmerId: modelToSave.id, // Link to local farmer id
          syncStatus: modelToSave.syncStatus // cascade sync status or manage independently
        );
        await localDatasource.createOrUpdatePlot(plotModel);
      }

      // Save/Update Household Members
      for (var memberEntity in farmer.householdMembers) {
         final householdMemberModel = HouseholdMemberModel.fromEntity(memberEntity).copyWith(
           // Assuming Household is linked to Farmer or managed separately
           // For now, let's assume member is directly linked to farmer's local ID for this example
           // farmerId: modelToSave.id, // This depends on your DB schema for HouseholdMember
           // For now, we assume household members might be part of a Household linked to the farmer
           // or directly linked. Let's assume a direct link for this example if no householdId provided
           farmerId: modelToSave.id, 
           syncStatus: modelToSave.syncStatus // cascade sync status or manage independently
         );
         await localDatasource.createOrUpdateHouseholdMember(householdMemberModel);
      }

      return const Right(null);
    } catch (e) {
      return Left(CacheFailure(message: 'Failed to save farmer locally: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, FarmerEntity>> getFarmer(String farmerId) async {
    try {
      FarmerModel? farmerModel;
      if (farmerId.startsWith('local_')) {
        farmerModel = await localDatasource.getFarmerById(farmerId);
      } else {
        farmerModel = await localDatasource.getFarmerByServerId(farmerId);
         if (farmerModel == null) { // Fallback to local ID if server ID not found (e.g. ID is ambiguous)
            farmerModel = await localDatasource.getFarmerById(farmerId);
        }
      }

      if (farmerModel != null) {
        // Fetch related plots and household members
        final plotModels = await localDatasource.getPlotsByFarmerId(farmerModel.id);
        final householdMemberModels = await localDatasource.getHouseholdMembersByFarmerId(farmerModel.id); // Assuming this method exists

        final plots = plotModels.map((plot) => plot.toEntity()).toList();
        final householdMembers = householdMemberModels.map((member) => member.toEntity()).toList();
        
        final farmerEntity = farmerModel.toEntity().copyWith(
          plots: plots,
          householdMembers: householdMembers,
        );
        return Right(farmerEntity);
      } else {
        return Left(CacheFailure(message: 'Farmer not found locally.'));
      }
    } catch (e) {
      return Left(CacheFailure(message: 'Failed to get farmer from local storage: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, List<FarmerEntity>>> getAllLocalFarmers() async {
    try {
      final farmerModels = await localDatasource.getAllFarmers();
      final List<FarmerEntity> farmerEntities = [];
      for (var farmerModel in farmerModels) {
        final plotModels = await localDatasource.getPlotsByFarmerId(farmerModel.id);
        final householdMemberModels = await localDatasource.getHouseholdMembersByFarmerId(farmerModel.id);
        
        farmerEntities.add(
          farmerModel.toEntity().copyWith(
            plots: plotModels.map((e) => e.toEntity()).toList(),
            householdMembers: householdMemberModels.map((e) => e.toEntity()).toList(),
          )
        );
      }
      return Right(farmerEntities);
    } catch (e) {
      return Left(CacheFailure(message: 'Failed to get all local farmers: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, List<FarmerEntity>>> getFarmersToSync() async {
    try {
      final farmerModels = await localDatasource.getFarmersBySyncStatus([
        SyncStatus.pendingCreate,
        SyncStatus.pendingUpdate,
        SyncStatus.pendingDelete,
      ]);
      final List<FarmerEntity> farmerEntities = [];
      for (var farmerModel in farmerModels) {
        final plotModels = await localDatasource.getPlotsByFarmerId(farmerModel.id);
        final householdMemberModels = await localDatasource.getHouseholdMembersByFarmerId(farmerModel.id);
        
        farmerEntities.add(
          farmerModel.toEntity().copyWith(
            plots: plotModels.map((e) => e.toEntity()).toList(),
            householdMembers: householdMemberModels.map((e) => e.toEntity()).toList(),
          )
        );
      }
      return Right(farmerEntities);
    } catch (e) {
      return Left(CacheFailure(message: 'Failed to get farmers to sync: ${e.toString()}'));
    }
  }
  
  @override
  Future<Either<Failure, List<FarmerEntity>>> searchLocalFarmers(String query) async {
    try {
      final farmerModels = await localDatasource.searchFarmersByName(query);
      final List<FarmerEntity> farmerEntities = [];
      for (var farmerModel in farmerModels) {
        final plotModels = await localDatasource.getPlotsByFarmerId(farmerModel.id);
        final householdMemberModels = await localDatasource.getHouseholdMembersByFarmerId(farmerModel.id);
        
        farmerEntities.add(
          farmerModel.toEntity().copyWith(
            plots: plotModels.map((e) => e.toEntity()).toList(),
            householdMembers: householdMemberModels.map((e) => e.toEntity()).toList(),
          )
        );
      }
      return Right(farmerEntities);
    } catch (e) {
      return Left(CacheFailure(message: 'Failed to search local farmers: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, void>> markFarmerAsSynced(String localId, String serverId, FarmerModel serverFarmerData) async {
    try {
      // Merge server data with local data if necessary (Server Wins for conflicting fields)
      // For now, directly updating with server data and new status.
      // A more complex merge would compare fields.
      final updatedModel = serverFarmerData.copyWith(
        id: localId, // Keep local ID
        serverId: serverId,
        syncStatus: SyncStatus.synced,
        syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
      );
      await localDatasource.updateFarmer(updatedModel);
      // Also mark related entities as synced if they were part of the same sync payload
      return const Right(null);
    } catch (e) {
      return Left(CacheFailure(message: 'Failed to mark farmer as synced: ${e.toString()}'));
    }
  }
  
  @override
  Future<Either<Failure, void>> markFarmerSyncFailed(String localId, String errorMessage) async {
    try {
      final farmer = await localDatasource.getFarmerById(localId);
      if (farmer != null) {
        final updatedFarmer = farmer.copyWith(
          syncStatus: SyncStatus.error,
          // Potentially store error message in farmerModel if it has such a field
          // localDraftData: farmer.localDraftData ?? '' + 'Sync Error: $errorMessage', 
          syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
        );
        await localDatasource.updateFarmer(updatedFarmer);
      }
      return const Right(null);
    } catch (e) {
      return Left(CacheFailure(message: 'Failed to mark farmer sync as failed: ${e.toString()}'));
    }
  }

  @override
  Future<Either<Failure, void>> deleteFarmer(String farmerId) async {
    try {
      FarmerModel? farmerModel;
      if (farmerId.startsWith('local_')) {
        farmerModel = await localDatasource.getFarmerById(farmerId);
      } else {
        farmerModel = await localDatasource.getFarmerByServerId(farmerId);
        if (farmerModel == null) {
            farmerModel = await localDatasource.getFarmerById(farmerId); // Fallback
        }
      }

      if (farmerModel != null) {
        if (farmerModel.syncStatus == SyncStatus.pendingCreate) {
          // If it was never synced, just delete it locally.
          await localDatasource.hardDeleteFarmer(farmerModel.id); 
          // also delete related plots and household members
          await localDatasource.deletePlotsByFarmerId(farmerModel.id);
          await localDatasource.deleteHouseholdMembersByFarmerId(farmerModel.id);
        } else {
          // Soft delete: mark for deletion and sync
          final updatedFarmer = farmerModel.copyWith(
            isDeleted: true,
            syncStatus: SyncStatus.pendingDelete,
            syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
          );
          await localDatasource.updateFarmer(updatedFarmer);
          // Also mark related entities for deletion if needed
        }
        return const Right(null);
      } else {
        return Left(CacheFailure(message: 'Farmer not found for deletion.'));
      }
    } catch (e) {
      return Left(CacheFailure(message: 'Failed to delete farmer: ${e.toString()}'));
    }
  }
}
```