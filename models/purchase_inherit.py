# -*- coding: utf-8 -*-

from odoo import models, fields, api


class tech_reports_extention(models.Model):
    _inherit = 'purchase.order'

    PURCHASE_ORDER_BC_STATE = [
        ('draft', 'Brouillon'),
        ('sent', 'Consultation envoyé'),
        ('to approve', 'To Approve'),
        ('purchase', 'Consultation répondue'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ]

    state_bc_order = fields.Selection(PURCHASE_ORDER_BC_STATE, compute='_set_bc_order_state')


    def print_purchase(self):
        self.write({'state': "sent"})
        return self.env.ref('tech_reports_extention.action_report_purchase').report_action(self)

    
    @api.depends('amount_total')
    def get_amount_in_words(self):
        amount_in_words = self.currency_id.amount_to_text(self.amount_total)
        return amount_in_words

    
    # def print_b_cmd(self):
    #     return self.env.ref('tech_reports_extention.action_report_b_cmd').report_action(self)

    def print_execution(self):
        return self.env.ref('tech_reports_extention.action_report_execution').report_action(self)

    
class tech_order_line(models.Model):
    _inherit = 'purchase.order.line'

    article_number = fields.Char('Article N°')

    @api.model
    def create(self, vals):
        vals['article_number'] = self.env['ir.sequence'].next_by_code('purchase.article') or '/'
        return super(tech_order_line, self).create(vals)


# class tech_sale_order(models.Model):
#     _inherit = 'sale.order'
    
#     def print_engagement(self):
#         return self.env.ref('tech_reports_extention.action_report_engagement').report_action(self)
    
#     def print_execution(self):
#         return self.env.ref('tech_reports_extention.action_report_execution').report_action(self)

class purchase_riquisition(models.Model):
    _inherit = 'purchase.requisition'

    def print_consultant_report(self):
        return self.env.ref('tech_reports_extention.action_report_examen').report_action(self)

    def print_appel_offre(self):
        return self.env.ref('tech_reports_extention.action_report_appel_offre').report_action(self)

    def print_appel_offre_ar(self):
        return self.env.ref('tech_reports_extention.action_report_appel_offre_ar').report_action(self)
    
    def print_engagement_ap_of(self):
        return self.env.ref('tech_reports_extention.action_report_engagmnt').report_action(self)
    
    def print_act_engagement(self):
        return self.env.ref('tech_reports_extention.action_report_act_eng').report_action(self)
 
    def print_decision_conv(self):
       return self.env.ref('tech_reports_extention.action_report_decision').report_action(self)

    def print_presentation(self):
       return self.env.ref('tech_reports_extention.action_report_engagement').report_action(self)
    
    def print_lettre_insertion(self):
       return self.env.ref('tech_reports_extention.action_report_insertion').report_action(self)

    def print_appel_ar(self):
       return self.env.ref('tech_reports_extention.action_report_appel_ar').report_action(self)

    def print_convocation(self):
       return self.env.ref('tech_reports_extention.action_report_convocation').report_action(self)

    def print_complement(self):
       return self.env.ref('tech_reports_extention.action_report_complement').report_action(self)

class market_execution(models.Model):
    _inherit = 'market.execution'

    @api.depends('purchase_order_id_bc.amount_total')
    def get_amount_in_words(self):
        amount_in_words = self.purchase_order_id_bc.currency_id.amount_to_text(self.purchase_order_id_bc.amount_total)
        return amount_in_words

    def print_engagement(self):
        return self.env.ref('tech_reports_extention.action_report_engagement').report_action(self)
        
    def print_commencement_order(self):
        return self.env.ref('tech_reports_extention.action_report_b_cmd').report_action(self)

class res_partner(models.Model):
    _inherit = 'res.partner'

    fax = fields.Char('Fax')

class res_company(models.Model):
    _inherit = 'res.company'

    fax = fields.Char('Fax')
