import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta


class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    # Ovverride the default_get function
    @api.model
    def default_get(self, fields):
        # print("Default get executed")
        res = super(CancelAppointmentWizard, self).default_get(fields)
        res['date_cancel'] = datetime.date.today()
        # if self.env.context.get('active_id'):
        #     res['appointment_id'] = self.env.context.get('active_id')
        return res

    appointment_id = fields.Many2one("hospital.appointment", string='Appointment For',
                                     domain=[('state', '=', 'draft'), ('priority', 'in', ('0', '1', False))])
    reason = fields.Text(string='Reason', default="no reason")
    date_cancel = fields.Date(string='Cancellation Date')

    def action_cancel(self):
        # Access conf. Value From Settings Inside the code
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_day')
        # print("cancle day", cancel_day)
        # print(self.appointment_id.booking_date)
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        print('allowed_date', allowed_date)
        if allowed_date < date.today():
            raise ValidationError(_("Sorry Cancellation is not allowed for this booking"))
        self.appointment_id.state = "cancle"

        # How To Execute SQL Queries
        query = """select id,patient_id from hospital_appointment where id =%s""" %self.appointment_id.id
        # from the environment we will be getting a database cursor then execute the query
        # self.env.cr.execute("""select id,name from hospital_patient""") or,
        self.env.cr.execute(query) # self.cr.execute(query)-> same thing
        result_query = self.env.cr.fetchall()
        # fetchall dily touple hishebe print krebe  & dictfetchall  hly dictionary a return krbe & dictfetchone hly 1 record return krbe
        print('Query Result', result_query)

        # For Prevent Closing of wizard
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'cancel.appointment.wizard',
            'target': 'new',
            'res_id': self.id,
        }

        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'reload',
        # }

        # return
