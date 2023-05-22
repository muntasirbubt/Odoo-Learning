from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import random


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"

    # chatter form view te add korar jonno inherit kora proyojon hoyese
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Appointment"
    _rec_name = 'sequence'
    _order = 'id desc'

    # ondelete restrict dily record ta delete kora jby nh
    # ondelete casecade
    patient_id = fields.Many2one('hospital.patient', string='Patient', ondelete='cascade', tracking=1)
    sequence = fields.Char(string="Sequence", tracking=True)

    # For a related field use related='patient_id.gender_new'and for change the value use readonly = False
    gender = fields.Selection(related='patient_id.gender_new', readonly=False, tracking=True)

    # for appointment time and booking time
    # add default for set these 2 variables default when creating a new form
    appointment_time = fields.Datetime(string="appointment time", default=fields.Datetime.now)
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today)
    duration = fields.Float(string="Duration", tracking=6)

    # For currency (Monetary fields)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id')

    # For define HTML feild
    prescription = fields.Html(string="Prescription")
    ref = fields.Char(string="Reference", help='Reference of the patient from the patient record', tracking=True)

    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=3)
    active = fields.Boolean(string="Active", default=True)

    # For one2many write like 'ids' then fields.One2many(which model you need to show, "a many2one relation from this model", string)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")

    # For Hide One2many Column Based On Parent Record
    hide_sales_price = fields.Boolean(string='Hide Sales Price')

    operation_id = fields.Many2one('hospital.operation', string="Operations")

    # for progress widget
    progress = fields.Integer(string="Progress", compute="_compute_progress")
    # For Calculating the total amount
    total_amount = fields.Monetary(string="Total", compute="_compute_total_amount",currency_field='currency_id')

    @api.depends('pharmacy_line_ids')
    def _compute_total_amount(self):
        for rec in self:
            amount_total = 0
            for lin in rec.pharmacy_line_ids:
                amount_total += lin.price_subtotal
            rec.amount_total = amount_total

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:

            if rec.state == 'draft':
                progress = random.randrange(0, 25)
            elif rec.state == 'in_consultation':
                progress = random.randrange(25, 99)
            elif rec.state == 'done':
                progress = 100
            else:
                progress = 0
            rec.progress = progress

    # for every change in patient id this onchange_patient_id function will call every time
    # sayeda nafia sultana
    @api.onchange('patient_id', )
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
        ('cancle', 'Cancelled')], default='draft', string="Status", required=True, tracking=2)

    def set_line_number(self):
        sl_no = 0
        for l in self.pharmacy_line_ids:
            sl_no += 1
            l.sl_no = sl_no
        return


    @api.model
    def create(self, vals):
        # add reference value in function by ref
        vals['sequence'] = self.env['ir.sequence'].next_by_code('hospital.appointment.seq')
        res = super(HospitalAppointment, self).create(vals)
        res.set_line_number()
        return res

    # For removing the delete option in done state record
    def unlink(self):
        print("TEST Unlink")
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError(_("You can delete the record which is only in draft state"))
        return super(HospitalAppointment, self).unlink()

    # For override the Write method
    def write(self, vals):
        res = super(HospitalAppointment, self).write(vals)
        self.set_line_number()
        return res

    # For Share in whatsapp
    def action_share_whatsapp(self):
        if not self.patient_id.phone:
            raise ValidationError(_("Missing Phone Number in Patient Record"))
        message = "Hi *%s* your *appointment* number is %s. Thank You" % (self.patient_id.name, self.sequence)
        whatsapp_api_url = "http://api.whatsapp.com/send?phone=%s&text=%s" % (self.patient_id.phone, message)
        self.message_post(body=message, subject="Whatsapp Message")
        return {
            'type': '.ir.actions.act_url',
            'target': 'new',
            'url': whatsapp_api_url
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for r in self:
            r.state = 'done'

    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for r in self:
            r.state = 'draft'

    # for adding button in appointment page
    def action_test(self):
        # URL Action
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',  # For open in same tab('self' for same tab, new for 'new' tab)
            'url': 'http://www.odoo.com',
        }

        # # for rainbow effect
        # return {
        #     'effect': {
        #         'fadeout': 'slow',  # for vanishing effect after sometimes automatically
        #         'message': 'Clicked Successfully',
        #         'type': 'rainbow_man',
        #     }
        # }

    def action_notification(self):
        action = self.env.ref('om_hospital.action_hospital_patient')
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Clicked to open the patient record'),
                'message': '%s',
                # 'links': [{
                #     'label': self.patient_id.name,
                #     'url': f'#action={action.id}&id={self.patient_id.id}&model=hospital.patient'
                # }],
                'sticky': False,
                'next': {
                    'type': 'ir.actions.act_window',
                    'res_model': 'hospital.patient',
                    'res_id': self.patient_id.id,
                    'views': [(False, 'form')],
                }
            },

        }
