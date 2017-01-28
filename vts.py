import logging
import time

import daemon
import vk_api
from slacker import Slacker

from settings import SLACK_TOKEN, VK_LOGIN, VK_PASSWORD, GROUP_ID, TOPIC_ID, ICON_URL, CHANNEL, USERNAME

slack = Slacker(SLACK_TOKEN)


class Vts:
    last_comment_id = 0
    vk = None

    @staticmethod
    def update_vk():
        if Vts.vk is not None:
            return

        vk_session = vk_api.VkApi(VK_LOGIN, VK_PASSWORD)

        try:
            vk_session.authorization()
        except vk_api.AuthorizationError as error_msg:
            logging.error(error_msg)
            return
        except vk_api.Captcha as captcha:
            logging.error(captcha)
            return

        Vts.vk = vk_session.get_api()

    @staticmethod
    def update_last_comment_id():
        Vts.update_vk()

        if Vts.vk is None:
            return

        try:
            response = Vts.vk.board.getComments(group_id=GROUP_ID, topic_id=TOPIC_ID, sort='desc', count=1)
        except vk_api.ApiError:
            return

        if response['count'] == 0:
            return

        Vts.last_comment_id = response['items'][0]['id']
        print('Set initial id to ' + str(Vts.last_comment_id))

    @staticmethod
    def get_comments():
        Vts.update_vk()

        if Vts.vk is None:
            return [], []

        try:
            response = Vts.vk.board.getComments(group_id=GROUP_ID, topic_id=TOPIC_ID,
                                                start_comment_id=Vts.last_comment_id, extended=1)
        except vk_api.ApiError:
            return [], []

        return response['items'], response['profiles']

    @staticmethod
    def get_topic():
        Vts.update_vk()

        if Vts.vk is None:
            return None

        try:
            response = Vts.vk.board.getTopics(group_id=GROUP_ID, topic_ids=[TOPIC_ID])
        except vk_api.ApiError:
            return None

        if response['count'] == 0:
            return None

        return response['items'][0]

    @staticmethod
    def run():
        while True:
            if Vts.last_comment_id == 0:
                Vts.update_last_comment_id()

            if Vts.last_comment_id == 0:
                time.sleep(60)
                return

            topic = Vts.get_topic()
            if topic is None:
                logging.warning('Topic not found')
                time.sleep(60)
                continue

            comments, profiles = Vts.get_comments()

            if len(comments) == 0:
                time.sleep(5)
                continue

            users = dict()

            for profile in profiles:
                users[profile['id']] = profile

            for comment in comments:
                id = comment['id']
                if id > Vts.last_comment_id:
                    Vts.last_comment_id = id

                    try:
                        user = users[abs(comment['from_id'])]
                        username = ' '.join([user['first_name'], user['last_name']])
                    except KeyError:
                        username = ''

                    message_date = '<!date^' + str(comment['date']) + '^Posted {date} {time}|Posted 2014-02-18 6:39:42>'
                    text = str(comment['text']).replace('\n', '\n>')
                    message = '>*{title}*\n>_{username}_ ({date})\n>{text}'.format(title=topic['title'],
                                                                                   username=username, date=message_date,
                                                                                   text=text)
                    slack.chat.post_message(channel=CHANNEL, text=message, username=USERNAME, icon_url=ICON_URL)
                    logging.info('Posted comment_id=%s\n%s', id, message)


with daemon.DaemonContext():
    Vts.run()
