# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _
from ..utils import constants # Assuming constants.py is in dfr_common/utils/

class DfrConfigSettings(models.TransientModel):
    """
    Extends res.config.settings to manage DFR common configurations.
    Allows administrators to view DPI principles, license info, and set
    common parameters like the Codebase Governance Document URL.
    """
    _inherit = 'res.config.settings'

    # DPI Principles (Display Only)
    dfr_common_dpi_principles_info = fields.Text(
        string=_("DFR DPI Principles"),
        readonly=True,
        compute='_compute_dfr_common_dpi_principles_info',
        help=_("Information about Digital Public Infrastructure (DPI) principles adhered to by the DFR platform.")
    )

    # License Information (Display Only)
    dfr_common_platform_license = fields.Char(
        string=_("DFR Platform License"),
        readonly=True,
        compute='_compute_dfr_common_platform_license',
        help=_("The primary open-source license under which the DFR platform is distributed.")
    )

    # Configurable Parameters
    dfr_common_codebase_governance_url = fields.Char(
        string=_("Codebase Governance Document URL"),
        config_parameter='dfr_common.governance_url', # Stored in ir.config_parameter
        help=_("URL to the DFR Codebase Governance Framework document.")
    )

    # Example of another configurable setting
    dfr_common_example_setting = fields.Boolean(
        string=_("Enable DFR Common Example Feature"),
        config_parameter='dfr_common.example_feature_enabled',
        help=_("An example boolean setting for the DFR common module.")
    )

    @api.depends('dfr_common_codebase_governance_url') # Dummy dependency to trigger compute if needed
    def _compute_dfr_common_dpi_principles_info(self):
        for record in self:
            principles = [
                f"<strong>{_('Openness')}</strong>: {constants.DPI_PRINCIPLE_OPENNESS}",
                f"<strong>{_('Reusability')}</strong>: {constants.DPI_PRINCIPLE_REUSABILITY}",
                f"<strong>{_('Inclusion')}</strong>: {constants.DPI_PRINCIPLE_INCLUSION}",
                f"<strong>{_('Data Sovereignty')}</strong>: {constants.DPI_PRINCIPLE_DATA_SOVEREIGNTY}",
            ]
            record.dfr_common_dpi_principles_info = "<ul>" + "".join(f"<li>{p}</li>" for p in principles) + "</ul>"


    @api.depends('dfr_common_codebase_governance_url') # Dummy dependency
    def _compute_dfr_common_platform_license(self):
        for record in self:
            # Fetch from manifest or constants.py for consistency
            record.dfr_common_platform_license = constants.DEFAULT_LICENSE_NAME