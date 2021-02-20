import os
from datetime import datetime

from flask import Flask, abort, request

# https://github.com/line/line-bot-sdk-python
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage,TemplateSendMessage,CarouselTemplate,
    ImageCarouselTemplate,ImageCarouselColumn,DatetimePickerAction,TextComponent,ButtonComponent,ButtonsTemplate,TemplateSendMessage,
    ImageMessage, VideoMessage, AudioMessage,CarouselTemplate,CarouselColumn,SeparatorComponent,ConfirmTemplate,
    PostbackAction,MessageAction,URIAction,BubbleContainer,ImageComponent,BoxComponent,FlexSendMessage,PostbackTemplateAction,
    TemplateSendMessage,CarouselColumn,CarouselTemplate,PostbackTemplateAction,MessageTemplateAction,URITemplateAction
)

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ.get("CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.environ.get("CHANNEL_SECRET"))


@app.route("/", methods=["GET", "POST"])
def callback():

    if request.method == "GET":
        return "Hello Heroku"
    if request.method == "POST":
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            abort(400)

        return "OK"


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    if text =='try':
        texts = '123'
    elif text == '蔬果品項':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://i.imgur.com/ItFGIvU.jpg',
                                action=URIAction(label='小番茄',
                                uri='https://kknews.cc/zh-tw/health/pynb2xj.html',
                                )),
            ImageCarouselColumn(image_url='https://i.imgur.com/anKHYy9.jpg',
                                action=URIAction(label='木瓜',
                                uri='https://heho.com.tw/archives/60267',
                                ))
        ])
        template_message = TemplateSendMessage(
            alt_text='蔬果品項', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == '654':
        confirm_template = ConfirmTemplate(text='還在測試中，尚未開業', actions=[
            MessageAction(label='課綱', text='class'),
            MessageAction(label='Nkust ic', text='https://nkust-ic.ddns.net/wordpress'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    else :
        texts = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=texts))
