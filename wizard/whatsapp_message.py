# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, sql_db, _, tools
# from odoo.tools.misc import formatLang,  format_amount
from odoo.tools.mimetypes import guess_mimetype
from datetime import datetime
from odoo.tools import pycompat
from odoo.exceptions import UserError
from ..klikapi import KlikApi
import requests
import json
import ast
import base64
import threading
import time
import logging

_logger = logging.getLogger(__name__)


    
class WhatsappComposeMessage(models.TransientModel):
    _name = 'whatsapp.compose.message'
    _description = "Whatsapp Message"

  
        
    #invoice_ids = fields.Many2many('account.invoice', string='Invoice')
    partner_ids = fields.Many2many('res.partner', string='Contacts')
    crm_id=fields.Many2one('crm.lead', string='Lead CRM')
    whatsapp = fields.Char('Whatsapp', default='0')
    whatsapp_name = fields.Char('Nama Penerima', default='-')

    message = fields.Text()

    model = fields.Char('Object')

    partner_address_id = fields.Many2one('res.partner', string='Address')

    
    def klikapi(self):
        WhatsappServer = self.env['ir.whatsapp_server']
        whatsapp_ids = WhatsappServer.sudo().search([])
        
        return KlikApi(whatsapp_ids[0]['url_server_whatapps'],whatsapp_ids[0]['api_secret'],whatsapp_ids[0]['uuid'],whatsapp_ids[0]['device_key'])
    

    @api.model
    def default_get(self, fields):
        result = super(WhatsappComposeMessage, self).default_get(fields)
        context = dict(self._context or {})
        Attachment = self.env['ir.attachment']
        active_model = context.get('active_model')
        active_ids = context.get('active_ids')
        active_id = context.get('active_id')
        msg = result.get('message', '')
        result['message'] = msg      
        if active_model and active_ids and active_model == 'crm.lead':
            crm = self.env[active_model].browse(active_ids)
            _logger.info('**********{}**********'.format(crm[0].partner_id.name))
            result['whatsapp']=crm[0].whatsapp
            result['whatsapp_name']=crm[0].partner_id.name
            result['crm_id'] = crm[0].id
            _logger.info('**********{}**********'.format(crm[0].id))

      
        return result
    

    def kirim_wa(self):

      
            KlikApi = self.klikapi() 

            data = {            
                'chatId': '{}@c.us'.format("62" + self.whatsapp[1:] if self.whatsapp.startswith("0") else self.whatsapp),
                "contentType": "string",
                'content': self.message
            }
            r=KlikApi.post_delete_api("send_message",data)
            if r.json()['success']==True:    
                    return {
            'type': 'ir.actions.client',
            'tag': 'reload',
    }   

                #     self.env['whatsapp.message'].create({
                #     'lead_id': self.crm_id.id,
                #     'body': '{}'.format(self.message),
                #     'date': datetime.now(),
                #     'timestamp': r.json()['message']['timestamp'],
                #     'from_user': r.json()['message']['from'],
                #     'to_user': r.json()['message']['to'],
                #     'from_me':r.json()['message']['fromMe'],
                #     'tipe':'odoo',               

                # })
                    _logger.info('**********kiriman dari odooo**********')           
            else:
                raise UserError(r.json()["errors"])  
        #           if self.crm_id.whatsapp_active: 
        # else :
        #        raise UserError("Whatsapp Belum Aktif")        
                
#             comment_values = {
#                 #  'body':'test',
#                'body':  '<div class="container"><img src="/mbf_crm_whatsapp/static/src/img/wa.png" style="width:32px;height:32px;" alt="Whatsapp Icon" ></img> <div class="message-blue"> <p class="message-content">{}</p></div></div>'.format(self.message),
#                'model': 'crm.lead',  # Replace with your actual model name
#                'res_id': self.crm_id.id# Replace with the ID of the record in your.model
# }

#             # Add the comment to the mail.message record
#             message = self.env['mail.message'].search([('model', '=', 'crm.lead'), ('res_id', '=', self.crm_id.id)], limit=1)
#             new_comment = self.env['mail.message'].create(comment_values)
#             message.child_ids += new_comment
            
#             # Commit the changes to the database (optional if not using ORM methods)
#             self.env.cr.commit()

  
  

