import pytz
from lxml import etree
from odoo import models, fields, api, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "appointment_date desc"

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        result = super(HospitalAppointment, self).fields_view_get(view_id,
                                                                  view_type,
                                                                  toolbar=toolbar,
                                                                  submenu=submenu)

        doc = etree.XML(result['arch'])
        # print("doc", doc)
        # for elem in doc.xpath("//field[@name='appointment_date']"):
        #     doc.remove(elem)
        # result['arch'] = doc
        return result

    # Deleting One2Many Lines From Code and Datetime Conversion , UTC -> Local
    # https://www.youtube.com/watch?v=ZxrDGTEU7B8&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=66
    # https://www.youtube.com/watch?v=2pOIxhE_xuY&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=59
    def delete_lines(self):
        for rec in self:
            user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
            time_in_timezone = pytz.utc.localize(rec.appointment_datetime).astimezone(user_tz)
            rec.appointment_lines = [(5, 0, 0)]

    # Moving the State Of the Record To Confirm State in Button Click
    # How to Add States/Statusbar for Records in Odoo
    # https://www.youtube.com/watch?v=lPHWsw3Iclk&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=21
    def action_confirm(self):
        for rec in self:
            patient = self.env['hospital.patient'].search([('id', '=', 19)])
            print("patient_name...", patient.patient_name)
            print("sequence...", patient.name_seq)
            print("Display Name...", patient.display_name)

            female_patients = self.env['hospital.patient'].search([('gender', '=', 'female')])
            filtered_female_patients = self.env['hospital.patient'].search([]).filtered(lambda s: s.gender == 'female')
            print("female_patients....", female_patients)
            print("filtered_female_patients....", filtered_female_patients)
            mapped_patient_name = self.env['hospital.patient'].search([]).sorted(key='patient_age').mapped(
                'patient_age')
            fg_patient_name = self.env['hospital.patient'].search([]).filtered(lambda s: s.gender == 'female').sorted(
                key='patient_age', reverse=True).mapped('patient_age')
            print("mapped_patient_name...", mapped_patient_name)
            print("fg_patient_name...", fg_patient_name)

            product_category = self.env['product.category'].search([]).mapped('name')
            product_category_context = self.env['product.category'].with_context(lang='ar_SY').search([]).mapped('name')
            print("product_category...", product_category)
            print("product_category_context...", product_category_context)

            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    # Overriding the Create Method in Odoo
    # https://www.youtube.com/watch?v=ZfKzmfiqeg0&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=8
    @api.model
    def create(self, vals):
        # overriding the create method to add the sequence
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result

    # How to Override the Write Method in Odoo
    # https://www.youtube.com/watch?v=v8sXFUi1SH4&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=50
    # @api.multi
    def write(self, vals):
        # overriding the write method of appointment model
        res = super(HospitalAppointment, self).write(vals)
        print("Test write function")
        # do as per the need
        return res

    # Give Domain For A field dynamically in Onchange
    # How To Give Domain For A Field Based On Another Field
    # https://www.youtube.com/watch?v=IpXXYCsK2ow&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=65
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        for rec in self:
            return {'domain': {'order_id': [('partner_id', '=', rec.partner_id.id)]}}

    @api.model
    def default_get(self, fields):
        res = super(HospitalAppointment, self).default_get(fields)
        print("test......")
        res['patient_id'] = 1
        res['notes'] = 'Tuna Object'
        return res

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'), tracking=True)
    patient_id = fields.Many2one(
        'hospital.patient',
        string='Patient',
        required=True,)
    doctor_id = fields.Many2one('hospital.doctor', string='Doctor')
    patient_age = fields.Integer('Age', related='patient_id.patient_age')
    notes = fields.Text(string="Registration Note")
    doctor_note = fields.Text(string="Note", track_visibility='onchange')
    # How to Create One2Many Field
    # https://www.youtube.com/watch?v=_O_tNBdg3HQ&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=34

    appointment_lines = fields.One2many(
        'hospital.appointment.lines',
        'appointment_id',
        string='Appointment Lines')

    pharmacy_note = fields.Text(string="Note", track_visibility='always')
    appointment_date = fields.Date(string='Date')
    appointment_datetime = fields.Datetime(string='Date Time')
    partner_id = fields.Many2one('res.partner', string="Customer")
    order_id = fields.Many2one('sale.order', string="Sale Order")
    amount = fields.Float(string="Total Amount")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')


class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')
    display_type = fields.Selection([
        ('line_section', "Section"),
        ('line_note', "Note")], default=False, help="Technical field for UX purpose.")
