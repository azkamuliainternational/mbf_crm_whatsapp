# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _, sql_db
from odoo.exceptions import UserError, ValidationError
import requests
import json
import re
import time
import logging
from ..klikapi import KlikApi

_logger = logging.getLogger(__name__)

def format_rupiah(amount):
        return "Rp {:,}".format(int(amount)).replace(",", ".")
class CrmLead(models.Model):
    """Inherit Partner."""
    _inherit = "crm.lead"
    
    whatsapp_message_ids = fields.One2many(
        'whatsapp.message',
        'lead_id',
        string='WhatsApp Messages'
    )

    # whatsapp_message_ids = fields.One2many(
    #     'whatsapp.message', 'partner_id',
    #     string='WhatsApp Messages (From Partner)',
    #     compute='_compute_whatsapp_message_ids',
    #     store=False  # optional; not stored
    # )

    whatsapp = fields.Char('Whatsapp',  readonly=False, store=True)
    whatsapp_active=fields.Boolean('WhatsApp Active',default=False)
    def send_whatsapp(self):
        if self.whatsapp_active: 
      
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
        else :
            raise UserError("Whatsapp Belum Aktif") 
     
    # def _compute_whatsapp_message_ids(self):
    #     for lead in self:
    #         lead.whatsapp_message_ids = lead.partner_id.whatsapp_message_ids        

    # @api.constrains('whatsapp')
    # def _validate_mobile(self):
    #     for rec in self:            
    #         if not rec.whatsapp.isdigit():
    #             raise ValidationError(_("Invalid whatsapp number."))
    @api.constrains('whatsapp')
    def _validate_mobile(self):
        for rec in self:
            number = rec.whatsapp.strip().replace(" ", "")

            if not number.isdigit():
                raise ValidationError(_("Invalid WhatsApp number. Only digits are allowed."))

            # Normalize to 62 format
            normalized = '62' + number[1:] if number.startswith('0') else number
            phone = re.sub(r'^62', '0', number)

              # Search for other records with same normalized number
            exists = self.env['crm.lead'].search([ ('id', '!=', rec.id),'|',
                ('whatsapp', '=', phone),('whatsapp', '=', normalized)
            ])
            # _logger.warning('********** {} **************'.format(exists))
            # _logger.warning('**********rec.whatsapp {} **************'.format(rec.whatsapp))
            # _logger.warning('********** {} **************'.format(normalized))
            # _logger.warning('********** {} **************'.format(phone))
            if exists:                
                raise ValidationError(_("WhatsApp %s Sudah Terpakai di Lead: %s") % (number, exists.name))
            
    def klikapi(self):
        WhatsappServer = self.env['ir.whatsapp_server']
        whatsapp_ids = WhatsappServer.sudo().search([])        
        return KlikApi(whatsapp_ids[0]['url_server_whatapps'],whatsapp_ids[0]['api_secret'],whatsapp_ids[0]['uuid'],whatsapp_ids[0]['device_key'])

          
  
    # @api.model
    # def create(self):
    #     self.test_send_message()
    @api.model
    def create(self, vals):
        record = super().create(vals)
        _logger.warning('********** {} **************'.format(record.name))
        self.test_send_message(record.name,record.user_id.name,record.partner_id.name,record.planned_revenue)
        return record


   


    def test_send_message(self,name,user,customer,revenue):
        KlikApi = self.klikapi() 
        message = (
        f"*Lead Baru*\n"
        f"_{name}_\n"        
        f"Sales : {user}\n"
        f"Customer : {customer}\n"
        f"Estimasi: {format_rupiah(revenue)}"
    )
    
        data = {
        "chatId": "6285204421100@c.us",
        "contentType": "string",
        "content": message
    }
        r=KlikApi.post_delete_api("send_message",data)
        _logger.warning('********** {} **************'.format(r.json()))
        