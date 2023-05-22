from odoo import api, fields, models


class ResGroup(models.Model):
    _inherit = "res.groups"

    @api.model
    def get_application_groups(self, domain):
        print("Domain...", domain)
        group_id = self.env.ref('account.group_sale_receipts').id
        wave_id = self.env.ref('stock.group_stock_picking_wave').id
        return super().get_application_groups(domain + [('id', '!=', (group_id, wave_id))])
