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
