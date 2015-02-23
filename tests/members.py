from urllib import quote
from base import BaseTestCase

class MembersTestCase(BaseTestCase):

    def test_home_displays_api(self):
        response = self.client.get('/')
        self.assertIn('Your Voice in House API', response.data)

    def test_non_get_method(self):
        response = self.client.post('/')
        self.assert405(response)

    def test_member_html(self):
        response = self.client.get('/members/')
        self.assertIn('Members', response.data)

    def test_member_json(self):
        headers = [('Accept', 'application/json')]
        response = self.client.get('/members/', headers=headers)
        self.assertIsInstance(response.json, dict)
        self.assertIn('members', response.json)

    def test_member_fields(self):
        response = self.client.get('/members/id/1')
        self.assert200(response)
        response = self.client.get('/members/id/non-numeric')
        self.assert400(response)
        response = self.client.get('/members/first_name/Kate')
        self.assert200(response)
        response = self.client.get('/members/second_name/Smith')
        self.assert200(response)
        response = self.client.get('/members/first_name/Smith')
        self.assert404(response)
        response = self.client.get('/members/id/999999')
        self.assert404(response)
        response = self.client.get('/members/test/thing')
        self.assert400(response)
        response = self.client.get('/members/first_name/Tony/role/immigration')
        self.assert200(response)
        url = quote('/members/role/The Nationals in the Senate')
        response = self.client.get(url)
        self.assert200(response)

    def test_member_fields_json(self):
        headers = [('Accept', 'application/json')]
        response = self.client.get('/members/id/1', headers=headers)
        self.assert200(response)
        response = self.client.get('/members/id/non-numeric', headers=headers)
        self.assert400(response)
        response = self.client.get('/members/first_name/Kate', headers=headers)
        self.assert200(response)
        response = self.client.get('/members/second_name/Smith', headers=headers)
        self.assert200(response)
        response = self.client.get('/members/first_name/Smith', headers=headers)
        self.assert404(response)
        response = self.client.get('/members/id/999999', headers=headers)
        self.assert404(response)
        response = self.client.get('/members/test/thing', headers=headers)
        self.assert400(response)
        response = self.client.get('/members/first_name/Tony/role/immigration', headers=headers)
        self.assert200(response)
        url = quote('/members/role/The Nationals in the Senate')
        response = self.client.get(url)
        self.assert200(response)
        response = self.client.get('/members/id/1/id/2', headers=headers)
        self.assert200(response)
        self.assertTrue(len(response.json['members']) == 2)


if __name__ == '__main__':
    unittest.main()
