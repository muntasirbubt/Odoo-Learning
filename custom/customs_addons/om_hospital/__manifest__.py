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
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'wizard/cancel_appointment_view.xml',
        'views/menu.xml',
        'views/patient_view.xml',
        'views/female_patient_view.xml',
        'views/male_patient_view.xml',
        'views/kids_patient_view.xml',
        'views/appointment_view.xml',
        'views/operation_view.xml',
        'views/patient_tag_view.xml',
        'views/odoo_playground_view.xml',
        'views/res_config_settings_views.xml',


    ],
    'demo': [],
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'assets': {},

}
