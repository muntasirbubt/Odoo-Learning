from odoo import api, fields, models
from datetime import date

class Hospital_Patient(models.Model):
    _name = "hospital.patient"
    # chatter add korar jonno inherit kora proyojon hoyese
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Hospital Patient"


    # add tracking = true for tracking like when anyone change name in log we will see which things changed
    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string="Reference")

    appointment_id = fields.Many2one('hospital.appointment', string="Appointments")

    # date of Birth fields for calculate the age and age will be the computed field
    date_of_birth = fields.Date(string="Date Of Birth")
    age = fields.Integer(string='age', compute='compute_age', tracking= True, store=True)
    kids = fields.Integer(string='kids', compute ="kids_func")
    gender_new = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender New", tracking=True,
                                  default='female')
    active = fields.Boolean(string="Active", default=True)

    # For add image fields
    image = fields.Image(string = "Image")

    #For one2Many
    appointment_ids = fields.One2many("hospital.appointment","patient_id",string ='Appointments')

    # For Many2Many
    tag_ids = fields.Many2many('patient.tag',string='Tags')

    #for statusbar option in patient record  page
    state = fields.Selection([('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancle', 'Cancelled')], default = 'done', string = 'Status', required = True)




#form calculate the age from date of Birth and
    @api.depends('date_of_birth')
    def compute_age(self):
        for reco in self:
            today = date.today()
            if reco.date_of_birth:
                print()
                reco.age = today.year - reco.date_of_birth.year
            else:
                reco.age = 0
