import requests

class Bot:
    def __init__(self, token: str, api_address: str = '', ):
        self._token: str = token
        self._api_address: str = api_address or 'https://api.telegram.org'
        self._bot_prefixed: str = f'bot{self._token}'

        fd = f'{self._api_address}/file/{self._bot_prefixed}'
        self._api_bot_address: str = f'{self._api_address}/{self._bot_prefixed}'
        self._api_file_download: str = fd

        # raise NotImplementedError(
        #     f'{self.__class__.__name__} is not implemented')
    
    def get_updates(self, offset: int, limit: int, timeout: int):
        '''Long polling method to fetch updates from server
        For more information read Telegram API documentation for this method
        '''
        method_name = 'getUpdates'
        print(self._api_bot_address)
        response = requests.get(f'{self._api_bot_address}/{method_name}')
        print(response.status_code)
        return response.json()

    def send_message(self, chat_id: str, text: str):
        raise NotImplementedError

    def set_webhook(self, url: str, ):
        ''' This method subscribes to a webhook to receive 
        incoming updates through this webhook
        '''
        raise NotImplementedError
    
    def delete_webhook(self):
        raise NotImplementedError
