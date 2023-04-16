import datetime
from odoo import api, fields, models

class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

# Ovverride the default_get function
    @api.model
    def default_get(self, fields):
        print("Default get executed")
        res = super(CancelAppointmentWizard,self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        return res

    appointment_id = fields.Many2one("hospital.appointment", string='Appoinment For')
    reason = fields.Text(string='Reason', default = "no reason")
    date_cancel = fields.Date(string ='Cancellation Date')

    def action_cancel(self):
        return

