# models/whatsapp_message.py

from odoo import models, fields

class WhatsAppMessage(models.Model):
    _name = 'whatsapp.message'
    _description = 'WhatsApp Message'

    lead_id = fields.Many2one('crm.lead', string='Lead')
    body = fields.Text('Message')
    caption = fields.Text('Caption')
    date = fields.Datetime('Date')
    timestamp = fields.Char('Timestamp', required=True)
    from_user = fields.Char('Dari')
    to_user = fields.Char('Ke ')
    tipe = fields.Char('Type ')
    from_me = fields.Boolean('From Me', default=False)
    from_odoo=fields.Boolean('From Odoo', default=False)

    
    
    
