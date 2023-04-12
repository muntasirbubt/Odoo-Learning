from odoo import api, fields, models

class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    # add required for value must be needed
    product_id = fields.Many2one('product.product', required=True)
    # add related because we need sales price based on product , product select korar sathy price auto niye nibe product model theke
    price_unit = fields.Float(string="Price", related='product_id.list_price')
    # add default for by default 1 show krbe
    qty = fields.Integer(string="Quantity", default=1)
    # many2One field
    appointment_id = fields.Many2one("hospital.appointment", string='Appointment')