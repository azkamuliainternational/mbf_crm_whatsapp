# models/res_partner.py

from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    whatsapp_message_ids = fields.One2many(
        'whatsapp.message', 'partner_id', string='WhatsApp Messages'
    )
