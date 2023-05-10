from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"
    confirmed_user_id = fields.Many2one('res.users', string='Confirmed User')

    def action_confirm(self):
        print("Success...........")
        # super(classname, self).func_name(self ar sathy kisu thakly ta )
        # like (self,test,test2) --> action_confirm(test,test2)
        super(SaleOrder, self).action_confirm()
        self.confirmed_user_id =self.env.user.id

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['so_confirmed_user_id'] = self.confirmed_user_id.id
        # print('invoice vals', invoice_vals)
        return invoice_vals
