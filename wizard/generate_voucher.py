# -*- coding: utf-8 -*-
# Part of Inceptus ERP Solutions Pvt.ltd.
# See LICENSE file for copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from random import randrange


class GenerateVoucher(models.TransientModel):
    """Not enabled"""
    _name = 'generate.voucher'

    coupon_qty = fields.Integer('Number of Voucher', default=1, required=1)
    partner_id = fields.Many2one('res.partner', 'Customer', required=1)

    @api.model
    def generate_coupon_number(self, digits):
        ean = map(int, list(digits))
        for x in range(10):
            ean.append(randrange(10))
        sum = lambda x, y: int(x) + int(y)
        evensum = reduce(sum, ean[::2])
        oddsum = reduce(sum, ean[1::2])
        ean.append((10 - ((evensum + oddsum * 3) % 10)) % 10)
        number = ''.join(map(str, ean))
        coupon_barcode = self.env['product.coupon'].search([('name', '=', number)])
        barcode = self.env['product.template'].search([('barcode', '=', number)])
        if len(coupon_barcode) or len(barcode):
            self.generate_coupon_number(digits)
        return number

    @api.model
    def get_barcode_number(self):
        user = self.env['res.users'].browse(self._uid)
        if not user.company_id.code_format:
            raise ValidationError(_('Please Configure Giftcard Code Format in Company.'))
        if user.company_id.code_format == 'ean13':
            return self.generate_coupon_number('99')
        elif user.company_id.code_format == 'upca':
            return self.generate_coupon_number('5')

    @api.multi
    def generate_voucher(self, context=False, line_id=False, product_id=False, qty=False):
        print line_id, product_id, qty
        coupon_env = self.env['product.coupon']
        product_id = product_id or self.env['product.template'].browse(self._context.get('active_id'))
        for qty in range(qty or self.coupon_qty):
            vals = {
                'name': self.get_barcode_number(),
                'amount': product_id.discount_amount,
                'rem_amount': product_id.discount_amount,
                'percentage': product_id.discount_percentage,
                'single_use': product_id.single_use,
                'expire_date': product_id.expires_on,
                'product_id': product_id.id,
                'type': product_id.discount_type,
                'sale_price': product_id.lst_price,
                'single_use': product_id.single_use,
                # 'partner_id': self.partner_id.id,
                'sale_line_id': line_id and line_id.id or False,
                'coupon_type': 'v',
                'cart_limit': product_id.cart_limit,
            }
            coupon_env.create(vals)

        product_id.generated = True

        return {'type': 'ir.actions.act_window_close'}
