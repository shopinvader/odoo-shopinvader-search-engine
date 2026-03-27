# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo_test_helper import FakeModelLoader

from odoo.addons.connector_search_engine.tests.common import TestSeBackendCaseBase
from odoo.addons.extendable.tests.common import ExtendableMixin
from odoo.addons.fs_product_multi_media.tests.test_fs_product_multi_media import (
    TestFsProductMultiMedia,
)


class ProductMediaCase(TestFsProductMultiMedia, TestSeBackendCaseBase, ExtendableMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.init_extendable_registry()
        cls.addClassCleanup(cls.reset_extendable_registry)

    def setUp(self):
        super().setUp()
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()
        from odoo.addons.connector_search_engine.tests.models import SeBackend, SeIndex

        self.loader.update_registry(
            (
                SeIndex,
                SeBackend,
            )
        )
        self.backend = self.env["se.backend"].create(
            {"name": "Fake SE", "tech_name": "fake_se", "backend_type": "fake"}
        )
        self.setup_records()

    def setup_records(self, backend=None):
        self.product_index = self.env["se.index"].create(
            {
                "name": "product",
                "backend_id": self.backend.id,
                "model_id": self.env.ref("product.model_product_product").id,
                "serializer_type": "shopinvader_product_exports",
            }
        )
        self.product_binding = self.product_a._add_to_index(self.product_index)

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    def _default_media(self, media):
        return {
            "name": media.media_id.name,
            "url": media.media_id.file.internal_url,
            "type": {
                "name": media.media_id.media_type_id.name,
                "code": media.media_id.media_type_id.code,
            },
            "sequence": media.sequence,
        }
