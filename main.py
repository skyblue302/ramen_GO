#import: API, uvicorn, linebot
from fastapi import FastAPI, Request
app = FastAPI()
import uvicorn

from linebot import WebhookParser
from linebot.models import *
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError


#爬蟲用
import requests

#其他
import time

#呼叫其他py程式
import library
import dict1
import config
import dict_emoji as em

from typing import Any, Dict, AnyStr, List, Union
JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


#載入token跟secret
line_api = LineBotApi(channel_access_token=config.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(channel_secret=config.LINE_CHANNEL_SECRET)


#主程式
@app.post("/")
async def handle_request(request: Request, arbitrary_json: JSONStructure = None):
    signature = request.headers.get("X-Line-Signature", "")
    body = (await request.body()).decode("utf-8")
    
    events = parser.parse(body,signature)

    for event in events:
        if event.type == "message":
            handle_message(event)
        if event.type == "postback":
            handle_postback(event)
    return "ok"



def handle_postback(event):
    data = event.postback.data
    
    #得到user資訊
    display_name = line_api.get_profile(event.source.user_id).display_name
    userId = line_api.get_profile(event.source.user_id).user_id
    now = time.ctime()
    print(f'(postback){display_name}:{data}\n{now}')

    if 'prize' in data:
        data1 = data.split('+')[1]
        if data1 == 'all':
            #呼叫library.prize
            name = library.prize_all()
            
            url = dict1.ramen_link_dict[library.branch(name)]
            
            #偵錯用
            print(f"{display_name}抽到的是{name}，其網址：{url}")
            
            inf = library.info(url)
            
            #name, address, score, critics, time1, url
            shop_name = inf[0]
            address = inf[1]
            score = inf[2]
            critics = inf[3]
            time1 = inf[4]
            url = inf[5]
            
            line_api.reply_message(event.reply_token, TextMessage(text=f'{em.ramen}今日抽到的拉麵是...\n{name}！\n\
                                                                        {em.house}地址{em.house}\n{shop_name}\n{address}\n\
                                                                        {em.link}連結{em.link}\n{url}\n\
                                                                        {em.star}Google評價{em.star}\n{score}({critics})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{time1}'))
        elif data1 == 'porkbone':
            line_api.reply_message(event.reply_token, TextMessage(text='測試中'))
        elif data1 == 'soysauce':
            line_api.reply_message(event.reply_token, TextMessage(text='測試中'))
        elif data1 == 'miso':
            line_api.reply_message(event.reply_token, TextMessage(text='測試中'))
        elif data1 == 'salt':
            line_api.reply_message(event.reply_token, TextMessage(text='測試中'))
        elif data1 == 'chicken':
            line_api.reply_message(event.reply_token, TextMessage(text='測試中'))
        elif data1 == 'sob':
            line_api.reply_message(event.reply_token, TextMessage(text='測試中'))
    else:
        line_api.reply_message(event.reply_token, TextMessage(text='bug:無此指令'))



def handle_message(event):
    #得到user資訊
    display_name = line_api.get_profile(event.source.user_id).display_name
    userId = line_api.get_profile(event.source.user_id).user_id
    now = time.ctime()
    
    
    #分辨型別為text
    if event.message.type == "text":
        text = event.message.text
    else:
        typeofmessage = event.message.type
        print(f'({typeofmessage}){display_name}:\n{now}')
        line_api.reply_message(event.reply_token,TextMessage(text="I can't reply this."))
        return 200

    print(f'(text){display_name}:{text}\n{now}')
    
    #抽拉麵
    if text.lower() in ["抽"]:
        line_api.reply_message(event.reply_token,TextSendMessage(text="今天想吃哪種湯頭呢?", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=PostbackAction(label="全都要，直接抽", data="prize+all")),
                        QuickReplyButton(action=PostbackAction(label="豚骨", data="prize+porkbone")),
                        QuickReplyButton(action=PostbackAction(label="醬油", data="prize+soysauce")),
                        QuickReplyButton(action=PostbackAction(label="味噌", data="prize+miso")),
                        QuickReplyButton(action=PostbackAction(label="鹽味", data="prize+salt")),
                        QuickReplyButton(action=PostbackAction(label="雞湯", data="prize+chicken")),
                        QuickReplyButton(action=PostbackAction(label="雞白湯", data="prize+soba")),
                        ])))
    elif '隱家拉麵' in text:
        if '士林' in text:
            url = dict1.ramen_link_dict['隱家拉麵_士林店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是隱家拉麵_士林店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '芝山' in text:
            url = dict1.ramen_link_dict['隱家拉麵_芝山店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是隱家拉麵_芝山店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '赤峰' in text:
            url = dict1.ramen_link_dict['隱家拉麵_赤峰店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是隱家拉麵_赤峰店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '公館' in text:
            url = dict1.ramen_link_dict['隱家拉麵_公館店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是隱家拉麵_公館店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到隱家拉麵\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="士林", text="隱家拉麵_士林店")),
                        QuickReplyButton(action=MessageAction(label="芝山", text="隱家拉麵_芝山店")),
                        QuickReplyButton(action=MessageAction(label="赤峰", text="隱家拉麵_赤峰店")),
                        QuickReplyButton(action=MessageAction(label="公館", text="隱家拉麵_公館店")),
                        ])))
    elif '雞吉君' in text:
        url = dict1.ramen_link_dict['雞吉君']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是雞吉君的資訊\n連結：{inf[5]}\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif ('麵屋武藏' in text) or ('武藏' in text):
        if '神山' in text:
            url = dict1.ramen_link_dict['麵屋武藏_神山']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是麵屋武藏_神山的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '本店' in text:
            url = dict1.ramen_link_dict['麵屋武藏_本店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是麵屋武藏_本店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到麵屋武藏\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="神山", text="麵屋武藏_神山")),
                        QuickReplyButton(action=MessageAction(label="本店", text="麵屋武藏_本店")),
                        ])))
    elif "麵屋昕家" in text:
        url = dict1.ramen_link_dict['麵屋昕家']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是麵屋昕家的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "麵屋一燈" in text:
        url = dict1.ramen_link_dict['麵屋一燈']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是麵屋一燈的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "勝王" in text:
        url = dict1.ramen_link_dict['勝王']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是勝王的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif ('鳥人拉麵' in text) or ('鳥人' in text):
        if '總店' in text or '台灣' in text:
            url = dict1.ramen_link_dict['鳥人拉麵_台灣總店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是鳥人拉麵_台灣總店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '中山店' in text:
            url = dict1.ramen_link_dict['鳥人拉麵_中山店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是鳥人拉麵_中山店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '西門店' in text:
            url = dict1.ramen_link_dict['鳥人拉麵_西門店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是鳥人拉麵_西門店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到鳥人拉麵\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="台灣總店", text="鳥人拉麵_台灣總店")),
                        QuickReplyButton(action=MessageAction(label="中山店", text="鳥人拉麵_中山店")),
                        QuickReplyButton(action=MessageAction(label="西門店", text="鳥人拉麵_西門店")),
                        ])))
    elif '鬼金棒' in text:
        if '沾麵' in text:
            url = dict1.ramen_link_dict['鬼金棒味噌沾麵_台北本店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是鬼金棒味噌沾麵_台北本店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif ('本店' in text) or ('台北' in text):
            url = dict1.ramen_link_dict['鬼金棒味噌拉麵_台北本店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是鬼金棒味噌拉麵_台北本店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif ('松江' in text) or ('南京' in text):
            url = dict1.ramen_link_dict['鬼金棒_松江南京']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是鬼金棒_松江南京的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到鬼金棒\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="沾麵_台北本店", text="鬼金棒味噌沾麵_台北本店")),
                        QuickReplyButton(action=MessageAction(label="拉麵_台北本店", text="鬼金棒味噌拉麵_台北本店")),
                        QuickReplyButton(action=MessageAction(label="松江南京", text="鬼金棒_松江南京")),
                        ])))
    elif "鷹流蘭丸" in text:
        url = dict1.ramen_link_dict['鷹流蘭丸_中山店']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是鷹流蘭丸_中山店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "柑橘" in text:
        if 'Soba' in text:
            url = dict1.ramen_link_dict['柑橘_Soba']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是柑橘_Soba的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '鴨蔥' in text:
            url = dict1.ramen_link_dict['柑橘_鴨蔥']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是柑橘_鴨蔥的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '魚水' in text:
            url = dict1.ramen_link_dict['柑橘_魚水']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是柑橘_魚水的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到柑橘\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="Soba", text="柑橘_Soba")),
                        QuickReplyButton(action=MessageAction(label="鴨蔥", text="柑橘_鴨蔥")),
                        QuickReplyButton(action=MessageAction(label="魚水", text="柑橘_魚水"))
                        ])))
    elif "墨洋" in text:
        url = dict1.ramen_link_dict['墨洋拉麵']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是墨洋拉麵的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "道樂" in text:
        if '屋台' in text:
            url = dict1.ramen_link_dict['道樂屋台']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是道樂屋台的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif ('拉麵' in text) or ('大北' in text):
            url = dict1.ramen_link_dict['道樂拉麵_大北店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是道樂拉麵_大北店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '商店' in text:
            url = dict1.ramen_link_dict['道樂商店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是道樂商店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到長生塩人\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="道樂屋台", text="道樂屋台")),
                        QuickReplyButton(action=MessageAction(label="道樂拉麵_大北店", text="道樂拉麵_大北店")),
                        QuickReplyButton(action=MessageAction(label="道樂商店", text="道樂商店"))
                        ])))
    elif "博多" in text:
        if ('台灣' in text) or ('總店' in text):
            url = dict1.ramen_link_dict['博多拉麵_台灣總店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是博多拉麵_台灣總店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '市大' in text:
            url = dict1.ramen_link_dict['博多拉麵_市大店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是博多拉麵_市大店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到博多拉麵\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="台灣總店", text="博多拉麵_台灣總店")),
                        QuickReplyButton(action=MessageAction(label="市大店", text="博多拉麵_市大店")),
                        ])))
    elif "一幻" in text:
        url = dict1.ramen_link_dict['一幻拉麵_台北信義店']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是一幻拉麵_台北信義店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "樂麵屋" in text:
        if '永康' in text:
            url = dict1.ramen_link_dict['樂麵屋_永康店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是樂麵屋_永康店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '永康公園' in text:
            url = dict1.ramen_link_dict['樂麵屋_永康公園店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是樂麵屋_永康公園店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '西門' in text:
            url = dict1.ramen_link_dict['樂麵屋_西門店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是樂麵屋_西門的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '南港' in text:
            url = dict1.ramen_link_dict['樂麵屋_南港店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是樂麵屋_南港店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到樂麵屋\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="永康", text="樂麵屋_永康店")),
                        QuickReplyButton(action=MessageAction(label="永康公園", text="樂麵屋_永康公園店")),
                        QuickReplyButton(action=MessageAction(label="西門", text="樂麵屋_西門店")),
                        QuickReplyButton(action=MessageAction(label="南港", text="樂麵屋_南港店"))
                        ])))
    elif "藏味" in text:
        url = dict1.ramen_link_dict['藏味拉麵']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是藏味拉麵的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "真劍" in text:
        url = dict1.ramen_link_dict['真劍拉麵']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是真劍拉麵的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif ("長生塩人" in text) or ("長生鹽人" in text):
        if '天母' in text:
            url = dict1.ramen_link_dict['長生塩人_天母']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是長生塩人_天母的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '辛亥' in text:
            url = dict1.ramen_link_dict['長生塩人_辛亥']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是長生塩人_辛亥的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '民生' in text:
            url = dict1.ramen_link_dict['長生塩人_民生']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是長生塩人_民生的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '北投' in text:
            url = dict1.ramen_link_dict['長生塩人_北投車站']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是長生塩人_北投車站的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到長生塩人\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="天母", text="長生塩人_天母")),
                        QuickReplyButton(action=MessageAction(label="辛亥", text="長生塩人_辛亥")),
                        QuickReplyButton(action=MessageAction(label="民生", text="長生塩人_民生")),
                        QuickReplyButton(action=MessageAction(label="北投車站", text="長生塩人_北投車站"))
                        ])))
    elif "麵屋壹慶" in text:
        url = dict1.ramen_link_dict['麵屋壹慶']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是麵屋壹慶的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "山嵐" in text:
        if '大安' in text:
            url = dict1.ramen_link_dict['山嵐拉麵_大安店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是山嵐拉麵_大安店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '古亭' in text:
            url = dict1.ramen_link_dict['山嵐拉麵_古亭店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是山嵐拉麵_古亭店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '公館' in text:
            url = dict1.ramen_link_dict['山嵐拉麵_公館店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是山嵐拉麵_公館店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '林森' in text:
            url = dict1.ramen_link_dict['山嵐拉麵_林森八條店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是山嵐拉麵_林森八條店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到山嵐拉麵\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="大安店", text="山嵐拉麵_大安")),
                        QuickReplyButton(action=MessageAction(label="古亭店", text="山嵐拉麵_古亭")),
                        QuickReplyButton(action=MessageAction(label="公館店", text="山嵐拉麵_公館")),
                        QuickReplyButton(action=MessageAction(label="林森八條店", text="山嵐拉麵_林森八條")),
                        ])))
    elif "五之神製作所" in text:
        url = dict1.ramen_link_dict['五之神製作所']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是五之神製作所的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "拉麵公子" in text:
        url = dict1.ramen_link_dict['拉麵公子']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是拉麵公子的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "特濃屋" in text:
        url = dict1.ramen_link_dict['特濃屋']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是特濃屋的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "壹之穴" in text:
        url = dict1.ramen_link_dict['壹之穴沾麵']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是壹之穴沾麵的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "一蘭" in text:
        if '本店' in text:
            url = dict1.ramen_link_dict['一蘭_台灣台北本店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是一蘭_台灣台北本店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '別館' in text:
            url = dict1.ramen_link_dict['一蘭_台灣台北別館']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是一蘭_台灣台北別館的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到一蘭\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="本店", text="一蘭_台灣台北本店")),
                        QuickReplyButton(action=MessageAction(label="別館", text="一蘭_台灣台北別館")),
                        ])))

    elif "麵試十一次" in text:
        url = dict1.ramen_link_dict['麵試十一次']
        inf = library.info(url)
        line_api.reply_message(event.reply_token,TextMessage(text=f'以下是麵試十一次的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
    elif "一風堂" in text:
        if ('本店' in text) or ('中山' in text):
            url = dict1.ramen_link_dict['一風堂_中山本店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是一風堂_中山本店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '北車' in text:
            url = dict1.ramen_link_dict['一風堂_微風北車店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是一風堂_微風北車店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '101' in text:
            url = dict1.ramen_link_dict['一風堂_台北101店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是一風堂_台北101店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif '南山' in text:
            url = dict1.ramen_link_dict['一風堂_微風南山店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是一風堂_微風南山店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        elif ('新莊' in text) or ('宏匯' in text):
            url = dict1.ramen_link_dict['一風堂_新莊宏匯店']
            inf = library.info(url)
            line_api.reply_message(event.reply_token,TextMessage(text=f'以下是一風堂_新莊宏匯店的資訊\n\
                                                                        {em.house}地址{em.house}\n{inf[1]}\n\
                                                                        {em.link}連結{em.link}\n{inf[5]}\n\
                                                                        {em.star}Google評價{em.star}\n{inf[2]}({inf[3]})\n\
                                                                        {em.clock1}營業時間{em.clock1}\n{inf[4]}'))
        else:
            line_api.reply_message(event.reply_token,TextSendMessage(text="已為您搜尋到一風堂\n按下下方按鈕獲得更多資訊", quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(action=MessageAction(label="中山本店", text="一風堂_中山本店")),
                        QuickReplyButton(action=MessageAction(label="微風北車", text="一風堂_微風北車店")),
                        QuickReplyButton(action=MessageAction(label="台北101", text="一風堂_台北101店")),
                        QuickReplyButton(action=MessageAction(label="微風南山", text="一風堂_微風南山店")),
                        QuickReplyButton(action=MessageAction(label="新莊宏匯", text="一風堂_新莊宏匯店")),
                        ])))
    else:
        line_api.reply_message(event.reply_token,TextMessage(text="測試else"))
    
        
            
       
#if __name__ == "__main__":
#    import nest_asyncio
#    nest_asyncio.apply()
#    import uvicorn
#    uvicorn.run(app, host="0.0.0.0", port=8080)
