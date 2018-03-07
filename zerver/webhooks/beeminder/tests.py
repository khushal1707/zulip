# -*- coding: utf-8 -*-
from unittest.mock import patch
from typing import Text, Any
from zerver.lib.test_classes import WebhookTestCase

class BeeminderHookTests(WebhookTestCase):
    STREAM_NAME = 'beeminder'
    URL_TEMPLATE = u"/api/v1/external/beeminder?api_key={api_key}&email=AARON@zulip.com"

    @patch('zerver.webhooks.beeminder.view.time.time')
    def test_beeminder_derail(self, time: Any) -> None:
        time.return_value = 1517739100  # 5.6 hours from fixture value
        expected_subject = u"beekeeper"
        expected_message = '\n'.join([
            'Hello **aaron**! I am the Beeminder bot! :octopus:',
            ' You are going to derail from goal **gainweight** in **{:0.1f} hours**'.format(5.6),
            ' You need **+2 in 7 days (60)** to avoid derailing',
            ' * Pledge: **0$** :relieved:'
        ])

        self.send_and_test_stream_message('derail',
                                          expected_subject,
                                          expected_message,
                                          content_type="application/x-www-form-urlencoded")

    @patch('zerver.webhooks.beeminder.view.time.time')
    def test_beeminder_derail_pm(self, time: Any) -> None:
        time.return_value = 1517739100  # 5.6 hours from fixture value
        self.url = self.build_webhook_url(
            email="AARON@zulip.com",
            username="aaron",
            user_ip="127.0.0.1"
        )
        expected_message = '\n'.join([
            'I am the Beeminder bot! :octopus:',
            ' You are going to derail from goal **gainweight** in **{:0.1f} hours**'.format(5.6),
            ' You need **+2 in 7 days (60)** to avoid derailing',
            ' * Pledge: **5$**:worried:'
        ])
        self.send_and_test_private_message('derail_pm',
                                           expected_message,
                                           content_type="application/json")

    def get_body(self, fixture_name: Text) -> Text:
        return self.fixture_data("beeminder", fixture_name, file_type="json")
