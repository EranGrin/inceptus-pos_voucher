# -*- coding: utf-8 -*-
# Part of Inceptus ERP Solutions Pvt.ltd.
# See LICENSE file for copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _name = 'product.template'

    _inherit = ["product.template", "ies.base"]

    @api.one
    @api.depends('coupon_ids')
    def _get_voucher_count(self):
        self.voucher_count = len(
            self.coupon_ids.filtered(lambda record: record.type in ['f', 'd'] and record.coupon_type == 'v'))

    @api.constrains('discount_type')
    def _check_discount_type(self):
        for rec in self:
            if rec.is_voucher and rec.discount_type == 'd':
                raise ValidationError(_('Voucher can not have type \"Dynamic Amount\".'))

    @api.multi
    def open_vouchers(self):
        domain = [('product_id', '=', self.id)]
        view_id, form_view_id = False, False
        name = False
        if self._context.get('type') == 'gc':
            name = _('Vouchers')
            domain += [('type', 'in', ['f', 'd'])]
            view_id = self.env.ref('ies_voucher.ies_product_voucher_tree').id
            form_view_id = self.env.ref('ies_voucher.ies_product_voucher_form').id

        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'product.coupon',
            'domain': domain,
            'views': [(view_id, 'tree'), (form_view_id, 'form')]
        }

    @api.multi
    def generate_voucher_wiz(self):
        name = "Generate Voucher"
        return {
            'name': name,
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'generate.voucher',
            'target': 'new'
        }

    @api.onchange("is_voucher")
    def onchange_Voucher(self):
        if self.is_voucher:
            self.discount_amount = 0.0
            self.lst_price = 0.0
            if self.discount_type == 'd':
                self.discount_type = 'f'

    @api.onchange('discount_amount')
    def onchange_discount_amount(self):
        if not self.is_voucher:
            self.write({'lst_price': self.discount_amount})

    voucher_count = fields.Integer('Voucher Count', compute="_get_voucher_count")


class ProductCoupon(models.Model):
    _inherit = 'product.coupon'

    partner_id = fields.Many2one('res.partner', 'Customer', required=0)
    # is_voucher = fields.Boolean()
    # invoice_id = fields.Many2one('account.invoice', "Related Invoice")
    sale_line_id = fields.Many2one('sale.order.line', "Related Invoice")
