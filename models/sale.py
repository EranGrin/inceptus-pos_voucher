# -*- coding: utf-8 -*-
# Part of Inceptus ERP Solutions Pvt.ltd.
# See LICENSE file for copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _name = 'sale.order'

    _inherit = ["sale.order", "ies.base"]

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        res = super(SaleOrder, self).action_invoice_create(grouped, final)
        inv_rec = self.env['account.invoice'].browse(res)
        for rec in self:
            voucher_list = []
            for line in rec.order_line:
                for voucher in line.coupon_ids:
                    voucher_list.append((4, voucher.id))

        inv_rec.write({'coupon_ids': voucher_list})
        return res


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'

    _inherit = ["sale.order.line", "ies.base"]

    coupon_ids = fields.One2many('product.coupon', 'sale_line_id', "Vouchers", compute="_get_vouchers", store=1)

    @api.depends('product_id', 'product_uom_qty')
    def _get_vouchers(self):
        if self.product_id.product_tmpl_id and self.product_id.product_tmpl_id.is_voucher \
                and self.product_id.product_tmpl_id.is_coupon:
            voucher_env = self.env['generate.voucher']
            qty = int(self.product_uom_qty)
            if len(self.coupon_ids):
                qty = int(self.product_uom_qty) - len(self.coupon_ids)
            if qty < 0:
                raise ValidationError(_('Can not Decrease the Product Qty for Voucher Products'))
            product_id = self.product_id.product_tmpl_id
            voucher_list = []
            for qty in range(qty):
                vals = {
                    'name': voucher_env.get_barcode_number(),
                    'amount': product_id.discount_amount,
                    'rem_amount': product_id.discount_amount,
                    'percentage': product_id.discount_percentage,
                    'single_use': product_id.single_use,
                    'expire_date': product_id.expires_on,
                    'product_id': product_id.id,
                    'type': product_id.discount_type,
                    'sale_price': product_id.lst_price,
                    'single_use': product_id.single_use,
                    'partner_id': self.order_id.partner_id.id,
                    'coupon_type': 'v',
                    'cart_limit': product_id.cart_limit,
                }
                voucher_list.append((0, 0, vals))
            self.coupon_ids = voucher_list
