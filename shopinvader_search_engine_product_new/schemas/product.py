# Copyright 2017 Akretion
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.shopinvader_product.schemas import ProductProduct as BaseProduct


class ProductProduct(BaseProduct, extends=True):
    new_product: bool = False

    @classmethod
    def from_product_product(cls, odoo_rec):
        obj = super().from_product_product(odoo_rec)
        obj.new_product = odoo_rec.new_product or False
        return obj
