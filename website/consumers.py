import json
from channels import Group
from .views import *

def ws_message(message):
    request = json.loads(message.content['text'])
    if request['type'] == 'append_record':
        append_record(request['params']['id'])
        Group('general').send({
            'text': get_day()
        })
    elif request['type'] == 'get_day':
        year = request['params']['year']
        month = request['params']['month']
        day = request['params']['day']
        Group('general').send({
            'text': get_day(year, month, day)
        })
    elif request['type'] == 'append_operation':
        append_operation(request['params']['name'])
        Group('general').send({
            'text': get_day()
        })
    elif request['type'] == 'get_month':
        year = request['params']['year']
        month = request['params']['month']
        message.reply_channel.send({
            'text': get_month(year, month)
        })
    elif request['type'] == 'del_operation':
        del_operation(request['params']['id'])
        Group('general').send({
            'text': get_day()
        })

def ws_connect(message):
    message.reply_channel.send({'accept': True})
    Group('general').add(message.reply_channel)

def ws_disconnect(message):
    Group('general').discard(message.reply_channel)
