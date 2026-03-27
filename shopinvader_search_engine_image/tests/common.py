# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
import base64
import io

from PIL import Image

from odoo.addons.shopinvader_search_engine.tests.common import TestBindingIndexBase


class TestSeMultiImageThumbnailCase(TestBindingIndexBase):
    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        # create thumbnail sizes
        self.size_small = self.env["se.thumbnail.size"].create(
            {
                "name": "small",
                "key": "small",
                "size_x": 5,
                "size_y": 5,
            }
        )
        self.size_medium = self.env["se.thumbnail.size"].create(
            {
                "name": "medium",
                "key": "medium",
                "size_x": 10,
                "size_y": 10,
            }
        )

        # create sizes for categories and products
        self.env["se.image.field.thumbnail.size"].create(
            {
                "model_id": self.env.ref("product.model_product_product").id,
                "field_id": self.env.ref(
                    "fs_product_multi_image.field_product_product__variant_image_ids"
                ).id,
                "backend_id": self.backend.id,
                "size_ids": [(6, 0, [self.size_small.id, self.size_medium.id])],
            }
        )

        self.env["se.image.field.thumbnail.size"].create(
            {
                "model_id": self.env.ref("product.model_product_category").id,
                "field_id": self.env.ref(
                    "fs_product_multi_image.field_product_category__image_ids"
                ).id,
                "backend_id": self.backend.id,
                "size_ids": [(6, 0, [self.size_small.id, self.size_medium.id])],
            }
        )

        # create image tag
        self.tag1 = self.env["image.tag"].create(
            {
                "name": "tag1",
            }
        )
        self.tag2 = self.env["image.tag"].create(
            {
                "name": "tag2",
            }
        )

        # create index for product and category
        self.product_index = self.env["se.index"].create(
            {
                "name": "product",
                "backend_id": self.backend.id,
                "model_id": self.env.ref("product.model_product_product").id,
                "serializer_type": "shopinvader_product_exports",
            }
        )
        self.category_index = self.env["se.index"].create(
            {
                "name": "category",
                "backend_id": self.backend.id,
                "model_id": self.env.ref("product.model_product_category").id,
                "serializer_type": "shopinvader_category_exports",
            }
        )
        self.white_image = self._create_image(16, 16, color="#FFFFFF")
        self.black_image = self._create_image(16, 16, color="#000000")
        self.logo_image = self._create_image(16, 16, color="#FFA500")
        self.product = self.env["product.product"].create(
            {
                "name": "Test product",
            }
        )
        self.product_white_image = self.env["fs.product.image"].create(
            {
                "sequence": 1,
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "specific_image": {
                    "filename": "white.png",
                    "content": base64.b64encode(self.white_image),
                },
                "tag_id": self.tag1.id,
            }
        )
        self.product_black_image = self.env["fs.product.image"].create(
            {
                "sequence": 2,
                "product_tmpl_id": self.product.product_tmpl_id.id,
                "specific_image": {
                    "filename": "black.png",
                    "content": base64.b64encode(self.black_image),
                },
                "tag_id": self.tag2.id,
            }
        )
        self.product_binding = self.product._add_to_index(self.product_index)

        self.category = self.env["product.category"].create(
            {
                "name": "Test category",
            }
        )
        self.category_logo_image = self.env["fs.product.category.image"].create(
            {
                "sequence": 1,
                "product_categ_id": self.category.id,
                "image": {
                    "filename": "logo.png",
                    "content": base64.b64encode(self.logo_image),
                },
            }
        )
        self.category_binding = self.category._add_to_index(self.category_index)
        # set odoo base_url
        self.env["ir.config_parameter"].sudo().set_param(
            "web.base.url", "http://localhost:8069"
        )

        self.fs_storage = self.env["fs.storage"].create(
            {
                "name": "Temp FS Storage",
                "protocol": "memory",
                "code": "mem_dir",
                "directory_path": "/tmp/",
                "model_xmlids": (
                    "fs_product_multi_image.model_fs_product_category_image,"
                    "fs_product_multi_image.model_fs_product_image,"
                    "search_engine_image_thumbnail.model_se_thumbnail"
                ),
                "base_url": "https://media.alcyonbelux.be/",
                "is_directory_path_in_url": False,
            }
        )
        return rv

    @classmethod
    def _create_image(cls, width, height, color="#4169E1", img_format="PNG"):
        f = io.BytesIO()
        Image.new("RGB", (width, height), color).save(f, img_format)
        f.seek(0)
        return f.read()

    def assert_image_size(self, value: bytes, width, height):
        self.assertEqual(Image.open(io.BytesIO(value)).size, (width, height))
