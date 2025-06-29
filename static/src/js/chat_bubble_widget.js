odoo.define('mbf_crm_whatsapp.chat_bubble_widget', function (require) {
    "use strict";

    var AbstractField = require('web.AbstractField');
    var fieldRegistry = require('web.field_registry');

    var ChatBubbleWidget = AbstractField.extend({
        supportedFieldTypes: ['one2many'],

        init: function () {
            this._super.apply(this, arguments);
        },

        _render: function () {
            var self = this;
            this.$el.empty();
        
            if (this.value.data && this.value.data.length > 0) {
                var ids = _.pluck(this.value.data, 'data').map(d => d.id);
                console.log('Fetching full records for IDs:', ids);
        
                this._rpc({
                    model: 'whatsapp.message',
                    method: 'read',
                    args: [ids, ['body', 'date','from_me','tipe','caption']],
                }).then(function (records) {
                    console.log('Fetched records:', records);
        
                    if (!records || records.length === 0) {
                        self.$el.append($('<p>No WhatsApp messages found.</p>'));
                        return;
                    }
        
                    _.each(records, function (record) {

                        
                        
                        var date = record.date || 'No date';
                        var tipe = record.tipe || 'No tipe';
                        if (tipe==='chat') {
                            var message = record.body.replace(/\n/g, '<br/>') || 'No message';
                        }
                        if (tipe === 'image') {
                            var message = `<img  style="width: 300px; height: 300px; object-fit: contain;" src="data:image/png;base64,${record.body}"> <br/> ${record.caption}`;
                        }
                        if (tipe === 'document') {
                            var message = `${record.body} <br/> ${record.caption}`;
                        }
                        
        
                        var formattedDate = moment(date).format('DD-MM-YYYY HH:mm:ss');

                        var isFromMe = record.from_me === true
                        
                        var bubbleClass = isFromMe ? 'left' : 'right';
                        var avatarImg = isFromMe
                            ? '/mbf_crm_whatsapp/static/src/img/cs.png'
                            : '/mbf_crm_whatsapp/static/src/img/customer.png';

                        var $bubble = $(`
                            <div class="chat-bubble ${bubbleClass}">
                                <div class="avatar">
                                    <img src="${avatarImg}" />
                                </div>


                                <div class="message">
                                    <div class="message-content"></div>
                                                         <br/>
                                    <span class="message-timestamp-${bubbleClass}">
                                        ${_.escape(formattedDate)}
                                    </span>
                                </div>
                            </div>
                        `);
                        $bubble.find('.message-content').html(message); 
                        self.$el.append($bubble);
                    });
                }).fail(function (error) {
                    console.error('RPC failed:', error);
                    self.$el.append($('<p>Error loading messages.</p>'));
                });
            } else {
                this.$el.append($('<p>No WhatsApp messages.</p>'));
            }
        }
        
        

        
    });

    fieldRegistry.add('whatsapp_chat_bubble', ChatBubbleWidget);
});
