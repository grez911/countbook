import json
from channels import Group
from .views import get_today, append_record

def ws_message(message):
    request = json.loads(message.content['text'])
    if request['operation'] == 'append_record':
        append_record(request['params']['id'])
        Group('chat').send({
            'text': get_today(),
        })
    elif request['operation'] == 'get_today':
        Group("chat").send({
            "text": get_today(),
        })

def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group("chat").add(message.reply_channel)

def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
