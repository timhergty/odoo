from odoo import models, fields


# Creating Model/Table to Store Doctor Details
# https://www.youtube.com/watch?v=L6MxDR71_1k&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=2
class HospitalDoctor(models.Model):
    _name = 'hospital.doctor'
    _inherits = {'hospital.patient': 'related_patient_id'}
    _description = 'Doctor Record'

    doctor_name = fields.Char(string="Doctors Name", required=True)
    image = fields.Binary(string="Image", attachment=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], default='male', string="Gender")
    user_id = fields.Many2one('res.users', string='Related User')
    patient_id = fields.Many2one('hospital.patient', string='Related Patient')
    related_patient_id = fields.Many2one('hospital.patient', string='Related Patient ID')
