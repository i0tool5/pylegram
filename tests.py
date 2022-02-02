import os
import json
import unittest
import pprint

import core.classes as classes

from core.bot import Bot
from core import formatting


TEST_RESPONSE = '''
{"ok": true,
    "result": [{"message": {"chat": {"first_name": "Alex",
                                     "id": 584874747,
                                     "type": "private",
                                     "username": "UserName"},
                            "date": 1631468558,
                            "entities": [{"length": 13,
                                          "offset": 0,
                                          "type": "bot_command"}],
                            "from": {"first_name": "Alex",
                                     "id": 584874747,
                                     "is_bot": false,
                                     "language_code": "ru",
                                     "username": "UserName"},
                            "message_id": 42,
                            "text": "/some_command"},
                "update_id": 112638473},
               {"message": {"chat": {"all_members_are_administrators": true,
                                     "id": -551169338,
                                     "title": "closed",
                                     "type": "group"},
                            "date": 1631468568,
                            "entities": [{"length": 13,
                                          "offset": 0,
                                          "type": "bot_command"}],
                            "from": {"first_name": "Alex",
                                     "id": 584874747,
                                     "is_bot": false,
                                     "language_code": "ru",
                                     "username": "UserName"},
                            "message_id": 43,
                            "text": "/chat_command"},
                "update_id": 112638474}]}
'''


class TestDecodeResponse(unittest.TestCase):
    def setUp(self):
        data = json.loads(TEST_RESPONSE)
        self.result: classes.Result = classes.Result(data['result'])

    def test_decode(self):
        for update in self.result:
            msg = update.message
            self.assertNotEqual(len(msg), 0)

    def test_update(self):
        upd = self.result[0]
        self.assertEqual(upd.update_id, 112638473)
        upd = self.result[1]
        self.assertEqual(upd.update_id, 112638474)

    def test_message(self):
        upd = self.result[0]
        msg = upd.message
        self.assertEqual(msg.entity_type, "bot_command")
        self.assertEqual(msg.get_date(), 'Sun Sep 12 20:42:38 2021')


class TestBot(unittest.TestCase):
    def setUp(self):
        bt = os.environ['BOT_TOKEN']
        self.bot = Bot(bt)

    def test_get_updates(self):
        r = self.bot.get_updates(0, 100, 0)
        result = classes.Result(r)
        self.assertGreater(len(result), 0)
        for upd in result:
            if upd.u_type == 'message':
                break
        print(upd.object.sender)

    def test_delete_webhook(self):
        r = self.bot.delete_webhook()
        self.assertEqual(r['ok'], True)
        self.assertTrue(r['result'])

    def test_send_message(self):
        r = self.bot.get_updates(0, 100, 0)
        result = classes.Result(r)
        self.assertNotEqual(0, len(result))

        try:
            upd = result[0]
        except IndexError:
            raise   # hmm...

        resp = self.bot.send_message(
            upd.object.chat.id,
            "Test message for {}".format(upd.object.sender)
        )
        pprint.pprint(resp)
        msg = classes.Message(resp['result'])
        self.assertTrue(msg.from_.is_bot)

    def test_command_message(self):
        r = self.bot.get_updates(0, 100, 0)
        result = classes.Result(r)
        self.assertGreater(len(result), 0)

        for upd in result:
            message = upd.object
            try:
                if message.entity_type() == 'bot_command':
                    self.assertTrue(str(message).startswith('/'))
                    print(message)
            except classes.TgEntityException:
                continue

    def test_document(self):
        r = self.bot.get_updates(0, 100, 0)
        result = classes.Result(r)
        self.assertGreater(len(result), 0)

        for upd in result:
            message = upd.object
            if (doc := message.document) is not None:
                print(repr(doc))
                self.assertNotEqual(doc.file_id, '')
                self.assertNotEqual(doc.file_name, '')
                self.assertNotEqual(doc.mime_type, '')
                self.assertNotEqual(doc.file_size, 0)


class TestFormats(unittest.TestCase):
    def test_check_formats(self):
        self.assertEqual(
            formatting.MODE_MARKDOWNV2, 'MarkdownV2')
        self.assertEqual(
            formatting.MODE_HTML, 'HTML')
        self.assertEqual(
            formatting.MODE_MARKDOWN, 'Markdown')


if __name__ == '__main__':
    unittest.main()
