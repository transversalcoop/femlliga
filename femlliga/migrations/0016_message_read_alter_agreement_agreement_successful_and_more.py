# Generated by Django 5.0.6 on 2024-05-27 08:49

from django.db import migrations, models

import femlliga.constants as consts


def create_resource_options(apps, schema_editor):
    ResourceOption = apps.get_model("femlliga", "ResourceOption")
    for option in consts.RESOURCE_OPTIONS:
        ResourceOption.objects.get_or_create(name=option[0])


def migrate_resource_options(apps, schema_editor):
    ResourceOption = apps.get_model("femlliga", "ResourceOption")
    Agreement = apps.get_model("femlliga", "Agreement")
    Need = apps.get_model("femlliga", "Need")
    Offer = apps.get_model("femlliga", "Offer")
    # Agreement, Need, Offer

    origin_1 = []
    for option in [
        "SOUND_SYSTEM_ACOUSTIC",
        "SOUND_SYSTEM_CONCERT",
        "PROJECTOR",
        "STAGE",
    ]:
        try:
            origin_1.append(ResourceOption.objects.get(name=option))
        except:
            pass

    destination_1, _ = ResourceOption.objects.get_or_create(name="EQUIPMENT_EVENTS")

    origin_2 = []
    for option in ["DISHES"]:
        try:
            origin_2.append(ResourceOption.objects.get(name=option))
        except:
            pass
    destination_2, _ = ResourceOption.objects.get_or_create(name="KITCHEN_EQUIPMENT")

    for a in Agreement.objects.all():
        merge_resource_options(a, origin_1, destination_1)
        merge_resource_options(a, origin_2, destination_2)

    for n in Need.objects.all():
        merge_resource_options(n, origin_1, destination_1)
        merge_resource_options(n, origin_2, destination_2)

    for o in Offer.objects.all():
        merge_resource_options(o, origin_1, destination_1)
        merge_resource_options(o, origin_2, destination_2)


def merge_resource_options(resource, origin, destination):
    has_option = any([o in resource.options.all() for o in origin])
    if has_option:
        resource.options.add(destination)


def delete_resource_options(apps, schema_editor):
    ResourceOption = apps.get_model("femlliga", "ResourceOption")
    options = set()
    for option in consts.RESOURCE_OPTIONS:
        options.add(option[0])

    for ro in ResourceOption.objects.all():
        if ro.name not in options:
            ro.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("femlliga", "0015_agreement_origin"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="read",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="agreement",
            name="agreement_successful",
            field=models.BooleanField(
                null=True, verbose_name="S'ha realitzat l'intercanvi"
            ),
        ),
        migrations.AlterField(
            model_name="agreement",
            name="resource",
            field=models.CharField(
                choices=[
                    ("PLACE", "Local"),
                    ("TRAINING", "Formació"),
                    ("SERVICE", "Servei"),
                    ("EQUIPMENT", "Materials"),
                    ("ALLIANCES", "Aliances"),
                    ("OTHER", "Altres"),
                ],
                max_length=100,
                verbose_name="Recurs",
            ),
        ),
        migrations.AlterField(
            model_name="agreement",
            name="successful_date",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="Intercanvi registrat el"
            ),
        ),
        migrations.AlterField(
            model_name="need",
            name="resource",
            field=models.CharField(
                choices=[
                    ("PLACE", "Local"),
                    ("TRAINING", "Formació"),
                    ("SERVICE", "Servei"),
                    ("EQUIPMENT", "Materials"),
                    ("ALLIANCES", "Aliances"),
                    ("OTHER", "Altres"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="offer",
            name="resource",
            field=models.CharField(
                choices=[
                    ("PLACE", "Local"),
                    ("TRAINING", "Formació"),
                    ("SERVICE", "Servei"),
                    ("EQUIPMENT", "Materials"),
                    ("ALLIANCES", "Aliances"),
                    ("OTHER", "Altres"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="org_type",
            field=models.CharField(
                choices=[
                    ("ASSOCIATION", "Associació"),
                    ("COOPERATIVE", "Cooperativa"),
                    ("NONPROFIT_COOPERATIVE", "Cooperativa sense ànim de lucre"),
                    ("FOUNDATION", "Fundació"),
                    ("LABOR_SOCIETY", "Societat laboral"),
                    ("MUTUALITY", "Mutualitat"),
                    ("INSERTION_COMPANY", "Empresa d'inserció"),
                    ("SPECIAL_WORK_CENTER", "Centre especial de treball"),
                    ("PUBLIC_PRIVATE_BASED", "Entitat pública de base privada"),
                ],
                max_length=100,
            ),
        ),
        migrations.AlterField(
            model_name="organizationscope",
            name="name",
            field=models.CharField(
                choices=[
                    ("EQUALITY", "Dona/Igualtat/Feminismes"),
                    ("EDUCATION", "Educació"),
                    ("OLDER_PEOPLE", "Persones majors"),
                    ("NEIGHBORHOOD", "Veïnal"),
                    ("SPORTS", "Activitat física i esportiva"),
                    ("CULTURE", "Cultura, patrimoni, territori, llengua..."),
                    ("YOUTH", "Infància, adolescència i joventut"),
                    ("SOCIAL_ASSISTANCE", "Benestar social"),
                    ("COOPERATION", "Cooperació i sensibilització"),
                    ("ENVIRONMENT", "Medi ambient i mobilitat sostenible"),
                    ("TRADITIONS", "Festa i tradicions"),
                    ("RELIGIOUS", "Religiosa"),
                    (
                        "PARTICIPATION",
                        "Participació ciutadana i dinamització comunitària",
                    ),
                    ("DESIGN", "Disseny i comunicació"),
                    ("TRAINING", "Formació i recerca"),
                    ("HOUSING", "Habitatge i gestió de l'entorn"),
                    ("FOOD", "Alimentació, restauració i hosteleria"),
                    ("LOGISTICS", "Logística i subministraments"),
                    ("FINANCE", "Finançament i Moneda Social"),
                    ("PRODUCTION", "Producció"),
                    ("TRADE", "Comerç"),
                    ("HEALTH", "Salut i Cures"),
                    ("TECHNOLOGY", "Tecnologia i electrònica"),
                    ("TEXTILE", "Textil"),
                    ("ACCESSIBILITY", "Accessibilitat"),
                    ("FUNCTIONAL_DIVERSITY", "Diversitat funcional"),
                    ("OTHER", "Altres"),
                ],
                max_length=100,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.AlterField(
            model_name="resourceoption",
            name="name",
            field=models.CharField(
                choices=[
                    ("DAILY_USAGE", "Ús diari"),
                    ("PUNCTUAL_USAGE", "Ús puntual"),
                    ("PUNCTUAL_MEETINGS", "Puntualment per a reunions"),
                    ("PUNCTUAL_EVENTS", "Puntualment per a actes"),
                    ("TRAINING_DIGITAL", "Digitalització"),
                    ("TRAINING_BUREAUCRACY", "Relacions amb l'administració"),
                    ("TRAINING_EQUALITY", "Igualtat i Feminismes"),
                    ("TRAINING_ENERGY_SAVING", "Eficiència i estalvi energètic"),
                    ("TRAINING_HISTORICAL_MEMORY", "Memòria històrica"),
                    ("TRAINING_ARTS", "Arts i cultura"),
                    ("TRAINING_PROJECTS", "Redacció de projectes"),
                    ("COMMUNITY_MANAGER", "Comunicació"),
                    ("INSURANCE", "Assegurances"),
                    ("AGENCY", "Gestoria"),
                    ("PROJECT_WRITING", "Redacció de projectes"),
                    ("DIGITAL_BUREAUCRACY", "Relacions digitals amb l'administració"),
                    ("SERVICE_PARTICIPATION", "Participació"),
                    ("SERVICE_REPAIR", "Reparació, manteniment i reutilització"),
                    (
                        "EQUIPMENT_EVENTS",
                        "Material d'esdeveniments, fires i exposicions",
                    ),
                    ("VEHICLE", "Vehicle"),
                    ("CHAIRS_TABLES", "Mobiliari"),
                    ("KITCHEN_EQUIPMENT", "Material de cuina"),
                    ("CAMPING_EQUIPMENT", "Material d'acampada"),
                    ("EQUIPMENT_DIY", "Material de bricolatge"),
                    ("EQUIPMENT_SPORTS", "Material esportiu"),
                    ("EQUIPMENT_EDUCATION", "Material pedagògic i de sensibilització"),
                    ("PROJECT_COLLABORATION", "Col·laboració en projectes"),
                    ("VOLUNTEERING", "Voluntariat"),
                ],
                max_length=100,
                primary_key=True,
                serialize=False,
            ),
        ),
        migrations.RunPython(
            create_resource_options, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            migrate_resource_options, reverse_code=migrations.RunPython.noop
        ),
        migrations.RunPython(
            delete_resource_options, reverse_code=migrations.RunPython.noop
        ),
    ]