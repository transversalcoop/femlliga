# Generated by Django 5.0.6 on 2024-08-06 14:39

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

    destinations = []
    for option in ["PUNCTUAL_MEETINGS", "PUNCTUAL_EVENTS"]:
        d, _ = ResourceOption.objects.get_or_create(name=option)
        destinations.append(d)

    for a in Agreement.objects.all():
        translate_resource_options(a, "PUNCTUAL_USAGE", destinations)

    for n in Need.objects.all():
        translate_resource_options(n, "PUNCTUAL_USAGE", destinations)

    for o in Offer.objects.all():
        translate_resource_options(o, "PUNCTUAL_USAGE", destinations)


def translate_resource_options(resource, origin, destinations):
    if origin in [x.name for x in resource.options.all()]:
        for d in destinations:
            resource.options.add(d)


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
        ("femlliga", "0019_excludecommentword"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resourceoption",
            name="name",
            field=models.CharField(
                choices=[
                    ("DAILY_USAGE", "Espai de treball d'oficina"),
                    ("PUNCTUAL_MEETINGS", "Espai per a reunions"),
                    ("PUNCTUAL_EVENTS", "Espai per a actes"),
                    ("PLACE_TRAINING", "Aula de formació"),
                    ("PLACE_WORKSHOP", "Taller"),
                    ("PLACE_WAREHOUSE", "Magatzem"),
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
                    ("PUBLICITY", "Difusió"),
                    ("MONEY", "Suport econòmic"),
                    ("USERS_REFERRAL", "Derivació d'usuàries"),
                    ("SUPPORT_GROUPS", "Xarxes i grups de suport"),
                    ("COMMON_STRATEGY", "Estratègia i protocols conjunts"),
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