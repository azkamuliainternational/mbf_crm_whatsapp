from odoo import _
from odoo.exceptions import Warning, UserError
from odoo.http import request, Response
import json
import requests
import datetime
import logging



_logger = logging.getLogger(__name__)

class KlikApi(object):
    def __init__(self,api_secret,uuid,device_key):
        APIUrl = request.env['ir.config_parameter'].sudo().get_param('mbf_crm_whatsapp.url_wajoss_server')
        self.APIUrl =APIUrl
        self.api_secret = api_secret
        self.uuid = uuid 
        self.device_key=device_key

    def get_api(self,tipe):

        try:
            Header={'Content-Type': 'application/json','Authorization':self.api_secret}
            if  (tipe=="cek_koneksi") :
                r=requests.get('{}device'.format(self.APIUrl), headers=Header)
            elif (tipe=="scan_init")  :    
                r=requests.get('{}device/{}/init'.format(self.APIUrl,self.uuid), headers=Header)
            elif (tipe=="scan_qr_code")  :    
                _logger.warning('********** {} **************'.format('{}device/{}/scan'.format(self.APIUrl,self.uuid)))
                r=requests.get('{}device/{}/scan'.format(self.APIUrl,self.uuid), headers=Header)
               
            _logger.warning('response get_api: {r.text}')
            return r
        except (requests.exceptions.HTTPError,
                requests.exceptions.RequestException,
                requests.exceptions.ConnectionError) as err:
            raise Warning(_('Error! Could not connect to Whatsapp account. %s')% (err))
        
    def post_delete_api(self,tipe,data):

        try:
            data_body = json.dumps(data)
            Header={'Content-Type': 'application/json','Authorization':self.api_secret}
            if  (tipe=="logout") :
                r=requests.delete('{}device/{}/logout'.format(self.APIUrl,self.uuid), headers=Header,data=data_body)
            elif (tipe=="create_device") :
                r=requests.post('{}device'.format(self.APIUrl), headers=Header,data=data_body)
            elif (tipe=="send_message"):
                _logger.warning('\n\n{}message/send-text'.format(self.APIUrl))
                _logger.warning('{}'.format(Header))
                _logger.warning('{}\n\n'.format(data_body))
                r=requests.post('{}message/send-text'.format(self.APIUrl), headers=Header,data=data_body)
                  
            return r
        except (requests.exceptions.HTTPError,
                requests.exceptions.RequestException,
                requests.exceptions.ConnectionError) as err:
            raise Warning(_('Error! Could not connect to Whatsapp account. %s')% (err))

    # def logout(self):
    #     url = self.APIUrl + 'logout'
    #     data = {}
    #     data['instance'] = self.klik_key
    #     data['key'] = self.klik_secret
    #     #get_version = request.env["ir.module.module"].sudo().search([('name','=','base')], limit=1)
    #     #data['get_version'] = get_version and get_version.latest_version
    #     data_s = {
    #         'params' : data
    #     }
    #     req = requests.post(url, json=data_s, headers={'Content-Type': 'application/json'})
    #     res = json.loads(req.text)
    #     return res['result']
    
    # def get_count(self):
    #     data = {}
    #     url = self.APIUrl + 'count/' + self.klik_key +'/' + self.klik_secret
    #     data_req = requests.get(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    #     res = json.loads(data_req.text)
    #     #print ('===res===',res)
    #     return res.get('result') and res['result'] or {}
    
    # def get_limit(self):
    #     data = {}
    #     url = self.APIUrl + 'limit/' + self.klik_key +'/' + self.klik_secret
    #     data_req = requests.get(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    #     res = json.loads(data_req.text)
    #     #print ('===res===',res)
    #     return res.get('result') and res['result'] or {}
    
    # def get_request(self, method, data):
    #     url = self.APIUrl + 'get/' + self.klik_key +'/' + self.klik_secret + '/' + method
    #     data_req = requests.get(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    #     res = json.loads(data_req.text)
    #     return res.get('result') and res['result'] or {}
    
    # def post_request(self, method, data):
    #     url = self.APIUrl + 'post/'
    #     data= json.loads(data)
    #     data['instance'] = self.klik_key
    #     data['key'] = self.klik_secret
    #     data['method'] = method
    #     #get_version = request.env["ir.module.module"].sudo().search([('name','=','base')], limit=1)
    #     #data['get_version'] = get_version and get_version.latest_version
    #     data_s = {
    #         'params' : data
    #     }
    #     response = requests.post(url, json=data_s, headers={'Content-Type': 'application/json'})
    #     if response.status_code == 200:
    #         message1 = json.loads(response.text)
    #         message = message1.get('result').get('message')
    #         chatID = message.get('id') and message.get('id').split('_')[1]
    #         return {'chatID': chatID, 'message': message}
    #     else:
    #         return {'message': {'sent': False, 'message': 'Error'}}
    
    
    # def get_phone(self, method, phone):
    #     data = {}
    #     url = self.APIUrl + 'phone/' + self.klik_key + '/'+self.klik_secret +'/'+ method + '/' + phone
    #     data = requests.get(url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
    #     res = json.loads(data.text)
    #     return res.get('result') and res['result'] or {}