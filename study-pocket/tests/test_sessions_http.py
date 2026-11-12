import http.cookiejar
import json
import os
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from unittest.mock import patch
from api.ai import handler, select_key, validate


class SessionHTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = patch.dict(os.environ, {'CODYSSEY_API_KEY':'mock-http-server-key','STUDY_APP_ACCESS_TOKEN':'mock-http-access-' + 'z' * 40})
        cls.env.start()
        def fake_ai(data, headers):
            validate(data)
            select_key(headers, os.environ)
            return {'text':'mock answer','model':'mock','usage':{},'truncated':False}
        cls.model = patch('api.ai.process', side_effect=fake_ai)
        cls.model.start()
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),handler)
        cls.base=f'http://127.0.0.1:{cls.server.server_port}'
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown(); cls.server.server_close(); cls.thread.join()
        cls.model.stop();cls.env.stop()

    def setUp(self):
        self.cookies=http.cookiejar.CookieJar()
        self.client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))

    def request(self, data=None, origin=None, path='/api/ai'):
        headers={'Content-Type':'application/json','Origin':origin or self.base} if data is not None else {}
        request=urllib.request.Request(self.base+path,data=json.dumps(data).encode() if data is not None else None,headers=headers)
        try:
            with self.client.open(request,timeout=5) as response:
                return response.status,response.headers,json.load(response)
        except urllib.error.HTTPError as error:
            with error:
                return error.code,error.headers,json.load(error)

    def test_login_reload_ai_and_logout_over_http(self):
        status,_,body=self.request(); self.assertEqual(status,200); self.assertFalse(body['authenticated'])
        status,headers,body=self.request({'action':'login','access_code':os.environ['STUDY_APP_ACCESS_TOKEN']})
        self.assertEqual(status,200);self.assertTrue(body['authenticated']);self.assertIn('HttpOnly',headers['Set-Cookie'])
        self.client=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookies))
        self.assertTrue(self.request()[2]['authenticated'])
        status,_,body=self.request({'messages':[{'role':'user','content':'test'}],'max_tokens':32})
        self.assertEqual(status,200);self.assertEqual(body['text'],'mock answer')
        self.assertFalse(self.request({'action':'logout'})[2]['authenticated'])
        self.assertFalse(self.request()[2]['authenticated'])
        self.assertEqual(self.request({'messages':[{'role':'user','content':'test'}]})[0],401)

    def test_wrong_code_and_foreign_origin_cannot_login(self):
        self.assertEqual(self.request({'action':'login','access_code':'wrong'})[0],401)
        self.assertEqual(self.request({'action':'login','access_code':os.environ['STUDY_APP_ACCESS_TOKEN']},origin='https://foreign.example')[0],403)
        self.assertFalse(self.request()[2]['authenticated'])

    def test_unknown_action_and_source_url_are_rejected(self):
        self.assertEqual(self.request({'action':'unknown'})[0],400)
        self.assertEqual(self.request(path='/api/ai.py')[0],404)


if __name__=='__main__':
    unittest.main()
