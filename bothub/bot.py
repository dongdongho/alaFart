# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from bothub_client.bot import BaseBot
from bothub_client.decorators import channel, command
from selenium import webdriver
import traceback
import requests

import dialogflow_alpha
import aladin
from bothub import telegram_alpha as telegram


class Bot(BaseBot):
    @channel('telegram')
    def telegram_handler(self, event, context):
        utterence = event['content']
        token = self.get_messenger_token(event, context)
        ## intent handler 필요

        if 'callback_query' in event['raw_data']:
            self.callback_query(event, token)
        elif 'message' in event['raw_data']:
            ## 중복 실행 처리
            data = self.get_user_data()
            data['list_index'] = 0
            data['book_list'] = aladin.search_book(utterence)

            ## Book is dictionary.
            for book in data['book_list'][:5]:
                book_name = book['name']
                book_info = book['writer'] + '\n' if 'writer' in book else ''
                book_info += book['publisher'] + '\n' if 'publisher' in book else ''
                book_info += book['publishing_day'] + '\n' if 'publishing_day' in book else ''
                book_img = book['cover_img'] if 'cover_img' in book else ''
                inline_keyboard = [{'text': "재고 현황", 'callback_data': 'book|' + book['name']}]
                caption = '*{}*\n\n{}'.format(book_name, book_info)
                # caption = book_info
                telegram.send_chat_action(token, event['sender']['id'], 'typing')
                ## Need to process no image item.
                telegram.send_photo(
                    token, event['sender']['id'], book_img, caption, inline_keyboard)
            self.set_user_data(data)

    # @channel('kakaotalk')
    # def telegram_handler(self, event, context):
    #     utterence = event['content']
    #     token = self.get_messenger_token(event, context)
    #     ## intent handler 필요

    #     if 'callback_query' in event['raw_data']:
    #         self.callback_query(event, token)
    #     elif 'message' in event['raw_data']:
    #         ## 중복 실행 처리
    #         data = self.get_user_data()
    #         data['list_index'] = 0
    #         data['book_list'] = aladin.search_book(utterence)

    #         ## Book is dictionary.
    #         for book in data['book_list'][:5]:
    #             book_name = book['name']
    #             book_info = book['writer'] + '\n' if 'writer' in book else ''
    #             book_info += book['publisher'] + '\n' if 'publisher' in book else ''
    #             book_info += book['publishing_day'] + '\n' if 'publishing_day' in book else ''
    #             book_img = book['cover_img'] if 'cover_img' in book else ''
    #             inline_keyboard = [{'text': "재고 현황", 'callback_data': 'book|' + book['name']}]
    #             caption = '*{}*\n\n{}'.format(book_name, book_info)
    #             # caption = book_info
    #             telegram.send_chat_action(token, event['sender']['id'], 'typing')
    #             ## Need to process no image item.
    #             telegram.send_photo(
    #                 token, event['sender']['id'], book_img, caption, inline_keyboard)
    #         self.set_user_data(data)


    def get_messenger_token(self, event, context):
        current_channel = event.get('channel')
        if current_channel and 'channel' in context:
            channels = context.get('channel', {}).get('channels', {})
            for ch in channels:
                ch_type = ch.get('type')
                if ch_type == current_channel:
                    if 'facebook' == ch_type:
                        return ch.get('page_access_token')
                    elif 'telegram' == ch_type:
                        return ch.get('api_key')
                    elif 'slack' == ch_type:
                        return ch.get('access_token')
                    elif 'line' == ch_type:
                        return ch.get('channel_access_token')
        return None


    def callback_query(self, event, token):
        callback_id = event['raw_data']['callback_query']['data']
        flag, flag_data = callback_id.split("|")
        if flag == "book":
            data = self.get_user_data()
            for book in data['book_list']:
                if book['name'] == flag_data:
                    inline_list = []
                    row_line = []
                    text = "원하시는 매장을 선택하세요"
                    for off_shop in book['detail_info']:
                        if len(row_line) == 2:
                            inline_list.append(row_line)
                            row_line = []
                        name = off_shop['name']
                        url = off_shop['url']
                        row_line.append({'text':name, 'url':url})
                    r = telegram.send_message(token, event['sender']['id'], text, inline_list)
                    self.logger(r)
        elif flag == "loc":
            self.logger("location")


    def get_session_id(self, event):
        return "{}:{}".format(event['channel'], event.get('user_id'))


    def logger(self, message):
        base_url = "https://api.telegram.org/bot{token}/{method}"
        method = 'sendMessage'

        token = "775553429:AAG4wGKQRlu9_5h4_W_NISpYAacK_pQVzf8"
        chat_id = '568763746' # Spacy Ops

        url = base_url.format(token=token, method=method)
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            'chat_id': chat_id,
            'text': "Aladin {}".format(message),
        }

        r = requests.post(url, json=payload, headers=headers)
