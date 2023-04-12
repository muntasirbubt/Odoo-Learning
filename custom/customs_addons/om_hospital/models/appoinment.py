from odoo import api, fields, models


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    # chatter form view te add korar jonno inherit kora proyojon hoyese
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'patient_id'

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    # For a related field use related='patient_id.gender_new'and for change the value use readonly = False
    gender = fields.Selection(related='patient_id.gender_new', readonly=False)
    # for appointment time and booking time
    # add default for set these 2 variables default when creating a new form
    appointment_time = fields.Datetime(string="appointment time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today, help="Insert the booking date")
    # For define HTML feild
    prescription = fields.Html(string="Prescription")
    ref = fields.Char(string="Reference", help='Reference of the patient from the patient record')

    doctor_id = fields.Many2one('res.users', string='Doctor')
    active = fields.Boolean(string="Active", default=True)
    # For one2many write like 'ids' then fields.One2many(which model you need to show, "a many2one relation from this model", string)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")

    # For Hide One2many Column Based On Parent Record
    hide_sales_price = fields.Boolean(string= 'Hide Sales Price')



    # for every change in patient id this onchange_patient_id function will call every time
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    # For Priority
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'Low'),
        ('2', 'High'),
        ('3', 'Very High'),
        ('4', 'High'),
        ('5', 'Very High')], string="Priority")

    # For Statusbar
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancle', 'Cancelled')], default='draft', string="Status", required=True)

    def action_in_consultation(self):
        for r in self:
            r.state = 'in_consultation'

    def action_done(self):
        for r in self:
            r.state = 'done'

    def action_cancel(self):
        for r in self:
            r.state = 'cancle'

    def action_draft(self):
        for r in self:
            r.state = 'draft'

    # for adding button in appointment page
    def action_test(self):
        print("Button Clicked.....")
        # for rainbow effect
        return {
            'effect': {
                'fadeout': 'slow',  # for vanishing effect after sometimes automatically
                'message': 'Clicked Successfully',
                'type': 'rainbow_man',
            }
        }



