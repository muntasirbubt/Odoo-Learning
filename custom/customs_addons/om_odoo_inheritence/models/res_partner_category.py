from odoo import api, fields, models


class PartnerCategory(models.Model):
    _name = 'res.partner.category'
    _inherit = ["res.partner.category", 'mail.thread']

    name = fields.Char(tracking=True)



