import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(
    'qzUqHpkuZ50G9AHsAOPytR/RUjiV3FFbPHap/+PYXQDv6AqB+p6wLsxlCrTr7IjOdAiTWbI9ciJwqFjCGTyHObiToBqQLZNY6utZgN1sGxwEscvZvuCbDpm/au3l53LhDq7E+IYZ8WH+tCcSWR/H7wdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('91f633d3c73473b814457134fe12bd29')

# 監聽所有來自 /callback 的 Post Request


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
   line_bot_api.reply_message(  # 回復「選擇地區」按鈕樣板訊息
                        event.reply_token,
                        {
  "type": "text", // ①
  "text": "Select your favorite food category or send me your location!",
  "quickReply": { // ②
    "items": [
      {
        "type": "action", // ③
        "imageUrl": "https://example.com/sushi.png",
        "action": {
          "type": "message",
          "label": "Sushi",
          "text": "Sushi"
        }
      },
      {
        "type": "action",
        "imageUrl": "https://example.com/tempura.png",
        "action": {
          "type": "message",
          "label": "Tempura",
          "text": "Tempura"
        }
      },
      {
        "type": "action", // ④
        "action": {
          "type": "location",
          "label": "Send location"
        }
      }
    ]
  }
}
                    )
#  Image 給
#    message = TemplateSendMessage(
#        alt_text='ImageCarousel template',
#        template=ImageCarouselTemplate(
#            columns=[
#                ImageCarouselColumn(
#                    image_url='https://example.com/item1.jpg',
#                    action=PostbackTemplateAction(
#                        label='postback1',
#                        text='postback text1',
#                        data='action=buy&itemid=1'
#                    )
#                ),
#                ImageCarouselColumn(
#                    image_url='https://example.com/item2.jpg',
#                    action=PostbackTemplateAction(
#                        label='postback2',
#                        text='postback text2',
#                        data='action=buy&itemid=2'
#                    )
#                )
#            ]
#        )
#    )
#    line_bot_api.reply_message(event.reply_token, message)

#  你說什麼 BOT說什麼
# message = TextSendMessage(text=event.message.text)
#line_bot_api.reply_message(event.reply_token, message)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
