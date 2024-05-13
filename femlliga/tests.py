from datetime import datetime, timedelta
from decimal import Decimal

from allauth.account.models import EmailAddress
from bs4 import BeautifulSoup
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse

from .constants import *
from .models import *
from .utils import (
    get_ordered_needs_and_offers,
    get_periodic_notification_data,
    send_periodic_notification,
)

AUTH_BACKENDS = settings.AUTHENTICATION_BACKENDS[1:]
PASS_FOR_TESTS = "passfortests"


# helper for visualizing response page when test fails
def save_response(response):
    with open("/tmp/tmp.html", "w") as f:
        f.write(str(response.content.decode("utf-8")))


def save_email(mail, filename):
    with open("/tmp/" + filename, "w") as f:
        f.write(mail.body)


class ResourcesTests(TestCase):
    def test_resource_types_match(self):
        for resource in RESOURCES:
            self.assertIn(resource[0], RESOURCE_ICONS_MAP)
            self.assertIn(resource[0], RESOURCE_OPTIONS_MAP)


class OrganizationTests(TestCase):
    def test_distance(self):
        p1 = (39.982639180269345, -0.030035858750823794)
        p2 = (39.96994470876123, 0.014310397939378215)
        p3 = (39.97577675810347, 0.01660298876575851)
        o1 = Organization(lat=Decimal(p1[0]), lng=Decimal(p1[1]))
        o2 = Organization(lat=Decimal(p2[0]), lng=Decimal(p2[1]))
        o3 = Organization(lat=Decimal(p3[0]), lng=Decimal(p3[1]))
        self.assertEqual(o1.distance(o2), 4.034916375924071)
        self.assertEqual(o1.distance(o3), 4.047659967585039)
        self.assertEqual(o2.distance(o3), 0.677473274790817)


class UtilsTests(TestCase):
    def test_date_intervals(self):
        start1 = datetime(year=2022, month=1, day=10, hour=10, minute=21)
        end1 = datetime(year=2022, month=1, day=10, hour=14, minute=21)
        end2 = datetime(year=2022, month=1, day=11, hour=14, minute=21)
        end3 = datetime(year=2022, month=2, day=12, hour=14, minute=21)
        end4 = datetime(year=2022, month=5, day=13, hour=12, minute=11)

        start01 = datetime(year=2022, month=1, day=10)
        end01 = datetime(year=2022, month=1, day=11)
        end02 = datetime(year=2022, month=1, day=12)
        mid01 = datetime(year=2022, month=1, day=17)
        mid02 = datetime(year=2022, month=1, day=24)
        mid03 = datetime(year=2022, month=1, day=31)
        mid04 = datetime(year=2022, month=2, day=7)
        end03 = datetime(year=2022, month=2, day=14)
        start02 = datetime(year=2022, month=1, day=1)
        mid05 = datetime(year=2022, month=2, day=1)
        mid06 = datetime(year=2022, month=3, day=1)
        mid07 = datetime(year=2022, month=4, day=1)
        mid08 = datetime(year=2022, month=5, day=1)
        end04 = datetime(year=2022, month=6, day=1)
        self.assertEqual(date_intervals(start1, end1), [start01, end01])
        self.assertEqual(date_intervals(start1, end2), [start01, end01, end02])
        self.assertEqual(
            date_intervals(start1, end3), [start01, mid01, mid02, mid03, mid04, end03]
        )
        self.assertEqual(
            date_intervals(start1, end4), [start02, mid05, mid06, mid07, mid08, end04]
        )


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

    @override_settings(AUTHENTICATION_BACKENDS=AUTH_BACKENDS)
    def test_logged(self):
        self.client.login(email="test@example.com", password=PASS_FOR_TESTS)
        org, org2 = self.get_orgs()
        URLS = [
            ("app", "Example organization", []),
            ("force-resources-wizard", "Local", [org.id, "needs", "PLACE"]),
            ("matches", "Has lligat!", [org.id]),
            ("agreements", "Encara no heu enviat ni rebut peticions", [org.id]),
        ]
        for x in URLS:
            self.aux_get(x[0], x[1], args=x[2])

    @override_settings(AUTHENTICATION_BACKENDS=AUTH_BACKENDS)
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
        org = (
            get_user_model()
            .objects.get(email="test@example.com")
            .organizations.all()[0]
        )
        org2 = (
            get_user_model()
            .objects.get(email="test2@example.com")
            .organizations.all()[0]
        )
        return org, org2


class ComponentTests(TestCase):
    fixtures = ["testdata.json"]

    def test_contact(self):
        self.assertEqual(len(mail.outbox), 0)

        response = self.client.post(reverse("contact"), {})
        self.assertContains(response, "Aquest camp és obligatori", count=2)
        self.assertEqual(len(mail.outbox), 0)

        content = "Email test content"
        response = self.client.post(
            reverse("contact"),
            {
                "email": "test@example.com",
                "content": content,
                "g-recaptcha-response": "test",
            },
        )
        self.assertContains(
            response,
            "Gràcies per enviar el missatge! Et respondrem tan aviat com puguem",
            count=1,
        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn("S'ha rebut un contacte a la web", mail.outbox[0].subject)
        self.assertIn("s'ha enviat correctament", mail.outbox[1].subject)
        save_email(mail.outbox[0], "contact0.html")
        save_email(mail.outbox[1], "contact1.html")


class IntegrationTests(TestCase):
    maxDiff = None
    fixtures = ["testdata.json"]

    def aux_wizard(self, url, resource, options, comments, contains, charge=False):
        params = {
            "resource": resource,
            "options": options,
            "comments": comments,
            "images-TOTAL_FORMS": 6,
            "images-INITIAL_FORMS": 0,
        }
        if charge:
            params["charge"] = "on"
        response = self.client.post(url, params, follow=True)
        save_response(response)
        self.assertContains(response, contains)

    def aux_create_org(self, name, email):
        self.client.logout()
        # signup
        response = self.client.post(
            reverse("account_signup"),
            {
                "email": email,
                "password1": PASS_FOR_TESTS,
                "password2": PASS_FOR_TESTS,
                "g-recaptcha-response": "test",
            },
            follow=True,
        )
        save_response(response)
        self.assertContains(response, "Verifica el correu electrònic")
        self.assertEqual(1, len(mail.outbox))
        save_email(mail.outbox[0], "email_verification.html")
        mail.outbox.clear()
        e = EmailAddress.objects.get(email=email)
        e.verified = True
        e.save()

        self.client.login(email=email, password=PASS_FOR_TESTS)

        # add organization
        response = self.client.get(reverse("app"), follow=True)
        self.assertContains(
            response, "Sembla que encara no heu donat d'alta cap entitat"
        )

        response = self.client.post(
            reverse("add_organization"),
            {
                "name": name,
                "description": "Descripció entitat de test",
                "social_media-0-media_type": "INSTAGRAM",
                "social_media-0-value": "usuari_instagram_de_test",
                "social_media-TOTAL_FORMS": "6",
                "social_media-INITIAL_FORMS": "0",
                "org_type": "ASSOCIATION",
                "scopes": ["EQUALITY", "EDUCATION"],
                "lat": "40.000",
                "lng": "0.100",
            },
            follow=True,
        )
        save_response(response)
        self.assertContains(
            response, "preguntes sobre els recursos que teniu o necessiteu"
        )
        return Organization.objects.get(name=name)

    @override_settings(AUTHENTICATION_BACKENDS=AUTH_BACKENDS)
    def test_happy_path(self):
        org_name = "Nom entitat de test"
        email3 = "test3@example.com"
        o = self.aux_create_org(org_name, email3)

        # needs wizard
        response = self.client.post(
            reverse("pre-wizard", args=[o.id]), {"start": "yes"}, follow=True
        )
        self.assertContains(response, "Local")

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "PLACE"])
        self.aux_wizard(
            needs_url,
            "PLACE",
            ["DAILY_USAGE", "PUNCTUAL_USAGE"],
            "comentaris de necessita local de test",
            "Formació",
        )

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "TRAINING"])
        self.aux_wizard(
            needs_url,
            "TRAINING",
            ["TRAINING_DIGITAL"],
            "comentaris de necessita formació de test",
            "Servei",
        )

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "SERVICE"])
        self.aux_wizard(
            needs_url,
            "SERVICE",
            ["AGENCY"],
            "comentaris de necessita servei de test",
            "Equipaments",
        )

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "EQUIPMENT"])
        self.aux_wizard(needs_url, "EQUIPMENT", [], "", "Aliances")

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "ALLIANCES"])
        self.aux_wizard(needs_url, "ALLIANCES", [], "", "Altres")

        needs_url = reverse("resources-wizard", args=[o.id, "needs", "OTHER"])
        self.aux_wizard(
            needs_url,
            "OTHER",
            [],
            "comentaris de necessita altres de test",
            "Ja vas per la meitat",
        )

        # offers wizard
        response = self.client.post(
            reverse("mid-wizard", args=[o.id]), {"start": "yes"}, follow=True
        )
        self.assertContains(response, "Local")

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "PLACE"])
        self.aux_wizard(
            offers_url, "PLACE", [], "comentaris de ofereix local de test", "Formació"
        )

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "TRAINING"])
        self.aux_wizard(
            offers_url,
            "TRAINING",
            ["TRAINING_DIGITAL"],
            "comentaris de ofereix formació de test",
            "Servei",
        )

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "SERVICE"])
        self.aux_wizard(
            offers_url,
            "SERVICE",
            [],
            "comentaris de ofereix serveis de test",
            "Equipaments",
            charge=True,
        )

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "EQUIPMENT"])
        self.aux_wizard(offers_url, "EQUIPMENT", [], "", "Aliances", charge=True)

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "ALLIANCES"])
        self.aux_wizard(offers_url, "ALLIANCES", [], "", "Altres", charge=True)

        offers_url = reverse("resources-wizard", args=[o.id, "offers", "OTHER"])
        self.aux_wizard(
            offers_url,
            "OTHER",
            [],
            "comentaris de ofereix altres de test",
            "Has acabat d'introduir la informació de la teua organització",
            charge=True,
        )

        # matches page
        response = self.client.get(reverse("matches", args=[o.id]))
        for s in [
            "Has lligat!",
            "Local",
            "Second example organization",
        ]:
            self.assertContains(response, s)

        self.assertNotContains(response, "Example organization")  # too far away

        matches = BeautifulSoup(response.content.decode(), "html.parser").find(
            "script", {"id": "django-json-data"}
        )
        for s in ["PLACE", "Servei", "Formació", "Equipaments", "Altres"]:
            self.assertNotIn(s, matches)

        # app main page
        response = self.client.get(reverse("app"))
        save_response(response)
        should_contain = [
            org_name,
            "Local",
            "Servei",
            "Formació",
            "Equipaments",
            "Altres",
            "comentaris de necessita local de test",
            "comentaris de necessita servei de test",
            "comentaris de necessita formació de test",
            "comentaris de ofereix formació de test",
            "comentaris de ofereix altres de test",
            "Producte o servei remunerat",
            "comentaris de necessita altres de test",
            "comentaris de ofereix local de test",
            "comentaris de ofereix serveis de test",
            "bi-book-half",
        ]
        for s in should_contain:
            self.assertContains(response, s)
        for s in [
            "bi-gear-fill",
        ]:
            self.assertNotContains(response, s)

        response = self.client.get(reverse("profile", args=[o.id]))
        should_contain = [
            "Descripció entitat de test",
            "Instagram",
            "usuari_instagram_de_test",
            "Associació",
            "Dona/Igualtat/Feminismes",
        ]
        for s in should_contain:
            self.assertContains(response, s)

        # view organization page
        response = self.client.get(reverse("view_organization", args=[o.id]))
        for s in should_contain[:6]:
            self.assertContains(response, s)

        # send message
        o2 = Organization.objects.get(name="Second example organization")
        o2.creator.accept_communications_automatically = False
        o2.creator.save()
        send_message_url = reverse("send_message", args=[o.id, o2.id, "offer", "PLACE"])
        test_msg_1 = "missatge de test per al primer missatge"
        response = self.client.post(
            send_message_url,
            {
                "options": ["DAILY_USAGE", "PUNCTUAL_USAGE"],
                "message": test_msg_1,
            },
        )
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 1)

        # check received
        self.client.login(email="test2@example.com", password=PASS_FOR_TESTS)
        response = self.client.get(reverse("agreements", args=[o2.id]))
        for s in ["Peticions enviades i rebudes", test_msg_1]:
            self.assertContains(response, s)

        a = Agreement.objects.get(solicitor=o, solicitee=o2)
        response = self.client.post(
            reverse("agreement_connect", args=[o2.id, a.id]),
            {
                "return_url": "received",
                "connect": "yes",
            },
            follow=True,
        )
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 2)
        save_email(mail.outbox[1], "agreement_connect.html")

        # check sent
        self.client.login(email=email3, password=PASS_FOR_TESTS)
        response = self.client.get(reverse("agreements", args=[o.id]))
        save_response(response)
        for s in [test_msg_1, '"communication_accepted": true']:
            self.assertContains(response, s)

        response = self.client.post(
            reverse("agreement_successful", args=[o.id, a.id]),
            {
                "return_url": "sent",
                "successful": "yes",
            },
            follow=True,
        )
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 2)

    def aux_send_message(self, o1_id, o2_id):
        send_message_url = reverse(
            "send_message", args=[o1_id, o2_id, "offer", "PLACE"]
        )
        response = self.client.post(
            send_message_url,
            {
                "options": ["DAILY_USAGE", "PUNCTUAL_USAGE"],
                "message": "test message",
            },
        )
        save_response(response)

    @override_settings(AUTHENTICATION_BACKENDS=AUTH_BACKENDS)
    def test_deleted_organizations(self):
        email4 = "test4@example.com"
        email5 = "test5@example.com"
        org1 = self.aux_create_org("Nom entitat de test 4", email4)
        org2 = self.aux_create_org("Nom entitat de test 5", email5)
        Offer.objects.create(resource="PLACE", organization=org1)
        Offer.objects.create(resource="PLACE", organization=org2)

        o1id, o2id = org1.id, org2.id
        self.client.login(email=email5, password=PASS_FOR_TESTS)
        self.aux_send_message(o2id, o1id)

        self.client.login(email=email4, password=PASS_FOR_TESTS)
        self.aux_send_message(o1id, o2id)
        self.assertEqual(Agreement.objects.filter(solicitor=org1).count(), 1)
        self.assertEqual(Agreement.objects.filter(solicitee=org1).count(), 1)

        org2.delete()  # delete org so Agreement's have None fields

        # org2 deleted, no new message is sent
        self.aux_send_message(o1id, o2id)
        self.assertEqual(Agreement.objects.filter(solicitor=org1).count(), 1)

        self.client.get(reverse("agreements", args=[o1id]))
        self.client.get(reverse("matches", args=[o1id]))
        self.client.get(reverse("search", args=[o1id]))

    @override_settings(AUTHENTICATION_BACKENDS=AUTH_BACKENDS)
    def test_immediate_notifications(self):
        email6 = "test6@example.com"
        email7 = "test7@example.com"
        org2 = self.aux_create_org("Nom entitat de test 7", email7)
        org1 = self.aux_create_org("Nom entitat de test 6", email6)
        user1 = CustomUser.objects.get(email=email6)
        user2 = CustomUser.objects.get(email=email7)
        user1.notify_immediate_communications_rejected = False
        user1.save()
        user2.accept_communications_automatically = False
        user2.notify_immediate_communications_received = False
        user2.save()
        offer = Offer.objects.create(
            organization=org2,
            resource="PLACE",
            has_resource=True,
        )
        option, _ = ResourceOption.objects.get_or_create(name="DAILY_USAGE")
        offer.options.add(option)

        send_message_url = reverse(
            "send_message", args=[org1.id, org2.id, "offer", "PLACE"]
        )
        test_msg_1 = "missatge de test per al primer missatge"
        response = self.client.post(
            send_message_url,
            {
                "options": ["DAILY_USAGE", "PUNCTUAL_USAGE"],
                "message": test_msg_1,
            },
        )
        save_response(response)
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 0)

        self.client.login(email=email7, password=PASS_FOR_TESTS)
        a = Agreement.objects.filter(solicitee=org2).first()
        connect_url = reverse("agreement_connect", args=[org2.id, a.id])
        response = self.client.post(
            connect_url,
            {
                "connect": "no",
            },
        )
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 0)

        # activate immediate notifications and check they are received
        a.delete()  # delete previous agreement to make simpler next queries
        user1.notify_immediate_communications_rejected = True
        user1.save()
        user2.notify_immediate_communications_received = True
        user2.save()

        self.client.login(email=email6, password=PASS_FOR_TESTS)
        test_msg_2 = "missatge de test per al segon missatge"
        response = self.client.post(
            send_message_url,
            {
                "options": ["DAILY_USAGE", "PUNCTUAL_USAGE"],
                "message": test_msg_2,
            },
        )
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 1)
        save_email(mail.outbox[0], "notify_communication_received.html")
        self.assertIn("T'han enviat una petició per compartir", mail.outbox[0].subject)

        self.client.login(email=email7, password=PASS_FOR_TESTS)
        a = Agreement.objects.filter(solicitee=org2).first()
        connect_url = reverse("agreement_connect", args=[org2.id, a.id])
        response = self.client.post(
            connect_url,
            {
                "connect": "no",
            },
        )
        self.assertJSONEqual(response.content, {"ok": True})
        self.assertEqual(len(mail.outbox), 2)
        save_email(mail.outbox[1], "notify_communication_rejected.html")
        self.assertIn("Us han declinat una petició", mail.outbox[1].subject)

    @override_settings(AUTHENTICATION_BACKENDS=AUTH_BACKENDS)
    def test_periodic_notifications(self):
        org3 = self.aux_create_org("Nom entitat de test 10", "test10@example.com")
        org2 = self.aux_create_org("Nom entitat de test 9", "test9@example.com")
        org1 = self.aux_create_org("Nom entitat de test 8", "test8@example.com")

        Need.objects.all().delete()
        Offer.objects.all().delete()
        self.aux_create_resource(Need, org1, "PLACE", ["DAILY_USAGE", "PUNCTUAL_USAGE"])
        self.aux_create_resource(Need, org1, "TRAINING", ["TRAINING_DIGITAL"])
        self.aux_create_resource(Need, org2, "PLACE", ["DAILY_USAGE"])
        self.aux_create_resource(
            Offer, org2, "PLACE", ["DAILY_USAGE", "PUNCTUAL_USAGE"]
        )
        self.aux_create_resource(
            Offer, org3, "PLACE", ["PUNCTUAL_MEETINGS", "PUNCTUAL_EVENTS"]
        )
        self.aux_create_resource(
            Offer, org2, "TRAINING", ["TRAINING_DIGITAL", "TRAINING_BUREAUCRACY"]
        )
        self.aux_create_resource(
            Offer, org3, "TRAINING", ["TRAINING_DIGITAL", "TRAINING_EQUALITY"]
        )

        org1.creator.last_notification_date = timezone.now() - timedelta(days=30 * 12)
        org1.creator.last_long_notification_date = timezone.now() - timedelta(
            days=30 * 12
        )
        a1 = Agreement.objects.create(
            solicitor=org2,
            solicitee=org1,
            resource="PLACE",
        )
        a2 = Agreement.objects.create(
            solicitor=org1,
            solicitee=org2,
            resource="PLACE",
            communication_accepted=True,
        )

        needs, offers = get_ordered_needs_and_offers(org1, 100)
        site = Site.objects.first()
        context = get_periodic_notification_data(site, org1.creator, needs, offers)
        self.assertEqual(
            context,
            {
                "current_site": site,
                "send_long_notification": True,
                "agreement_communication_pending": {
                    "agreements": [a1],
                    "total_agreements": 1,
                },
                "agreement_success_pending": {
                    "organization": org1,
                    "agreements": [a2],
                    "total_agreements": 1,
                },
                "matches": {
                    "need": {"name": "local per a ús diari", "count": 1},
                    "offer": {"name": "formació en digitalització", "count": 2},
                },
                "new_resources": {
                    "resources": [
                        {
                            "code": "PLACE",
                            "options": [
                                ResourceOption.objects.get(name="PUNCTUAL_EVENTS"),
                                ResourceOption.objects.get(name="PUNCTUAL_MEETINGS"),
                            ],
                        },
                        {
                            "code": "TRAINING",
                            "options": [
                                ResourceOption.objects.get(name="TRAINING_BUREAUCRACY"),
                                ResourceOption.objects.get(name="TRAINING_EQUALITY"),
                            ],
                        },
                    ],
                },
            },
        )
        send_periodic_notification(
            "subject",
            "email/periodic_notification.html",
            org1.creator,
            context,
        )
        self.assertEqual(len(mail.outbox), 1)
        save_email(mail.outbox[0], "periodic_notification.html")
        for s in [
            "Us han fet una petició de col·laboració...",
            "Heu arribat a fer l'intercanvi finalment?",
            "Possibles lligues",
            "Novetats a la plataforma",
        ]:
            self.assertIn(s, mail.outbox[0].body)

    def aux_create_resource(self, model, org, resource, options):
        offer = model.objects.create(
            organization=org,
            resource=resource,
            has_resource=True,
        )
        for option in options:
            ro, _ = ResourceOption.objects.get_or_create(name=option)
            offer.options.add(ro)
