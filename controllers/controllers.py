# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import http
from odoo.http import request
import logging
import json
_logger = logging.getLogger(__name__)

class whataspp_webhook(http.Controller):
    @http.route('/whatsapp', type='json', auth='none', methods=['POST'],csrf=False)
    def get_webhook_url(self, **post):
        print('received webhook data')
        data = json.loads(request.httprequest.data)
        if data["type"]=='message':
            
            nomerhp=data['body']['key']['remoteJid'].replace('@s.whatsapp.net','')
            pesan=data['body']['message']['conversation']
            _logger.info('CONNECTION SUCCESSFUL!!')                     
            _logger.info('\n**********\nNomer HP :{}\n**********'.format(nomerhp))
            _logger.info('\n**********\nPesan :{}\n**********'.format(pesan))
            crm_lead=request.env['crm.lead'].sudo().search([
            '|',('whatsapp', '=', nomerhp),('whatsapp', '=', nomerhp.replace('62','0',1))],  limit=1)
            if crm_lead[0]:
                values = {
                'date':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'body':'<div class="container"><img src="/mbf_crm_whatsapp/static/src/img/wa.png" style="width:32px;height:32px;" alt="Whatsapp Icon" ></img> <div class="message-orange"> <p class="message-content">{}</p></div></div>'.format(pesan),
                'model':'crm.lead',
                'res_id':crm_lead[0].id,
                'record_name':'confirm',
                'message_type':'email',
                'email_from':'odoobot@example.com',
                'author_id':2,                      
                }
                _logger.info('\n**********\nData :{}\n**********'.format((values)))
                mailmessage = request.env['mail.message'].sudo().create(values)




