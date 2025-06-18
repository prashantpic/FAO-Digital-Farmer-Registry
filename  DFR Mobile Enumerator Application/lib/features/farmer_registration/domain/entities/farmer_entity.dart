import 'package:equatable/equatable.dart';
// Placeholder imports - these files would define PlotEntity and HouseholdMemberEntity
import 'package:dfr_mobile/features/farmer_registration/domain/entities/plot_entity.dart';
import 'package:dfr_mobile/features/farmer_registration/domain/entities/household_member_entity.dart';

/// Represents a Farmer domain entity.
///
/// This class defines the core attributes of a farmer within the application's
/// domain layer. It is independent of data sources (API, local DB) and UI concerns.
/// The `id` can be a local client-generated UUID or a server-assigned UUID depending on context.
class FarmerEntity extends Equatable {
  /// Unique identifier for the farmer. Can be a local (client-generated) ID or
  /// a server-assigned ID post-synchronization.
  final String id;

  /// Farmer's unique identification number (UID) as per system requirements.
  final String uid;

  /// Full name of the farmer.
  final String fullName;

  /// Date of birth of the farmer.
  final DateTime? dateOfBirth;

  /// Gender/sex of the farmer.
  final String? sex;

  /// Contact phone number of the farmer.
  final String contactPhone;

  /// Type of national identification document.
  final String? nationalIdType;

  /// National identification number from the document.
  final String? nationalIdNumber;

  /// Current status of the farmer (e.g., "Active", "Inactive").
  final String status;

  /// Identifier for the administrative area the farmer belongs to.
  final String? adminAreaId;

  /// List of plots associated with this farmer.
  final List<PlotEntity>? plots;

  /// List of household members associated with this farmer's household.
  final List<HouseholdMemberEntity>? householdMembers;

  /// Consent status (e.g., "Given", "Pending", "Refused").
  final String? consentStatus;

  /// Version of the consent form signed/agreed to.
  final String? consentVersion;

  /// Date when consent was given/updated.
  final DateTime? consentDate;

  const FarmerEntity({
    required this.id,
    required this.uid,
    required this.fullName,
    this.dateOfBirth,
    this.sex,
    required this.contactPhone,
    this.nationalIdType,
    this.nationalIdNumber,
    required this.status,
    this.adminAreaId,
    this.plots,
    this.householdMembers,
    this.consentStatus,
    this.consentVersion,
    this.consentDate,
  });

  @override
  List<Object?> get props => [
        id,
        uid,
        fullName,
        dateOfBirth,
        sex,
        contactPhone,
        nationalIdType,
        nationalIdNumber,
        status,
        adminAreaId,
        plots,
        householdMembers,
        consentStatus,
        consentVersion,
        consentDate,
      ];

  FarmerEntity copyWith({
    String? id,
    String? uid,
    String? fullName,
    DateTime? dateOfBirth,
    String? sex,
    String? contactPhone,
    String? nationalIdType,
    String? nationalIdNumber,
    String? status,
    String? adminAreaId,
    List<PlotEntity>? plots,
    List<HouseholdMemberEntity>? householdMembers,
    String? consentStatus,
    String? consentVersion,
    DateTime? consentDate,
  }) {
    return FarmerEntity(
      id: id ?? this.id,
      uid: uid ?? this.uid,
      fullName: fullName ?? this.fullName,
      dateOfBirth: dateOfBirth ?? this.dateOfBirth,
      sex: sex ?? this.sex,
      contactPhone: contactPhone ?? this.contactPhone,
      nationalIdType: nationalIdType ?? this.nationalIdType,
      nationalIdNumber: nationalIdNumber ?? this.nationalIdNumber,
      status: status ?? this.status,
      adminAreaId: adminAreaId ?? this.adminAreaId,
      plots: plots ?? this.plots,
      householdMembers: householdMembers ?? this.householdMembers,
      consentStatus: consentStatus ?? this.consentStatus,
      consentVersion: consentVersion ?? this.consentVersion,
      consentDate: consentDate ?? this.consentDate,
    );
  }
}