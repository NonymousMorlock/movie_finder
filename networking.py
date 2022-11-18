import requests


class Networking:
    @staticmethod
    def get(url: str, **kw) -> requests.Response:
        response = requests.get(url=url, headers=kw.get("headers"), params=kw.get("params"))
        response.raise_for_status()
        return response

    @staticmethod
    def post(url: str, **kw) -> requests.Response:
        response = requests.post(url=url, headers=kw.get("headers"), json=kw.get("body"))
        response.raise_for_status()
        return response
