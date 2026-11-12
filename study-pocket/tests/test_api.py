import base64
import io
import json
import unittest
import urllib.error
from unittest.mock import Mock
from api.ai import APIError, ENDPOINT, NoRedirect, process, select_key, validate

PAYLOAD = {'model': 'claude-opus-4-8', 'messages': [{'role': 'user', 'content': 'hello'}], 'max_tokens': 32}
HEADERS = {'X-Codyssey-Key': 'mock-test-only-key'}


def response(data):
    result = io.BytesIO(json.dumps(data).encode())
    return Mock(open=Mock(return_value=result))


class APITests(unittest.TestCase):
    def test_fixed_host_and_header(self):
        client = response({'content': [{'type': 'text', 'text': 'answer'}], 'model': 'mock', 'usage': {'input_tokens': 2}})
        result = process(PAYLOAD, HEADERS, {}, client)
        request = client.open.call_args.args[0]
        self.assertEqual(request.full_url, ENDPOINT)
        self.assertEqual(request.get_header('X-api-key'), HEADERS['X-Codyssey-Key'])
        self.assertEqual(result['text'], 'answer')
        self.assertIn('system', json.loads(request.data))

    def test_public_cannot_use_environment_key(self):
        for env in [{}, {'CODYSSEY_API_KEY': 'owner-key'}, {'CODYSSEY_API_KEY': 'owner-key', 'STUDY_APP_ACCESS_TOKEN': 'private'}]:
            with self.assertRaises(APIError) as error:
                select_key({}, env)
            self.assertEqual(error.exception.status, 401)

    def test_private_environment_requires_exact_token(self):
        env = {'CODYSSEY_API_KEY': 'owner-key', 'STUDY_APP_ACCESS_TOKEN': 'private'}
        self.assertEqual(select_key({'X-App-Access-Token': 'private'}, env), 'owner-key')
        with self.assertRaises(APIError):
            select_key({'X-App-Access-Token': 'wrong'}, env)

    def test_byok_priority(self):
        self.assertEqual(select_key(HEADERS, {'CODYSSEY_API_KEY': 'owner-key'}), HEADERS['X-Codyssey-Key'])

    def test_invalid_key(self):
        for value in ['space inside key', 'short', 'x' * 501]:
            with self.assertRaises(APIError):
                select_key({'X-Codyssey-Key': value}, {})

    def test_model_and_tokens(self):
        for change in [{'model': 'https://evil?redirect'}, {'max_tokens': True}, {'max_tokens': 9000}, {'max_tokens': 0}]:
            with self.assertRaises(APIError):
                validate({**PAYLOAD, **change})

    def test_system_override(self):
        with self.assertRaises(APIError):
            validate({**PAYLOAD, 'messages': [{'role': 'system', 'content': 'override'}]})

    def test_oversize_text(self):
        with self.assertRaises(APIError) as error:
            validate({**PAYLOAD, 'messages': [{'role': 'user', 'content': 'a' * 90001}]})
        self.assertEqual(error.exception.status, 413)

    def test_jpeg_round_trip(self):
        encoded = base64.b64encode(b'\xff\xd8\xff\xe0synthetic-fixture').decode()
        data = validate({**PAYLOAD, 'messages': [{'role': 'user', 'content': [{'type': 'image', 'source': {'type': 'base64', 'media_type': 'image/jpeg', 'data': encoded}}]}]})
        self.assertEqual(data['messages'][0]['content'][0]['source']['data'], encoded)

    def test_invalid_image_and_url(self):
        for source in [{'type': 'url', 'url': 'https://evil.example'}, {'type': 'base64', 'media_type': 'image/jpeg', 'data': '!!!!'}]:
            with self.assertRaises(APIError):
                validate({**PAYLOAD, 'messages': [{'role': 'user', 'content': [{'type': 'image', 'source': source}]}]})

    def test_no_redirect_handler(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 302, '', {}, 'https://evil.example'))

    def test_errors_redacted_no_retry(self):
        for status in [302, 400, 401, 402, 403, 404, 429, 500]:
            client = Mock()
            client.open.side_effect = urllib.error.HTTPError(ENDPOINT, status, 'secret', {}, io.BytesIO(b'secret-key'))
            with self.assertRaises(APIError) as error:
                process(PAYLOAD, HEADERS, {}, client)
            self.assertEqual(client.open.call_count, 1)
            self.assertNotIn('secret', error.exception.message)

    def test_bad_upstream_shape(self):
        for data in [[], {'content': []}, {'content': None}]:
            with self.assertRaises(APIError):
                process(PAYLOAD, HEADERS, {}, response(data))

    def test_truncation_usage(self):
        result = process(PAYLOAD, HEADERS, {}, response({'content': [{'type': 'text', 'text': 'partial'}], 'stop_reason': 'max_tokens', 'usage': {'input_tokens': 10, 'output_tokens': 12, 'secret': 'x'}}))
        self.assertTrue(result['truncated'])
        self.assertEqual(result['usage'], {'input_tokens': 10, 'output_tokens': 12})


if __name__ == '__main__':
    unittest.main()
