# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
import base64

from odoo.addons.shopinvader_search_engine_image.tests.common import (
    TestSeMultiImageThumbnailCase,
)


class ProductBrandImageCase(TestSeMultiImageThumbnailCase):
    def setUp(self):
        super().setUp()
        self.backend.image_data_url_strategy = "odoo"

    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        # create index for brands
        self.brand_index = self.env["se.index"].create(
            {
                "name": "brand",
                "backend_id": self.backend.id,
                "model_id": self.env.ref("product_brand.model_product_brand").id,
                "serializer_type": "shopinvader_brand_exports",
            }
        )
        # create sizes for brands
        self.env["se.image.field.thumbnail.size"].create(
            {
                "model_id": self.env.ref("product_brand.model_product_brand").id,
                "field_id": self.env.ref(
                    "fs_product_brand_multi_image.field_product_brand__image_ids"
                ).id,
                "backend_id": self.backend.id,
                "size_ids": [(6, 0, [self.size_small.id, self.size_medium.id])],
            }
        )
        self.brand = self.env["product.brand"].create(
            {
                "name": "Test Brand",
            }
        )
        self.brand_white_image = self.env["fs.product.brand.image"].create(
            {
                "sequence": 1,
                "brand_id": self.brand.id,
                "specific_image": {
                    "filename": "white.png",
                    "content": base64.b64encode(self.white_image),
                },
                "tag_id": self.tag1.id,
            }
        )
        self.brand_black_image = self.env["fs.product.brand.image"].create(
            {
                "sequence": 2,
                "brand_id": self.brand.id,
                "specific_image": {
                    "filename": "black.png",
                    "content": base64.b64encode(self.black_image),
                },
                "tag_id": self.tag2.id,
            }
        )
        self.brand_binding = self.brand._add_to_index(self.brand_index)

        self.fs_storage = self.env["fs.storage"].create(
            {
                "name": "Temp FS Storage",
                "protocol": "memory",
                "code": "mem_dir_brand",
                "directory_path": "/tmp/",
                "model_xmlids": "fs_product_brand_multi_image."
                "model_fs_product_brand_image",
                "base_url": "https://media.alcyonbelux.be/",
                "is_directory_path_in_url": False,
            }
        )
        return rv
