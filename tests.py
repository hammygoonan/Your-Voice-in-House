import os
import json
import yvih
import unittest
import tempfile

class YvihTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, yvih.app.config['DATABASE'] = tempfile.mkstemp()
        yvih.app.config['TESTING'] = True
        self.app = yvih.app.test_client()
        #yvih.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(yvih.app.config['DATABASE'])

    def test_home_displays_api(self):
        rv = self.app.get('/')
        assert 'Your Voice in House API' in rv.data

    # def test_members_displays_content(self):
    #     rv = self.app.get('/members/')
    #     assert 'Members' in rv.data
    # def test_members_json(self):
    #     headers = [('Content-Type', 'application/json')]
    #     resp = self.app.get('/members/', headers=headers)
    #     data = json.loads(resp.data)
    #     assert isinstance(data, dict)


if __name__ == '__main__':
    unittest.main()
