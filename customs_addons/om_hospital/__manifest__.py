# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Hospital Management',
    'version': '1.0.0',
    'category': 'Hospital',
    'author': 'Muntasir',

    'sequence': -100,
    'summary': 'Hospital Management System',
    'description': """ Hospital Management System of a hospital""",
    # add mail in depends for chatter
    'depends': ['mail', 'product', 'calendar','report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'data/mail_template_data.xml',
        'wizard/cancel_appointment_view.xml',
        'wizard/appointment_view_report.xml',
        'wizard/all_patient_view_report.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
        'views/female_patient_view.xml',
        'views/male_patient_view.xml',
        'views/kids_patient_view.xml',
        'views/operation_view.xml',
        'views/patient_tag_view.xml',
        'views/odoo_playground_view.xml',
        'views/res_config_settings_views.xml',
        'views/menu.xml',
        'report/report.xml',
        'report/patient_card.xml',
        'report/patient_details_template.xml',
        'report/appointment_details_template.xml',
        'report/all_patient_list.xml',

    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {},

}
