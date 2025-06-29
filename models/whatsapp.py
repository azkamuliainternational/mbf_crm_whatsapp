from odoo import models, fields, api

class WhatsAppChat(models.Model):
    _name = 'whatsapp.chat'
    _description = 'WhatsApp Chat'
    _sql_constraints = [
        ('session_chat_uniq', 'UNIQUE(session_id, chat_id)', 'Session + Chat ID must be unique!')
    ]

    session_id = fields.Char('Session ID', required=True, index=True)
    chat_id = fields.Char('Chat ID', required=True)
    archived = fields.Boolean()
    contact_primary_identity_key = fields.Binary('Contact Identity Key')
    conversation_timestamp = fields.Float()
    created_at = fields.Float('Created At')
    created_by = fields.Char('Created By')
    description = fields.Char('Description')
    disappearing_mode = fields.Text('Disappearing Mode')  # JSON data
    display_name = fields.Char('Display Name')
    end_of_history_transfer = fields.Boolean()
    end_of_history_transfer_type = fields.Integer()
    ephemeral_expiration = fields.Integer()
    ephemeral_setting_timestamp = fields.Float()
    is_default_subgroup = fields.Boolean('Default Subgroup')
    is_parent_group = fields.Boolean('Parent Group')
    last_msg_timestamp = fields.Float('Last Message Time')
    lid_jid = fields.Char('LID JID')
    marked_as_unread = fields.Boolean()
    media_visibility = fields.Integer()
    messages = fields.Text('Messages')  # JSON data
    mute_end_time = fields.Float('Mute End')
    name = fields.Char('Name')
    new_jid = fields.Char('New JID')
    not_spam = fields.Boolean('Not Spam')
    old_jid = fields.Char('Old JID')
    p_hash = fields.Char('pHash')
    parent_group_id = fields.Char('Parent Group ID')
    participant = fields.Text('Participant')  # JSON data
    pinned = fields.Float('Pinned Time')
    pn_jid = fields.Char('PN JID')
    pnh_duplicate_lid_thread = fields.Boolean()
    read_only = fields.Boolean('Read Only')
    share_own_pn = fields.Boolean('Share Own PN')
    support = fields.Boolean()
    suspended = fields.Boolean()
    tc_token = fields.Binary('TC Token')
    tc_token_sender_timestamp = fields.Float()
    tc_token_timestamp = fields.Float()
    terminated = fields.Boolean()
    unread_count = fields.Integer('Unread Count')
    unread_mention_count = fields.Integer('Unread Mentions')
    wallpaper = fields.Text('Wallpaper')  # JSON data
    last_message_recv_timestamp = fields.Integer('Last Message Received')
    comments_count = fields.Integer('Comments Count')

class WhatsAppContact(models.Model):
    _name = 'whatsapp.contact'
    _description = 'WhatsApp Contact'
    _sql_constraints = [
        ('session_contact_uniq', 'UNIQUE(session_id, contact_id)', 'Session + Contact ID must be unique!')
    ]

    session_id = fields.Char('Session ID', required=True, index=True)
    contact_id = fields.Char('Contact ID', required=True)
    name = fields.Char()
    notify = fields.Char('Notification Name')
    verified_name = fields.Char('Verified Name')
    img_url = fields.Char('Image URL')
    status = fields.Char('Status')

class WhatsAppGroupMetadata(models.Model):
    _name = 'whatsapp.group_metadata'
    _description = 'WhatsApp Group Metadata'
    _sql_constraints = [
        ('session_group_uniq', 'UNIQUE(session_id, group_id)', 'Session + Group ID must be unique!')
    ]

    session_id = fields.Char('Session ID', required=True, index=True)
    group_id = fields.Char('Group ID', required=True)
    owner = fields.Char('Owner JID')
    subject = fields.Char(required=True)
    subject_owner = fields.Char('Subject Owner')
    subject_time = fields.Integer('Subject Changed')
    creation = fields.Integer('Created At')
    desc = fields.Text('Description')
    desc_owner = fields.Char('Desc Owner')
    desc_id = fields.Char('Desc ID')
    restrict = fields.Boolean('Restricted')
    announce = fields.Boolean('Announce')
    is_community = fields.Boolean('Community')
    is_community_announce = fields.Boolean('Community Announce')
    join_approval_mode = fields.Boolean('Join Approval')
    member_add_mode = fields.Boolean('Member Add Mode')
    author = fields.Char('Author')
    size = fields.Integer('Group Size')
    participants = fields.Text('Participants')  # JSON data
    ephemeral_duration = fields.Integer('Ephemeral Duration')
    invite_code = fields.Char('Invite Code')

class WhatsAppMessage(models.Model):
    _name = 'whatsapp.message'
    _description = 'WhatsApp Message'
    _sql_constraints = [
        ('message_uniq', 'UNIQUE(session_id, remote_jid, message_id)', 'Message must be unique per session/chat!')
    ]

    session_id = fields.Char('Session ID', required=True, index=True)
    remote_jid = fields.Char('Remote JID', required=True)
    message_id = fields.Char('Message ID', required=True)
    agent_id = fields.Char('Agent ID')
    biz_privacy_status = fields.Integer('Biz Privacy')
    broadcast = fields.Boolean()
    clear_media = fields.Boolean()
    duration = fields.Integer()
    ephemeral_duration = fields.Integer('Ephemeral Duration')
    ephemeral_off_to_on = fields.Boolean('Ephemeral Enabled')
    ephemeral_out_of_sync = fields.Boolean('Ephemeral Out of Sync')
    ephemeral_start_timestamp = fields.Float('Ephemeral Start')
    final_live_location = fields.Text('Final Location')  # JSON
    futureproof_data = fields.Binary('Futureproof Data')
    ignore = fields.Boolean()
    keep_in_chat = fields.Text('Keep in Chat')  # JSON
    key = fields.Text('Key', required=True)  # JSON
    labels = fields.Text('Labels')  # JSON
    media_ciphertext_sha256 = fields.Binary('Media Hash')
    media_data = fields.Text('Media Data')  # JSON
    message = fields.Text('Message Content')  # JSON
    message_c2s_timestamp = fields.Float('Message C2S Time')
    message_secret = fields.Binary('Message Secret')
    message_stub_parameters = fields.Text('Stub Parameters')  # JSON
    message_stub_type = fields.Integer('Stub Type')
    message_timestamp = fields.Float('Message Time')
    multicast = fields.Boolean()
    original_self_author = fields.Char('Original Author')
    participant = fields.Char('Participant')
    payment_info = fields.Text('Payment Info')  # JSON
    photo_change = fields.Text('Photo Change')  # JSON
    poll_additional_metadata = fields.Text('Poll Metadata')  # JSON
    poll_updates = fields.Text('Poll Updates')  # JSON
    push_name = fields.Char('Push Name')
    quoted_payment_info = fields.Text('Quoted Payment')  # JSON
    quoted_sticker_data = fields.Text('Quoted Sticker')  # JSON
    reactions = fields.Text('Reactions')  # JSON
    revoke_message_timestamp = fields.Float('Revoke Time')
    starred = fields.Boolean()
    status = fields.Integer()
    status_already_viewed = fields.Boolean('Status Viewed')
    status_psa = fields.Text('Status PSA')  # JSON
    url_number = fields.Boolean('Has URL Number')
    url_text = fields.Boolean('Has URL Text')
    user_receipt = fields.Text('User Receipt')  # JSON
    verified_biz_name = fields.Char('Verified Biz')
    event_responses = fields.Text('Event Responses')  # JSON
    pin_in_chat = fields.Text('Pin in Chat')  # JSON
    reporting_token_info = fields.Text('Reporting Token')  # JSON

class WhatsAppSession(models.Model):
    _name = 'whatsapp.session'
    _description = 'WhatsApp Session'
    _sql_constraints = [
        ('session_key_uniq', 'UNIQUE(session_id, session_key)', 'Session key must be unique!')
    ]

    session_id = fields.Char('Session ID', required=True, index=True)
    session_key = fields.Char('Session Key', required=True)
    data = fields.Text('Session Data', required=True)