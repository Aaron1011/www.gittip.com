import datetime

from mock import patch
import pytz

from gittip.testing import GITHUB_USER_UNREGISTERED_LGTEST, Harness
from gittip.testing.client import TestClient

class TestPages(Harness):
    def setUp(self):
        super(Harness, self).setUp()
        self.client = TestClient()

    def get(self, url, returning='body'):
        request = self.client.get(url)
        return getattr(request, returning)

    def test_homepage(self):
        actual = self.client.get('/').body
        expected = "Sustainable Crowdfunding"
        assert expected in actual, actual

    def test_profile(self):
        self.make_participant('cheese',
                              claimed_time=datetime.datetime.now(pytz.utc))
        expected = "I'm grateful for gifts"
        actual = self.get('/cheese/')
        assert expected in actual, actual

    def test_widget(self):
        self.make_participant('cheese',
                              claimed_time=datetime.datetime.now(pytz.utc))
        expected = "javascript: window.open"
        actual = self.get('/cheese/widget.html')
        assert expected in actual, actual

    def test_bank_account(self):
        expected = "add<br> or change your bank account"
        actual = self.get('/bank-account.html')
        assert expected in actual, actual

    def test_credit_card(self):
        expected = "add<br> or change your credit card"
        actual = self.get('/credit-card.html')
        assert expected in actual, actual

    def test_github_associate(self):
        expected = "Bad request, program!"
        actual = self.get('/on/github/associate')
        assert expected in actual, actual

    def test_twitter_associate(self):
        expected = "Bad request, program!"
        actual = self.get('/on/twitter/associate')
        assert expected in actual, actual

    def test_about(self):
        expected = "small weekly cash gifts"
        actual = self.get('/about/')
        assert expected in actual, actual

    def test_about_stats(self):
        expected = "have joined Gittip"
        actual = self.get('/about/stats.html')
        assert expected in actual, actual

    def test_about_charts(self):
        expected = "Money transferred"
        actual = self.get('/about/charts.html')
        assert expected in actual, actual

    @patch('gittip.elsewhere.github.requests')
    def test_github_proxy(self, requests):
        requests.get().status_code = 200
        requests.get().text = GITHUB_USER_UNREGISTERED_LGTEST
        expected = "lgtest has not joined"
        actual = self.get('/on/github/lgtest/')
        assert expected in actual, actual

    # This hits the network. XXX add a knob to skip this
    def test_twitter_proxy(self):
        expected = "Twitter has not joined"
        actual = self.get('/on/twitter/twitter/')
        assert expected in actual, actual
