# -*- coding: utf-8 -*-
import logging
import json

from odoo import http, _
from odoo.http import request
from odoo.exceptions import UserError, AccessError, ValidationError
from werkzeug.exceptions import NotFound, Forbidden

_logger = logging.getLogger(__name__)

class FarmerPortalController(http.Controller):

    def _get_preregistration_render_values(self, errors=None, form_values=None):
        """Helper to prepare values for rendering the preregistration form."""
        errors = errors or {}
        form_values = form_values or {}

        # Fetch options for form fields
        # These are examples, replace with actual models from dfr_farmer_registry or dfr_common
        national_id_types = []
        villages = []
        try:
            national_id_types = request.env['dfr.national.id.type'].sudo().search_read([], ['id', 'name'])
        except Exception as e:
            _logger.warning(f"Could not fetch national ID types: {e}")
            # Potentially add a user-facing error if this is critical
        
        try:
            # Assuming a generic model for villages, adjust as needed.
            # This might be res.country.state.village or a custom model in dfr_common/dfr_farmer_registry
            villages = request.env['res.country.state.village'].sudo().search_read([], ['id', 'name']) # Placeholder
        except Exception as e:
            _logger.warning(f"Could not fetch villages: {e}")

        return {
            'errors': errors,
            'form_values': form_values,
            'national_id_types': national_id_types,
            'villages': villages,
            'page_name': 'farmer_preregistration',
        }

    def _validate_preregistration_data(self, data):
        """Server-side validation for pre-registration form."""
        errors = {}
        required_fields = {
            'full_name': _("Full Name"),
            'village_id': _("Village"), # Assuming village_id is submitted if a selection
            'primary_crop_type': _("Primary Crop Type"),
            'contact_number': _("Contact Number"),
        }

        for field, label in required_fields.items():
            if not data.get(field):
                errors[field] = _("%s is required.") % label
        
        # Example: Basic format check for contact number (can be more specific)
        contact_number = data.get('contact_number')
        if contact_number and not contact_number.isdigit(): # Basic check
            errors['contact_number'] = _("Contact Number must be numeric.")

        # If National ID Type is selected, National ID Number becomes required
        if data.get('national_id_type_id') and not data.get('national_id_number'):
            errors['national_id_number'] = _("National ID Number is required when National ID Type is selected.")

        return errors

    @http.route('/dfr/info', type='http', auth='public', website=True, methods=['GET'], sitemap=True)
    def dfr_information_page(self, **kw):
        """
        Renders the DFR informational page.
        REQ-FSSP-002
        """
        # Informational content can be fetched from ir.config_parameter,
        # website snippets, or a dedicated model.
        # Example: Fetching from config parameters
        # about_dfr = request.env['ir.config_parameter'].sudo().get_param('dfr.portal.info.about_dfr', '')
        # benefits_farmers = request.env['ir.config_parameter'].sudo().get_param('dfr.portal.info.benefits_farmers', '')
        # how_to_register = request.env['ir.config_parameter'].sudo().get_param('dfr.portal.info.how_to_register', '')

        # For simplicity in this example, we'll pass placeholder flags or let QWeb handle static content.
        # The QWeb template itself can contain editable areas if using website editor.
        values = {
            'page_name': 'dfr_info',
            # 'about_dfr': about_dfr,
            # 'benefits_farmers': benefits_farmers,
            # 'how_to_register': how_to_register,
        }
        return request.render('dfr_farmer_portal.portal_info_page_template', values)

    @http.route('/farmer/register', type='http', auth='public', website=True, methods=['GET'], sitemap=True)
    def farmer_preregistration_form(self, **kw):
        """
        Displays the farmer pre-registration form.
        REQ-FSSP-003
        """
        render_values = self._get_preregistration_render_values(
            errors=kw.get('errors'),
            form_values=kw.get('form_values')
        )
        return request.render('dfr_farmer_portal.portal_preregistration_form_template', render_values)

    @http.route('/farmer/register', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def farmer_preregistration_submit(self, **post):
        """
        Handles the submission of the farmer pre-registration form.
        REQ-FSSP-003
        """
        errors = self._validate_preregistration_data(post)
        if errors:
            render_values = self._get_preregistration_render_values(errors=errors, form_values=post)
            return request.render('dfr_farmer_portal.portal_preregistration_form_template', render_values)

        values_dict = {
            'full_name': post.get('full_name'),
            'village_id': int(post.get('village_id')) if post.get('village_id') else False, # Assuming village is an ID
            'primary_crop_type': post.get('primary_crop_type'),
            'contact_number': post.get('contact_number'),
            'national_id_type_id': int(post.get('national_id_type_id')) if post.get('national_id_type_id') else False,
            'national_id_number': post.get('national_id_number'),
            # Add any other relevant fields from the form
        }
        
        try:
            farmer_registry_service = request.env['dfr.farmer.registry.service'] # Ensure this service model exists
            result = farmer_registry_service.sudo().create_farmer_from_portal(values_dict)

            if result.get('success'):
                # Redirect to a confirmation page
                return request.redirect('/farmer/register/thank-you?farmer_uid=%s' % result.get('farmer_uid', ''))
            else:
                errors['form'] = result.get('message', _("An unknown error occurred during pre-registration."))
                render_values = self._get_preregistration_render_values(errors=errors, form_values=post)
                return request.render('dfr_farmer_portal.portal_preregistration_form_template', render_values)

        except UserError as e: # Catch business logic errors
            _logger.warning(f"UserError during farmer pre-registration: {e}")
            errors['form'] = str(e)
            render_values = self._get_preregistration_render_values(errors=errors, form_values=post)
            return request.render('dfr_farmer_portal.portal_preregistration_form_template', render_values)
        except Exception as e:
            _logger.error(f"System error during farmer pre-registration: {e}", exc_info=True)
            errors['form'] = _("A technical error occurred. Please try again later.")
            render_values = self._get_preregistration_render_values(errors=errors, form_values=post)
            return request.render('dfr_farmer_portal.portal_preregistration_form_template', render_values)

    @http.route('/farmer/register/thank-you', type='http', auth='public', website=True, methods=['GET'], sitemap=False)
    def farmer_preregistration_confirmation(self, **kw):
        """Displays the pre-registration confirmation page."""
        return request.render('dfr_farmer_portal.portal_preregistration_confirmation_template', {
            'farmer_uid': kw.get('farmer_uid'),
            'page_name': 'preregistration_confirmation',
        })

    @http.route('/portal/forms/<model("dfr.dynamic.form"):form_id>', type='http', auth='public', website=True, methods=['GET'], sitemap=False)
    def portal_dynamic_form_render(self, form_id, **kw):
        """
        Renders a publicly accessible dynamic form.
        REQ-FSSP-009
        """
        if not form_id or not form_id.exists():
            raise NotFound()

        if not form_id.is_public_portal_accessible:
            _logger.warning(f"Attempt to access non-public dynamic form {form_id.id} by public user.")
            raise Forbidden(_("This form is not accessible."))

        try:
            dynamic_form_service = request.env['dfr.dynamic.form.service'] # Ensure this service model exists
            form_definition = dynamic_form_service.sudo().get_form_render_definition(form_id, lang=request.lang)
        except Exception as e:
            _logger.error(f"Error fetching form definition for form {form_id.id}: {e}", exc_info=True)
            # Display a user-friendly error on the portal page itself or redirect to an error page
            return request.render('dfr_farmer_portal.portal_error_template', {
                'error_message': _("Could not load the form definition. Please try again later.")
            })

        render_values = {
            'form_record': form_id,
            'form_definition': form_definition, # This should be a structured dict/list
            'form_definition_json': json.dumps(form_definition), # For JS
            'errors': kw.get('errors'),
            'form_values': kw.get('form_values'),
            'page_name': 'dynamic_form_display',
        }
        return request.render('dfr_farmer_portal.portal_dynamic_form_display_template', render_values)

    @http.route('/portal/forms/<model("dfr.dynamic.form"):form_id>', type='http', auth='public', website=True, methods=['POST'], csrf=True)
    def portal_dynamic_form_submit(self, form_id, **post):
        """
        Handles the submission of a publicly accessible dynamic form.
        REQ-FSSP-009
        """
        if not form_id or not form_id.exists():
            raise NotFound()

        if not form_id.is_public_portal_accessible:
            _logger.warning(f"Attempt to submit non-public dynamic form {form_id.id} by public user.")
            raise Forbidden(_("This form is not accessible for submission."))

        errors = {}
        farmer_record = None

        # Farmer Identification (as per SDS, field name 'farmer_identifier_field_name' is an example)
        # The actual field name must be part of the dynamic form definition itself or a known convention.
        # For this example, let's assume the dynamic form definition specifies which field is the farmer identifier.
        # A more robust way would be for dfr.dynamic.form.service to handle this.
        # Here, we'll assume a field like 'farmer_uid' is submitted within the form if required for linking.
        
        # Simplified: Assume the form includes a field named 'farmer_uid_identifier' for this example.
        # In a real scenario, the dynamic form definition should specify this.
        farmer_identifier_value = post.get('farmer_uid_identifier') # Example field name
        
        if farmer_identifier_value: # If form requires explicit farmer identification
            # Assuming 'uid' is the field on 'dfr.farmer' to search by.
            # This search should ideally be done by a service in dfr_farmer_registry.
            farmer_record = request.env['dfr.farmer'].sudo().search([('uid', '=', farmer_identifier_value)], limit=1)
            if not farmer_record:
                errors['farmer_uid_identifier'] = _("Farmer with identifier '%s' not found.") % farmer_identifier_value
        # else: if form doesn't require explicit farmer ID on submission (e.g. for anonymous surveys, or if user is logged in - not covered here)
        #    pass 

        # Server-Side Validation against form definition
        # This should be done by dfr_dynamic_form.service
        dynamic_form_service = request.env['dfr.dynamic.form.service']
        try:
            # Assume a validation method in the service
            # validation_errors = dynamic_form_service.sudo().validate_portal_submission(form_id, post)
            # For now, let's proceed and assume the service handles internal validation before processing.
            # If `validate_portal_submission` returns errors, merge them.
            # errors.update(validation_errors)
            pass # Placeholder for explicit validation call. process_portal_submission should do it.
        except ValidationError as e: # Catch validation errors raised by services
             _logger.warning(f"Validation error during dynamic form {form_id.id} submission: {e}")
             errors['form'] = str(e) # General form error
        except Exception as e:
            _logger.error(f"Error during validation pre-check for dynamic form {form_id.id}: {e}", exc_info=True)
            errors['form'] = _("A technical error occurred during validation.")


        if errors:
            # Re-render the form with errors
            # We need to fetch form_definition again for re-rendering
            try:
                form_definition_rerender = dynamic_form_service.sudo().get_form_render_definition(form_id, lang=request.lang)
            except Exception: # Simplified error handling for re-render
                form_definition_rerender = {} 
            
            render_values = {
                'form_record': form_id,
                'form_definition': form_definition_rerender,
                'form_definition_json': json.dumps(form_definition_rerender),
                'errors': errors,
                'form_values': post,
                'page_name': 'dynamic_form_display',
            }
            return request.render('dfr_farmer_portal.portal_dynamic_form_display_template', render_values)

        # Prepare submission data (exclude CSRF token, and potentially the farmer_identifier if handled separately)
        submission_data = {key: value for key, value in post.items() if key not in ['csrf_token', 'farmer_uid_identifier']}
        
        try:
            # The service should handle linking to farmer_record.id if farmer_record is found and required by form.
            result = dynamic_form_service.sudo().process_portal_submission(form_id, farmer_record.id if farmer_record else False, submission_data)

            if result.get('success'):
                # Redirect to a confirmation page
                return request.redirect(f'/portal/forms/thank-you?form_id={form_id.id}&submission_id={result.get("submission_id")}')
            else:
                errors['form'] = result.get('message', _("An unknown error occurred while submitting the form."))
                # Re-render form with error
                form_definition_rerender_fail = dynamic_form_service.sudo().get_form_render_definition(form_id, lang=request.lang)
                render_values = {
                    'form_record': form_id,
                    'form_definition': form_definition_rerender_fail,
                    'form_definition_json': json.dumps(form_definition_rerender_fail),
                    'errors': errors,
                    'form_values': post,
                    'page_name': 'dynamic_form_display',
                }
                return request.render('dfr_farmer_portal.portal_dynamic_form_display_template', render_values)

        except UserError as e: # Catch business logic errors from service
            _logger.warning(f"UserError during dynamic form {form_id.id} submission: {e}")
            errors['form'] = str(e)
            form_definition_rerender_ue = dynamic_form_service.sudo().get_form_render_definition(form_id, lang=request.lang)
            render_values = {
                'form_record': form_id,
                'form_definition': form_definition_rerender_ue,
                'form_definition_json': json.dumps(form_definition_rerender_ue),
                'errors': errors,
                'form_values': post,
                'page_name': 'dynamic_form_display',
            }
            return request.render('dfr_farmer_portal.portal_dynamic_form_display_template', render_values)
        except Exception as e:
            _logger.error(f"System error during dynamic form {form_id.id} submission: {e}", exc_info=True)
            errors['form'] = _("A technical error occurred. Please try again later.")
            # Attempt to re-render, gracefully handling potential errors in fetching definition again
            try:
                form_definition_rerender_ex = dynamic_form_service.sudo().get_form_render_definition(form_id, lang=request.lang)
            except Exception:
                form_definition_rerender_ex = {}

            render_values = {
                'form_record': form_id,
                'form_definition': form_definition_rerender_ex,
                'form_definition_json': json.dumps(form_definition_rerender_ex),
                'errors': errors,
                'form_values': post,
                'page_name': 'dynamic_form_display',
            }
            return request.render('dfr_farmer_portal.portal_dynamic_form_display_template', render_values)

    @http.route('/portal/forms/thank-you', type='http', auth='public', website=True, methods=['GET'], sitemap=False)
    def portal_dynamic_form_confirmation(self, **kw):
        """Displays the dynamic form submission confirmation page."""
        form_id = kw.get('form_id')
        form_record = None
        if form_id:
            try:
                form_record = request.env['dfr.dynamic.form'].sudo().browse(int(form_id))
            except ValueError:
                pass # Invalid form_id

        return request.render('dfr_farmer_portal.portal_dynamic_form_confirmation_template', {
            'form_record': form_record,
            'submission_id': kw.get('submission_id'),
            'page_name': 'dynamic_form_confirmation',
        })

    @http.route('/portal/error', type='http', auth='public', website=True, sitemap=False)
    def portal_error_page(self, error_message=None, **kw):
        """A generic error page for the portal."""
        return request.render("dfr_farmer_portal.portal_error_template", {
            'error_message': error_message or _("An unexpected error occurred.")
        })