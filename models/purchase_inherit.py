# -*- coding: utf-8 -*-

from odoo import models, fields, api


class tech_reports_extention(models.Model):
    _inherit = 'purchase.order'
#     _description = 'tech_reports_extention.tech_reports_extention'

    def print_purchase(self):
        return self.env.ref('tech_reports_extention.action_report_purchase').report_action(self)
    