# Copyright 2018 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# Simone Orsi <simahawk@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.addons.queue_job.tests.common import JobMixin
from odoo.addons.shopinvader_search_engine.tests.common import TestBindingIndexBase


class StockCommonCase(TestBindingIndexBase, JobMixin):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.env = cls.env(
            context=dict(
                cls.env.context,
                tracking_disable=True,  # speed up tests
                queue_job__no_delay=False,  # we want the jobs
            )
        )

    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        ref = self.env.ref
        self.warehouse_1 = ref("stock.warehouse0")
        self.loc_1 = self.warehouse_1.lot_stock_id
        self.warehouse_2 = self.env["stock.warehouse"].create(
            {"name": "WH2", "code": "WH2"}
        )
        self.loc_2 = self.warehouse_2.lot_stock_id
        self.product = self.env["product.product"].create(
            {
                "name": "Stock prod 1",
                "type": "consu",
                "is_storable": True,
            }
        )
        self.index = self.env["se.index"].create(
            {
                "name": "product",
                "backend_id": self.backend.id,
                "model_id": self.env.ref("product.model_product_product").id,
                "serializer_type": "shopinvader_product_exports",
                "warehouse_ids": [(6, 0, self.warehouse_1.ids)],
                "product_stock_field_id": ref(
                    "stock.field_product_product__qty_available"
                ).id,
            }
        )
        self.product_binding = self.product._add_to_index(self.index)
        self.loc_supplier = self.env.ref("stock.stock_location_suppliers")
        self.picking_type_in = self.env.ref("stock.picking_type_in")
        return rv

    def _add_stock_to_product(self, product, location, qty):
        """Set the stock quantity of the product.

        :param product: product.product recordset
        :param qty: float
        """
        self.env["stock.quant"].with_context(inventory_mode=True).create(
            {
                "product_id": product.id,
                "location_id": location.id,
                "inventory_quantity_auto_apply": qty,
            }
        )

    def _create_incoming_move(self):
        location_dest = self.picking_type_in.default_location_dest_id
        return self.env["stock.move"].create(
            {
                "name": "Forced Move",
                "location_id": self.loc_supplier.id,
                "location_dest_id": location_dest.id,
                "product_id": self.product.id,
                "product_uom_qty": 2.0,
                "product_uom": self.product.uom_id.id,
                "picking_type_id": self.picking_type_in.id,
            }
        )
