from requests import Session, get


class BaseApi:
    def __init__(self, api_base_url, session=Session()):
        self.api_base_url = api_base_url
        self.session = session

    def send_get(self, url='/'):
        try:
            response = get(url=f'{self.api_base_url}{url}', verify=False)
            return response
        except Exception as e:
            print('Непредвиденная ошибка:', e)

    def send_post(self, data=None, url='/'):
        if data is None:
            data = {}
        try:
            is_json = isinstance(data, dict)
            response = self.session.post(
                url=f'{self.api_base_url}{url}',
                json=data if is_json else None,
                data=None if is_json else data,
                verify=False
            )
            if response.content != '':
                return response
        except Exception as e:
            print('Непредвиденная ошибка:', e)