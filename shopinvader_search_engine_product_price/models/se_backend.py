# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class SeBackend(models.Model):
    _inherit = "se.backend"

    pricelist_id = fields.Many2one(
        "product.pricelist",
        string="Pricelist",
    )
