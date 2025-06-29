- dalam windows untuk melihat log
Get-Content d:/log_odoo.log -Wait -Tail 30
- start odoo di linux
sudo -su odoo12
/opt/odoo12/venv/bin/python3 /opt/odoo12/odoo-bin -c /etc/odoo/odoo12.conf
- server whatsapp menggunakan webwhatass js dimana menggunakan rest api tanpa database
server whatsapp :ws.azkamulia.com
- pengambilan data di webhook
controller {base_url}/whatsapp 

- history whatsapp adalah chat per lead dengan dibatasi percakapan pertama 
- table whatsapp message 
  lead_id = fields.Many2one('crm.lead', string='Lead')
    body = fields.Text('Message')
    date = fields.Datetime('Date')
    timestamp = fields.Char('Timestamp', required=True)
    from_user = fields.Char('Dari')
    to_user = fields.Char('Ke ')
    tipe = fields.Char('Type ')
    from_me = fields.Boolean('From Me', default=False)
