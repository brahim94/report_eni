# -*- coding: utf-8 -*-

from odoo import models, fields, api


class tech_reports_extention(models.Model):
    _inherit = 'purchase.order'
#     _description = 'tech_reports_extention.tech_reports_extention'

    def print_purchase(self):
        return self.env.ref('tech_reports_extention.action_report_purchase').report_action(self)

    article_number = fields.Char('Article N°')

    @api.model
    def create(self, vals):
        vals['article_number'] = self.env['ir.sequence'].next_by_code('purchase.article') or '/'
        return super(tech_order_line, self).create(vals)
    
class tech_order_line(models.Model):
    _inherit = 'purchase.order.line'

    article_number = fields.Char('Article N°')

    @api.model
    def create(self, vals):
        vals['article_number'] = self.env['ir.sequence'].next_by_code('purchase.article') or '/'
        return super(tech_order_line, self).create(vals)
    