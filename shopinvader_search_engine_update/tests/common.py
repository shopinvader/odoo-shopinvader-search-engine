# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader_search_engine.tests.common import TestProductBindingBase


class TestProductBindingUpdateBase(TestProductBindingBase):
    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        self.product_binding.state = "done"
        return rv
