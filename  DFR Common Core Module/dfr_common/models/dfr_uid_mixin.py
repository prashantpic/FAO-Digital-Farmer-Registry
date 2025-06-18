# -*- coding: utf-8 -*-
import uuid
from odoo import models, fields, api
from odoo.tools.translate import _

class DfrUidMixin(models.AbstractModel):
    """
    Mixin class for DFR models to automatically generate a unique DFR UID upon creation.
    Uses UUID v4 for generating UIDs to ensure global uniqueness.
    The 'dfr_uid' field should be unique per model that inherits this mixin.
    """
    _name = 'dfr.uid.mixin'
    _description = 'DFR Unique Identifier Mixin'

    dfr_uid = fields.Char(
        string='DFR UID',
        readonly=True,
        copy=False,
        index=True, # Important for search performance
        help="Unique Digital Farmer Registry Identifier for this record (UUID based)."
    )

    # SQL constraint to ensure uniqueness at the database level for inheriting models.
    # Note: The constraint name needs to be unique across the database or specific to the table.
    # Odoo usually handles this by prefixing with table name.
    # For an abstract mixin, this is illustrative; the concrete model would typically enforce it.
    # However, if we want to suggest a pattern:
    # _sql_constraints = [
    #    ('dfr_uid_uniq_on_model', 'unique (dfr_uid)', 'DFR UID must be unique for this record type!')
    # ]
    # This generic constraint name might clash if multiple models inherit it directly.
    # Odoo's ORM might handle this correctly by applying it to the inheriting model's table.
    # It's safer to define this in concrete models or ensure the ORM handles it.
    # For now, we rely on the `create` override to ensure uniqueness at generation.
    # A global unique index across all DFR UIDs if they were in one table is different.
    # Here, it's unique per model.

    @api.model_create_multi
    def create(self, vals_list):
        """
        Overrides create to generate a DFR UID if not provided.
        """
        for vals in vals_list:
            if 'dfr_uid' not in vals or not vals['dfr_uid']:
                vals['dfr_uid'] = str(uuid.uuid4())
        return super(DfrUidMixin, self).create(vals_list)

    def name_get(self):
        """
        Appends DFR UID to the display name if available.
        This is a common pattern but might be too generic for a base mixin.
        Consider if this is desired for all models inheriting this.
        If not, this method should be in DfrAbstractModel or specific models.
        """
        res = []
        for record in self:
            name = super(DfrUidMixin, record).name_get()[0][1] # Get the original name
            if record.dfr_uid:
                name = f"{name} [{record.dfr_uid}]"
            res.append((record.id, name))
        return res