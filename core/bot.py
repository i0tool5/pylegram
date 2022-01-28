import requests


class Bot:
    def __init__(self, token: str, api_address: str = '', ):
        self._token: str = token
        self._api_address: str = api_address or 'https://api.telegram.org'
        self._bot_prefixed: str = f'bot{self._token}'

        f_link = f'{self._api_address}/file/{self._bot_prefixed}'
        addr = f'{self._api_address}/{self._bot_prefixed}'

        self._api_bot_address: str = addr
        self._api_file_download: str = f_link

    def get_updates(self, offset: int, limit: int, timeout: int):
        '''Long polling method to fetch updates from server
        For more information read Telegram API documentation for this method
        '''
        method_name = 'getUpdates'
        pars = {
            'offset': offset,
            'limit': limit,
            'timeout': timeout
        }
        response = requests.get(
            f'{self._api_bot_address}/{method_name}',
            params=pars)
        return response.json()

    def send_message(self, chat_id: str, text: str, parse_mode: str = "", **kwargs):
        method_name = 'sendMessage'
        data = {
            'chat_id': chat_id,
            'text': text,
        }

        if parse_mode:
            data['parse_mode'] = parse_mode

        data |= kwargs
        r = requests.post(
            f'{self._api_bot_address}/{method_name}', json=data)

        return r.json()

    def set_webhook(self, url: str, **kwargs) -> dict:
        ''' This method subscribes to a webhook to receive
        incoming updates through this webhook.
        **kwargs are arguments described in telegram documentation
        https://core.telegram.org/bots/api#setwebhook
        '''
        method_name = 'setWebhook'
        data = {'url': url}
        data |= kwargs
        # r = requests.post(
        #    f'{self._api_bot_address}/{method_name}', json=data)
        raise NotImplementedError

    def delete_webhook(self, drop_pending_updates: bool = False) -> dict:
        method_name = 'deleteWebhook'
        r = requests.post(
            f'{self._api_bot_address}/{method_name}',
            json={'drop_pending_updates': drop_pending_updates})
        return r.json()

    def get_file(self, file_id: str):
        ''' File size is limited to 20MB.
        '''
        method_name: str = 'getFile'
        # r = requests.post(f'{self._api_bot_address}/{method_name}', )
        ...

    def send_document(self, chat_id, ):
        ''' This method is used by bot to send general files.
        File size is limited to 50MB at this moment.
        '''
        method_name = ''
        ...
