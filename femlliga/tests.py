from decimal import Decimal
from datetime import datetime

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from .models import *
from .constants import *
from .utils import date_intervals

AUTH_BACKENDS = settings.AUTHENTICATION_BACKENDS[1:]

class ResourcesTests(TestCase):
    def test_resource_types_match(self):
        for resource in RESOURCES:
            self.assertIn(resource[0], RESOURCE_ICONS_MAP)
            self.assertIn(resource[0], RESOURCE_OPTIONS_MAP)
            self.assertIn(resource[0], RESOURCE_NEED_DESCRIPTIONS)
            self.assertIn(resource[0], RESOURCE_OFFER_DESCRIPTIONS)

class OrganizationTests(TestCase):
    def test_disstance(self):
        p1 = (39.982639180269345, -0.030035858750823794)
        p2 = (39.96994470876123, 0.014310397939378215)
        p3 = (39.97577675810347, 0.01660298876575851)
        o1 = Organization(lat = Decimal(p1[0]), lng = Decimal(p1[1]))
        o2 = Organization(lat = Decimal(p2[0]), lng = Decimal(p2[1]))
        o3 = Organization(lat = Decimal(p3[0]), lng = Decimal(p3[1]))
        self.assertEqual(o1.distance(o2), 4.034916375924071)
        self.assertEqual(o1.distance(o3), 4.047659967585039)
        self.assertEqual(o2.distance(o3), 0.677473274790817)

class UtilsTests(TestCase):
    def test_date_intervals(self):
        start1 = datetime(year=2022, month=1, day=10, hour=10, minute=21)
        end1   = datetime(year=2022, month=1, day=10, hour=14, minute=21)
        end2   = datetime(year=2022, month=1, day=11, hour=14, minute=21)
        end3   = datetime(year=2022, month=2, day=12, hour=14, minute=21)
        end4   = datetime(year=2022, month=5, day=13, hour=12, minute=11)

        start01 = datetime(year=2022, month=1, day=10)
        end01   = datetime(year=2022, month=1, day=11)
        end02   = datetime(year=2022, month=1, day=12)
        mid01   = datetime(year=2022, month=1, day=17)
        mid02   = datetime(year=2022, month=1, day=24)
        mid03   = datetime(year=2022, month=1, day=31)
        mid04   = datetime(year=2022, month=2, day=7)
        end03   = datetime(year=2022, month=2, day=14)
        start02 = datetime(year=2022, month=1, day=1)
        mid05   = datetime(year=2022, month=2, day=1)
        mid06   = datetime(year=2022, month=3, day=1)
        mid07   = datetime(year=2022, month=4, day=1)
        mid08   = datetime(year=2022, month=5, day=1)
        end04   = datetime(year=2022, month=6, day=1)
        self.assertEqual(date_intervals(start1, end1), [start01, end01])
        self.assertEqual(date_intervals(start1, end2), [start01, end01, end02])
        self.assertEqual(date_intervals(start1, end3), [start01, mid01, mid02, mid03, mid04, end03])
        self.assertEqual(date_intervals(start1, end4), [start02, mid05, mid06, mid07, mid08, end04])

class SmokeTests(TestCase):
    fixtures = ["testdata.json"]

    def test_not_logged(self):
        URLS = [
            ("index", "Fem lliga! és una xarxa on les organitzacions", []),
            ("page", "és una xarxa on les organitzacions", ["faq"]),
            ("page", "Avís legal", ["legal"]),
            ("contact", "Si tens qualsevol pregunta o suggerència", []),
        ]
        for x in URLS:
            self.aux_get(x[0], x[1], args=x[2])

    def test_login_required(self):
        org, org2 = self.get_orgs()
        URLS = [
            ("app", []),
            ("add_organization", []),
            ("edit_organization", [org.id]),
            ("pre-wizard", [org.id]),
            ("mid-wizard", [org.id]),
            ("reset-wizard", [org.id]),
            ("resources-wizard", [org.id, "needs"]),
            ("force-resources-wizard", [org.id, "needs", "PLACE"]),
            ("send_message", [org.id, org2.id, "offer", "SERVICE"]),
            ("matches", [org.id]),
            ("agreements_sent", [org.id]),
            ("agreements_received", [org.id]),
            ("agreement_connect", [org.id, org.id]),
            ("agreement_successful", [org.id, org.id]),
            ("uploads", ["path"]),
            ("report", []),
        ]
        for x in URLS:
            self.aux_get(x[0], args=x[1], status_code=302)

    @override_settings(AUTHENTICATION_BACKENDS = AUTH_BACKENDS)
    def test_logged(self):
        self.client.login(email='test@example.com', password='passfortests')
        org, org2 = self.get_orgs()
        URLS = [
            ("app", "Example organization", []),
            ("force-resources-wizard", "Esteu buscant un local", [org.id, "needs", "PLACE"]),
            ("send_message", "Sol·licita Servei a Second example org", [org.id, org2.id, "offer", "SERVICE"]),
            ("matches", "Has lligat!", [org.id]),
            ("agreements_sent", "Encara no has enviat cap petició", [org.id]),
            ("agreements_received", "Encara no has rebut", [org.id]),
        ]
        for x in URLS:
            self.aux_get(x[0], x[1], args=x[2])

    @override_settings(AUTHENTICATION_BACKENDS = AUTH_BACKENDS)
    def test_logged_error(self):
        self.client.login(email='test@example.com', password='passfortests')
        org, org2 = self.get_orgs()
        self.aux_get("edit_organization", args=[org2.id], status_code=403)

    def aux_get(self, url, contains="", args=[], status_code=200):
        full_url = reverse(url, args=args)
        response = self.client.get(full_url)
        self.assertEqual(response.status_code, status_code, msg=url)
        if contains != "":
            self.assertContains(response, contains, msg_prefix=url)

    def get_orgs(self):
        org = get_user_model().objects.get(email='test@example.com').organizations.all()[0]
        org2 = get_user_model().objects.get(email='test2@example.com').organizations.all()[0]
        return org, org2

class ComponentTests(TestCase):
    fixtures = ["testdata.json"]

    def test_contact(self):
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse("contact"), {})
        self.assertContains(response, "Aquest camp és obligatori", count=2)
        self.assertEqual(len(mail.outbox), 0)

        content = "Email test content"
        response = self.client.post(reverse("contact"), {"email": "test@example.com", "content": content})
        self.assertContains(response, "Gràcies per enviar el missatge! Et respondrem tan aviat com puguem", count=1)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn("S'ha rebut un contacte a la web", mail.outbox[0].subject)
        self.assertIn("s'ha enviat correctament", mail.outbox[1].subject)

class IntegrationTests(TestCase):
    fixtures = ["testdata.json"]

    # TODO test the full interaction of a new user
    def test_happy_path(self):
        pass
