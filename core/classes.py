import time


class Update:
    def __init__(self, tg_response: dict):
        self.update_id: int = tg_response.get('update_id', 0)
        self.message: Message = Message(tg_response.get('message', None))
        self.channel_post: Message = Message(tg_response.get('message', None))
    
    def __repr__(self):
        return f'<Update {self.update_id}>'


class Result:
    def __init__(self, tg_result):
        self.updates = [Update(upd) for upd in tg_result]
    
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


class Chat:
    def __init__(self, tg_chat: dict):
        self.id: str = str(tg_chat.get('id', 0))

        self.type: str = tg_chat.get('type', '')

        self.title: str = tg_chat.get('title', '')
        self.first_name: str = tg_chat.get('first_name', '')
        self.last_name: str = tg_chat.get('last_name', '')
        self.username: str = tg_chat.get('username', '')

        all_members_are_administrators: bool = tg_chat.get(
            'all_members_are_administrators', False)

    def __str__(self):
        s = f'{self.title} {self.username} {self.first_name} {self.last_name}'
        return s.strip()

    def __repr__(self):
        return f'<Chat(id={self.id},type={self.type}>'


class Document:
    def __init__(self, tg_document: dict):
        self.file_id: str = tg_document.get('file_id', '')
        self.file_unique_id: str = tg_document.get('file_unique_id', '')
        self.file_name: str = tg_document.get('file_name', '')
        self.mime_type: str = tg_document.get('mime_type', '')
        self.file_size: int = tg_document.get('file_size', 0)


class MessageEntity:
    def __init__(self, tg_msg_entity: dict):
        self.type: str = tg_msg_entity.get('type', '')
        self.offset: int = tg_msg_entity.get('offset', 0)
        self.length: int = tg_msg_entity.get('length', 0)
        self.language: str = tg_msg_entity.get('language', '')
    
    def __repr__(self):
        return f'<Entity {self.type}>'


class Message:
    def __init__(self, tg_message: dict):
        self.message_id: int = tg_message.get('message_id', 0)
        self.from_: User = User(tg_message.get('from', {}))  # optional field

        self.chat: Chat = Chat(tg_message.get('chat'))

        self.text: str = tg_message.get('text', '')
        self.date: int = tg_message.get('date', 0)

        self.document: Document = Document(tg_message.get('document', {}))
        
        ents = tg_message.get('entities', [])
        self.entities: list[MessageEntity] = [MessageEntity(me) for me in ents]
        
        self.caption: str = tg_message.get('caption', '')  # optional field
        c_ents = tg_message.get('caption_entities', [])
        self.caption_entities: list[MessageEntity] = [
            MessageEntity(me) for me in c_ents]  # optional field

    @property
    def sender(self):
        '''This method returns username of the User in `from_` variable.
        '''
        return self.from_.username

    def get_date(self) -> str:
        '''Returns date of this message in string format
        '''
        return time.ctime(self.date)

    def entities_count(self) -> int:
        return len(self.entities)

    def caption_entities_count(self) -> int:
        return len(self.caption_entities)

    @property
    def entity_type(self):
        if self.entities_count() == 1:
            return self.entities[0].type
        elif self.entities_count() > 1:
            t = self.entities[0].type
            for ent in self.entities:
                if ent.type != t:
                    raise Exception(
                        'multiple entities with different types')
            return t
        else:
            raise Exception('no entities')

    def __len__(self):
        return len(self.text)

    def __str__(self):
        return self.text

    def __repr__(self):
        return f'<Message {self.message_id} at {self.get_date()}>'
