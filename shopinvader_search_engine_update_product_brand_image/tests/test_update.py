# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64

from odoo.addons.shopinvader_search_engine_product_brand_image.tests.common import (
    ProductBrandImageCase,
)


class TestUpdate(ProductBrandImageCase):
    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        self.product.product_brand_id = self.brand
        self.product_binding.state = "done"
        self.brand_binding.state = "done"
        self.new_tag = self.env["image.tag"].create(
            {
                "name": "new_tag",
            }
        )
        return rv

    def test_unlink_image(self):
        self.brand.image_ids.unlink()
        self.assertEqual(self.brand_binding.state, "to_recompute")
        self.assertEqual(self.product_binding.state, "to_recompute")

    def test_add_image(self):
        self.env["fs.product.brand.image"].create(
            {
                "sequence": 3,
                "brand_id": self.brand.id,
                "specific_image": {
                    "filename": "white2.png",
                    "content": base64.b64encode(self.white_image),
                },
            }
        )
        self.assertEqual(self.brand_binding.state, "to_recompute")
        self.assertEqual(self.product_binding.state, "to_recompute")

    def test_update_image(self):
        self.brand.image_ids[0].tag_id = self.new_tag
        self.assertEqual(self.brand_binding.state, "to_recompute")
        self.assertEqual(self.product_binding.state, "to_recompute")
