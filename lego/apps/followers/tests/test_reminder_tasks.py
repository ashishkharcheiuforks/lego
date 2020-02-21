from datetime import timedelta
from unittest import mock
from unittest.mock import patch

from django.conf import settings
from django.utils import timezone

from lego.apps.events.models import Event, Pool
from lego.apps.events.tests.utils import get_dummy_users
from lego.apps.followers.notifications import RegistrationReminderNotification
from lego.apps.followers.tasks import send_registration_reminder_mail
from lego.apps.users.models import AbakusGroup, User
from lego.utils.test_utils import BaseTestCase
from lego.apps.followers.models import FollowEvent


@mock.patch("lego.apps.followers.tasks.RegistrationReminderNotification.notify")
class RegistrationReminderTestCase(BaseTestCase):
    fixtures = [
        "test_abakus_groups.yaml",
        "test_users.yaml",
        "test_companies.yaml",
        "test_events.yaml",
    ]

    def setUp(self):
        Pool.objects.all().update(
            activation_date=timezone.now() + timedelta(hours=2), name="Webkom"
        )
        self.recipient = get_dummy_users(1)[0]
        AbakusGroup.objects.get(name="Webkom").add_user(self.recipient)
        self.pool = Pool.objects.first()
        self.notifier = RegistrationReminderNotification(
            self.recipient, event=self.pool.event
        )

    def test_follows_registration_under_one_hour(self, mock_notification):
        current_time = timezone.now()
        self.pool.activation_date = current_time + timedelta(minutes=45)
        self.pool.save()
        FollowEvent.objects.get_or_create(
            follower=self.recipient, target=self.pool.event
        )
        send_registration_reminder_mail.delay()
        mock_notification.assert_called()

    def test_follows_registration_over_one_hour(self, mock_notification):
        current_time = timezone.now()
        self.pool.activation_date = current_time + timedelta(minutes=75)
        self.pool.save()
        FollowEvent.objects.get_or_create(
            follower=self.recipient, target=self.pool.event
        )
        send_registration_reminder_mail.delay()
        mock_notification.assert_not_called()

    def test_not_follows_registration_under_one_hour(self, mock_notification):
        current_time = timezone.now()
        self.pool.activation_date = current_time + timedelta(minutes=45)
        self.pool.save()

        send_registration_reminder_mail.delay()
        mock_notification.assert_not_called()

