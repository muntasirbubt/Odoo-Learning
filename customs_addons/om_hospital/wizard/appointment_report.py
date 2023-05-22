import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from datetime import date
from dateutil import relativedelta


class AppointmentReportWizard(models.TransientModel):
    _name = "appointment.report.wizard"
    _description = "Appointment Report Wizard"

    patient_id = fields.Many2one("hospital.patient", string='Patient')
    date_form = fields.Date(string='Date Form')
    date_to = fields.Date(string='Date To')

    def action_print_report(self):
        domain=[]
        patient_id = self.patient_id
        if patient_id:
            domain += [('patient_id', '=', patient_id.id)]
        date_form = self.date_form
        if date_form:
            domain += [('booking_date', '>=', date_form)]
        date_to = self.date_to
        if patient_id:
            domain += [('booking_date', '<=', date_to)]

        appointments = self.env['hospital.appointment'].search_read(domain)
        # appointments = self.env['hospital.appointment'].search(domain)
        # appointments_list = []
        # for appointment in appointments:
        #     vals = {
        #         'ref':'appointment.ref',
        #         'booking_date':'appointment.booking_date',
        #         'age':'self.age',
        #     }
        #     appointments_list.append(vals)
        data = {
            'form_data': self.read()[0],
            'appointments':appointments,
            # 'appointments':appointments_list,
        }
        return self.env.ref('om_hospital.action_report_appointment_tu').report_action(self, data=data)

    def action_print_excel_report(self):
        # print("Print the Excel Report")
        domain = []
        patient_id = self.patient_id
        if patient_id:
            domain += [('patient_id', '=', patient_id.id)]
        date_form = self.date_form
        if date_form:
            domain += [('booking_date', '>=', date_form)]
        date_to = self.date_to
        if patient_id:
            domain += [('booking_date', '<=', date_to)]
        print(domain)

        appointments = self.env['hospital.appointment'].search_read(domain)
        data = {
            'appointments': appointments,
            'form_data': self.read()[0]
        }
        return self.env.ref('om_hospital.report_patient_appointment_xlsx').report_action(self, data=data)



