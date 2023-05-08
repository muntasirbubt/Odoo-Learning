import os
from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta


class Hospital_Patient(models.Model):
    _name = "hospital.patient"
    # chatter add korar jonno inherit kora proyojon hoyese
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"
    # _rec_name = 'ref'

    # add tracking = true for tracking like when anyone change name in log we will see which things changed
    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string="Reference")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointments")
    # date of Birth fields for calculate the age and age will be the computed field
    date_of_birth = fields.Date(string="Date Of Birth")
    appointment_counter = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointment")
    marital_status = fields.Selection([('single', 'Single'), ('married', 'Married')], string="Maritial Status")
    partner_name = fields.Char(string="Partner Name")
    parent = fields.Char(string="Parent")

    # For Birthday wish check
    is_birthday = fields.Boolean(string="Birthday ?", compute='_compute_is_birthday')

    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    website = fields.Char(string="Website")
    # appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count')

    # @api.depends('name')
    # def _ap_count(self):
    #     for rec in self:
    #         print('Working.......*******')
    #         ap_count = rec.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
    #         rec.appointment_count = ap_count

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        appointment_group = self.env['hospital.appointment'].read_group(domain=[],
                                                                        fields=['patient_id'], groupby=['patient_id'])
        for appointment in appointment_group:
            patient_id = appointment.get('patient_id')
            if patient_id:
                # print(patient_id[0])
                patient_rec = self.browse(patient_id[0])
                patient_rec.appointment_counter = appointment['patient_id_count']
            self -= patient_rec
        self.appointment_counter= 0


    # @api.depends('appointment_ids')
    # def _compute_appointment_count(self):
    #
    #     for appointment_group in self.env['hospital.appointment'].read_group(domain=[],
    #                                                                          fields=['patient_id'],
    #                                                                          groupby=['patient_id']):
    #         patient_id = appointment_group.get('patient_id')
    #         if patient_id:
    #             patient_rec = self.browse(patient_id[0])
    #             patient_rec.appointment_counter = 10
    #
    #     self.appointment_counter = 10

    # phone_num = fields.Integer(string="Phone Number")
    age = fields.Integer(string='age', compute='compute_age', inverse="_inverse_compute_age",
                         search="_search_age", tracking=True)
    kids = fields.Integer(string='kids', compute="kids_func")
    gender_new = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender New", tracking=True,
                                  default='female')
    active = fields.Boolean(string="Active", default=True)

    # For add image fields
    image = fields.Image(string="Image")

    # For one2Many
    appointment_ids = fields.One2many("hospital.appointment", "patient_id", string='Appointments')

    # For Many2Many
    tag_ids = fields.Many2many('patient.tag', string='Tags')

    # appointment_count = fields.Integer(string= "Appointment Count")

    # for statusbar option in patient record  page
    state = fields.Selection([('draft', 'Draft'),
                              ('in_consultation', 'In Consultation'),
                              ('done', 'Done'),
                              ('cancle', 'Cancelled')], default='done', string='Status', required=True)



    # for Birthday date validation
    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for i in self:
            if i.date_of_birth and i.date_of_birth > fields.Date.today():
                raise ValidationError(_("The Entered date of birth is not acceptable"))

    # patient ar record ar under a jdi kono appointment thky thky oi patient record ta delete kora jby nh
    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("Can't delete a patient with appointments"))

    # inherit create method
    @api.model
    def create(self, vals):
        # add refference value in function by ref
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(Hospital_Patient, self).create(vals)

    # For override the Write method
    def write(self, vals):
        # print("Write method is triggered", vals)
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(Hospital_Patient, self).write(vals)

    # form calculate the age from date of Birth
    @api.depends('date_of_birth')
    def compute_age(self):
        for reco in self:
            today = date.today()
            if reco.date_of_birth:
                print()
                reco.age = today.year - reco.date_of_birth.year
            else:
                reco.age = 0

    @api.depends("age")
    def _inverse_compute_age(self):
        today = date.today()
        for reco in self:
            reco.date_of_birth = today - relativedelta.relativedelta(years=reco.age)

    # For doing the compute field into searchable
    def _search_age(self, operator, value):
        print("Entered in Search Age")
        date_of_birth = date.today() - relativedelta.relativedelta(years=value)
        print("date of Birth", date_of_birth)
        start_of_year = date_of_birth.replace(day=1, month=1)
        end_of_year = date_of_birth.replace(day=31, month=12)
        print("start..........", start_of_year)
        print("End..........", end_of_year)
        return [('date_of_birth', '>=', start_of_year), ('date_of_birth', '<=', end_of_year)]

    help(os.unlink)

    def action_test(self):
        print("Clicked.. yoooo")
        return

    api.depends("date_of_birth")

    # For Birthday wish check
    def _compute_is_birthday(self):
        for rec in self:
            birthday = False
            if rec.date_of_birth:
                today = date.today()
                # print("Today's Date", today)
                # print("Employee's Date", rec.date_of_birth)
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    birthday = True
            rec.is_birthday = birthday


    def action_view_appointments(self):
        return {
            'name': _('Appointments'),
            'view_mode': 'list,form',
            'res_model': 'hospital.appointment',
            'context': {'default_patient_id': self.id},
            'domain':[('patient_id', '=', self.id)],
            'target':'current',
            'type': 'ir.actions.act_window',
        }
