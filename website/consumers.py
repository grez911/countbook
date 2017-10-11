import json
from channels import Group
from .views import get_day, append_record, append_operation

def ws_message(message):
    request = json.loads(message.content['text'])
    if request['operation'] == 'append_record':
        append_record(request['params']['id'])
        Group('countbook').send({
            'text': get_day()
        })
    elif request['operation'] == 'get_day':
        request = json.loads(message.content['text'])
        year = request['params']['year']
        month = request['params']['month']
        day = request['params']['day']
        Group('countbook').send({
            'text': get_day(year, month, day)
        })
    elif request['operation'] == 'append_operation':
        append_operation(request['params']['name'])
        Group('countbook').send({
            'text': get_day()
        })

def ws_connect(message):
    message.reply_channel.send({'accept': True})
    Group('countbook').add(message.reply_channel)

def ws_disconnect(message):
    Group('countbook').discard(message.reply_channel)
