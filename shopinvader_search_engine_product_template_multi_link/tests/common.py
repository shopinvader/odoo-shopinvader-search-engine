# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# Copyright 2020 Camptocamp SA (http://www.camptocamp.com)
# @author Simone Orsi <simahawk@gmail.com>
# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.addons.shopinvader_search_engine.tests.common import (
    TestProductBindingBase,
)


class TestProductLinkBase(TestProductBindingBase):
    def setup_records(self, backend=None):
        rv = super().setup_records(backend=backend)
        self.template_1 = self.env.ref(
            "shopinvader_product.product_template_armchair_mid_century"
        )
        self.template_1.product_template_link_ids.unlink()
        self.template_2 = self.env.ref(
            "shopinvader_product.product_template_chair_mid_century"
        )
        self.template_2.product_template_link_ids.unlink()
        self.template_3 = self.env.ref(
            "shopinvader_product.product_template_tv_cabinet_shaker_wood"
        )
        self.template_3.product_template_link_ids.unlink()

        self.variant_1_1 = self.template_1.product_variant_ids[0]
        self.variant_1_2 = self.template_1.product_variant_ids[1]
        self.variant_2_1 = self.template_2.product_variant_ids[0]
        self.variant_2_2 = self.template_2.product_variant_ids[1]
        self.variant_3_1 = self.template_3.product_variant_ids[0]
        self.variant_3_2 = self.template_3.product_variant_ids[1]
        self.link_type_asym = self.env["product.template.link.type"].create(
            {"name": "One way link", "code": "one-way", "is_symmetric": False}
        )
        self.cross_selling_type = self.env["product.template.link.type"].get_by_code(
            "cross-selling"
        )
        self.up_selling_type = self.env["product.template.link.type"].get_by_code(
            "up-selling"
        )
        self._create_links()
        self.variant_1_1_binding = self.variant_1_1._add_to_index(self.se_product_index)
        self.variant_1_2_binding = self.variant_1_2._add_to_index(self.se_product_index)
        self.variant_2_1_binding = self.variant_2_1._add_to_index(self.se_product_index)
        self.variant_2_2_binding = self.variant_2_2._add_to_index(self.se_product_index)
        self.variant_3_1_binding = self.variant_3_1._add_to_index(self.se_product_index)
        self.variant_3_2_binding = self.variant_3_2._add_to_index(self.se_product_index)
        return rv

    def _create_links(self):
        self.link_upselling_1_2 = self.env["product.template.link"].create(
            {
                "left_product_tmpl_id": self.template_1.id,
                "right_product_tmpl_id": self.template_2.id,
                "type_id": self.up_selling_type.id,
            }
        )
        self.link_crosselling_1_3 = self.env["product.template.link"].create(
            {
                "left_product_tmpl_id": self.template_1.id,
                "right_product_tmpl_id": self.template_3.id,
                "type_id": self.cross_selling_type.id,
            }
        )
        self.link_crosselling_2_3 = self.env["product.template.link"].create(
            {
                "left_product_tmpl_id": self.template_2.id,
                "right_product_tmpl_id": self.template_3.id,
                "type_id": self.env.ref(
                    "product_template_multi_link."
                    "product_template_link_type_cross_selling"
                ).id,
            }
        )
        self.link_one_way_3_2 = self.env["product.template.link"].create(
            {
                "left_product_tmpl_id": self.template_3.id,
                "right_product_tmpl_id": self.template_2.id,
                "type_id": self.link_type_asym.id,
            }
        )
