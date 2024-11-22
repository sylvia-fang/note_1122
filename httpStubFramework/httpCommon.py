import threading
import requests


class HttpCommon:
    def __init__(self):
        self.res = None
        self.status_code = None
        self.res_text = None

    def target_http_func(self, **kwargs):
        self.res = requests.request(**kwargs)
        self.status_code = self.res.status_code
        self.res_text = self.res.text

    def thread_run_requests(self, **kwargs):
        """支持http协议请求时的多线程等待"""
        t = threading.Thread(target=self.target_http_func, kwargs=kwargs)
        t.start()
