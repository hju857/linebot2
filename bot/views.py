from django.shortcuts import render
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse,HttpResponseBadRequest,HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

from linebot import LineBotApi, WebhookHandler,WebhookParser
from linebot.exceptions import InvalidSignatureError,LineBotApiError
from linebot.models import MessageEvent,TextSendMessage,TextMessage,ImageSendMessage



line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parse=WebhookParser(settings.LINE_CHANNEL_SECRET)


@csrf_exempt    
def callback(request):
    if request.method=='POST':
        signature=request.META['HTTP_X_LINE_SIGNATURE']
        body=request.body.decode('utf-8')
        try:
            events=parse.parse(body,signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        for event in events:
            if isinstance(event,MessageEvent):
                if isinstance(event.message,TextMessage):
                  text=event.message.text
                  print(text)
                  if'時刻表'in text:
                      message='https://ebus.gov.taipei/'
                  elif'公車路線圖' in text:
                      image_url='https://www-ws.gov.taipei/Download.ashx?u=LzAwMS9VcGxvYWQvNDU4L2NrZmlsZS83ZjllMTU4MS1hMDlkLTRhMTktYjRjYy0xNzRjNzNlZTEzMzUucG5n&n=5bm56YGT6Lev5buK5ZyWX%2bmggemdol8yLnBuZw%3d%3d&icon=.png'
                     
                     
                  else:
                      message= '無法解析'   
                if message is not None:
                       line_bot_api.reply_message(
                         event.reply_token,
                         TextSendMessage(text=message)  
                       ) 
                      
                
                
                if image_url is not None:
                         line_bot_api.reply_message(
                             event.reply_token,
                             ImageSendMessage(original_content_url=image_url,
                                                  preview_image_url=image_url,))
                      
        return HttpResponse()
    else:
        return HttpResponseBadRequest()