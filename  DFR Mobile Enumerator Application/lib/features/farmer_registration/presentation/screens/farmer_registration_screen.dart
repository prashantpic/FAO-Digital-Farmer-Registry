```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:uuid/uuid.dart';

import '../../../../core/localization/app_localizations.dart';
import '../../../../core/platform_services/gps_service.dart'; // Placeholder
import '../../../../injection_container.dart'; // For GetIt
import '../../domain/entities/farmer_entity.dart';
import '../../domain/entities/plot_entity.dart';
import '../../domain/entities/household_member_entity.dart';
import '../bloc/farmer_registration_bloc/farmer_registration_bloc.dart';
import '../bloc/farmer_registration_bloc/farmer_registration_event.dart';
import '../bloc/farmer_registration_bloc/farmer_registration_state.dart';
import '../widgets/plot_input_widget.dart'; // Placeholder
import '../widgets/household_member_input_widget.dart'; // Placeholder
import '../widgets/custom_text_field.dart'; // Placeholder
import '../widgets/date_picker_field.dart'; // Placeholder
import '../widgets/location_picker_field.dart'; // Placeholder

/// Screen for registering a new farmer or editing an existing one.
///
/// This screen provides a form to capture farmer details, including personal information,
/// plots, and household members. It interacts with [FarmerRegistrationBloc] for state
/// management and data submission.
class FarmerRegistrationScreen extends StatefulWidget {
  /// Optional farmer ID for editing an existing farmer.
  /// If null, the screen is in "new registration" mode.
  final String? farmerId;

  const FarmerRegistrationScreen({super.key, this.farmerId});

  @override
  State<FarmerRegistrationScreen> createState() =>
      _FarmerRegistrationScreenState();
}

class _FarmerRegistrationScreenState extends State<FarmerRegistrationScreen> {
  final _formKey = GlobalKey<FormState>();
  final Uuid _uuid = const Uuid();

  // TextEditingControllers for farmer fields
  late TextEditingController _uidController;
  late TextEditingController _fullNameController;
  late TextEditingController _contactPhoneController;
  late TextEditingController _nationalIdNumberController;

  // Other farmer state variables
  DateTime? _dateOfBirth;
  String? _sex;
  String? _nationalIdType;
  String? _status; // e.g. 'Active', 'Inactive'
  String? _adminAreaId; // Selected admin area
  bool _consentGiven = false;
  String? _consentVersion = "1.0"; // Default or fetched
  DateTime? _consentDate;


  // Lists to manage plots and household members
  List<PlotEntity> _plots = [];
  List<HouseholdMemberEntity> _householdMembers = [];

  bool _isEditMode = false;
  String? _editingFarmerLocalId; // To store local DB ID if editing

  @override
  void initState() {
    super.initState();
    _isEditMode = widget.farmerId != null;

    _uidController = TextEditingController();
    _fullNameController = TextEditingController();
    _contactPhoneController = TextEditingController();
    _nationalIdNumberController = TextEditingController();

    if (_isEditMode) {
      context
          .read<FarmerRegistrationBloc>()
          .add(LoadFarmerForEdit(widget.farmerId!));
    } else {
      // Generate a default UID for new farmer or leave empty for user input
      // _uidController.text = 'FARM-${_uuid.v4().substring(0, 8).toUpperCase()}';
    }
  }

  @override
  void dispose() {
    _uidController.dispose();
    _fullNameController.dispose();
    _contactPhoneController.dispose();
    _nationalIdNumberController.dispose();
    super.dispose();
  }

  void _prefillForm(FarmerEntity farmer) {
    _editingFarmerLocalId = farmer.id; // Store local ID if available (prefixed 'local_') or serverId
    _uidController.text = farmer.uid ?? '';
    _fullNameController.text = farmer.fullName;
    _contactPhoneController.text = farmer.contactPhone;
    _nationalIdNumberController.text = farmer.nationalIdNumber ?? '';
    setState(() {
      _dateOfBirth = farmer.dateOfBirth;
      _sex = farmer.sex;
      _nationalIdType = farmer.nationalIdType;
      _status = farmer.status;
      _adminAreaId = farmer.adminAreaId;
      _plots = List<PlotEntity>.from(farmer.plots);
      _householdMembers = List<HouseholdMemberEntity>.from(farmer.householdMembers);
      _consentGiven = farmer.consentStatus == 'Given'; // Example
      _consentVersion = farmer.consentVersion;
      _consentDate = farmer.consentDate;
    });
  }

  void _onSubmit() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();

      final farmerEntity = FarmerEntity(
        id: _isEditMode ? _editingFarmerLocalId : null, // Pass ID for updates
        uid: _uidController.text,
        fullName: _fullNameController.text,
        dateOfBirth: _dateOfBirth,
        sex: _sex,
        contactPhone: _contactPhoneController.text,
        nationalIdType: _nationalIdType,
        nationalIdNumber: _nationalIdNumberController.text,
        status: _status ?? 'Active', // Default status
        adminAreaId: _adminAreaId,
        plots: _plots,
        householdMembers: _householdMembers,
        consentStatus: _consentGiven ? 'Given' : 'NotGiven',
        consentVersion: _consentVersion,
        consentDate: _consentGiven ? (_consentDate ?? DateTime.now()) : null,
      );

      context
          .read<FarmerRegistrationBloc>()
          .add(SubmitFarmerRegistration(farmerEntity));
    }
  }

  void _addPlot() {
    // Show a dialog or navigate to a new screen to add plot details
    // For simplicity, adding a placeholder plot here
    // In a real app, this would involve capturing GPS, size, etc.
    showDialog(
        context: context,
        builder: (_) => PlotInputWidget(
              plot: null, // New plot
              onSave: (plot) {
                 setState(() {
                  _plots.add(plot.copyWith(id: 'local_plot_${_uuid.v4()}')); // Assign local temporary ID
                });
                Navigator.of(context).pop();
              },
            ));
  }

  void _editPlot(int index) {
    showDialog(
      context: context,
      builder: (_) => PlotInputWidget(
        plot: _plots[index],
        onSave: (updatedPlot) {
          setState(() {
            _plots[index] = updatedPlot;
          });
          Navigator.of(context).pop();
        },
      ),
    );
  }

  void _removePlot(int index) {
    setState(() {
      _plots.removeAt(index);
    });
  }


  void _addHouseholdMember() {
    showDialog(
      context: context,
      builder: (_) => HouseholdMemberInputWidget(
        member: null, // New member
        onSave: (member) {
          setState(() {
            _householdMembers.add(member.copyWith(id: 'local_member_${_uuid.v4()}')); // Assign local temporary ID
          });
           Navigator.of(context).pop();
        },
      ),
    );
  }

   void _editHouseholdMember(int index) {
    showDialog(
      context: context,
      builder: (_) => HouseholdMemberInputWidget(
        member: _householdMembers[index],
        onSave: (updatedMember) {
          setState(() {
            _householdMembers[index] = updatedMember;
          });
          Navigator.of(context).pop();
        },
      ),
    );
  }

  void _removeHouseholdMember(int index) {
    setState(() {
      _householdMembers.removeAt(index);
    });
  }


  @override
  Widget build(BuildContext context) {
    final localization = AppLocalizations.of(context)!;
    return Scaffold(
      appBar: AppBar(
        title: Text(_isEditMode
            ? localization.translate('editFarmer')
            : localization.translate('registerFarmer')),
      ),
      body: BlocConsumer<FarmerRegistrationBloc, FarmerRegistrationState>(
        listener: (context, state) {
          if (state is FarmerRegistrationSuccess) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(localization.translate(state.messageKey) ?? state.messageKey)),
            );
            Navigator.of(context).pop(true); // Pop with a success flag
          } else if (state is FarmerRegistrationFailure) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(localization.translate(state.errorKey) ?? state.errorKey)),
            );
          } else if (state is FarmerLoadedForEdit) {
            _prefillForm(state.farmer);
          }
        },
        builder: (context, state) {
          if (state is FarmerRegistrationLoading) {
            return const Center(child: CircularProgressIndicator());
          }
          return SingleChildScrollView(
            padding: const EdgeInsets.all(16.0),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  // Farmer UID (Can be auto-generated or manual)
                  CustomTextField(
                    controller: _uidController,
                    labelText: localization.translate('farmerUid'),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return localization.translate('validationRequiredField');
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),

                  // Full Name
                  CustomTextField(
                    controller: _fullNameController,
                    labelText: localization.translate('fullName'),
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return localization.translate('validationRequiredField');
                      }
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),

                  // Date of Birth
                  DatePickerField(
                    labelText: localization.translate('dateOfBirth'),
                    initialDate: _dateOfBirth,
                    onDateSelected: (date) {
                      setState(() {
                        _dateOfBirth = date;
                      });
                    },
                  ),
                  const SizedBox(height: 16),

                  // Sex
                  DropdownButtonFormField<String>(
                    value: _sex,
                    decoration: InputDecoration(
                      labelText: localization.translate('sex'),
                      border: const OutlineInputBorder(),
                    ),
                    items: ['Male', 'Female', 'Other'] // Example values, should be configurable/localized
                        .map((label) => DropdownMenuItem(
                              value: label,
                              child: Text(localization.translate(label.toLowerCase()) ?? label),
                            ))
                        .toList(),
                    onChanged: (value) {
                      setState(() {
                        _sex = value;
                      });
                    },
                  ),
                  const SizedBox(height: 16),
                  
                  // Contact Phone
                  CustomTextField(
                    controller: _contactPhoneController,
                    labelText: localization.translate('contactPhone'),
                    keyboardType: TextInputType.phone,
                    validator: (value) {
                      if (value == null || value.isEmpty) {
                        return localization.translate('validationRequiredField');
                      }
                      // Add more specific phone validation if needed
                      return null;
                    },
                  ),
                  const SizedBox(height: 16),

                  // National ID Type
                  // This could be a dropdown fetched from config/server
                  DropdownButtonFormField<String>(
                    value: _nationalIdType,
                    decoration: InputDecoration(
                      labelText: localization.translate('nationalIdType'),
                      border: const OutlineInputBorder(),
                    ),
                    items: ['Passport', 'NationalIDCard', 'DrivingLicense'] // Example
                        .map((label) => DropdownMenuItem(
                              value: label,
                              child: Text(localization.translate(label.toLowerCase()) ?? label),
                            ))
                        .toList(),
                    onChanged: (value) {
                      setState(() {
                        _nationalIdType = value;
                      });
                    },
                  ),
                  const SizedBox(height: 16),

                  // National ID Number
                  CustomTextField(
                    controller: _nationalIdNumberController,
                    labelText: localization.translate('nationalIdNumber'),
                  ),
                  const SizedBox(height: 16),

                  // Administrative Area (Dropdown, potentially complex picker)
                  // For simplicity, a text field or basic dropdown.
                  // In a real app, this might involve fetching areas.
                   DropdownButtonFormField<String>(
                    value: _adminAreaId,
                    decoration: InputDecoration(
                      labelText: localization.translate('administrativeArea'),
                      border: const OutlineInputBorder(),
                    ),
                    // items: fetchedAdminAreas.map(...).toList(),
                    items: [ // Placeholder
                        DropdownMenuItem(value: 'area1', child: Text(localization.translate('area1Name') ?? 'Area 1')),
                        DropdownMenuItem(value: 'area2', child: Text(localization.translate('area2Name') ?? 'Area 2')),
                    ],
                    onChanged: (value) {
                      setState(() {
                        _adminAreaId = value;
                      });
                    },
                  ),
                  const SizedBox(height: 16),

                  // Consent
                  SwitchListTile(
                    title: Text(localization.translate('consentGiven')),
                    value: _consentGiven,
                    onChanged: (bool value) {
                      setState(() {
                        _consentGiven = value;
                        if(value) {
                          _consentDate = DateTime.now();
                        } else {
                          _consentDate = null;
                        }
                      });
                    },
                  ),
                  if (_consentGiven) ...[
                    Text('${localization.translate('consentVersion')}: $_consentVersion'),
                    Text('${localization.translate('consentDate')}: ${_consentDate != null ? MaterialLocalizations.of(context).formatMediumDate(_consentDate!) : localization.translate('notSet')}'),
                  ],
                  const SizedBox(height: 24),


                  // Plots Section
                  _buildSectionHeader(localization.translate('plots'), _addPlot),
                  ..._plots.asMap().entries.map((entry) {
                    int idx = entry.key;
                    PlotEntity plot = entry.value;
                    return Card(
                      margin: const EdgeInsets.symmetric(vertical: 8),
                      child: ListTile(
                        title: Text(localization.translate('plot') + ' ${idx + 1}'), // E.g., Plot at Lat: ${plot.latitude}, Lng: ${plot.longitude}
                        subtitle: Text('${localization.translate('area')}: ${plot.size} ${plot.sizeUnit}, ${localization.translate('gps')}: ${plot.latitude?.toStringAsFixed(4)}, ${plot.longitude?.toStringAsFixed(4)}'),
                        trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            IconButton(icon: const Icon(Icons.edit), onPressed: () => _editPlot(idx)),
                            IconButton(icon: const Icon(Icons.delete), onPressed: () => _removePlot(idx)),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                  const SizedBox(height: 24),

                  // Household Members Section
                  _buildSectionHeader(localization.translate('householdMembers'), _addHouseholdMember),
                   ..._householdMembers.asMap().entries.map((entry) {
                    int idx = entry.key;
                    HouseholdMemberEntity member = entry.value;
                    return Card(
                      margin: const EdgeInsets.symmetric(vertical: 8),
                      child: ListTile(
                        title: Text(member.fullName ?? localization.translate('member') + ' ${idx + 1}'),
                        subtitle: Text('${localization.translate('relationshipToHead')}: ${member.relationshipToHead}'),
                         trailing: Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            IconButton(icon: const Icon(Icons.edit), onPressed: () => _editHouseholdMember(idx)),
                            IconButton(icon: const Icon(Icons.delete), onPressed: () => _removeHouseholdMember(idx)),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                  const SizedBox(height: 32),

                  ElevatedButton(
                    onPressed: _onSubmit,
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size(double.infinity, 50), // Full width
                    ),
                    child: Text(
                      _isEditMode
                          ? localization.translate('updateFarmerButton')
                          : localization.translate('registerFarmerButton'),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget _buildSectionHeader(String title, VoidCallback onAdd) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(title, style: Theme.of(context).textTheme.titleLarge),
        IconButton(
          icon: const Icon(Icons.add_circle, color: Colors.green),
          onPressed: onAdd,
        ),
      ],
    );
  }
}
```