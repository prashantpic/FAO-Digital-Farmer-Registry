odoo.define('dfr_farmer_portal.portal_dynamic_form', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.DFRDynamicForm = publicWidget.Widget.extend({
    selector: '.dfr-dynamic-form', // Selector for the dynamic form container
    events: {
        'submit form': '_onSubmit',
        'change .dfr-dynamic-field': '_onFieldChange', // For conditional logic
        'input .dfr-dynamic-field': '_onInputValidate', // Real-time validation
        'focusout .dfr-dynamic-field': '_onFocusOutValidate', // Validate on blur
    },

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this.form = this.el.querySelector('form');
        if (!this.form) return;

        this.submitButton = this.form.querySelector('button[type="submit"]');
        const formDefinitionData = this.el.dataset.formDefinition;
        
        try {
            this.formDefinition = formDefinitionData ? JSON.parse(formDefinitionData) : null;
        } catch (e) {
            console.error("Failed to parse form definition JSON:", e);
            this.formDefinition = null;
            // Display an error to the user or prevent form interaction
            this._displayGlobalFormError("Error: Form configuration is invalid. Please contact support.");
            if(this.submitButton) this.submitButton.disabled = true;
            return;
        }
        
        if (this.formDefinition) {
            this._initDynamicFormInteractions();
            this._applyInitialConditionalLogic();
        } else {
            console.warn("DFR Dynamic Form: No form definition found or it's invalid.");
            this._displayGlobalFormError("Warning: Form is not configured correctly.");
            if(this.submitButton) this.submitButton.disabled = true;
        }
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------
    _displayGlobalFormError(message) {
        let errorContainer = this.form.querySelector('.dynamic-form-global-error');
        if (!errorContainer) {
            errorContainer = document.createElement('div');
            errorContainer.className = 'alert alert-danger dynamic-form-global-error';
            errorContainer.setAttribute('role', 'alert');
            this.form.prepend(errorContainer);
        }
        errorContainer.textContent = message;
    },

    _initDynamicFormInteractions: function () {
        // Iterate through fields to apply initial settings or attach specific listeners if needed beyond general ones
        // This is also where you would parse and prepare conditional logic rules.
        if (this.formDefinition && this.formDefinition.fields) {
            this.formDefinition.fields.forEach(fieldInfo => {
                // Example: If a field type needs special JS initialization (e.g., a date picker)
                // const fieldElement = this.form.querySelector(`[name="${fieldInfo.name}"]`);
                // if (fieldElement && fieldInfo.type === 'date_custom_widget') {
                //     new MyCustomDateWidget(fieldElement, fieldInfo.options);
                // }
            });
        }
    },
    
    _applyInitialConditionalLogic: function() {
        if (!this.formDefinition || !this.formDefinition.fields) return;

        this.formDefinition.fields.forEach(fieldInfo => {
            if (fieldInfo.conditional_logic && fieldInfo.conditional_logic.rules) {
                this._evaluateConditionalLogic(fieldInfo.name);
            }
        });
    },

    _evaluateConditionalLogic: function(fieldName) {
        const fieldInfo = this.formDefinition.fields.find(f => f.name === fieldName);
        if (!fieldInfo || !fieldInfo.conditional_logic || !fieldInfo.conditional_logic.rules) {
            return;
        }

        const targetFieldElement = this.form.querySelector(`[name="${fieldName}"]`);
        const targetFieldGroup = targetFieldElement ? targetFieldElement.closest('.form-group, .mb-3') : null; // Common Bootstrap group
        
        if (!targetFieldGroup) {
            console.warn(`Conditional logic: Target field group for ${fieldName} not found.`);
            return;
        }

        let isVisible = fieldInfo.conditional_logic.action === 'hide'; // Default to opposite of action for easier logic

        for (const rule of fieldInfo.conditional_logic.rules) {
            const sourceFieldElement = this.form.querySelector(`[name="${rule.source_field}"]`);
            if (!sourceFieldElement) {
                console.warn(`Conditional logic: Source field ${rule.source_field} not found for ${fieldName}.`);
                continue; // Or handle as false
            }
            
            const sourceValue = sourceFieldElement.type === 'checkbox' ? sourceFieldElement.checked : sourceFieldElement.value;
            let ruleMet = false;

            switch (rule.operator) {
                case 'is':
                    ruleMet = String(sourceValue) === String(rule.value);
                    break;
                case 'is_not':
                    ruleMet = String(sourceValue) !== String(rule.value);
                    break;
                case 'contains':
                    ruleMet = String(sourceValue).includes(String(rule.value));
                    break;
                // Add more operators as needed: 'greater_than', 'less_than', 'is_empty', 'is_not_empty'
            }

            if (fieldInfo.conditional_logic.relation === 'AND') {
                if (!ruleMet) {
                    isVisible = fieldInfo.conditional_logic.action === 'hide'; // If AND and one fails, visibility is set
                    break; 
                }
                isVisible = fieldInfo.conditional_logic.action === 'show'; // If AND and all pass
            } else { // OR
                if (ruleMet) {
                    isVisible = fieldInfo.conditional_logic.action === 'show'; // If OR and one passes, visibility is set
                    break;
                }
                // if OR and rule not met, visibility remains default (hide if action is show, show if action is hide)
            }
        }
        
        if (isVisible) {
            targetFieldGroup.style.display = '';
            targetFieldGroup.setAttribute('aria-hidden', 'false');
            // If field becomes visible, it might become required
            // This needs to be carefully managed with server-side logic too
        } else {
            targetFieldGroup.style.display = 'none';
            targetFieldGroup.setAttribute('aria-hidden', 'true');
            // If field becomes hidden, it might no longer be required / its value might be cleared
            // if (targetFieldElement) targetFieldElement.value = ''; // Optional: clear value when hidden
        }
    },

    _onFieldChange: function (ev) {
        // Triggered by fields that might affect other fields' visibility
        if (!this.formDefinition || !this.formDefinition.fields) return;
        
        const changedFieldName = ev.currentTarget.name;

        this.formDefinition.fields.forEach(fieldInfo => {
            if (fieldInfo.conditional_logic && fieldInfo.conditional_logic.rules) {
                const dependsOnChangedField = fieldInfo.conditional_logic.rules.some(rule => rule.source_field === changedFieldName);
                if (dependsOnChangedField) {
                    this._evaluateConditionalLogic(fieldInfo.name);
                }
            }
        });
        // Also validate the changed field itself
        this._validateField(ev.currentTarget, true);
    },
    
    _onInputValidate: function(ev) {
        this._validateField(ev.currentTarget);
    },

    _onFocusOutValidate: function(ev) {
        this._validateField(ev.currentTarget, true); // Force validation feedback on blur
    },

    _validateField: function (field, forceFeedback = false) {
        if (!this.formDefinition) return true;

        const fieldName = field.name;
        const fieldInfo = this.formDefinition.fields.find(f => f.name === fieldName);
        if (!fieldInfo) return true; // No definition, can't validate client-side

        const value = field.type === 'checkbox' ? field.checked : (field.type === 'file' ? field.files[0] : field.value.trim());
        let isValid = true;
        let errorMessage = '';

        // Check visibility first - don't validate hidden fields usually
        const fieldGroup = field.closest('.form-group, .mb-3');
        if (fieldGroup && fieldGroup.style.display === 'none' && !fieldInfo.validate_when_hidden) {
            // Clear any previous errors for hidden fields
            field.setAttribute('aria-invalid', 'false');
            const errorDiv = this.form.querySelector(`#${field.id}_error`);
            if (errorDiv) {
                errorDiv.textContent = '';
                errorDiv.style.display = 'none';
            }
            return true;
        }


        if (fieldInfo.is_required && (value === '' || value === false || (field.type === 'file' && !value))) {
            isValid = false;
            errorMessage = fieldInfo.label + ' is required.';
        }

        if (isValid && value && fieldInfo.validation_rules) {
            if (fieldInfo.validation_rules.regex && !new RegExp(fieldInfo.validation_rules.regex).test(value)) {
                isValid = false;
                errorMessage = fieldInfo.validation_rules.regex_error_message || 'Invalid format for ' + fieldInfo.label + '.';
            }
            if (isValid && fieldInfo.validation_rules.min_length && value.length < fieldInfo.validation_rules.min_length) {
                isValid = false;
                errorMessage = `${fieldInfo.label} must be at least ${fieldInfo.validation_rules.min_length} characters.`;
            }
            if (isValid && fieldInfo.validation_rules.max_length && value.length > fieldInfo.validation_rules.max_length) {
                isValid = false;
                errorMessage = `${fieldInfo.label} must be at most ${fieldInfo.validation_rules.max_length} characters.`;
            }
             if (isValid && field.type === 'number') {
                const numValue = parseFloat(value);
                if (fieldInfo.validation_rules.min_value !== undefined && numValue < fieldInfo.validation_rules.min_value) {
                    isValid = false;
                    errorMessage = `${fieldInfo.label} must be at least ${fieldInfo.validation_rules.min_value}.`;
                }
                if (isValid && fieldInfo.validation_rules.max_value !== undefined && numValue > fieldInfo.validation_rules.max_value) {
                    isValid = false;
                    errorMessage = `${fieldInfo.label} must be at most ${fieldInfo.validation_rules.max_value}.`;
                }
            }
            // Add more specific validation types (email, url, etc.)
        }
        
        const errorDivId = field.id + '_error';
        const errorDiv = this.form.querySelector('#' + errorDivId);
        const describedBy = field.getAttribute('aria-describedby') || '';
        let newDescribedBy = describedBy.split(' ').filter(id => id !== errorDivId).join(' ');

        if (!isValid && (value || forceFeedback || field.type === 'checkbox')) {
            field.setAttribute('aria-invalid', 'true');
            if (errorDiv) {
                errorDiv.textContent = errorMessage;
                errorDiv.style.display = 'block';
                if (!newDescribedBy.includes(errorDivId)) {
                    newDescribedBy = (newDescribedBy + ' ' + errorDivId).trim();
                }
            }
        } else {
            field.setAttribute('aria-invalid', 'false');
            if (errorDiv) {
                errorDiv.textContent = '';
                errorDiv.style.display = 'none';
            }
        }
        field.setAttribute('aria-describedby', newDescribedBy);
        return isValid;
    },

    _validateForm: function () {
        if (!this.formDefinition) return true; // If no definition, cannot validate client-side

        let isFormValid = true;
        this.formDefinition.fields.forEach(fieldInfo => {
            const fieldElement = this.form.querySelector(`[name="${fieldInfo.name}"]`);
            if (fieldElement) {
                // Only validate if the field is visible (or explicitly set to validate when hidden)
                const fieldGroup = fieldElement.closest('.form-group, .mb-3');
                if ((fieldGroup && fieldGroup.style.display !== 'none') || fieldInfo.validate_when_hidden) {
                    if (!this._validateField(fieldElement, true)) { // force feedback
                        isFormValid = false;
                    }
                }
            }
        });
        return isFormValid;
    },

    _onSubmit: function (ev) {
        if (!this._validateForm()) {
            ev.preventDefault();
            const firstInvalidField = this.form.querySelector('[aria-invalid="true"]');
            if (firstInvalidField) {
                firstInvalidField.focus();
            }
            // Announce validation errors
            const liveRegion = document.getElementById('aria-live-dynamic-form-status');
            if (liveRegion) {
                liveRegion.textContent = 'Please correct the errors in the form.';
            }
        } else {
            if (this.submitButton) {
                this.submitButton.setAttribute('disabled', 'disabled');
                const spinner = document.createElement('span');
                spinner.className = 'spinner-border spinner-border-sm';
                spinner.setAttribute('role', 'status');
                spinner.setAttribute('aria-hidden', 'true');
                this.submitButton.prepend(spinner, ' ');
            }
             // Announce submission attempt
            const liveRegion = document.getElementById('aria-live-dynamic-form-status');
            if (liveRegion) {
                liveRegion.textContent = 'Submitting form...';
            }
        }
    },
});

return {
    DFRDynamicForm: publicWidget.registry.DFRDynamicForm,
};
});