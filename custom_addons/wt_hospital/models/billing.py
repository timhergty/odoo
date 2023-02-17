from odoo import api, models, fields, _


class HospitalBilling(models.Model):
    _name = 'hospital.billing'
    _description = 'Billing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "order_id_id desc"

    patient_id_id = fields.Many2one('hospital.appointment', string='Patient')
    order_id_id = fields.Many2one('hospital.appointment', 'Pay Reference', tracking=True)
    hospital_attendant = fields.Many2one('res.users', string="Hospital Attendant", tracking=True)
    billing_date = fields.Date(string='Date', tracking=True)
    doctor_notes = fields.Char(string='Doctors Notes', tracking=True)

    payment_type = fields.Selection([
        ('full', 'Full'),
        ('partial', 'Partial'),
    ], string='Payment Type', default='partial', tracking=True)
    payment_mode = fields.Selection([
        ('mobile_money', 'Mobile Money'),
        ('cash', 'Cash'),
        ('card', 'Card'),
    ], string='Payment Mode', default='card', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft', tracking=True)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    # @api.onchange('patient_id_id')
    # def set_order_id_id(self):
    #     for rec in self:
    #         if rec.patient_id_id:
    #             rec.order_id_id = rec.patient_id_id.order_id
