import time

from collections.abc import Mapping


class Update:
    ''' Telegram update event
    '''
    def __init__(self, tg_response: dict):
        self.update_id: int = tg_response.pop('update_id')
        self._type: str = ''
        self.object: Message | None = None
        for k in tg_response.keys():
            self._type = k
            self.object = Message(tg_response.get(k, {}))

    @property
    def u_type(self) -> str:
        return self._type

    def __repr__(self) -> str:
        return f'<Update:{self._type} {self.update_id}>'


class Result:
    ''' Result of Telegram update event
    '''
    def __init__(self, tg_result: dict):
        updates = [
            upd for upd in tg_result['result']
        ]

        self.updates = [Update(upd) for upd in updates]

    def __repr__(self) -> str:
        return f'<Result [{len(self.updates)}]>'

    def __len__(self) -> int:
        return len(self.updates)

    def __getitem__(self, key: int) -> Update:
        return self.updates[key]


class User:
    def __init__(self, tg_user: dict):
        self.id: int = tg_user.get('id', 0)
        self.is_bot: bool = tg_user.get('is_bot', False)
        self.first_name: str = tg_user.get('first_name', '')
        self.last_name: str = tg_user.get('last_name', '')
        self.username: str = tg_user.get('username', '')
        self.language_code: str = tg_user.get('language_code', '')

    def __str__(self):
        return self.username


class Chat:
    def __init__(self, tg_chat: dict):
        self.id: str = str(tg_chat.get('id', 0))

        self.type: str = tg_chat.get('type', '')

        self.title: str = tg_chat.get('title', '')
        self.first_name: str = tg_chat.get('first_name', '')
        self.last_name: str = tg_chat.get('last_name', '')
        self.username: str = tg_chat.get('username', '')

        self.all_members_are_administrators: bool = tg_chat.get(
            'all_members_are_administrators', False)

    def __str__(self):
        s = f'{self.title} {self.username} {self.first_name} {self.last_name}'
        return s.strip()

    def __repr__(self):
        return f'<Chat(id={self.id},type={self.type}>'


class Document:
    ''' Document class represents two telegram objects:
    File and Document. Documentation for this types can be found at
    https://core.telegram.org/bots/api#file
    and
    https://core.telegram.org/bots/api#document
    respectively
    '''
    def __init__(self, tg_document: dict):
        self.file_id: str = tg_document.get('file_id', '')
        self.file_unique_id: str = tg_document.get('file_unique_id', '')
        self.file_name: str = tg_document.get('file_name', '')
        self.mime_type: str = tg_document.get('mime_type', '')
        self.file_size: int = tg_document.get('file_size', 0)
        # File type fields
        self.file_path = tg_document.get('file_path', '')

    def __str__(self):
        return self.file_name

    def __repr__(self):
        return f'<File: {self.file_name} {self.file_size}bytes>'


class MessageEntity:
    def __init__(self, tg_msg_entity: Mapping):
        self.type: str = tg_msg_entity.get('type', '')
        self.offset: int = tg_msg_entity.get('offset', 0)
        self.length: int = tg_msg_entity.get('length', 0)
        self.language: str = tg_msg_entity.get('language', '')

    def __repr__(self):
        return f'<Entity {self.type}>'


class Message:
    def __init__(self, tg_message: Mapping):
        self.message_id: int = tg_message.get('message_id', 0)

        self.from_: User | None = None  # optional field
        if (usr := tg_message.get('from')) is not None:
            self.from_ = User(usr)

        self.chat: Chat | None = None
        if (chat := tg_message.get('chat')) is not None:
            self.chat = Chat(chat)

        self.text: str = tg_message.get('text', '')
        self.date: int = tg_message.get('date', 0)

        self.document: Document | None = None
        if (doc := tg_message.get('document')) is not None:
            self.document = Document(doc)

        ents = tg_message.get('entities', [])
        self.entities: list[MessageEntity] = [MessageEntity(me) for me in ents]

        self.caption: str = tg_message.get('caption', '')  # optional field
        c_ents = tg_message.get('caption_entities', [])
        self.caption_entities: list[MessageEntity] = [
            MessageEntity(me) for me in c_ents]  # optional field

    @property
    def sender(self) -> str:
        '''This method returns username of the User in `from_` variable.
        '''
        if self.from_ is not None:
            return self.from_.username
        return ''

    def get_date(self) -> str:
        '''Returns date of this message in string format
        '''
        return time.ctime(self.date)

    def entities_count(self) -> int:
        return len(self.entities)

    def caption_entities_count(self) -> int:
        return len(self.caption_entities)

    def entity_type(self):
        entities = self.entities + self.caption_entities

        if len(entities) == 1:
            return entities[0].type
        elif len(entities) > 1:
            t = entities[0].type
            for ent in entities:
                if ent.type != t:
                    raise Exception(
                        'multiple entities with different types')
            return t
        else:
            raise TgEntityException('no entities')

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.text or self.caption

    def __repr__(self):
        return f'<Message {self.message_id} at {self.get_date()}>'


class TgEntityException(Exception):
    ...
