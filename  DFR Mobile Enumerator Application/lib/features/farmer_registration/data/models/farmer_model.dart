import 'package:equatable/equatable.dart';
import 'package:dfr_mobile/features/farmer_registration/domain/entities/farmer_entity.dart';
// These imports are placeholders for now.
// Actual PlotModel and HouseholdMemberModel would be in their respective files.
import 'package:dfr_mobile/features/farmer_registration/data/models/plot_model.dart';
import 'package:dfr_mobile/features/farmer_registration/data/models/household_member_model.dart';


/// Represents the data transfer object (DTO) for a Farmer.
///
/// This model is used for communication with the API (serialization/deserialization)
/// and for local database storage (mapping to/from database rows).
/// It includes all fields necessary for these operations, including synchronization-related fields.
class FarmerModel extends Equatable {
  /// Local unique identifier (e.g., UUID) for the farmer record, primarily used before first sync.
  final String id;

  /// Server-side unique identifier (e.g., UUID) for the farmer, populated after synchronization.
  final String? serverId;

  /// Farmer's unique identification number (UID) as per system requirements.
  final String uid;

  /// Full name of the farmer.
  final String fullName;

  /// Date of birth of the farmer, stored as an ISO8601 string (e.g., "YYYY-MM-DD").
  final String? dateOfBirth;

  /// Gender/sex of the farmer.
  final String? sex;

  /// Contact phone number of the farmer.
  final String contactPhone;

  /// Type of national identification document (e.g., "National ID Card", "Passport").
  final String? nationalIdType;

  /// National identification number from the document.
  final String? nationalIdNumber;

  /// Current status of the farmer (e.g., "Active", "Inactive"), typically from the server.
  final String status;

  /// Foreign key to the local `AdministrativeArea` table.
  final String? adminAreaId;

  /// Consent status (e.g., "Given", "Pending", "Refused").
  final String? consentStatus;

  /// Version of the consent form signed/agreed to.
  final String? consentVersion;

  /// Date when consent was given/updated, stored as an ISO8601 string.
  final String? consentDate;

  /// Synchronization status of this record with the server.
  /// Possible values: 'Synced', 'PendingCreate', 'PendingUpdate', 'PendingDelete', 'Conflict', 'Error'.
  final String syncStatus;

  /// Unix timestamp of the last synchronization attempt for this record.
  final int? syncAttemptTimestamp;

  /// Flag indicating if the record is marked for soft deletion.
  final bool isDeleted;

  /// List of plots associated with this farmer.
  final List<PlotModel>? plots;

  /// List of household members associated with this farmer's household.
  /// Note: This might be part of a `HouseholdModel` linked to the farmer,
  /// depending on the exact data structure. Included here as per SDS example.
  final List<HouseholdMemberModel>? householdMembers;

  /// Local draft data, potentially JSON string for changes not yet finalized.
  final String? localDraftData;


  const FarmerModel({
    required this.id,
    this.serverId,
    required this.uid,
    required this.fullName,
    this.dateOfBirth,
    this.sex,
    required this.contactPhone,
    this.nationalIdType,
    this.nationalIdNumber,
    required this.status,
    this.adminAreaId,
    this.consentStatus,
    this.consentVersion,
    this.consentDate,
    required this.syncStatus,
    this.syncAttemptTimestamp,
    required this.isDeleted,
    this.plots,
    this.householdMembers,
    this.localDraftData,
  });

  /// Creates a [FarmerModel] from a JSON map (typically from API response).
  factory FarmerModel.fromJson(Map<String, dynamic> json) {
    return FarmerModel(
      // Prefer serverId from JSON if available, otherwise it might be a local-only record
      // or the JSON structure needs to clarify if `id` is local or server.
      // Assuming `id` from JSON is serverId for now. Local `id` should be handled separately.
      id: json['localId'] as String? ?? json['id'] as String, // Adjust based on API contract for local vs server id
      serverId: json['serverId'] as String? ?? json['id'] as String?, // If `id` in JSON is server's ID
      uid: json['uid'] as String,
      fullName: json['fullName'] as String,
      dateOfBirth: json['dateOfBirth'] as String?,
      sex: json['sex'] as String?,
      contactPhone: json['contactPhone'] as String,
      nationalIdType: json['nationalIdType'] as String?,
      nationalIdNumber: json['nationalIdNumber'] as String?,
      status: json['status'] as String,
      adminAreaId: json['adminAreaId'] as String?,
      consentStatus: json['consentStatus'] as String?,
      consentVersion: json['consentVersion'] as String?,
      consentDate: json['consentDate'] as String?,
      syncStatus: json['syncStatus'] as String? ?? 'Synced', // Default if not provided
      syncAttemptTimestamp: json['syncAttemptTimestamp'] as int?,
      isDeleted: json['isDeleted'] as bool? ?? false,
      plots: (json['plots'] as List<dynamic>?)
          ?.map((plotJson) => PlotModel.fromJson(plotJson as Map<String, dynamic>))
          .toList(),
      householdMembers: (json['householdMembers'] as List<dynamic>?)
          ?.map((memberJson) => HouseholdMemberModel.fromJson(memberJson as Map<String, dynamic>))
          .toList(),
      localDraftData: json['localDraftData'] as String?,
    );
  }

  /// Converts this [FarmerModel] to a JSON map (typically for API request).
  Map<String, dynamic> toJson() {
    return {
      'localId': id, // Send localId for mapping on server if needed
      'serverId': serverId,
      'uid': uid,
      'fullName': fullName,
      'dateOfBirth': dateOfBirth,
      'sex': sex,
      'contactPhone': contactPhone,
      'nationalIdType': nationalIdType,
      'nationalIdNumber': nationalIdNumber,
      'status': status,
      'adminAreaId': adminAreaId,
      'consentStatus': consentStatus,
      'consentVersion': consentVersion,
      'consentDate': consentDate,
      'syncStatus': syncStatus,
      'syncAttemptTimestamp': syncAttemptTimestamp,
      'isDeleted': isDeleted,
      'plots': plots?.map((plot) => plot.toJson()).toList(),
      'householdMembers': householdMembers?.map((member) => member.toJson()).toList(),
      'localDraftData': localDraftData,
    };
  }

  /// Creates a [FarmerModel] from a database map.
  /// The `id` field from the DB map is assumed to be the `serverId` if `id` is server UUID.
  /// If local DB uses its own local `id`, adjust accordingly.
  /// Based on `databaseDesign.json`, `Farmer.id` is TEXT PK storing server-side UUID.
  /// So `dbMap['id']` is `serverId`. Local client-generated UUID for `FarmerModel.id`
  /// should be handled if `FarmerModel.id` is different from `Farmer.id` in DB.
  /// For this implementation: DB `id` column maps to `FarmerModel.serverId`.
  /// `FarmerModel.id` is a client-side UUID, which might need a separate column in DB or be transient.
  /// Let's assume the DB `id` column is the `serverId`. A `localId` field in the DB could store the client-side `id`.
  ///
  /// Revisiting: Per SDS 4.1, "Primary Keys: Server-side UUIDs will be stored as TEXT for entities synced from the server".
  /// This implies the `id` column in `Farmer` table is the `serverId`.
  /// `FarmerModel.id` is the client-generated local UUID.
  factory FarmerModel.fromDb(Map<String, dynamic> dbMap, {required String localId}) {
    return FarmerModel(
      id: localId, // This would be read from a dedicated 'localId' column or passed in
      serverId: dbMap['id'] as String?, // `id` column in DB stores serverId
      uid: dbMap['uid'] as String,
      fullName: dbMap['fullName'] as String,
      dateOfBirth: dbMap['dateOfBirth'] as String?,
      sex: dbMap['sex'] as String?,
      contactPhone: dbMap['contactPhone'] as String,
      nationalIdType: dbMap['nationalIdType'] as String?,
      nationalIdNumber: dbMap['nationalIdNumber'] as String?,
      status: dbMap['status'] as String,
      adminAreaId: dbMap['adminAreaId'] as String?, // Assuming this column exists
      consentStatus: dbMap['consentStatus'] as String?, // Assuming this column exists
      consentVersion: dbMap['consentVersion'] as String?, // Assuming this column exists
      consentDate: dbMap['consentDate'] as String?, // Assuming this column exists
      syncStatus: dbMap['syncStatus'] as String,
      syncAttemptTimestamp: dbMap['syncAttemptTimestamp'] as int?,
      isDeleted: (dbMap['isDeleted'] as int? ?? 0) == 1, // SQLite stores BOOLEAN as INTEGER 0 or 1
      // plots and householdMembers would typically be loaded separately via their respective DAOs
      plots: const [], // Placeholder, load separately
      householdMembers: const [], // Placeholder, load separately
      localDraftData: dbMap['localDraftData'] as String?,
    );
  }

  /// Converts this [FarmerModel] to a map suitable for database insertion/update.
  /// The `id` key in the map should correspond to the `serverId` for the DB's `id` column.
  /// The `FarmerModel.id` (local UUID) might be stored in a `localId` column.
  Map<String, dynamic> toDbMap() {
    return {
      'id': serverId, // `id` column in DB stores serverId
      'localId': id, // Store local client-generated UUID in a separate 'localId' column
      'uid': uid,
      'fullName': fullName,
      'dateOfBirth': dateOfBirth,
      'sex': sex,
      'contactPhone': contactPhone,
      'nationalIdType': nationalIdType,
      'nationalIdNumber': nationalIdNumber,
      'status': status,
      'adminAreaId': adminAreaId,
      'consentStatus': consentStatus,
      'consentVersion': consentVersion,
      'consentDate': consentDate,
      'syncStatus': syncStatus,
      'syncAttemptTimestamp': syncAttemptTimestamp,
      'isDeleted': isDeleted ? 1 : 0, // SQLite stores BOOLEAN as INTEGER
      'localDraftData': localDraftData,
      // plots and householdMembers are stored in separate tables
    };
  }


  /// Creates a [FarmerModel] from a [FarmerEntity].
  factory FarmerModel.fromEntity(FarmerEntity entity) {
    return FarmerModel(
      id: entity.id, // Entity ID can be local or server ID. If local, model.id gets it.
                     // If entity.id is serverID, then model.serverId should get it, and model.id needs a local UUID.
                     // Assuming entity.id is the primary concept of ID (local or server)
      serverId: entity.id.startsWith("local_") ? null : entity.id, // Simple heuristic, refine as needed
      uid: entity.uid,
      fullName: entity.fullName,
      dateOfBirth: entity.dateOfBirth?.toIso8601String().substring(0,10),
      sex: entity.sex,
      contactPhone: entity.contactPhone,
      nationalIdType: entity.nationalIdType,
      nationalIdNumber: entity.nationalIdNumber,
      status: entity.status,
      adminAreaId: entity.adminAreaId,
      consentStatus: entity.consentStatus,
      consentVersion: entity.consentVersion,
      consentDate: entity.consentDate?.toIso8601String().substring(0,10),
      syncStatus: 'PendingCreate', // Default for new entity, adjust if entity has sync status
      isDeleted: false, // Default for new entity
      plots: entity.plots?.map((plotEntity) => PlotModel.fromEntity(plotEntity)).toList(),
      householdMembers: entity.householdMembers?.map((memberEntity) => HouseholdMemberModel.fromEntity(memberEntity)).toList(),
      // syncAttemptTimestamp and localDraftData usually managed internally by data layer
    );
  }

  /// Converts this [FarmerModel] to a [FarmerEntity].
  FarmerEntity toEntity() {
    return FarmerEntity(
      id: serverId ?? id, // Prefer serverId if available, otherwise use local id
      uid: uid,
      fullName: fullName,
      dateOfBirth: dateOfBirth != null ? DateTime.tryParse(dateOfBirth!) : null,
      sex: sex,
      contactPhone: contactPhone,
      nationalIdType: nationalIdType,
      nationalIdNumber: nationalIdNumber,
      status: status,
      adminAreaId: adminAreaId,
      consentStatus: consentStatus,
      consentVersion: consentVersion,
      consentDate: consentDate != null ? DateTime.tryParse(consentDate!) : null,
      plots: plots?.map((plotModel) => plotModel.toEntity()).toList(),
      householdMembers: householdMembers?.map((memberModel) => memberModel.toEntity()).toList(),
      // syncStatus, isDeleted etc. are data layer concerns, not typically part of pure entity
    );
  }

  FarmerModel copyWith({
    String? id,
    String? serverId,
    String? uid,
    String? fullName,
    String? dateOfBirth,
    String? sex,
    String? contactPhone,
    String? nationalIdType,
    String? nationalIdNumber,
    String? status,
    String? adminAreaId,
    String? consentStatus,
    String? consentVersion,
    String? consentDate,
    String? syncStatus,
    int? syncAttemptTimestamp,
    bool? isDeleted,
    List<PlotModel>? plots,
    List<HouseholdMemberModel>? householdMembers,
    String? localDraftData,
  }) {
    return FarmerModel(
      id: id ?? this.id,
      serverId: serverId ?? this.serverId,
      uid: uid ?? this.uid,
      fullName: fullName ?? this.fullName,
      dateOfBirth: dateOfBirth ?? this.dateOfBirth,
      sex: sex ?? this.sex,
      contactPhone: contactPhone ?? this.contactPhone,
      nationalIdType: nationalIdType ?? this.nationalIdType,
      nationalIdNumber: nationalIdNumber ?? this.nationalIdNumber,
      status: status ?? this.status,
      adminAreaId: adminAreaId ?? this.adminAreaId,
      consentStatus: consentStatus ?? this.consentStatus,
      consentVersion: consentVersion ?? this.consentVersion,
      consentDate: consentDate ?? this.consentDate,
      syncStatus: syncStatus ?? this.syncStatus,
      syncAttemptTimestamp: syncAttemptTimestamp ?? this.syncAttemptTimestamp,
      isDeleted: isDeleted ?? this.isDeleted,
      plots: plots ?? this.plots,
      householdMembers: householdMembers ?? this.householdMembers,
      localDraftData: localDraftData ?? this.localDraftData,
    );
  }

  @override
  List<Object?> get props => [
        id,
        serverId,
        uid,
        fullName,
        dateOfBirth,
        sex,
        contactPhone,
        nationalIdType,
        nationalIdNumber,
        status,
        adminAreaId,
        consentStatus,
        consentVersion,
        consentDate,
        syncStatus,
        syncAttemptTimestamp,
        isDeleted,
        plots,
        householdMembers,
        localDraftData,
      ];
}