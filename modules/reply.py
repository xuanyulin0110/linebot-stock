from linebot.models import (
    MessageEvent, TextMessage, StickerMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, TemplateSendMessage, ButtonsTemplate, PostbackAction, MessageAction, URIAction, CarouselTemplate, CarouselColumn, QuickReply, QuickReplyButton
)

# 官方文件
# https://github.com/line/line-bot-sdk-python

# 常見問答表
faq1 = {
    '貼圖': StickerSendMessage(
        package_id='1',
        sticker_id='1'
    ),
    '台北照片': ImageSendMessage(
        original_content_url='https://dynamic-media-cdn.tripadvisor.com/media/photo-o/04/62/e9/2b/101.jpg?w=400&h=300&s=1',
        preview_image_url='https://dynamic-media-cdn.tripadvisor.com/media/photo-o/04/62/e9/2b/101.jpg?w=400&h=300&s=1'
        #https://picsum.photos/id/395/900/400
    ),
    '交通': TextSendMessage(text='請問您想使用何種方式前往？',
                          quick_reply=QuickReply(items=[
                              QuickReplyButton(action=MessageAction(
                                  label="搭乘捷運", text="捷運")
                              ),
                              QuickReplyButton(action=MessageAction(
                                  label="搭乘公車", text="公車")
                              )
                          ])
                          ),
    '捷運': TextSendMessage(
        text="搭乘捷運至木柵線科技大樓站步行5分鐘即可抵達。"
    ),
    '台北地址': LocationSendMessage(
        title='台北',
        address='Taipei',
        latitude=25.0329694,
        longitude=121.5654177
    ),
    '簡介ooxx': TextMessage(text='這是一個和電腦玩ooxx的小遊戲'),
    'ooxx玩法': TextSendMessage(text='輸入:put o 位置\n例如:put o 1-1'),
    '公車': TextSendMessage(text='11路'),
}

# 主選單
menu1 = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                # 卡片一圖片網址
                thumbnail_image_url='https://play-lh.googleusercontent.com/-m7FLASLq_ju8khe6btxBvwGlRolgtKeYaweJ1-0-FSKQXh64j7eWBbWi4ttV8_Tmaw=w240-h480-rw',
                title='遊戲ooxx',
                text='點選下方按鈕開始互動',
                actions=[
                    MessageAction(
                        label='觀看簡介',
                        text='簡介ooxx'
                    ),
                    MessageAction(
                        label='遊戲玩法',
                        text='ooxx玩法'
                    ),
                    MessageAction(
                        label='開始遊戲',
                        text='ooxx'
                    )
                ]
            ),
            CarouselColumn(
                # 卡片二圖片網址
                thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT4SnFsFO-_ZzqHqCvSWhodUvlKguixd1bPzw&usqp=CAU',
                title='台北介紹',
                text='點選下方按鈕開始互動',
                actions=[
                    MessageAction(
                        label='地址',
                        text='台北地址'
                    ),
                    MessageAction(
                        label='照片',
                        text='台北照片'
                    ),
                    URIAction(
                        label='官方網站',
                        uri='https://zh.m.wikipedia.org/zh-tw/taipei'
                    )
                ]
            )
        ]
    )
)

#ooxx主選單
menu2 = TemplateSendMessage(
    alt_text='Carousel template',
    template=CarouselTemplate(
        columns=[
            CarouselColumn(
                # 卡片一圖片網址
                thumbnail_image_url='https://play-lh.googleusercontent.com/-m7FLASLq_ju8khe6btxBvwGlRolgtKeYaweJ1-0-FSKQXh64j7eWBbWi4ttV8_Tmaw=w240-h480-rw',
                title='遊戲ooxx',
                text='點選下方按鈕開始互動',
                actions=[
                    MessageAction(
                        label='1-1',
                        text='put o 1-1'
                    ),
                    MessageAction(
                        label='2-1',
                        text='put o 2-1'
                    ),
                    MessageAction(
                        label='3-1',
                        text='put o 3-1'
                    )
                ]
            ),
            CarouselColumn(
                # 卡片二圖片網址
                thumbnail_image_url='https://play-lh.googleusercontent.com/-m7FLASLq_ju8khe6btxBvwGlRolgtKeYaweJ1-0-FSKQXh64j7eWBbWi4ttV8_Tmaw=w240-h480-rw',
                title='遊戲ooxx',
                text='點選下方按鈕開始互動',
                actions=[
                    MessageAction(
                        label='1-2',
                        text='put o 1-2'
                    ),
                    MessageAction(
                        label='2-2',
                        text='put o 2-2'
                    ),
                    MessageAction(
                        label='3-2',
                        text='put o 3-2'
                    )
                ]
            ),
            CarouselColumn(
                # 卡片三圖片網址
                thumbnail_image_url='https://play-lh.googleusercontent.com/-m7FLASLq_ju8khe6btxBvwGlRolgtKeYaweJ1-0-FSKQXh64j7eWBbWi4ttV8_Tmaw=w240-h480-rw',
                title='遊戲ooxx',
                text='點選下方按鈕開始互動',
                actions=[
                    MessageAction(
                        label='1-3',
                        text='put o 1-3'
                    ),
                    MessageAction(
                        label='2-3',
                        text='put o 2-3'
                    ),
                    MessageAction(
                        label='3-3',
                        text='put o 3-3'
                    )
                ]
            )
        ]
    )
)
