from channels import Group
from .views import get

def ws_message(message):
    Group("chat").send({
        "text": get(message.content['text']),
    })

def ws_connect(message):
    message.reply_channel.send({"accept": True})
    Group("chat").add(message.reply_channel)

def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)
