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
        self.bot = Bot('<bot_token_here>')

    def test_get_updates(self):
        r = self.bot.get_updates(0, 100, 0)
        pprint.pprint(r)

    def test_delete_webhook(self):
        r = self.bot.delete_webhook()
        self.assertEqual(r['ok'], True)
        self.assertTrue(r['result'])

    def test_send_message(self):
        r = self.bot.get_updates(0, 100, 0)
        pprint.pprint(r)
        result = classes.Result(r)
        print(result)
        self.assertNotEqual(0, len(result))


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
