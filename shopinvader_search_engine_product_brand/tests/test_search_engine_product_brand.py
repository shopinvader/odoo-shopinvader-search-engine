# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader_search_engine.tests.common import TestBindingIndexBase


class TestBrandBinding(TestBindingIndexBase):
    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        self.brand = self.env["product.brand"].create({"name": "Test Brand"})
        # create index for brand
        self.brand_index = self.env["se.index"].create(
            {
                "name": "brand",
                "backend_id": self.backend.id,
                "model_id": self.env.ref("product_brand.model_product_brand").id,
                "serializer_type": "shopinvader_brand_exports",
            }
        )
        self.brand_binding = self.brand._add_to_index(self.brand_index)
        return rv

    def test_product_brand(self):
        brand = self.brand_binding._contextualize(self.brand_binding)
        data = self.brand_index.model_serializer.serialize(brand.record)
        self.assertIn("name", data)
        self.assertEqual(data["name"], "Test Brand")
