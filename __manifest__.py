# -*- coding: utf-8 -*-
{
    'name': "tech_reports_extention",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    "external_dependencies": {
        'python': ['num2words']
    },

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'sale', 'wt_purchase_request_extend', 'purchase_requisition', 'web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/purchase_view_inherit.xml',
        'data/sequence_purchase.xml',
        'report/lettre_consultation.xml',
        'report/examen_devis.xml',
        'report/fiche_engagement.xml',
        'report/bon_execution.xml',
        'report/bon_cmd.xml',
        'report/avis_ao.xml',
        'report/avis_ao_ar.xml',
        'report/engagement.xml',
        'report/acte_engagement.xml',
        'report/decision_convention.xml',
        'report/presentation.xml',
        'report/lettre_insertion.xml',
        'report/avis_appel_ar.xml',
        'report/convocation_membres.xml',
        'report/complement_dossier.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
