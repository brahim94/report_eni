# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from num2words import num2words


class tech_reports_extention(models.Model):
    _inherit = 'purchase.order'

    PURCHASE_ORDER_BC_STATE = [
        ('draft', 'Brouillon'),
        ('sent', 'Consultation envoyé'),
        ('to approve', 'To Approve'),
        ('purchase', 'Consultation répondue'),
        ('done', 'Fournisseur choisi'),
        ('cancel', 'Cancelled')
    ]

    state_bc_order = fields.Selection(PURCHASE_ORDER_BC_STATE, compute='_set_bc_order_state')
    lot_number = fields.Char('N° de lot')
    
    def action_fournisseur_choisi(self):
        return self.write({'state': "done"})

    def action_back_reponse(self):
        return self.write({'state': "purchase"})

    def print_purchase(self):
        self.write({'state': "sent"})
        return self.env.ref('tech_reports_extention.action_report_purchase').report_action(self)

    @api.depends('amount_total')
    def get_amount_in_words(self):
        amount_in_words = self.currency_id.amount_to_text(self.amount_total)
        return amount_in_words

    
    # def print_b_cmd(self):
    #     return self.env.ref('tech_reports_extention.action_report_b_cmd').report_action(self)

    # def print_execution(self):
    #     return self.env.ref('tech_reports_extention.action_report_execution').report_action(self)

    
class tech_order_line(models.Model):
    _inherit = 'purchase.order.line'

    article_number = fields.Char('Article N°')

    @api.model
    def create(self, vals):
        vals['article_number'] = self.env['ir.sequence'].next_by_code('purchase.article') or '/'
        return super(tech_order_line, self).create(vals)


class purchase_riquisition(models.Model):
    _inherit = 'purchase.requisition'

    def print_consultant_report(self):
        return self.env.ref('tech_reports_extention.action_report_examen').report_action(self)

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

    def print_attributaire(self):
       return self.env.ref('tech_reports_extention.action_report_attributaire').report_action(self)

    def print_non_retenu(self):
       return self.env.ref('tech_reports_extention.action_report_non_retenu').report_action(self)

    def print_borderau(self):
       return self.env.ref('tech_reports_extention.action_report_borderau').report_action(self)

    def print_approbation(self):
       return self.env.ref('tech_reports_extention.action_report_approbation').report_action(self)

    def print_prestation(self):
       return self.env.ref('tech_reports_extention.action_report_prestation').report_action(self)

    montant_ttc_marche = fields.Float(string='Montant TTC', compute='_total_lot_all')

    def _total_lot_all(self):
        for lot in self:
            montant_ttc_marche  = 0.0
            for line in lot.lot_details_ids:
                montant_ttc_marche += line.estimated_price
            lot.update({
                'montant_ttc_marche': montant_ttc_marche,
            })    
    
    text_amount = fields.Char(string="Montant en lettre", required=False, compute="onchange_amount_total" )

    @api.onchange('montant_ttc_marche')
    def onchange_amount_total(self):
        self.text_amount = num2words(self.montant_ttc_marche, lang='ar_AR')

    def create_purchase_quotation(self):
        purchase_order = self.env['purchase.order']
        purchase_order_lst = []
        purchase_order_ids = self.env['purchase.order'].search([('requisition_id', '=', self.id), ('state', 'in', ['draft', 'sent', 'to_approve'])])
        purchase_order_ids.button_cancel()
        purchase_order_ids.unlink()
        self.create_decision_final_lines()
        for each in self.tender_decision_ids:
            product_lst = []
            lot_line_ids = self.lot_details_ids.filtered(lambda l: l.id == each.lot_id.id)
            for lot_line in lot_line_ids:
                for rec in lot_line.product_ids:
                    product_line = self.line_ids.filtered(lambda l: l.product_id.id == rec.id)
                    product_lst.append((0, 0, {'product_id': rec.id,
                                                'name': rec.name,
                                                'product_qty': product_line[0].product_qty if product_line else 1.0,
                                                'product_uom': rec.uom_id.id,
                                                'price_unit': product_line[0].price_unit if product_line else 0.00,
                                                'date_planned': product_line[0].schedule_date if product_line and product_line[0].schedule_date else fields.Date.today(),
                                                'purchase_request_line_ids': [(6, 0, product_line.purchase_request_line_ids.ids)]}))
            purchase_id = purchase_order.create({'partner_id': each.bidder_id.id,
                                                  'partner_ref': (self.tender_number or '') + '-' + str(each.lot_id.n_lot) + ('-' + each.lot_id.object_name if each.lot_id.object_name else ''),
                                                  'lot_number': (self.name) + '-' + str(each.lot_id.n_lot) + ('-' + each.lot_id.object_name if each.lot_id.object_name else ''),
                                                  'requisition_id': self.id,
                                                  'tender_decision_line_id': each.id,
                                                  'order_line': product_lst})
            purchase_order_lst.append(purchase_id.id)
        
        action = self.env.ref('purchase_requisition.action_purchase_requisition_list').read()[0]
        action['domain'] = [('requisition_id', '=', self.id)]
        action['context'] = {'default_requisition_id': self.id, 'default_user_id': False, 'default_partner_ref': self.tender_number, 'search_default_group_partner_ref': 1}
        return action

class market_execution(models.Model):
    _inherit = 'market.execution'

    @api.depends('purchase_order_id_bc.amount_total')
    def get_amount_in_words(self):
        amount_in_words = self.purchase_order_id_bc.currency_id.amount_to_text(self.purchase_order_id_bc.amount_total)
        return amount_in_words

    def print_engagement(self):
        # if self.name:
        #     if self.engagement_number == _('New') or self.engagement_number == 'New':
        #         self.write({'engagement_number': self.env['ir.sequence'].next_by_code('market.engag')})
        #     return True
        return self.env.ref('tech_reports_extention.action_report_engagement').report_action(self)
        
    @api.model
    def create(self, vals):
        vals['engagement_number'] = self.env['ir.sequence'].next_by_code('market.engag') or '/'
        return super(market_execution, self).create(vals)

    def print_notification(self):
        if self.notification_number == _('New') or self.notification_number == 'New':
            self.write({'notification_number': self.env['ir.sequence'].next_by_code('market.notif')})
        return self.env.ref('tech_reports_extention.action_report_approbation').report_action(self)

    def print_commencement_order(self):
        return self.env.ref('tech_reports_extention.action_report_execution').report_action(self)
    
    def print_b_cmd(self):
        return self.env.ref('tech_reports_extention.action_report_b_cmd').report_action(self)

    def print_engagement_ap_of(self):
        return self.env.ref('tech_reports_extention.action_report_engagmnt').report_action(self)

            
class res_partner(models.Model):
    _inherit = 'res.partner'

    fax = fields.Char('Fax')

class res_company(models.Model):
    _inherit = 'res.company'

    fax = fields.Char('Fax')


class NewsPaper(models.Model):
    _inherit = 'newspaper.publication'

    def print_report_avis(self):
        for pack in self:
            for line in pack.requisition_id.newspaper_publication_ids:
                if line.notice_type == 'français':
                    return self.env.ref('tech_reports_extention.action_report_appel_offre').report_action(self)
                elif line.notice_type == 'Arabe':
                    return self.env.ref('tech_reports_extention.action_report_appel_offre_ar').report_action(self)
                
    @api.depends('requisition_id.montant_ttc_marche')
    def get_amount_in_words(self):
        amount_in_words = self.requisition_id.currency_id.montant_ttc_marche(self.requisition_id.montant_ttc_marche)
        return amount_in_words

    