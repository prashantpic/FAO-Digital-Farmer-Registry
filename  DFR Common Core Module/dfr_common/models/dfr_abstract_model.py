# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.tools.translate import _

class DfrAbstractModel(models.AbstractModel):
    """
    Abstract base model for DFR entities.
    Inherits UID generation and audit trail capabilities.
    Provides a common foundation for DFR-specific models.
    """
    _name = 'dfr.abstract.model'
    _description = 'DFR Abstract Base Model'
    # Inherits from DfrUidMixin and DfrAuditMixin.
    # These mixins should be defined in this module and imported.
    _inherit = ['dfr.uid.mixin', 'dfr.audit.mixin']

    # Example of a common helper method if needed
    # def get_dfr_context_info(self):
    #     """ Returns common DFR context information. """
    #     self.ensure_one()
    #     # Example: could fetch country-specific context if this model is used in a country-specific way
    #     # For now, a placeholder or a common utility access.
    #     return {'dfr_module': self._name}

    # Add any other common fields or methods that should be part of all DFR models,
    # e.g., fields for managing record status, activity states, etc., if they are truly universal.
    # However, try to keep this abstract model lean and use mixins for distinct functionalities.