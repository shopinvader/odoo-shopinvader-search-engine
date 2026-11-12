# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64

from odoo.addons.shopinvader_search_engine_product_media.tests.common import (
    ProductMediaCase,
)


class TestUpdate(ProductMediaCase):
    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        self.env["fs.product.media"].create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "media_id": self.media_c.id,
                "sequence": 10,
                "link_existing": True,
            }
        )
        self.product_binding.state = "done"
        return rv

    def test_unlink_media(self):
        self.product_a.media_ids.unlink()
        self.assertEqual(self.product_binding.state, "to_recompute")

    def test_add_media(self):
        self.env["fs.product.media"].create(
            {
                "product_tmpl_id": self.product_a.product_tmpl_id.id,
                "file": {
                    "filename": "new.txt",
                    "content": base64.b64encode(b"new media"),
                },
                "media_type_id": self.media_type_b.id,
            }
        )
        self.assertEqual(self.product_binding.state, "to_recompute")

    def test_update_media(self):
        self.product_a.media_ids[0].media_type_id = self.media_type_a.id
        self.assertEqual(self.product_binding.state, "to_recompute")
