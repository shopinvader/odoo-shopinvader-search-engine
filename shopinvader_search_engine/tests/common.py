# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo_test_helper import FakeModelLoader

from odoo.addons.connector_search_engine.tests.common import TestSeBackendCaseBase
from odoo.addons.extendable.tests.common import ExtendableMixin


class TestBindingIndexBase(TestSeBackendCaseBase, ExtendableMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.init_extendable_registry()
        cls.addClassCleanup(cls.reset_extendable_registry)

    def setUp(self):
        super().setUp()
        # Load fake models ->/
        self.loader = FakeModelLoader(self.env, self.__module__)
        self.loader.backup_registry()

        from odoo.addons.connector_search_engine.tests.models import (
            FakeSeAdapter,
            SeBackend,
            SeIndex,
        )

        self.loader.update_registry((SeIndex, SeBackend))
        self.se_adapter = FakeSeAdapter
        self.backend = self.env["se.backend"].create(
            {"name": "Fake SE", "tech_name": "fake_se", "backend_type": "fake"}
        )
        self.setup_records()

    def tearDown(self):
        self.loader.restore_registry()
        super().tearDown()

    def setup_records(self, backend=None):
        pass


class TestCategoryBindingBase(TestBindingIndexBase):
    def _prepare_category_index_values(self, backend=None):
        backend = backend or self.backend
        return {
            "name": "Category Index",
            "backend_id": backend.id,
            "model_id": self.env["ir.model"]
            .search([("model", "=", "product.category")], limit=1)
            .id,
            "lang_id": self.env.ref("base.lang_en").id,
            "serializer_type": "shopinvader_category_exports",
        }

    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        backend = backend or self.backend
        # create an index for category model
        self.se_categ_index = self.env["se.index"].create(
            self._prepare_category_index_values(backend)
        )
        # create a binding + category alltogether
        self.category = self.env["product.category"].create({"name": "Test category"})
        self.category_binding = self.category._add_to_index(self.se_categ_index)
        return rv


class TestProductBindingBase(TestBindingIndexBase):
    def _prepare_product_index_values(self, backend=None):
        backend = backend or self.backend
        return {
            "name": "Product Index",
            "backend_id": backend.id,
            "model_id": self.env["ir.model"]
            .search([("model", "=", "product.product")], limit=1)
            .id,
            "lang_id": self.env.ref("base.lang_en").id,
            "serializer_type": "shopinvader_product_exports",
        }

    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        backend = backend or self.backend
        # create an index for product model
        self.se_product_index = self.env["se.index"].create(
            self._prepare_product_index_values(backend)
        )
        # create a binding + product alltogether
        self.product = self.env.ref(
            "shopinvader_product.product_product_chair_vortex_white"
        )
        self.product_binding = self.product._add_to_index(self.se_product_index)
        self.product_expected = {
            "id": self.product.id,
            "name": self.product.name,
        }
        return rv
