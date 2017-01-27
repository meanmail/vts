from slacker import Slacker

import vk_api

import time

import logging

from settings import SLACK_TOKEN, VK_LOGIN, VK_PASSWORD, GROUP_ID, TOPIC_ID, ICON_URL, CHANNEL, USERNAME

slack = Slacker(SLACK_TOKEN)


class Vts:
    def __init__(self):
        self.last_comment_id = 0
        self.vk = None

    def update_vk(self):
        if self.vk is not None:
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

        self.vk = vk_session.get_api()

    def update_last_comment_id(self):
        self.update_vk()

        if self.vk is None:
            return

        response = self.vk.board.getComments(group_id=GROUP_ID, topic_id=TOPIC_ID, sort='desc', count=1)
        if response['count'] == 0:
            time.sleep(5)
            return
        self.last_comment_id = response['items'][0]['id']
        print('Set initial id to ' + str(self.last_comment_id))

    def get_comments(self):
        self.update_vk()

        if self.vk is None:
            return [], []

        response = self.vk.board.getComments(group_id=GROUP_ID, topic_id=TOPIC_ID,
                                             start_comment_id=self.last_comment_id, extended=1)

        return response['items'], response['profiles']

    def get_topic(self):
        self.update_vk()

        response = self.vk.board.getTopics(group_id=GROUP_ID, topic_ids=[TOPIC_ID])
        if response['count'] == 0:
            return None

        return response['items'][0]

    def run(self):
        while True:
            if self.last_comment_id == 0:
                self.update_last_comment_id()

            topic = self.get_topic()
            if topic is None:
                logging.warning('Topic not found')
                time.sleep(60)
                continue

            comments, profiles = self.get_comments()

            if len(comments) == 0:
                time.sleep(5)
                continue

            users = dict()

            for profile in profiles:
                users[profile['id']] = profile

            for comment in comments:
                id = comment['id']
                if id > self.last_comment_id:
                    self.last_comment_id = id
                    text = comment['text']
                    title = topic['title']
                    user_id = abs(comment['from_id'])
                    try:
                        user = users[user_id]
                        username = ' '.join([user['first_name'], user['last_name']])
                    except KeyError:
                        username = ''

                    date = comment['date']
                    message_date = '<!date^' + str(date) + '^Posted {date} {time}|Posted 2014-02-18 6:39:42>'
                    text = "\n".join(map(lambda s: ">" + s, text.split("\n")))
                    message = '>*' + title + '*\n>_' + username + '_ (' + message_date + ')\n' + text
                    slack.chat.post_message(channel=CHANNEL, text=message, username=USERNAME, icon_url=ICON_URL)
                    logging.info('Posted comment_id=%s\n%s', id, message)

if __name__ == '__main__':
    vts = Vts()
    try:
        while True:
            try:
                vts.run()
            except vk_api.requests.exceptions.ConnectionError:
                time.sleep(10)
    except KeyboardInterrupt:
        pass
