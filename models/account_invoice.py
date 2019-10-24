# -*- coding: utf-8 -*-
# Part of Inceptus ERP Solutions Pvt.ltd.
# See LICENSE file for copyright and licensing details.

from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    # voucher_ids = fields.One2many('product.coupon', 'invoice_id', "Vouchers")
    #  moved to base redeem renamed to coupon_ids

    # @api.multi
    # def write(self, vals):
    #     res = super(AccountInvoice, self).write(vals)
    #     if vals.get('state') == 'paid':
    #         for rec in self:
    #             expiry_date = False
    #             if rec.coupon_ids and rec.coupon_ids[0] and rec.coupon_ids[0].product_id.expiry_after_sale:
    #                 product_id = rec.vocher_ids[0].product_id
    #                 expiry_date = self.env['product.template'].compute_expiry_date(product_id.expiry_unit,
    #                                                                                product_id.expiry_interval)
    #             rec.coupon_ids.write({
    #                 'state': 's',
    #                 'sale_date': fields.Date.today(),
    #                 'expire_date': expiry_date or False
    #             })
    #     return res
