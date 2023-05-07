from odoo import api, fields, models, _


class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "Hospital Operation"
    # For not add the default field when create the new model
    _log_access = False
    _order = 'sequence,id'
    _rec_name = 'operation_name'

    doctor_id = fields.Many2one('res.users', string='Doctor')
    operation_name = fields.Char(string='Name')
    # For reference field(Patient ar maddome hospital.patient er patient name gula nisse)
    reference_record = fields.Reference(
        selection=[('hospital.patient', 'Patient'), ('hospital.appointment', 'Appointment')], string='Record')
    sequence = fields.Integer(string="Sequence", default = 10)

    # For the many2One field(Cause there is no rec_name)
    @api.model
    def name_create(self, name):
        print("Name.................**", name)
        return self.create({'operation_name': name}).name_get()[0]
