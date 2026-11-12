# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader_search_engine_update.tests.common import (
    TestProductBindingUpdateBase,
)


class TestProductBrandUpdateBase(TestProductBindingUpdateBase):
    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        self.brand = self.env["product.brand"].create({"name": "brand"})
        self.brand_index = self.env["se.index"].create(
            {
                "name": "brand",
                "backend_id": self.backend.id,
                "model_id": self.env.ref("product_brand.model_product_brand").id,
                "serializer_type": "shopinvader_brand_exports",
            }
        )
        self.product.product_brand_id = self.brand
        self.brand_binding = self.brand._add_to_index(self.brand_index)
        self.brand_binding.state = "done"
        self.new_brand = self.env["product.brand"].create({"name": "new brand"})
        self.new_brand_binding = self.new_brand._add_to_index(self.brand_index)
        self.new_brand_binding.state = "done"
        return rv
