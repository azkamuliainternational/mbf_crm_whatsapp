# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import requests
from email import encoders
from email.charset import Charset
from email.header import Header
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formataddr, formatdate, getaddresses, make_msgid
import logging
import re
import smtplib
import json
import threading
import time
import uuid
import qrcode
import base64
import io
from ..klikapi import KlikApi

from datetime import datetime

# import html2text

from odoo import api, fields, models, tools, _, sql_db
from odoo.exceptions import except_orm, UserError,ValidationError
from odoo.tools import ustr, pycompat

_logger = logging.getLogger(__name__)

SMTP_TIMEOUT = 60


class WaKlikodoo(models.TransientModel):
    _name = "wa.klikodoo.popup"
    _description = "Wa Klikodoo"
    
    qr_scan = fields.Binary("QR Scan")
    # qr_text = fields.Text(string="Kode QR Code")
    

class IrWhatsappServer(models.Model):
    """Represents an SMTP server, able to send outgoing emails, with SSL and TLS capabilities."""
    _name = "ir.whatsapp_server"
    _description = 'Whatsapp Server'

    name = fields.Char(string='Description', index=True)
    sequence = fields.Integer(string='Priority', default=10, help="When no specific mail server is requested for a mail, the highest priority one "
                                                                  "is used. Default priority is 10 (smaller number = higher priority)")
    active = fields.Boolean(default=True)
    klik_key = fields.Char("KlikApi Key", help="Optional key for SMTP authentication")
    klik_secret = fields.Char("KlikApi Secret", help="Optional secret for SMTP authentication")
    uuid = fields.Char("UUID", default=lambda self: str(uuid.uuid4()), readonly=True, required=True)
    url_server_whatapps = fields.Char("Server Whatsapp", required=True)
    api_secret = fields.Char("Api Secret",required=True)
    device_key=fields.Char("Device Key")
    qr_scan = fields.Binary("QR Scan", readonly=True)
    whatsapp_number = fields.Char('Whatsapp Number',required=True)
    status = fields.Selection([('create','Create Device'),
                               ('init', 'Init QR Code'),
                               ('got qr code', 'QR Code'),
                               ('authenticated', 'Authenticated')], default='init', string="Status")
    hint = fields.Char(string='Hint', readonly=True, default="Configure Token and Instance")
    # message_ids = fields.One2many('mail.message', 'whatsapp_server_id', string="Mail Message")    
    # message_counts = fields.Integer('Message Sent Counts', compute='_get_mail_message_whatsapp')
    # message_response = fields.Text('Message Response', compute='_get_mail_message_whatsapp')
    message_counts = fields.Integer('Message Sent Counts',default=0)
    message_response = fields.Text('Keterangan',default="")
    
    notes = fields.Text(readonly=True)
    

        
   
    def klikapi(self):
        self.ensure_one()
        return KlikApi(self.url_server_whatapps,self.api_secret,self.uuid,self.device_key)
    # MBF add
    def cek_koneksi(self):      
        KlikApi = self.klikapi()
        r1=KlikApi.get_api("cek_koneksi")
        _logger.warning('********** {} **************'.format(r1.json()))
        if (r1.json()["success"]==True):          
            self.message_response=r1.json()["message"]   
            self.status='authenticated'  
            self.qr_scan=''       
        else:
            raise UserError(r1.text)  
            self.status='create' 

    def create_device(self):
        KlikApi = self.klikapi()        
        data = {
            'jid':"6285204421100@s.whatsapp.net",
            'message':  { "text": "What's that @6285xxxxxx?" }     
        }
        r1=KlikApi.post_delete_api("create_device",data)
        _logger.warning('********** {} **************'.format(r1.json()))
        # if (r1.json()["ok"]==True):
        #     self.message_response="Device Berhasil Ditambahkan"
        #     self.uuid=r1.json()['data']['uuid']
        #     self.name=r1.json()['data']['name']
        #     self.device_key=r1.json()['data']["key"]            
        # else:    
        #     raise UserError(r1.text)  

    def test_send_message(self):
        KlikApi = self.klikapi() 
        data = {
  "chatId": "6285204421100@c.us",
  "contentType": "string",
  "content": "ini ada test whatsapp dari Odoo "
}
        r=KlikApi.post_delete_api("send_message",data)
        _logger.warning('********** {} **************'.format(r.json()))
        # self.message_response=r.text
        # if (r.json()["ok"]==True):
        #     self.message_response="Test Kirim WhatsApp ke no Sendiri"  
        #     return {
		# 'effect': {
		# 	'fadeout': 'slow',
		# 	'message': 'Whatsapp Telah Terkirim',
		# 	'type': 'rainbow_man',
		# }  }
        # else:
        #     raise UserError(r.json()["errors"])  

    def logout(self):
        KlikApi = self.klikapi()        
        r=KlikApi.get_api("logout")
        
        if (r.json()["success"]==True):            
            self.message_response="Odoo Tidak Tersambung Ke Server Whatsapp"        
            self.qr_scan=False
            self.status='init'
        else:    
            raise UserError(r.text)
            # raise UserError(r.text)

    def scan_init(self):
        KlikApi = self.klikapi()
        r1=KlikApi.get_api("scan_init")
        if (r1.json()['success']==True):
            self.message_response='{},{}'.format(r1.json()['message'],"Silakan Tekan Scan QR Code, Expired Scan 34 detik ")            
            self.qr_scan=False
            self.status='init'  
        else:
            raise UserError(r1.text)
                     
    def generate_qr_code(self, data):
        qr_img = qrcode.make(data)
        buf = io.BytesIO()
        qr_img.save(buf, format='PNG')
        buf.seek(0)
        self.qr_scan = base64.b64encode(buf.read())    
            
    def scan_qr_code(self):
        KlikApi = self.klikapi()
        r2=KlikApi.get_api("scan_qr_code")
        if (r2.json()["success"]==True):                
            self.message_response="1.Buka Whatsapp\n2.Tambahkan linked devices Whatsapp\n3.Scan QR Code\nJika Sudah Berhasil Check Connection"
            # qr_code=r2.json()["data"]["qrcode"].replace("data:image/png;base64,","")
            # qr_code=r2.json()["qr"]
            # self.qr_scan=qr_code 
            self.generate_qr_code(r2.json()["qr"])
            self.status='got qr code'   
         
        else:
            raise UserError(r2.text)    
   

    # def get_status(self):
    #     APIUrl='https://wajoss.fikrihost.my.id/v1/'        
    #     r=requests.get(APIUrl+'device/'+self.uuid, headers={'Content-Type': 'application/json','Authorization':self.api_secret})
    #     self.message_response=r.text
    #     if (r.json()["ok"]==True): 
    #         self.qr_scan=False
    #         self.status='authenticated'   
    #         self.device_key=r.json()["data"]["key"]
    #     else:   
    #         raise UserError(r.json()["errors"])

    # MBF end add
    