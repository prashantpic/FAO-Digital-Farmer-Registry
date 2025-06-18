import 'package:dartz/dartz.dart';
import 'package:dfr_mobile/core/error/failures.dart';
import 'package:dfr_mobile/features/farmer_registration/domain/entities/farmer_entity.dart';
// Note: FarmerModel is from data layer, for markFarmerAsSynced, domain layer should ideally work with FarmerEntity.
// If server data necessitates FarmerModel, this is an exception or a mapping should occur within repository impl.
// For now, adhering to SDS reference of FarmerModel for serverFarmerData.
import 'package:dfr_mobile/features/farmer_registration/data/models/farmer_model.dart';


/// Abstract interface defining the contract for farmer data operations.
///
/// This repository decouples the domain logic (use cases) from the specific
/// implementations of data sources (local database, remote API).
/// It uses `Either` for functional error handling, returning a `Failure` on error
/// or the expected success type.
abstract class FarmerRepository {
  /// Retrieves a specific farmer by their ID.
  ///
  /// - [farmerId]: The ID of the farmer to retrieve.
  /// Returns `Either<Failure, FarmerEntity>`.
  Future<Either<Failure, FarmerEntity>> getFarmer(String farmerId);

  /// Registers a new farmer or updates an existing one.
  ///
  /// - [farmer]: The [FarmerEntity] object containing farmer data.
  /// Returns `Either<Failure, void>` indicating success or failure.
  Future<Either<Failure, void>> registerOrUpdateFarmer(FarmerEntity farmer);

  /// Retrieves all farmers stored locally on the device.
  ///
  /// Returns `Either<Failure, List<FarmerEntity>>`.
  Future<Either<Failure, List<FarmerEntity>>> getAllLocalFarmers();

  /// Retrieves a list of farmers that are pending synchronization with the server.
  /// This typically includes farmers with `syncStatus` like 'PendingCreate', 'PendingUpdate', 'PendingDelete'.
  ///
  /// Returns `Either<Failure, List<FarmerEntity>>`.
  Future<Either<Failure, List<FarmerEntity>>> getFarmersToSync();

  /// Searches for local farmers based on a query string (e.g., name).
  ///
  /// - [query]: The search query.
  /// Returns `Either<Failure, List<FarmerEntity>>`.
  Future<Either<Failure, List<FarmerEntity>>> searchLocalFarmers(String query);

  /// Marks a locally stored farmer as synchronized with the server.
  ///
  /// This method updates the local record's `syncStatus` to 'Synced', stores the `serverId`,
  /// and potentially merges any conflicting data based on the `serverFarmerData`.
  /// The `serverFarmerData` is of type `FarmerModel` as per SDS, which might contain
  /// more raw data structure from the server.
  ///
  /// - [localId]: The local ID of the farmer record.
  /// - [serverId]: The server-assigned ID for the farmer.
  /// - [serverFarmerData]: The farmer data as received from the server (potentially `FarmerModel`).
  ///                       Consider if this should be `FarmerEntity` for consistency, with mapping done earlier.
  ///                       As per SDS (5.2.1 repositories/farmer_repository_impl.dart), it's `FarmerModel serverFarmerData`.
  ///                       The interface matches the signature, implying `FarmerModel` from server is directly used here for merging.
  Future<Either<Failure, void>> markFarmerAsSynced(String localId, String serverId, FarmerModel serverFarmerData);


  /// Marks a locally stored farmer as failed to synchronize.
  ///
  /// This method updates the local record's `syncStatus` to 'Error' and stores
  /// an error message for troubleshooting.
  ///
  /// - [localId]: The local ID of the farmer record.
  /// - [errorMessage]: A message describing the synchronization failure.
  /// Returns `Either<Failure, void>`.
  Future<Either<Failure, void>> markFarmerSyncFailed(String localId, String errorMessage);

  /// Deletes a farmer record (typically a soft delete locally, marking for sync).
  ///
  /// - [farmerId]: The ID of the farmer to delete.
  /// Returns `Either<Failure, void>`.
  Future<Either<Failure, void>> deleteFarmer(String farmerId);
}