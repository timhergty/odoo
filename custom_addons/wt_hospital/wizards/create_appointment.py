from odoo import models, fields


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'
    _description = 'Create Appointment Wizard'

    patient_id = fields.Many2one('hospital.patient', string="Patient")
    appointment_date = fields.Date(string="Appointment Date")

    def print_report(self):
        data = {
            'model': 'create.appointment',
            'form': self.read()[0]
        }

        return self.env.ref('wt_hospital.report_appointment').with_context(landscape=True).report_action(self,
                                                                                                         data=data)

    def delete_patient(self):
        for rec in self:
            rec.patient_id.unlink()

    # Create Record From Code
    # https://www.youtube.com/watch?v=Jssb15ADeyg&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=40
    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Created From The Wizard/Code'
        }
        # adding a message to the chatter from code
        # https://www.youtube.com/watch?v=J3MvgwHnR0A&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=48
        self.patient_id.message_post(body="Test string ", subject="Appointment Creation")
        # creating appointments from the code
        new_appointment = self.env['hospital.appointment'].create(vals)
        context = dict(self.env.context)
        import logging
        _logger = logging.getLogger(__name__)
        _logger.info("account.py cornerstone_account calling")
        context['form_view_initial_mode'] = 'edit'
        return {'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'hospital.appointment',
                'res_id': new_appointment.id,
                'context': context
                }

    # Fetching/ Taking Data From Database Tables
    # https://www.youtube.com/watch?v=hUPSvL8GTQE&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=49
    def get_data(self):
        appointments = self.env['hospital.appointment'].search([])
        for rec in appointments:
            print("Appointment Name", rec.name)
        # How to Prevent Wizard Getting Closed After Button Click
        # https://www.youtube.com/watch?v=n5La3aTue7o&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=68
        return {
            "type": "ir.actions.do_nothing"
        }
