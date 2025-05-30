# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _, sql_db
from odoo.exceptions import UserError, ValidationError
import requests
import json
import re
import time
import logging

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    """Inherit Partner."""
    _inherit = "crm.lead"
    
    whatsapp = fields.Char('Whatsapp',  readonly=False, store=True)
    def send_whatsapp(self):
        if self.whatsapp:
            return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.compose.message',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_user_id': self.id},
        }
        else:
            raise ValidationError(("Nomor Whatsapp belum Terinput!!."))
            

    @api.constrains('whatsapp')
    def _validate_mobile(self):
        for rec in self:            
            if not rec.whatsapp.isdigit():
                raise ValidationError(_("Invalid whatsapp number."))
   