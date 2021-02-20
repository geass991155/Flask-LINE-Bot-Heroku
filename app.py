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
    elif text == 'class':
        Carousel_template = TemplateSendMessage(
            alt_text='師資',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/kCtPXcK.jpg',
                        title='張添香',
                        text='系主任',
                        actions=[
                            PostbackTemplateAction(
                                label='國立台灣科技大學',
                                text='國立台灣科技大學',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='工業管理系博士',
                                text='工業管理系博士'
                            ),
                            URITemplateAction(
                                label='thchang@nkust.edu.tw',
                                uri='https://mail.google.com/mail'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://imgur.com/7IdkwHy.jpg',
                        title='謝文川',
                        text='電子商務研究中心主任',
                        actions=[
                            PostbackTemplateAction(
                                label='國立交通大學',
                                text='國立交通大學',
                                data='action=buy&itemid=2'
                            ),
                            MessageTemplateAction(
                                label='資訊管理研究所博士',
                                text='資訊管理研究所博士'
                            ),
                            URITemplateAction(
                                label='wchsieh@nkust.edu.tw',
                                uri='https://mail.google.com/mail'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token,Carousel_template)
    elif text == '789':
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
