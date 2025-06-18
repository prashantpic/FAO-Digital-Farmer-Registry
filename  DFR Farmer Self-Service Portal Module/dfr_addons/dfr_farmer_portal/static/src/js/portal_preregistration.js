odoo.define('dfr_farmer_portal.portal_preregistration', function (require) {
'use strict';

var publicWidget = require('web.public.widget');

publicWidget.registry.DFRPreRegistrationForm = publicWidget.Widget.extend({
    selector: '#dfr_preregistration_form', // Selector for the pre-registration form
    events: {
        'submit': '_onSubmit',
        'change #national_id_type': '_onNationalIdTypeChange',
        'input .form-control': '_onInputValidate', // Real-time validation on input
        'focusout .form-control': '_onFocusOutValidate', // Validate on blur
    },

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this.form = this.el;
        this.submitButton = this.$('button[type="submit"]');
        this._initPreRegistrationFormValidation();
        this._handleNationalIdVisibility(); // Initial check on page load
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    _initPreRegistrationFormValidation: function () {
        // This function sets up initial state, specific complex listeners, or overall form logic.
        // Individual field validation logic is primarily in _validateField.
        // For example, you might want to disable submit button initially if fields are empty
    },

    _onInputValidate: function(ev) {
        const field = ev.currentTarget;
        this._validateField(field);
    },

    _onFocusOutValidate: function(ev) {
        const field = ev.currentTarget;
        this._validateField(field, true); // Force validation feedback on blur
    },


    _validateField: function (field, forceFeedback = false) {
        const fieldId = field.id;
        const value = field.value.trim();
        let isValid = true;
        let errorMessage = '';

        // Generic required check (can be enhanced by specific field rules)
        if (field.hasAttribute('required') && !value) {
            isValid = false;
            errorMessage = 'This field is required.';
        }

        switch (fieldId) {
            case 'full_name':
                // Add specific validation for full_name if any, e.g. length
                break;
            case 'village':
                // Add specific validation for village if any
                break;
            case 'primary_crop_type':
                // Add specific validation
                break;
            case 'contact_number':
                if (value && !/^\+?[0-9\s\-()]{7,20}$/.test(value)) { // Basic phone number regex
                    isValid = false;
                    errorMessage = 'Please enter a valid contact number.';
                }
                break;
            case 'national_id_type':
                // If national_id_type itself has validation
                break;
            case 'national_id_number':
                const nationalIdType = this.$('#national_id_type').val();
                if (nationalIdType && nationalIdType !== 'NONE' && !value && field.offsetParent !== null) { // Check if visible
                    isValid = false;
                    errorMessage = 'National ID Number is required when a type is selected.';
                }
                // Add pattern validation based on nationalIdType if available
                // e.g. if (nationalIdType === 'PASSPORT' && !/^[A-Z0-9]{6,9}$/.test(value)) { ... }
                break;
        }

        const errorDivId = fieldId + '_error';
        const errorDiv = this.form.querySelector('#' + errorDivId);
        const describedBy = field.getAttribute('aria-describedby') || '';
        let newDescribedBy = describedBy.split(' ').filter(id => id !== errorDivId).join(' ');

        if (!isValid && (value || forceFeedback)) { // Show error if invalid and has value or feedback is forced
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
        let isFormValid = true;
        const fieldsToValidate = this.form.querySelectorAll('input[required], select[required], textarea[required], input#contact_number, input#national_id_number');
        
        fieldsToValidate.forEach(field => {
            if (!this._validateField(field, true)) { // Force feedback for all fields on submit
                isFormValid = false;
            }
        });
        return isFormValid;
    },

    _handleNationalIdVisibility: function () {
        const nationalIdTypeField = this.$('#national_id_type');
        const nationalIdNumberGroup = this.$('#national_id_number_group'); // Assuming the input and its label are wrapped
        const nationalIdNumberField = this.$('#national_id_number');

        if (nationalIdTypeField.length && nationalIdNumberGroup.length) {
            const selectedType = nationalIdTypeField.val();
            if (selectedType && selectedType !== 'NONE' && selectedType !== '') {
                nationalIdNumberGroup.show();
                nationalIdNumberGroup.attr('aria-hidden', 'false');
                nationalIdNumberField.attr('required', 'required');
                nationalIdNumberField.attr('aria-required', 'true');
            } else {
                nationalIdNumberGroup.hide();
                nationalIdNumberGroup.attr('aria-hidden', 'true');
                nationalIdNumberField.removeAttr('required');
                nationalIdNumberField.attr('aria-required', 'false');
                nationalIdNumberField.val(''); // Clear value when hidden
                this._validateField(nationalIdNumberField[0]); // Clear any errors
            }
        }
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    _onNationalIdTypeChange: function (ev) {
        this._handleNationalIdVisibility();
        // Also validate the national_id_number field as its requirement might have changed
        const nationalIdNumberField = this.form.querySelector('#national_id_number');
        if (nationalIdNumberField) {
            this._validateField(nationalIdNumberField, true);
        }
    },

    _onSubmit: function (ev) {
        if (!this._validateForm()) {
            ev.preventDefault(); // Prevent submission if client-side validation fails
            // Optionally, focus the first invalid field
            const firstInvalidField = this.form.querySelector('[aria-invalid="true"]');
            if (firstInvalidField) {
                firstInvalidField.focus();
            }
             // Announce validation errors
            const liveRegion = document.getElementById('aria-live-form-preregistration-status');
            if (liveRegion) {
                liveRegion.textContent = 'Please correct the errors in the form.';
            }
        } else {
            this.submitButton.attr('disabled', 'disabled');
            this.submitButton.prepend('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> ');
             // Announce submission attempt
            const liveRegion = document.getElementById('aria-live-form-preregistration-status');
            if (liveRegion) {
                liveRegion.textContent = 'Submitting form...';
            }
        }
        // Server-side validation is still the definitive validation.
    },
});

return {
    DFRPreRegistrationForm: publicWidget.registry.DFRPreRegistrationForm,
};
});