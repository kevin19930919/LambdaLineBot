from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import LineBotApiError, InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import requests, traceback, json, sys, os


channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)    

def compose_textReplyMessage(userId, messageText):
    return TextSendMessage(text='Please wait %s！' % messageText)

@handler.add(MessageEvent, message=TextMessage)    
def handle_text_message(event):
    userId = event.source.user_id
    messageText = event.message.text
    line_bot_api.reply_message(event.reply_token, compose_textReplyMessage(userId, messageText))

def lambda_handler(event, context):
    try:
        signature = event['headers']['x-line-signature']
        body = event['body']        
        handler.handle(body, signature)
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps('server error') }
    return {
        'statusCode': 200,
        'body': json.dumps('OK') }