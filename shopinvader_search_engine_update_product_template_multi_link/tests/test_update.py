# Copyright 2022 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.addons.shopinvader_search_engine_update.tests.common import (
    TestProductBindingUpdateBase,
)


class TestUpdate(TestProductBindingUpdateBase):
    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        self.product_template = self.product.product_tmpl_id
        self.product_template_2 = self.env["product.template"].create({"name": "P2"})
        self.product_2 = self.product_template_2.product_variant_id

        self.product_template_3 = self.env["product.template"].create({"name": "P3"})
        self.product_3 = self.product_template_3.product_variant_id

        xmlid = "product_template_multi_link.product_template_link_type_up_selling"
        self.link_type_up_sell = self.env.ref(xmlid)
        self.model = self.env["product.template.link"]

        self.product_binding_2 = self.product_2._add_to_index(self.se_product_index)
        self.product_binding_3 = self.product_3._add_to_index(self.se_product_index)
        self.product_bindings = (
            self.product_binding + self.product_binding_2 + self.product_binding_3
        )
        self.product_bindings.write({"state": "done"})
        return rv

    def test_flow(self):
        # given
        vals = {
            "left_product_tmpl_id": self.product_template.id,
            "right_product_tmpl_id": self.product_template_2.id,
            "type_id": self.link_type_up_sell.id,
        }
        # when
        link = self.model.create(vals)
        # then
        self.assertEqual(self.product_binding.state, "to_recompute")
        self.assertEqual(self.product_binding_2.state, "to_recompute")
        self.assertEqual(self.product_binding_3.state, "done")

        # given
        self.product_bindings.write({"state": "done"})
        # when
        link.right_product_tmpl_id = self.product_template_3
        # then
        self.assertEqual(self.product_binding.state, "to_recompute")
        self.assertEqual(self.product_binding_3.state, "to_recompute")
        self.assertEqual(self.product_binding_2.state, "to_recompute")

        # given
        self.product_bindings.write({"state": "done"})
        # when
        link.unlink()
        # then
        self.assertEqual(self.product_binding.state, "to_recompute")
        self.assertEqual(self.product_binding_3.state, "to_recompute")
        self.assertEqual(self.product_binding_2.state, "done")
