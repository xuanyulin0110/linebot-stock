# 運行以下程式需安裝模組: line-bot-sdk, flask, pyquery
# 安裝方式，輸入指令: pip install 模組名稱

from linebot.models import QuickReply, QuickReplyButton

# 引入FLEX message json
# 引入zuvio
from zuvio import zuvio_check
# 引入ooxx
from ooxx import ooxx, ooxx_gamestart, ooxx_refrash
# 引入股票查詢系統
from stock.StockModule import stock
# 引入flask模組
from flask import Flask, request, abort
# 引入linebot相關模組
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)

# 如需增加其他處理器請參閱以下網址的 Message objects 章節
# https://github.com/line/line-bot-sdk-python
from linebot.models import (
    MessageEvent,
    TextMessage,
    StickerMessage,
    TextSendMessage,
    StickerSendMessage,
    ImageSendMessage,
    MessageAction
)

# 把modules/reply.py 裡的 faq1,menu1 引用進來
from modules.reply import faq1, menu1

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = '8ohI2V3DlyJ6xaoxNxRi5r0a/2arpFgsEfoylAS7ffejAtm9xs44hh+le/yrWrswZn0mSXOH2kU2CTsK2gnBXK1HwXQKinwXvw/IOKYfQ5nJlJ8u+dAu89ksjym9DLrQGjeuyom5opQT8pp2VXQpEwdB04t89/1O/w1cDnyilFU='  # '請將此字串置換成你的_CHANNEL_ACCESS_TOKEN'
CHANNEL_SECRET = '9d75f482ffad592a3476d90e18f51695'  # '請將此字串置換成你的_CHANNEL_SECRET'

# ********* 以下為 X-LINE-SIGNATURE 驗證程序 *********
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    print("[已接收訊息]")
    print(body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# ********* 以上為 X-LINE-SIGNATURE 驗證程序 *********


# 文字訊息傳入時的處理器
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 當有文字訊息傳入時

    # event.message.text : 使用者輸入的訊息內容
    print('*' * 100)
    print('[使用者傳入文字訊息]')
    print(str(event))
    # 取得使用者說的文字
    user_msg = event.message.text
    # 取得使用者ID
    UserId = event.source.user_id
    # 取得使用者profile
    User_profile = line_bot_api.get_profile(UserId)
    # print('\n\n')
    print(User_profile.display_name)
    # 準備要回傳的文字訊息
    reply = []
    reply = [menu1]
    if user_msg in faq1:
        reply = faq1[user_msg]
    # reply = TextSendMessage(text=f'恭喜你，你已收到程式的回應，你剛才說的是「{user_msg}」對吧！')

    # ooxx程式
    if user_msg[0:5] == 'ooxx-' or user_msg[0:3] == 'put':
        reply = []
        if user_msg[5] == '一':
            text = ooxx_gamestart(User_profile.display_name, '房間一' + user_msg[6])

        elif user_msg[5:7] == '單人':
            text = ooxx_gamestart(User_profile.display_name, '單人')
        # reply = [TextSendMessage(text=ooxx(User_profile.display_name, user_msg))]
        elif user_msg[5:7] == '重整':
            text = (ooxx_refrash(User_profile.display_name))
        elif user_msg[7] == '-':
            text = ooxx(User_profile.display_name, user_msg)
        reply.append(text[0])
        reply.append(
            # quickreplay
            TextSendMessage(text[2],
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=MessageAction(
                                    label="重整", text="ooxx-重整")
                                ),
                                QuickReplyButton(action=MessageAction(
                                    label="重新開始", text="ooxx")
                                )
                            ])
                            ))
    try:
        userStock = int(user_msg[:4])
        if 0 <= userStock <= 9999:
            userStock = str(userStock)
            reply = [TextSendMessage(text="股票"+userStock)]
            reply.append(TextSendMessage("是否正確(若錯誤請重新輸入)",
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=MessageAction(
                                    label="正確", text="股票-" + userStock)
                                )
                            ])
                            ))
    except:
        if user_msg[:2] == "股票":
            reply = []
            Stock = stock()
            if len(user_msg) >= 6:
                StockNumber = user_msg[3:7]
                try:
                    if 0 < int(StockNumber) < 9999:
                        Stock.get_url(StockNumber)
                    else:
                        print("輸入錯誤，將使用", Stock.STOCK_NUMBER)

                except:
                    print("將使用", Stock.STOCK_NUMBER)
                if len(user_msg) >= 9:
                    url = "https://linebot-stock.fly.dev"
                    url = "https://ffd9-150-116-38-205.jp.ngrok.io"
                    if user_msg[8] == "1":
                        Stock.get_revenue()
                        reply.append(TextSendMessage(
                            text=url + '/static/tmp/stock-' + Stock.STOCK_NUMBER + '-最新營收表.xlsx'))

                    elif user_msg[8] == "2":
                        try:
                            Stock.get_compare()
                            reply.append(TextSendMessage(
                                text=url + '/static/tmp/stock-' + Stock.STOCK_NUMBER + '-營收比較表.xlsx'))
                        except:
                            reply.append(TextSendMessage("error"))
                    elif user_msg[8] == "3":

                        Stock.get_value()

            reply.append(
                # quickreplay
                TextSendMessage("選擇模式",
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(
                                        label="mode 1", text="股票-" + StockNumber + "-1")
                                    ),
                                    QuickReplyButton(action=MessageAction(
                                        label="mode 2", text="股票-" + StockNumber + "-2")
                                    ),
                                    QuickReplyButton(action=MessageAction(
                                        label="mode 3", text="股票-" + StockNumber + "-3")
                                    )
                                ])
                                ))
    if user_msg == '簽到':
        zuvio_check()
        reply = [TextSendMessage(text='簽到done')]
        reply.append(ImageSendMessage(
            original_content_url='https://line-bot-xy.herokuapp.com/static/tmp/test.png',
            preview_image_url='https://line-bot-xy.herokuapp.com/static/tmp/test.png'
        ))




    # if user_msg == '電話' or user_msg == '123':
    #    reply = TextSendMessage(text='電話：0932162951')
    # elif user_msg == '地址':
    #    reply = TextSendMessage(text='地址：台北市中正區重慶南路一段122號')
    # elif user_msg == 'Youtube':
    #    reply = TextSendMessage(text='https://youtube.com')

    # 回傳訊息
    # 若需要回覆多筆訊息可使用
    # line_bot_api.reply_message(token, [Object, Object, ...])
    line_bot_api.reply_message(
        event.reply_token,
        reply)


# 貼圖訊息傳入時的處理器
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    # 當有貼圖訊息傳入時
    print('*' * 30)
    print('[使用者傳入貼圖訊息]')
    print(str(event))

    # 準備要回傳的貼圖訊息
    # HINT: 機器人可用的貼圖 https://devdocs.line.me/files/sticker_list.pdf
    reply = StickerSendMessage(package_id='2', sticker_id='149')

    # 回傳訊息
    line_bot_api.reply_message(
        event.reply_token,
        reply)


import os

if __name__ == "__main__":
    print('[伺服器開始運行]')
    # 取得遠端環境使用的連接端口，若是在本機端測試則預設開啟於port=5500
    port = int(os.environ.get('PORT', 5500))
    # 使app開始在此連接端口上運行
    print(f'[Flask運行於連接端口:{port}]')
    # 本機測試使用127.0.0.1, debug=True
    # Heroku部署使用 0.0.0.0
    app.run(host='0.0.0.0', port=port, debug=True)
