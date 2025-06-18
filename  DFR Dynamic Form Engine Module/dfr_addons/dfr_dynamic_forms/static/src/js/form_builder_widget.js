odoo.define('dfr_dynamic_forms.FormBuilderWidget', function (require) {
    "use strict";

    const { Component, useState, onWillStart, onWillUpdateProps, onMounted, useRef } = owl;
    const { registry } = require("@web/core/registry");
    const { standardFieldProps } = require("@web/views/fields/standard_field_props");
    const { _t } = require("@web/core/l10n/translation");
    const { useService } = require("@web/core/utils/hooks");
    const { Dialog } = require("@web/core/dialog/dialog_service");

    class FieldPropertiesModal extends Component {
        static template = "dfr_dynamic_forms.FieldPropertiesModal";
        static props = {
            close: Function,
            title: String,
            fieldData: Object,
            formVersionId: Number,
            isEditable: Boolean,
            onSave: Function,
            formFieldsForCondition: Array, // list of {name, label} of other fields in the form version
        };

        setup() {
            this.state = useState({
                field: JSON.parse(JSON.stringify(this.props.fieldData)), // Deep copy
                activeTab: 'general',
                newCondition: { field_name: "", operator: "=", value: "", value_type: "text" },
                conditionalLogicError: null,
            });

            this.fieldTypes = [
                { id: 'text', label: _t('Text') },
                { id: 'number', label: _t('Number') },
                { id: 'date', label: _t('Date') },
                { id: 'datetime', label: _t('Datetime') },
                { id: 'selection', label: _t('Selection (Dropdown)') },
                { id: 'multi_selection', label: _t('Multi-Selection (Tags)') },
                { id: 'boolean', label: _t('Boolean (Checkbox)') },
                { id: 'gps_point', label: _t('GPS Point') },
                { id: 'image', label: _t('Image/File Attachment') },
                { id: 'computed_text', label: _t('Computed Text (Read-only)') },
            ];
            
            this.conditionalOperators = [
                { id: '=', label: _t('= (Equals)') },
                { id: '!=', label: _t('!= (Not Equals)') },
                { id: '>', label: _t('> (Greater Than)') },
                { id: '<', label: _t('< (Less Than)') },
                { id: '>=', label: _t('>= (Greater Than or Equals)') },
                { id: '<=', label: _t('<= (Less Than or Equals)') },
                // { id: 'contains', label: _t('Contains') },
                // { id: 'not_contains', label: _t('Does Not Contain') },
            ];
            this.conditionalValueTypes = [
                { id: 'text', label: _t('Text') },
                { id: 'number', label: _t('Number') },
                { id: 'boolean', label: _t('Boolean (true/false)') },
            ];


            this._parseConditionalLogic();
        }

        _parseConditionalLogic() {
            try {
                this.state.field.parsedConditionalLogic = this.state.field.conditional_logic_json ?
                    JSON.parse(this.state.field.conditional_logic_json) : [];
                if (!Array.isArray(this.state.field.parsedConditionalLogic)) {
                    this.state.field.parsedConditionalLogic = [];
                    this.state.conditionalLogicError = _t("Invalid conditional logic JSON structure: not an array.");
                } else {
                     this.state.conditionalLogicError = null;
                }
            } catch (e) {
                this.state.field.parsedConditionalLogic = [];
                this.state.conditionalLogicError = _t("Error parsing conditional logic JSON: ") + e.message;
            }
        }

        get isFieldTypeWithSelectionOptions() {
            return ['selection', 'multi_selection'].includes(this.state.field.field_type);
        }

        get isFieldTypeNumeric() {
            return ['number'].includes(this.state.field.field_type);
        }

        get isFieldTypeText() {
            return ['text'].includes(this.state.field.field_type);
        }

        _onSave() {
            try {
                this.state.field.conditional_logic_json = this.state.field.parsedConditionalLogic.length > 0 ?
                    JSON.stringify(this.state.field.parsedConditionalLogic) : "";
                if (this.state.field.conditional_logic_json) { // Validate it's parseable
                    JSON.parse(this.state.field.conditional_logic_json);
                }
                this.state.conditionalLogicError = null;
            } catch (e) {
                this.state.conditionalLogicError = _t("Invalid conditional logic JSON: ") + e.message;
                return; 
            }

            this.props.onSave(this.state.field);
            this.props.close();
        }

        _onCancel() {
            this.props.close();
        }

        _addCondition() {
            if (!this.state.newCondition.field_name || !this.state.newCondition.operator) {
                this.state.conditionalLogicError = _t("Trigger field name and operator are required for a condition.");
                return;
            }
            // Ensure parsedConditionalLogic is an array
            if (!Array.isArray(this.state.field.parsedConditionalLogic)) {
                this.state.field.parsedConditionalLogic = [];
            }
            this.state.field.parsedConditionalLogic.push({ ...this.state.newCondition });
            this.state.newCondition = { field_name: "", operator: "=", value: "", value_type: "text" };
            this.state.conditionalLogicError = null;
        }

        _removeCondition(index) {
             if (Array.isArray(this.state.field.parsedConditionalLogic)) {
                this.state.field.parsedConditionalLogic.splice(index, 1);
            }
        }
         _updateRawJson(ev) {
            try {
                const newParsedLogic = JSON.parse(ev.target.value || '[]');
                if (Array.isArray(newParsedLogic)) {
                    this.state.field.parsedConditionalLogic = newParsedLogic;
                    this.state.conditionalLogicError = null;
                } else {
                     this.state.conditionalLogicError = _t("Invalid JSON structure: must be an array.");
                }
            } catch (e) {
                this.state.conditionalLogicError = _t("Invalid JSON: ") + e.message;
            }
        }
    }

    class FormBuilderWidget extends Component {
        static template = "dfr_dynamic_forms.FormBuilderWidget";
        static props = {
            ...standardFieldProps,
        };
        static components = { FieldPropertiesModal };

        setup() {
            this.state = useState({
                fields: [],
                isEditable: true,
                formVersionId: null,
            });
            this.orm = useService("orm");
            this.notification = useService("notification");
            this.dialogService = useService("dialog");
            this.draggedItem = null;
            this.fieldContainerRef = useRef("fieldContainer");


            onWillStart(async () => {
                this.state.formVersionId = this.props.record.data.id;
                await this._loadFields();
                this.state.isEditable = this.props.record.data.is_editable;
            });

            onWillUpdateProps(async (nextProps) => {
                const newFormVersionId = nextProps.record.data.id;
                let needsReload = false;
                if (newFormVersionId !== this.state.formVersionId) {
                    this.state.formVersionId = newFormVersionId;
                    needsReload = true;
                }
                // A simple way to detect if field_ids themselves changed (e.g. by server action)
                // This is a rough check, a more robust one would compare actual data if complex.
                if (nextProps.record.data.field_ids.currentIds.length !== this.state.fields.length ||
                    !nextProps.record.data.field_ids.currentIds.every(id => this.state.fields.find(f => f.id === id))) {
                    needsReload = true;
                }

                if (needsReload) {
                    await this._loadFields();
                }
                this.state.isEditable = nextProps.record.data.is_editable;
            });
        }

        async _loadFields() {
            if (!this.state.formVersionId) {
                this.state.fields = [];
                return;
            }
            const fieldDetails = await this.orm.searchRead(
                'dfr.form.field',
                [['form_version_id', '=', this.state.formVersionId]],
                [
                    'name', 'label', 'field_type', 'sequence', 'is_required', 'help_text',
                    'selection_options', 'validation_rule_required', 'validation_rule_min_length',
                    'validation_rule_max_length', 'validation_rule_min_value', 'validation_rule_max_value',
                    'validation_rule_regex', 'validation_error_message', 'conditional_logic_json',
                    'placeholder', 'default_value_text', 'default_value_number', 'default_value_boolean',
                    'form_version_id'
                ],
                { order: 'sequence' }
            );
            this.state.fields = fieldDetails.map(f => ({ ...f, key: f.id, display_name: f.label })); // key for OWL
        }

        async _updateRecordAndResequence(notifyMsg = null) {
            // This tells Odoo that the underlying x2m field has changed.
            // It needs a list of commands. For reordering, we update sequences.
            // For add/delete, the ORM calls handle it, then we call this to refresh.
            const commands = [];
            this.state.fields.forEach((field, index) => {
                commands.push(this.orm.commands.update(field.id, { sequence: (index + 1) * 10 }));
            });
            
            // This is how to update an x2m field value.
            // The `update` method comes from the `useRecord` hook that manages the record.
            await this.props.record.update({ [this.props.name]: commands });
            // After updating the record, Odoo might reload parts of it or the whole view.
            // If the list doesn't auto-refresh with correct sequences, explicitly call _loadFields.
            await this._loadFields();

            if (notifyMsg) {
                 this.notification.add(notifyMsg, { type: 'success' });
            }
        }

        async _onAddField(ev) {
            if (!this.state.isEditable) return;

            const highestSequence = this.state.fields.reduce((max, f) => Math.max(max, f.sequence || 0), 0);
            const newFieldData = {
                form_version_id: this.state.formVersionId,
                name: `new_field_${new Date().getTime().toString().slice(-6)}`,
                label: _t("New Field"),
                field_type: 'text',
                sequence: highestSequence + 10,
            };

            try {
                const newFieldId = await this.orm.create('dfr.form.field', [newFieldData]);
                await this._loadFields(); // Reload fields to include the new one
                this._openFieldPropertiesModal(newFieldId); // Open modal for the new field
                this.notification.add(_t("Field added. Configure its properties."), { type: 'success' });
            } catch (error) {
                console.error("Error adding field:", error);
                this.notification.add(error.data?.message || _t("Error adding field."), { type: 'danger' });
            }
        }

        _onEditField(fieldId) {
            this._openFieldPropertiesModal(fieldId);
        }

        _openFieldPropertiesModal(fieldId) {
            const field = this.state.fields.find(f => f.id === fieldId);
            if (!field) return;

            const otherFieldsForCondition = this.state.fields
                .filter(f => f.id !== fieldId) // Exclude current field
                .map(f => ({ name: f.name, label: f.label}));


            this.dialogService.add(FieldPropertiesModal, {
                title: field.id ? _t("Edit Field Properties: ") + field.label : _t("Add New Field"),
                fieldData: field,
                formVersionId: this.state.formVersionId,
                isEditable: this.state.isEditable,
                formFieldsForCondition: otherFieldsForCondition,
                onSave: async (updatedFieldData) => {
                    await this._saveField(updatedFieldData);
                },
            });
        }

        async _saveField(fieldData) {
            if (!this.state.isEditable) return;
            try {
                const { id, ...dataToWrite } = fieldData; // Separate ID from data
                // Remove 'key' and other client-side properties if any
                delete dataToWrite.key;
                delete dataToWrite.display_name;
                delete dataToWrite.parsedConditionalLogic;

                await this.orm.write('dfr.form.field', [id], dataToWrite);
                await this._loadFields();
                this.notification.add(_t("Field properties saved."), { type: 'success' });
            } catch (error) {
                console.error("Error saving field:", error);
                this.notification.add(error.data?.message || _t("Error saving field."), { type: 'danger' });
            }
        }

        async _onDeleteField(fieldId) {
            if (!this.state.isEditable) return;

            this.dialogService.add(Dialog, {
                title: _t("Confirm Deletion"),
                body: _t("Are you sure you want to delete this field?"),
                confirmLabel: _t("Delete"),
                confirm: async () => {
                    try {
                        await this.orm.unlink('dfr.form.field', [fieldId]);
                        await this._loadFields();
                        this.notification.add(_t("Field deleted."), { type: 'success' });
                    } catch (error) {
                        console.error("Error deleting field:", error);
                        this.notification.add(error.data?.message || _t("Error deleting field."), { type: 'danger' });
                    }
                },
                cancelLabel: _t("Cancel"),
                cancel: () => {},
            });
        }

        _onDragStart(ev, field) {
            if (!this.state.isEditable) return;
            this.draggedItem = field;
            ev.dataTransfer.effectAllowed = 'move';
            ev.dataTransfer.setData('text/plain', field.id.toString());
            ev.currentTarget.classList.add('dragging');
        }

        _onDragOver(ev) {
            if (!this.state.isEditable || !this.draggedItem) return;
            ev.preventDefault();
            const targetElement = ev.currentTarget;
            // Basic visual cue by adding class to potential drop target
            targetElement.classList.add('drag-over');
        }

        _onDragLeave(ev) {
             if (!this.state.isEditable) return;
            ev.currentTarget.classList.remove('drag-over');
        }

        async _onDrop(ev, targetField) {
            if (!this.state.isEditable || !this.draggedItem) return;
            ev.preventDefault();
            ev.currentTarget.classList.remove('drag-over');

            if (this.draggedItem.id === targetField.id) {
                this.draggedItem = null;
                document.querySelectorAll('.form-field-item.dragging').forEach(el => el.classList.remove('dragging'));
                return;
            }

            const fieldsCopy = [...this.state.fields];
            const draggedIndex = fieldsCopy.findIndex(f => f.id === this.draggedItem.id);
            let targetIndex = fieldsCopy.findIndex(f => f.id === targetField.id);

            const [draggedElement] = fieldsCopy.splice(draggedIndex, 1);
            // If dragging downwards and target is after original position of dragged item
            if (draggedIndex < targetIndex) {
                 fieldsCopy.splice(targetIndex, 0, draggedElement);
            } else {
                 fieldsCopy.splice(targetIndex, 0, draggedElement);
            }


            this.state.fields = fieldsCopy; // Optimistic update for UI responsiveness

            const sequenceUpdates = this.state.fields.map((f, index) => {
                return this.orm.write('dfr.form.field', [f.id], { sequence: (index + 1) * 10 });
            });

            try {
                await Promise.all(sequenceUpdates);
                await this._loadFields(); // Re-fetch to confirm order and sequences from server
                this.notification.add(_t("Field order updated."), { type: 'success' });
            } catch (error) {
                console.error("Error reordering fields:", error);
                await this._loadFields(); // Revert to server state on error
                this.notification.add(error.data?.message || _t("Error reordering fields."), { type: 'danger' });
            }
            this.draggedItem = null;
            document.querySelectorAll('.form-field-item.dragging').forEach(el => el.classList.remove('dragging'));
        }

        _onDragEnd(ev) {
            if (!this.state.isEditable) return;
            if(ev.currentTarget.classList) ev.currentTarget.classList.remove('dragging');
            document.querySelectorAll('.form-field-item.drag-over').forEach(el => el.classList.remove('drag-over'));
            this.draggedItem = null;
        }
    }

    registry.category("fields").add("form_builder", FormBuilderWidget);

    return {
        FormBuilderWidget,
        FieldPropertiesModal,
    };
});