import logging
from odoo import fields, models
from odoo.addons import decimal_precision as dp

from odoo.tools import pycompat
from odoo.tools import float_compare

_logger = logging.getLogger(__name__)


class Product(models.Model):
    _inherit = "product.product"

    website_price = fields.Float(
        'Website price',
        compute='_compute_website_price',
        digits=dp.get_precision('Product Price')
    )
    website_public_price = fields.Float(
        'Website public price',
        compute='_compute_website_price',
        digits=dp.get_precision('Product Price')
    )
    website_price_difference = fields.Boolean(
        'Website price difference',
        compute='_compute_website_price'
    )

    def _compute_website_price(self):

        qty = self._context.get('quantity', 1.0)
        partner = self.env.user.partner_id
        current_website = self.env['website'].get_current_website()
        pricelist = current_website.get_current_pricelist()
        company_id = current_website.company_id

        context = dict(self._context, pricelist=pricelist.id, partner=partner)
        self2 = self.with_context(context) if self._context != context else self

        ret = self.env.user.has_group(
            'sale.group_show_price_subtotal') and 'total_excluded' or 'total_included'

        # para que calcule el precio con iva incluido
        ret = 'total_included'

        # p tiene el precio base
        # p2 tiene el precio aplicando la pricelist
        for p, p2 in pycompat.izip(self, self2):
            taxes = partner.property_account_position_id.map_tax(
                p.sudo().taxes_id.filtered(lambda x: x.company_id == company_id))

            p.website_price = taxes.compute_all(
                p2.price, pricelist.currency_id, quantity=qty, product=p2,
                partner=partner)[ret]

            # We must convert the price_without_pricelist in the same currency than the
            # website_price, otherwise the comparison doesn't make sense. Moreover, we show a price
            # difference only if the website price is lower
            price_without_pricelist = p.list_price
            if company_id.currency_id != pricelist.currency_id:
                price_without_pricelist = company_id.currency_id.compute(
                    price_without_pricelist, pricelist.currency_id)

            price_without_pricelist = taxes.compute_all(
                price_without_pricelist, pricelist.currency_id)[ret]

            p.website_price_difference = True if float_compare(
                price_without_pricelist, p.website_price,
                precision_rounding=pricelist.currency_id.rounding) > 0 else False

            p.website_public_price = taxes.compute_all(
                p2.lst_price, quantity=qty, product=p2, partner=partner)[ret]
