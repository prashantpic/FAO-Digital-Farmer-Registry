```dart
import 'package:dartz/dartz.dart';

import '../../../../core/error/failures.dart';
import '../../../../core/network/connectivity_service.dart';
import '../../../../core/security/secure_storage_service.dart';
import '../../../../core/utils/app_constants.dart'; // For sync status and storage keys
import '../../../dynamic_forms/data/datasources/dynamic_form_local_datasource.dart';
import '../../../dynamic_forms/data/datasources/form_submission_local_datasource.dart';
import '../../../dynamic_forms/data/models/form_definition_model.dart';
import '../../../dynamic_forms/data/models/form_submission_model.dart';
import '../../../farmer_registration/data/datasources/farmer_local_datasource.dart';
import '../../../farmer_registration/data/models/farmer_model.dart';
import '../../domain/entities/sync_result_entity.dart';
import '../../domain/repositories/sync_repository.dart';
import '../datasources/sync_remote_datasource.dart';
// Import response models from remote datasource if they are specific
// e.g. import '../models/sync_farmer_response_model.dart';

/// Implementation of the [SyncRepository] interface.
///
/// This repository manages the bi-directional data synchronization process
/// between the mobile application and the DFR backend API. It handles
/// pushing local changes and pulling server updates.
class SyncRepositoryImpl implements SyncRepository {
  final SyncRemoteDatasource remoteDatasource;
  final FarmerLocalDatasource farmerLocalDatasource;
  final DynamicFormLocalDatasource dynamicFormLocalDatasource;
  final FormSubmissionLocalDatasource formSubmissionLocalDatasource;
  final ConnectivityService connectivityService;
  final SecureStorageService secureStorageService;

  SyncRepositoryImpl({
    required this.remoteDatasource,
    required this.farmerLocalDatasource,
    required this.dynamicFormLocalDatasource,
    required this.formSubmissionLocalDatasource,
    required this.connectivityService,
    required this.secureStorageService,
  });

  @override
  Future<Either<Failure, SyncResultEntity>> synchronizeAllData() async {
    final bool isConnected = await connectivityService.isConnected();
    if (!isConnected) {
      return Left(NetworkFailure(message: 'No internet connection.'));
    }

    int successCount = 0;
    int conflictCount = 0;
    List<String> errorMessages = [];

    try {
      // --- PUSH PHASE ---
      // 1. Push Farmers
      final farmersToPush = await farmerLocalDatasource.getFarmersBySyncStatus([
        SyncStatus.pendingCreate,
        SyncStatus.pendingUpdate,
        SyncStatus.pendingDelete,
      ]);

      if (farmersToPush.isNotEmpty) {
        final pushFarmerResult = await remoteDatasource.pushFarmers(farmersToPush);
        await pushFarmerResult.fold(
          (failure) {
            errorMessages.add('Failed to push farmers: ${failure.message}');
            // Optionally mark these farmers as error locally
            for (var farmer in farmersToPush) {
               farmerLocalDatasource.updateFarmer(farmer.copyWith(syncStatus: SyncStatus.error, syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch));
            }
          },
          (syncFarmerResponse) async {
            // Process successful pushes and conflicts for farmers
            for (var syncedFarmerInfo in syncFarmerResponse.syncedFarmers) {
              final localFarmer = await farmerLocalDatasource.getFarmerById(syncedFarmerInfo.localId);
              if (localFarmer != null) {
                if (localFarmer.syncStatus == SyncStatus.pendingDelete && syncedFarmerInfo.isSuccess) {
                    await farmerLocalDatasource.hardDeleteFarmer(localFarmer.id); // Hard delete after successful server delete
                     // also delete related plots and household members
                    await farmerLocalDatasource.deletePlotsByFarmerId(localFarmer.id);
                    await farmerLocalDatasource.deleteHouseholdMembersByFarmerId(localFarmer.id);
                } else if (syncedFarmerInfo.isSuccess && syncedFarmerInfo.serverData != null) {
                   await farmerLocalDatasource.updateFarmer(
                    syncedFarmerInfo.serverData!.copyWith( // Use server data as truth
                        id: localFarmer.id, // Keep local ID
                        serverId: syncedFarmerInfo.serverData!.serverId ?? syncedFarmerInfo.serverData!.id, // Ensure serverId is set
                        syncStatus: SyncStatus.synced,
                        syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
                        isDeleted: false, // ensure not marked as deleted if successfully synced
                    ));
                }
                successCount++;
              }
            }
            for (var conflictedFarmerInfo in syncFarmerResponse.conflictedFarmers) {
              final localFarmer = await farmerLocalDatasource.getFarmerById(conflictedFarmerInfo.localId);
               if (localFarmer != null && conflictedFarmerInfo.serverData != null) {
                 // Server Wins: Overwrite local with server version in case of conflict during push
                 await farmerLocalDatasource.updateFarmer(
                    conflictedFarmerInfo.serverData!.copyWith(
                        id: localFarmer.id, // Keep local ID
                        serverId: conflictedFarmerInfo.serverData!.serverId ?? conflictedFarmerInfo.serverData!.id,
                        syncStatus: SyncStatus.synced, // Mark as synced, as server has resolved it
                        syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
                        isDeleted: false,
                    ));
                  conflictCount++; // Or treat as success if server wins is the policy
                  errorMessages.add('Farmer conflict (localId: ${conflictedFarmerInfo.localId}): Server version applied. ${conflictedFarmerInfo.message}');
               } else {
                  // If serverData is null, mark as error or keep pending with conflict note
                  await farmerLocalDatasource.updateFarmer(localFarmer!.copyWith(syncStatus: SyncStatus.conflict, syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch));
                  conflictCount++;
                  errorMessages.add('Farmer conflict (localId: ${conflictedFarmerInfo.localId}): ${conflictedFarmerInfo.message}');
               }
            }
             for (var erroredFarmerInfo in syncFarmerResponse.erroredFarmers) {
              final localFarmer = await farmerLocalDatasource.getFarmerById(erroredFarmerInfo.localId);
              if (localFarmer != null) {
                await farmerLocalDatasource.updateFarmer(localFarmer.copyWith(syncStatus: SyncStatus.error, syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch));
                errorMessages.add('Farmer sync error (localId: ${erroredFarmerInfo.localId}): ${erroredFarmerInfo.message}');
              }
            }
          },
        );
      }

      // 2. Push Form Submissions
      final submissionsToPush = await formSubmissionLocalDatasource.getFormSubmissionsByStatus([
          SyncStatus.pendingCreate, // Assuming submissions are only created, not updated/deleted via this flow directly
      ]);
      if (submissionsToPush.isNotEmpty) {
        final pushSubmissionResult = await remoteDatasource.pushFormSubmissions(submissionsToPush);
        await pushSubmissionResult.fold(
          (failure) {
            errorMessages.add('Failed to push form submissions: ${failure.message}');
            for (var sub in submissionsToPush) {
               formSubmissionLocalDatasource.updateFormSubmission(sub.copyWith(status: SyncStatus.error, syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch));
            }
          },
          (syncSubmissionResponse) async {
            for (var syncedInfo in syncSubmissionResponse.syncedSubmissions) {
              final localSubmission = await formSubmissionLocalDatasource.getFormSubmissionById(syncedInfo.localId);
              if (localSubmission != null && syncedInfo.isSuccess && syncedInfo.serverData != null) {
                await formSubmissionLocalDatasource.updateFormSubmission(
                  syncedInfo.serverData!.copyWith( // Use server data
                    id: localSubmission.id,
                    serverId: syncedInfo.serverData!.serverId ?? syncedInfo.serverData!.id,
                    status: SyncStatus.synced, // 'status' here is syncStatus for the model
                    syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
                  )
                );
                successCount++;
              }
            }
            for (var erroredInfo in syncSubmissionResponse.erroredSubmissions) {
               final localSubmission = await formSubmissionLocalDatasource.getFormSubmissionById(erroredInfo.localId);
               if (localSubmission != null) {
                 await formSubmissionLocalDatasource.updateFormSubmission(localSubmission.copyWith(status: SyncStatus.error, syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch, errorMessage: erroredInfo.message));
                 errorMessages.add('Form submission sync error (localId: ${erroredInfo.localId}): ${erroredInfo.message}');
               }
            }
             // Handle conflicts if form submissions can have conflicts
          },
        );
      }

      // --- PULL PHASE ---
      final String? lastSyncTimestamp = await secureStorageService.read(key: StorageKeys.lastSyncTimestamp);
      
      // 1. Pull Farmers
      final pullFarmerResult = await remoteDatasource.pullFarmers(lastSyncTimestamp ?? '0');
      await pullFarmerResult.fold(
        (failure) => errorMessages.add('Failed to pull farmers: ${failure.message}'),
        (updatedFarmers) async {
          for (var farmerModel in updatedFarmers) {
            // Server Wins: If farmer exists locally, update with server version. Otherwise, create.
            FarmerModel? localFarmer = await farmerLocalDatasource.getFarmerByServerId(farmerModel.serverId ?? farmerModel.id);
            if (localFarmer != null) {
              // Server data is source of truth for pull.
              await farmerLocalDatasource.updateFarmer(farmerModel.copyWith(
                id: localFarmer.id, // Retain local PK
                syncStatus: SyncStatus.synced,
                syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
              ));
            } else {
              // New farmer from server
               await farmerLocalDatasource.createOrUpdateFarmer(farmerModel.copyWith(
                id: 'local_${farmerModel.serverId ?? farmerModel.id}', // Create a new local ID if needed, or use serverId as local too if schema allows. For safety, new local ID
                syncStatus: SyncStatus.synced,
                syncAttemptTimestamp: DateTime.now().millisecondsSinceEpoch,
              ));
            }
            successCount++;
          }
        },
      );

      // 2. Pull Form Definitions
      final pullFormDefResult = await remoteDatasource.pullFormDefinitions(lastSyncTimestamp ?? '0'); // Assuming form defs also use timestamp logic
      await pullFormDefResult.fold(
        (failure) => errorMessages.add('Failed to pull form definitions: ${failure.message}'),
        (formDefinitions) async {
          for (var formDefModel in formDefinitions) {
            // Upsert form definitions
            await dynamicFormLocalDatasource.createOrUpdateFormDefinition(formDefModel);
            // Upsert form fields associated with this definition
            if (formDefModel.fields != null) {
              for (var fieldModel in formDefModel.fields!) {
                await dynamicFormLocalDatasource.createOrUpdateFormField(fieldModel.copyWith(formId: formDefModel.id));
              }
            }
            successCount++;
          }
        },
      );

      if (errorMessages.isEmpty && conflictCount == 0) {
        await secureStorageService.write(
            key: StorageKeys.lastSyncTimestamp,
            value: DateTime.now().millisecondsSinceEpoch.toString());
      }

      return Right(SyncResultEntity(
        isSuccess: errorMessages.isEmpty && conflictCount == 0,
        successfulSyncs: successCount,
        conflicts: conflictCount,
        errors: errorMessages.length,
        errorMessages: errorMessages,
        syncTimestamp: DateTime.now(),
      ));

    } catch (e) {
      errorMessages.add('Unhandled synchronization error: ${e.toString()}');
      return Left(ServerFailure(message: 'Unhandled synchronization error: ${e.toString()}'));
      // Consider returning a more complete SyncResultEntity with the error
      /*
      return Right(SyncResultEntity(
        isSuccess: false,
        successfulSyncs: successCount,
        conflicts: conflictCount,
        errors: errorMessages.length,
        errorMessages: errorMessages,
        syncTimestamp: DateTime.now(),
      ));
      */
    }
  }
}
```