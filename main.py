# 安裝所需的套件
# pip install Flask line-bot-sdk

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定你的 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = 'HRPz1stAAOGnaGMyGH3LYiLFs2tpaYgfigaixfB65HrvkAE5J0LlQwe9JWgMsgOKYqH23+yKg7IBreS6RQ0yPs8hWNVIFU8PR+v8pSNYPApK9V1UdDLKLveuq9SfomFWWOsLO9YnWMeyGNDrC+WEvAdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'acd24b1ccb99fec2cb9c06a348f0ae84'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 LINE 平台傳來的簽名
    signature = request.headers['X-Line-Signature']

    # 獲取請求的 body
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 驗證簽名
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回應使用者的訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

if __name__ == "__main__":
    app.run()
