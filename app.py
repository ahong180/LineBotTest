import os
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

# googleExcel
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 日期
#import datetime
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
    # 開局
    text = event.message.text
    if text == '開局':
        InsertExcel('0', text)
        quickreplay(event)
    elif text[0:2] == '開局':
        InsertExcel('1', text)
        quickreplay(event)
    elif text == 'quickReplay':
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text='Quick reply',
                quick_reply=QuickReply(
                    items=[
                     QuickReplyButton(
                         action=PostbackAction(
                             label="label1", data="data1")
                     ),
                        QuickReplyButton(
                         action=MessageAction(label="label2", text="t1ext2")
                     ),
                        QuickReplyButton(
                         action=DatetimePickerAction(label="label3",
                                                     data="data3",
                                                     mode="date")
                     ),
                        QuickReplyButton(
                         action=CameraAction(label="label4")
                     ),
                        QuickReplyButton(
                         action=CameraRollAction(label="label5")
                     ),
                        QuickReplyButton(
                         action=LocationAction(label="label6")
                     ),
                    ])))
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text))


def quickreplay(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Quick reply',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="Hong", text="開局_Hong")),
                    QuickReplyButton(
                        action=MessageAction(label="Amilia", text="開局_Amilia")),
                    QuickReplyButton(
                        action=MessageAction(label="登寓", text="開局_登寓")),
                    QuickReplyButton(
                        action=MessageAction(label="陳彤", text="開局_陳彤")),
                    QuickReplyButton(
                        action=MessageAction(label="堉瑄", text="開局_堉瑄")),
                    QuickReplyButton(
                        action=MessageAction(label="狗哥", text="開局_狗哥")),
                    QuickReplyButton(
                        action=MessageAction(label="JILL", text="開局_JILL")
                    )
                ])))

# 寫入Google Excel


def InsertExcel(type_, value_):
    #today = datetime.date.today()
    auth_json_path = 'A.json'
    gss_scopes = ['https://spreadsheets.google.com/feeds']
    # 連線
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        auth_json_path, gss_scopes)
    gss_client = gspread.authorize(credentials)
    # 開啟 Google Sheet 資料表
    spreadsheet_key = '1CRMSn60TB5ZuE6TNCML-wgmQYtjHuSjhmkHFdCsk3_w'
    # 建立工作表1
    sheet = gss_client.open_by_key(spreadsheet_key).sheet1
    # gss_client.open_by_key(spreadsheet_key).add_worksheet(today,5,5)
    # 自定義工作表名稱
    #sheet = gss_client.open_by_key(spreadsheet_key).worksheet(today)
    # Google Sheet 資料表操作(舊版)
    # sheet.clear()  # 清除 Google Sheet 資料表內容
    if (type_ == '0') | (type_ == '1'):
        listtitle = sheet.row_values(1)  # 讀取第1列的一整列
        sheet.update_cell(1, len(listtitle)+1, value_) 

    #listtitle = ["姓名", value_]
    # sheet.append_row(listtitle)  # 標題
    #listdata = ["Liu", "0912-345678"]
    # sheet.append_row(listdata)  # 資料內容
    # Google Sheet 資料表操作(20191224新版)
    # sheet.update_acell('D2', 'ABC')  # D2加入ABC
    # sheet.update_cell(2, 4, 'ABC')  # D2加入ABC(第2列第4行即D2)
    # 寫入一整列(list型態的資料)
    #values = ['A', 'B', 'C', 'D']
    # sheet.insert_row(values, 1)  # 插入values到第1列
    # 讀取儲存格
    # sheet.acell('B1').value
    #sheet.cell(1, 2).value
    # 讀取整欄或整列
    # sheet.row_values(1)  # 讀取第1列的一整列
    # sheet.col_values(1)  # 讀取第1欄的一整欄
    # 讀取整個表
    # sheet.get_all_values()

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
# line_bot_api.reply_message(event.reply_token, message)

# quickreplay


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
