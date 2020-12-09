# -*- coding: utf-8 -*-

from odoo import models, fields, api


class tech_reports_extention(models.Model):
    _inherit = 'purchase.order'

    def print_purchase(self):
        self.write({'state': "sent"})
        return self.env.ref('tech_reports_extention.action_report_purchase').report_action(self)

    
    @api.depends('amount_total')
    def get_amount_in_words(self):
        amount_in_words = self.currency_id.amount_to_text(self.amount_total)
        return amount_in_words

    
    def print_b_cmd(self):
        return self.env.ref('tech_reports_extention.action_report_b_cmd').report_action(self)
        
    
class tech_order_line(models.Model):
    _inherit = 'purchase.order.line'

    article_number = fields.Char('Article N°')

    @api.model
    def create(self, vals):
        vals['article_number'] = self.env['ir.sequence'].next_by_code('purchase.article') or '/'
        return super(tech_order_line, self).create(vals)


class tech_sale_order(models.Model):
    _inherit = 'sale.order'
    
    def print_engagement(self):
        return self.env.ref('tech_reports_extention.action_report_engagement').report_action(self)
    
    def print_execution(self):
        return self.env.ref('tech_reports_extention.action_report_execution').report_action(self)

class purchase_riquisition(models.Model):
    _inherit = 'purchase.requisition'

    def print_consultant_report(self):
        return self.env.ref('tech_reports_extention.action_report_examen').report_action(self)

class market_execution(models.Model):
    _inherit = 'market.execution'

    @api.depends('purchase_order_id_bc.amount_total')
    def get_amount_in_words(self):
        amount_in_words = self.purchase_order_id_bc.currency_id.amount_to_text(self.purchase_order_id_bc.amount_total)
        return amount_in_words

    def print_engagement(self):
        return self.env.ref('tech_reports_extention.action_report_b_cmd').report_action(self)
