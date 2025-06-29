# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import http
from odoo.http import request
import logging
import json
import re
_logger = logging.getLogger(__name__)

class whataspp_webhook(http.Controller):
    @http.route('/whatsapp', type='json', auth='none', methods=['POST'],csrf=False)
    def get_webhook_url(self, **post):
        def to_local_number(wanumber):
            match = re.match(r'62(\d+)@c\.us', wanumber)
            return '0' + match.group(1) if match else None
      


        try:
            data = json.loads(request.httprequest.data)            
          
            # or (data["dataType"]=='message_create')
            
            


            if (data["dataType"] in ('message_create','media')) :
                
                _logger.info('webhook data: %s', data)
                message_data = data['data']['message']
                from_me = message_data.get('fromMe')
                from_user = message_data.get('from')
                to_user = message_data.get('to')
                timestamp = message_data.get('timestamp')
                body = message_data.get('body')
                tipe = message_data.get('type')
                _logger.info("datatype: {}".format(data["dataType"]))
                _logger.info("from_me: {}".format(from_me))
                
                from_phone = to_local_number(from_user)
                to_phone = to_local_number(to_user)
                # caption =''
                # if (tipe=='image'):
                #     body = message_data['_data'].get('body')
                #     caption = message_data['_data'].get('caption')
                # else :
                #     caption = message_data.get('tipe')
                    
                
                domain = ['&', 
    ('whatsapp_active', '=', True),
    '|',
        '|',
            ('whatsapp', '=', from_phone),
            ('whatsapp', '=', re.sub(r'^0', '62', from_phone)),
        '|',
            ('whatsapp', '=', to_phone),
            ('whatsapp', '=', re.sub(r'^0', '62', to_phone))
]

                # domain = ['&', ('whatsapp_active', '=', True), '|', 
                #           ('whatsapp', '=', from_phone),('whatsapp', '=', re.sub(r'^0', '62',from_phone)), 
                #           ('whatsapp', '=', to_phone),('whatsapp', '=', re.sub(r'^0', '62',to_phone))]
                _logger.info('from Phone: %s', from_phone)
                _logger.info('to Phone: %s', to_phone)
                _logger.info('body: %s', body)
                _logger.info('tipe: %s', tipe)
                # _logger.info('caption: %s', caption)

                lead_crm = request.env['crm.lead'].sudo().search(domain, limit=1)
              
                
    #             lead_crm_id = request.env['crm.lead'].sudo().search(
    # [('whatsapp', '=', '0' + re.match(r'62(\d+)@c\.us', from_user).group(1)) or ('whatsapp', '=', '0' + re.match(r'62(\d+)@c\.us', to_user).group(1))    and ('whatsapp_active', '=', True)   ],
    # limit=1
    #        )    
                _logger.info("from_user :{} / to_user :{}".format(from_user,to_user))              
              
                if (lead_crm)  :  
                    _logger.info(' crm')
#                     cek_send_odoo=request.env['whatsapp.message'].sudo().search_count([
#     ('tipe', '=', 'odoo')
# ])          
#                     _logger.info('cek kiriman dari odoo: %s', cek_send_odoo)
#                     if  cek_send_odoo==0 :
                    if tipe=='chat' :
                        _logger.info('tipe chat')
                        
                        
                        
                    # if not (tipe=='image' and not from_me):
                        request.env['whatsapp.message'].sudo().create({
                'lead_id': lead_crm.id,
                'body': body,
                'date': datetime.now(),
                'timestamp': timestamp,
                'from_user': from_user,
                'to_user': to_user,
                'from_me':from_me,
                'tipe':tipe,
                'caption':'',               
                
            })
                        
                    if ((tipe=='document') and (data["dataType"]=='message_create') ):
                        _logger.info('tipe document')
                        body = 'Tipe file Document'
                        caption = message_data['_data'].get('caption')     
                        _logger.info("lead_id: {},body: {},date: {},timestamp: {},from_user: {},to_user: {},from_me:{},tipe:{},caption:{},".format(lead_crm.id,body,datetime.now(),timestamp,from_user,to_user,from_me,tipe,caption))     

                        
                        request.env['whatsapp.message'].sudo().create({
                'lead_id': lead_crm.id,
                'body': body,
                'date': datetime.now(),
                'timestamp': timestamp,
                'from_user': from_user,
                'to_user': to_user,
                'from_me':from_me,
                'tipe':tipe,
                'caption':caption,  
                             })   
                             
                    if ((tipe=='image') and (data["dataType"]=='message_create') and from_me) :
                         
                        _logger.info('tipe image dan data tipe message_create')
                        body = message_data['_data'].get('body')
                        caption = message_data['_data'].get('caption')        

                        
                        request.env['whatsapp.message'].sudo().create({
                'lead_id': lead_crm.id,
                'body': body,
                'date': datetime.now(),
                'timestamp': timestamp,
                'from_user': from_user,
                'to_user': to_user,
                'from_me':from_me,
                'tipe':tipe,
                'caption':caption,  
                             })   
                    
                        
                    if ((tipe=='image') and (data["dataType"]=='media')) :
                # _logger.info('webhook data: %s', data)
                        _logger.info('tipe image dan data tipe media')
                        image_data = data['data']['messageMedia']
                        image = image_data.get('data')
                        _logger.info('image data: %s', image)
                
                        message_data = data['data']['message']['_data']
                        from_me = message_data.get('fromMe')
                        from_user = message_data.get('from')
                        to_user = message_data.get('to')
                        timestamp = message_data.get('mediaKeyTimestamp')
                        body = message_data.get('body')
                        tipe = message_data.get('type')
                        caption =  message_data.get('caption')

                        from_phone = to_local_number(from_user)
                        to_phone = to_local_number(to_user)
                        _logger.info('data Image: %s', image)
                        _logger.info('from Phone: %s', from_phone)
                        _logger.info('to Phone: %s', to_phone)
                
            #             domain = ['&', 
            # ('whatsapp_active', '=', True),
            # '|',
            #     '|',
            #         ('whatsapp', '=', from_phone),
            #         ('whatsapp', '=', re.sub(r'^0', '62', from_phone)),
            #     '|',
            #         ('whatsapp', '=', to_phone),
            #         ('whatsapp', '=', re.sub(r'^0', '62', to_phone))

            #             ]

            #             lead_crm = request.env['crm.lead'].sudo().search(domain, limit=1)


            #             _logger.info("from_user :{} / to_user :{}".format(from_user,to_user))              

            #             if lead_crm :  
            #                 if (data["dataType"]=='media') :
                        request.env['whatsapp.message'].sudo().create({
                        'lead_id': lead_crm.id,
                        'body': image,
                        'date': datetime.now(),
                        'timestamp': timestamp,
                        'from_user': from_user,
                        'to_user': to_user,
                        'from_me':from_me,
                        'tipe':tipe,   
                         'caption':caption,             

                    })
               
        except Exception as e:
            _logger.error('Error parsing webhook data: %s', str(e))
            return {'status': 'error', 'message': 'Invalid JSON'}

        # You can now process `data` as needed, e.g., store in DB
        return {'status': 'ok'}
      
        # if data["type"]=='message':
            
        #     nomerhp=data['body']['key']['remoteJid'].replace('@s.whatsapp.net','')
        #     pesan=data['body']['message']['conversation']
        #     _logger.info('CONNECTION SUCCESSFUL!!')                     
        #     _logger.info('\n**********\nNomer HP :{}\n**********'.format(nomerhp))
        #     _logger.info('\n**********\nPesan :{}\n**********'.format(pesan))
        #     crm_lead=request.env['crm.lead'].sudo().search([
        #     '|',('whatsapp', '=', nomerhp),('whatsapp', '=', nomerhp.replace('62','0',1))],  limit=1)
        #     if crm_lead[0]:
        #         values = {
        #         'date':datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        #         'body':'<div class="container"><img src="/mbf_crm_whatsapp/static/src/img/wa.png" style="width:32px;height:32px;" alt="Whatsapp Icon" ></img> <div class="message-orange"> <p class="message-content">{}</p></div></div>'.format(pesan),
        #         'model':'crm.lead',
        #         'res_id':crm_lead[0].id,
        #         'record_name':'confirm',
        #         'message_type':'email',
        #         'email_from':'odoobot@example.com',
        #         'author_id':2,                      
        #         }
        #         _logger.info('\n**********\nData :{}\n**********'.format((values)))
        #         mailmessage = request.env['mail.message'].sudo().create(values)




