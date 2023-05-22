from odoo import api, fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"
    confirmed_user_id = fields.Many2one('res.users', string='Confirmed User', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        # s represent sale order
        fields['confirmed_user_id'] = ", s.confirmed_user_id"
        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)




