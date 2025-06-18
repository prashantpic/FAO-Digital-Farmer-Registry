```dart
import 'package:dio/dio.dart';
import 'package:dartz/dartz.dart';
import 'package:dfr_mobile/core/network/api_client.dart';
import 'package:dfr_mobile/core/error/failures.dart';
import 'package:dfr_mobile/features/farmer_registration/data/models/farmer_model.dart';
import 'package:dfr_mobile/features/dynamic_forms/data/models/form_definition_model.dart';
import 'package:dfr_mobile/features/dynamic_forms/data/models/form_submission_model.dart';

// Placeholder models, these would typically be defined in their respective feature folders
// or a shared models location, based on actual API response structures.

/// Model representing information about the application version from the API.
///
/// Corresponds to REQ-4-013 and SD-DFR-012.
class AppVersionInfoModel {
  final String latestVersion;
  final String minRequiredVersion;
  final String? updateUrl;
  final bool isCriticalUpdate;

  AppVersionInfoModel({
    required this.latestVersion,
    required this.minRequiredVersion,
    this.updateUrl,
    required this.isCriticalUpdate,
  });

  factory AppVersionInfoModel.fromJson(Map<String, dynamic> json) {
    return AppVersionInfoModel(
      latestVersion: json['latestVersion'] as String,
      minRequiredVersion: json['minRequiredVersion'] as String,
      updateUrl: json['updateUrl'] as String?,
      isCriticalUpdate: json['isCriticalUpdate'] as bool,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'latestVersion': latestVersion,
      'minRequiredVersion': minRequiredVersion,
      'updateUrl': updateUrl,
      'isCriticalUpdate': isCriticalUpdate,
    };
  }
}

/// Model representing the response from the farmer data synchronization API.
///
/// Corresponds to REQ-API-005.
class SyncFarmerResponseModel {
  // Example fields: lists of created, updated, conflicted IDs, or full objects
  final List<String> createdIds;
  final List<String> updatedIds;
  final List<String> conflictIds;
  // Potentially: final List<FarmerModel> updatedFarmers;

  SyncFarmerResponseModel({
    required this.createdIds,
    required this.updatedIds,
    required this.conflictIds,
    // this.updatedFarmers = const [],
  });

  factory SyncFarmerResponseModel.fromJson(Map<String, dynamic> json) {
    return SyncFarmerResponseModel(
      createdIds: List<String>.from(json['createdIds'] ?? []),
      updatedIds: List<String>.from(json['updatedIds'] ?? []),
      conflictIds: List<String>.from(json['conflictIds'] ?? []),
      // updatedFarmers: (json['updatedFarmers'] as List<dynamic>?)
      //         ?.map((e) => FarmerModel.fromJson(e as Map<String, dynamic>))
      //         .toList() ??
      //     [],
    );
  }
}

/// Model representing the response from the form submissions synchronization API.
///
/// Corresponds to REQ-API-005.
class SyncFormResponseModel {
  // Example fields similar to SyncFarmerResponseModel
  final List<String> createdSubmissionIds;
  final List<String> updatedSubmissionIds;

  SyncFormResponseModel({
    required this.createdSubmissionIds,
    required this.updatedSubmissionIds,
  });

  factory SyncFormResponseModel.fromJson(Map<String, dynamic> json) {
    return SyncFormResponseModel(
      createdSubmissionIds:
          List<String>.from(json['createdSubmissionIds'] ?? []),
      updatedSubmissionIds:
          List<String>.from(json['updatedSubmissionIds'] ?? []),
    );
  }
}

/// Service class for interacting with the DFR backend REST APIs.
///
/// This class abstracts the communication with specific DFR backend API endpoints
/// used for data synchronization, lookups, and app management.
/// It handles request building, response parsing, and error transformation.
/// Requirements: REQ-PCA-006, REQ-4-006, REQ-API-004, REQ-API-005.
class DfrApiService {
  final ApiClient _apiClient;

  /// Constructs a [DfrApiService].
  ///
  /// Requires an [ApiClient] instance for making HTTP requests.
  DfrApiService(this._apiClient);

  /// Fetches updated farmer data from the server since a given timestamp.
  ///
  /// Corresponds to REQ-API-005.
  /// Endpoint: GET `/api/v1/farmers/updates?since=:lastSyncTimestamp`
  Future<Either<Failure, List<FarmerModel>>> getUpdatedFarmerData(
      String lastSyncTimestamp) async {
    try {
      final response = await _apiClient.dio.get(
        '/api/v1/farmers/updates',
        queryParameters: {'since': lastSyncTimestamp},
      );
      final List<dynamic> data = response.data as List<dynamic>;
      final farmers = data
          .map((json) => FarmerModel.fromJson(json as Map<String, dynamic>))
          .toList();
      return Right(farmers);
    } on DioException catch (e) {
      return Left(ServerFailure(_handleDioError(e)));
    } catch (e) {
      return Left(ServerFailure('An unexpected error occurred: ${e.toString()}'));
    }
  }

  /// Synchronizes local farmer data with the server.
  ///
  /// Sends a list of [FarmerModel] to the backend for creation or update.
  /// Corresponds to REQ-API-005.
  /// Endpoint: POST `/api/v1/farmers/sync`
  Future<Either<Failure, SyncFarmerResponseModel>> syncFarmerData(
      List<FarmerModel> farmersToSync) async {
    try {
      final payload = farmersToSync.map((farmer) => farmer.toJson()).toList();
      final response =
          await _apiClient.dio.post('/api/v1/farmers/sync', data: payload);
      return Right(
          SyncFarmerResponseModel.fromJson(response.data as Map<String, dynamic>));
    } on DioException catch (e) {
      return Left(ServerFailure(_handleDioError(e)));
    } catch (e) {
      return Left(ServerFailure('An unexpected error occurred: ${e.toString()}'));
    }
  }

  /// Fetches all dynamic form definitions from the server.
  ///
  /// Corresponds to REQ-API-005.
  /// Endpoint: GET `/api/v1/forms/definitions`
  Future<Either<Failure, List<FormDefinitionModel>>>
      getFormDefinitions() async {
    try {
      final response = await _apiClient.dio.get('/api/v1/forms/definitions');
      final List<dynamic> data = response.data as List<dynamic>;
      final forms = data
          .map((json) =>
              FormDefinitionModel.fromJson(json as Map<String, dynamic>))
          .toList();
      return Right(forms);
    } on DioException catch (e) {
      return Left(ServerFailure(_handleDioError(e)));
    } catch (e) {
      return Left(ServerFailure('An unexpected error occurred: ${e.toString()}'));
    }
  }

  /// Synchronizes local form submissions with the server.
  ///
  /// Sends a list of [FormSubmissionModel] to the backend.
  /// Corresponds to REQ-API-005.
  /// Endpoint: POST `/api/v1/forms/submissions/sync`
  Future<Either<Failure, SyncFormResponseModel>> syncFormSubmissions(
      List<FormSubmissionModel> submissionsToSync) async {
    try {
      final payload =
          submissionsToSync.map((sub) => sub.toJson()).toList();
      final response = await _apiClient.dio
          .post('/api/v1/forms/submissions/sync', data: payload);
      return Right(
          SyncFormResponseModel.fromJson(response.data as Map<String, dynamic>));
    } on DioException catch (e) {
      return Left(ServerFailure(_handleDioError(e)));
    } catch (e) {
      return Left(ServerFailure('An unexpected error occurred: ${e.toString()}'));
    }
  }

  /// Checks the application version with the server.
  ///
  /// Retrieves information about the latest and minimum required app versions.
  /// Supports REQ-4-013 and SD-DFR-012.
  /// Endpoint: GET `/api/v1/app/version`
  Future<Either<Failure, AppVersionInfoModel>> checkAppVersion() async {
    try {
      final response = await _apiClient.dio.get('/api/v1/app/version');
      return Right(
          AppVersionInfoModel.fromJson(response.data as Map<String, dynamic>));
    } on DioException catch (e) {
      return Left(ServerFailure(_handleDioError(e)));
    } catch (e) {
      return Left(ServerFailure('An unexpected error occurred: ${e.toString()}'));
    }
  }

  /// Looks up a farmer by their unique ID (UID) on the server.
  ///
  /// Corresponds to REQ-API-004.
  /// Endpoint: GET `/api/v1/farmers/lookup?uid=:uid`
  Future<Either<Failure, FarmerModel?>> lookupFarmerByUid(String uid) async {
    try {
      final response = await _apiClient.dio.get(
        '/api/v1/farmers/lookup',
        queryParameters: {'uid': uid},
      );
      if (response.data == null || (response.data is Map && response.data.isEmpty) ) {
        return const Right(null);
      }
      return Right(FarmerModel.fromJson(response.data as Map<String, dynamic>));
    } on DioException catch (e) {
      if (e.response?.statusCode == 404) {
        return const Right(null); // Farmer not found
      }
      return Left(ServerFailure(_handleDioError(e)));
    } catch (e) {
      return Left(ServerFailure('An unexpected error occurred: ${e.toString()}'));
    }
  }

  /// Looks up farmers based on a set of query parameters.
  ///
  /// Corresponds to REQ-API-004.
  /// Endpoint: GET `/api/v1/farmers/lookup`
  Future<Either<Failure, List<FarmerModel>>> lookupFarmer(
      Map<String, String> queryParams) async {
    try {
      final response = await _apiClient.dio.get(
        '/api/v1/farmers/lookup',
        queryParameters: queryParams,
      );
      final List<dynamic> data = response.data as List<dynamic>;
      final farmers = data
          .map((json) => FarmerModel.fromJson(json as Map<String, dynamic>))
          .toList();
      return Right(farmers);
    } on DioException catch (e) {
      return Left(ServerFailure(_handleDioError(e)));
    } catch (e) {
      return Left(ServerFailure('An unexpected error occurred: ${e.toString()}'));
    }
  }

  /// Handles [DioException] and converts it to a meaningful error message.
  String _handleDioError(DioException error) {
    String errorMessage;
    switch (error.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        errorMessage = "Connection timeout. Please check your internet connection.";
        break;
      case DioExceptionType.badResponse:
        // Customize based on status code
        final statusCode = error.response?.statusCode;
        if (statusCode == 401) {
          errorMessage = "Unauthorized. Please login again.";
        } else if (statusCode == 403) {
          errorMessage = "Forbidden. You do not have permission to access this resource.";
        } else if (statusCode == 404) {
          errorMessage = "Resource not found.";
        } else if (statusCode != null && statusCode >= 500) {
          errorMessage = "Server error (Code: $statusCode). Please try again later.";
        } else {
          errorMessage = "Received invalid status code: ${error.response?.statusCode}";
        }
        // Log error.response?.data for more details if needed for debugging
        break;
      case DioExceptionType.cancel:
        errorMessage = "Request to API server was cancelled.";
        break;
      case DioExceptionType.connectionError:
         errorMessage = "Connection error. Please check your internet connection.";
         break;
      case DioExceptionType.unknown:
      default:
        errorMessage = "An unexpected network error occurred. Please try again.";
        if (error.message != null && error.message!.contains('SocketException')) {
          errorMessage = 'No Internet connection. Please check your network settings.';
        }
        break;
    }
    // Log the error internally if a logging service is available
    // getIt<LoggingService>().error('DioException: ${error.message}', error: error, stackTrace: error.stackTrace);
    return errorMessage;
  }
}

```