from odoo import api, fields, models


class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"

    name = fields.Char(string="Name", required=True)
    active = fields.Boolean(string='Active', default=True , copy= False)
    color_new = fields.Integer(string='Color')
    color_2 = fields.Char(string='Color_2')
    sequence = fields.Integer(string="Sequence")

    _sql_constraints = [
        ('unique_tag_name', 'unique (name, active)', 'name must be unique'),
        ('check_sequence', 'check (sequence > 0)', 'sequence must be greater then zero positive number')
        # unique name, add a constrain , some message
    ]

    # Need to override the copy method for enable the duplicate button
    @api.returns('self' , lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):

            default['name'] = self.name + " (copy)"
            default['name'] = self.name + " (copy)"
            default['sequence'] = 5

        return super(PatientTag, self).copy(default)
