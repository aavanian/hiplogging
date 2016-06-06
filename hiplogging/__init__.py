# -*- coding: utf-8 -*-
""" Refactors hiplogging (https://github.com/invernizzi/hiplogging) to use
HipChat's API v2 via HypChat (https://github.com/RidersDiscountCom/HypChat)
"""
from functools import partial
import logging
from hypchat import HypChat


class HipChatHandler(logging.Handler):

    def __init__(self, access_token, room_name, endpoint='https://api.hipchat.com', notification_only=False):
        logging.Handler.__init__(self)
        if notification_only:
            self.notification = partial(HypChat(access_token, endpoint).send_notification, id_or_name=room_name)
        else:
            self.notification = partial(HypChat(access_token, endpoint).get_room(room_name).notification)

    def emit(self, record):
        if hasattr(record, "color"):
            color = record.color
        else:
            color = self.__color_for_level(record.levelno)
        if hasattr(record, "notify"):
            notify = bool(record.notify)
        else:
            notify = self.__notify_for_level(record.levelno)
        kwargs = {
            'message': self.format(record),
            'color' : color,
            'notify': notify
        }
        self.notification(**kwargs)

    def __color_for_level(self, levelno):
        if levelno > logging.WARNING:
            return 'red'
        if levelno == logging.WARNING:
            return 'yellow'
        if levelno == logging.INFO:
            return 'green'
        if levelno == logging.DEBUG:
            return 'gray'
        return 'purple'

    def __notify_for_level(self, levelno):
        if levelno > logging.WARNING:
            return True
        if levelno == logging.WARNING:
            return False
        if levelno == logging.INFO:
            return False
        if levelno == logging.DEBUG:
            return False
        return False


