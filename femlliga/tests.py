from decimal import Decimal
from datetime import datetime

from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied

from bs4 import BeautifulSoup
from allauth.account.models import EmailAddress

from .models import *
from .constants import *
from .utils import date_intervals

AUTH_BACKENDS = settings.AUTHENTICATION_BACKENDS[1:]
PASS_FOR_TESTS = "passfortests"

# helper for visualizing response page when test fails
def save_response(response):
    with open('/tmp/tmp.html', 'w') as f:
        f.write(str(response.content.decode("utf-8")))

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
            ("account_login", "Inicia sessió", []),
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
            ("resources-wizard", [org.id, "needs", "PLACE"]),
            ("force-resources-wizard", [org.id, "needs", "PLACE"]),
            ("send_message", [org.id, org2.id, "offer", "SERVICE"]),
            ("matches", [org.id]),
            ("agreements", [org.id]),
            ("agreement_connect", [org.id, org.id]),
            ("agreement_successful", [org.id, org.id]),
            ("uploads", ["path"]),
            ("report", []),
        ]
        for x in URLS:
            self.aux_get(x[0], args=x[1], status_code=302)

    @override_settings(AUTHENTICATION_BACKENDS = AUTH_BACKENDS)
    def test_logged(self):
        self.client.login(email="test@example.com", password=PASS_FOR_TESTS)
        org, org2 = self.get_orgs()
        URLS = [
            ("app", "Example organization", []),
            ("force-resources-wizard", "Esteu buscant un local", [org.id, "needs", "PLACE"]),
            ("matches", "Has lligat!", [org.id]),
            ("agreements", "Encara no heu enviat ni rebut peticions", [org.id]),
        ]
        for x in URLS:
            self.aux_get(x[0], x[1], args=x[2])

    @override_settings(AUTHENTICATION_BACKENDS = AUTH_BACKENDS)
    def test_logged_error(self):
        self.client.login(email="test@example.com", password=PASS_FOR_TESTS)
        org, org2 = self.get_orgs()
        self.aux_get("edit_organization", args=[org2.id], status_code=403)

    def aux_get(self, url, contains=None, args=[], status_code=200):
        full_url = reverse(url, args=args)
        response = self.client.get(full_url)

        self.assertEqual(response.status_code, status_code, msg=url)
        if isinstance(contains, str):
            self.assertContains(response, contains, msg_prefix=url)
        elif isinstance(contains, list):
            for s in contains:
                self.assertContains(response, s, msg_prefix=url)

    def get_orgs(self):
        org = get_user_model().objects.get(email="test@example.com").organizations.all()[0]
        org2 = get_user_model().objects.get(email="test2@example.com").organizations.all()[0]
        return org, org2

class ComponentTests(TestCase):
    fixtures = ["testdata.json"]

    def test_contact(self):
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse("contact"), {})
        self.assertContains(response, "Aquest camp és obligatori", count=2)
        self.assertEqual(len(mail.outbox), 0)

        content = "Email test content"
        response = self.client.post(reverse("contact"), {
            "email": "test@example.com",
            "content": content,
            "g-recaptcha-response": "test",
        })
        self.assertContains(response, "Gràcies per enviar el missatge! Et respondrem tan aviat com puguem", count=1)
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn("S'ha rebut un contacte a la web", mail.outbox[0].subject)
        self.assertIn("s'ha enviat correctament", mail.outbox[1].subject)

class IntegrationTests(TestCase):
    fixtures = ["testdata.json"]

    def aux_wizard(self, url, resource, options, comments, has_resource, contains, charge=False):
        params = {
            "resource": resource,
            "options": options,
            "comments": comments,
            "has_resource": has_resource,
        }
        if charge:
            params["charge"] = "on"
        response = self.client.post(url, params, follow=True)
        self.assertContains(response, contains)

    @override_settings(AUTHENTICATION_BACKENDS = AUTH_BACKENDS)
    def test_happy_path(self):
        # signup
        response = self.client.post(reverse("account_signup"), {
            "email": "test3@example.com",
            "password1": PASS_FOR_TESTS,
            "password2": PASS_FOR_TESTS,
            "g-recaptcha-response": "test",
        }, follow=True)
        self.assertContains(response, "Verifica el correu electrònic")
        e = EmailAddress.objects.get(email="test3@example.com")
        e.verified = True
        e.save()
        self.client.login(email="test3@example.com", password=PASS_FOR_TESTS)

        # add organization
        response = self.client.get(reverse("app"), follow=True)
        self.assertContains(response, "Sembla que encara no heu donat d'alta cap entitat")

        response = self.client.post(reverse("add_organization"), {
            "name": "Nom entitat de test",
            "description": "Descripció entitat de test",
            "social_media-0-media_type": "INSTAGRAM",
            "social_media-0-value": "usuari_instagram_de_test",
            "social_media-TOTAL_FORMS": "6",
            "social_media-INITIAL_FORMS": "0",
            "org_type": "ASSOCIATION",
            "scopes": ["EQUALITY", "EDUCATION"],
            "lat": "40.000",
            "lng": "1.000",
        }, follow=True)
        self.assertContains(response, "preguntes sobre els recursos que teniu o necessiteu")
        o = Organization.objects.get(name="Nom entitat de test")

        # needs wizard
        response = self.client.post(reverse("pre-wizard", args=[o.id]), {"start": "yes"}, follow=True)
        self.assertContains(response, "Esteu buscant un local on poder desenvolupar")

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "PLACE"])
        self.aux_wizard(needs_url, "PLACE", ["DAILY_USAGE", "PUNCTUAL_USAGE"], "comentaris de necessita local de test", "yes",
            "Voleu rebre formació en algun d&#39;aquests temes")

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "TRAINING"])
        self.aux_wizard(needs_url, "TRAINING", ["TRAINING_DIGITAL"], "comentaris de necessita formació de test", "yes",
            "Esteu buscant algú que us proporcione aquests serveis")

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "SERVICE"])
        self.aux_wizard(needs_url, "SERVICE", ["AGENCY"], "comentaris de necessita servei de test", "yes",
            "Necessiteu alguna d&#39;aquestes coses")

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "EQUIPMENT"])
        self.aux_wizard(needs_url, "EQUIPMENT", [], "comentaris de necessita material de test", "no",
            "Podeu indicar qualsevol altra necessitat que tingueu")

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "OTHER"])
        self.aux_wizard(needs_url, "OTHER", [], "comentaris de necessita altres de test", "no",
            "Ja vas per la meitat")

        # offers wizard
        response = self.client.post(reverse("mid-wizard", args=[o.id]), {"start": "yes"}, follow=True)
        self.assertContains(response, "Teniu un local que estigueu disposats a compartir amb altres entitats")

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "PLACE"])
        self.aux_wizard(offers_url, "PLACE", [], "comentaris de ofereix local de test", "no",
            "Oferiu formació en algun d&#39;aquests temes")

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "TRAINING"])
        self.aux_wizard(offers_url, "TRAINING", ["TRAINING_DIGITAL"], "comentaris de ofereix formació de test", "yes",
            "Oferiu algun d&#39;aquests serveis per a altres entitats")

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "SERVICE"])
        self.aux_wizard(offers_url, "SERVICE", [], "comentaris de ofereix serveis de test", "no",
            "Teniu alguna d&#39;aquestes coses que pugueu compartir", charge = True)

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "EQUIPMENT"])
        self.aux_wizard(offers_url, "EQUIPMENT", [], "comentaris de ofereix material de test", "yes",
            "Podeu indicar qualsevol altre servei o material que oferiu", charge = True)

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "OTHER"])
        self.aux_wizard(offers_url, "OTHER", [], "comentaris de ofereix altres de test", "yes",
            "Has acabat d'introduir la informació de la teua associació", charge = True)

        # matches page
        response = self.client.post(reverse("post-wizard", args=[o.id]), {"start": "yes"}, follow=True)
        for s in [
            "Has lligat!",
            "Local",
            "Second example organization",
        ]:
            self.assertContains(response, s)

        matches = BeautifulSoup(response.content.decode(), "html.parser").find("script", {"id": "matches-data"})
        for s in ["PLACE", "Servei", "Formació", "Equipaments", "Altres"]:
            self.assertNotIn(s, matches)

        # app main page
        response = self.client.get(reverse("app"))
        should_contain = [
            "Nom entitat de test",
            "Descripció entitat de test",
            "Instagram",
            "usuari_instagram_de_test",
            "Associació",
            "Dona/Igualtat/Feminismes",
            "Local",
            "Servei",
            "Formació",
            "Equipaments",
            "Altres",
            "comentaris de necessita local de test",
            "comentaris de necessita servei de test",
            "comentaris de necessita formació de test",
            "comentaris de ofereix formació de test",
            "comentaris de ofereix material de test",
            "comentaris de ofereix altres de test",
            "Es demana remuneració a canvi",
        ]
        for s in should_contain:
            self.assertContains(response, s)
        for s in [
            "comentaris de necessita material de test",
            "comentaris de necessita altres de test",
            "comentaris de ofereix local de test",
            "comentaris de ofereix serveis de test",
        ]:
            self.assertNotContains(response, s)

        # view organization page
        response = self.client.get(reverse("view_organization", args=[o.id]))
        for s in should_contain[:6]:
            self.assertContains(response, s)

        # send message
        o2 = Organization.objects.get(name="Second example organization")
        send_message_url = reverse("send_message", args=[o.id, o2.id, "offer", "PLACE"])
        test_msg_1 =  "missatge de test per al primer missatge"
        response = self.client.post(send_message_url, {
            "options": ["DAILY_USAGE", "PUNCTUAL_USAGE"],
            "message": test_msg_1,
        }, follow=True)
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 1)

        # check received
        self.client.login(email="test2@example.com", password=PASS_FOR_TESTS)
        response = self.client.get(reverse("agreements", args=[o2.id]))
        for s in ["Peticions enviades i rebudes", test_msg_1]:
            self.assertContains(response, s)

        a = Agreement.objects.get(solicitor=o, solicitee=o2)
        response = self.client.post(reverse("agreement_connect", args=[o2.id, a.id]), {
            "return_url": "received",
            "connect": "yes",
        }, follow=True)
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 2)

        # check sent
        self.client.login(email="test3@example.com", password=PASS_FOR_TESTS)
        response = self.client.get(reverse("agreements", args=[o.id]))
        save_response(response)
        for s in [test_msg_1, '"communication_accepted": true']:
            self.assertContains(response, s)

        response = self.client.post(reverse("agreement_successful", args=[o.id, a.id]), {
            "return_url": "sent",
            "successful": "yes",
        }, follow=True)
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 2)

