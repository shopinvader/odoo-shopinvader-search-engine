# Copyright 2024 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo.addons.shopinvader_search_engine.tests.common import TestProductBindingBase


class TestMultiProductBindingBase(TestProductBindingBase):
    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        self.product_2 = self.env.ref(
            "shopinvader_product.product_product_chair_vortex_blue"
        )
        self.product_2_binding = self.product_2._add_to_index(self.se_product_index)

        self.pricelist = self.env["product.pricelist"].create(
            {
                "name": "Test pricelist",
            }
        )

        self.pricelist_item = self.env["product.pricelist.item"].create(
            {
                "compute_price": "fixed",
                "product_id": self.product.id,
                "applied_on": "0_product_variant",
                "fixed_price": 70,
                "pricelist_id": self.pricelist.id,
            }
        )
        return rv
