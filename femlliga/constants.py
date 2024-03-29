APP_NAME = "Fem lliga!"
FROM_EMAIL = f"{APP_NAME} <no-reply@femlliga.org>"

NOTIFICATION_CHOICES = [
    ("DAILY", "Diàriament"),
    ("WEEKLY", "Setmanalment"),
    ("NEVER", "Mai"),
]

SOCIAL_MEDIA_TYPES = [
    ("EMAIL", "Correu electrònic"),
    ("WEBSITE", "Lloc web"),
    ("FACEBOOK", "Facebook"),
    ("INSTAGRAM", "Instagram"),
    ("TWITTER", "Twitter"),
    ("LINKEDIN", "Linkedin"),
    ("WHATSAPP", "Whatsapp"),
    # TODO add phone
]

SOCIAL_MEDIA_TYPES_MAP, SOCIAL_MEDIA_TYPES_ORDER = {}, []
for mt in SOCIAL_MEDIA_TYPES:
    SOCIAL_MEDIA_TYPES_MAP[mt[0]] = mt[1]
    SOCIAL_MEDIA_TYPES_ORDER.append(mt[0])

SOCIAL_MEDIA_TYPES_PLACEHOLDERS = {
    "EMAIL": "correu@example.com",
    "WEBSITE": "example.com",
    "FACEBOOK": "Nom d'usuari",
    "INSTAGRAM": "Nom d'usuari",
    "TWITTER": "Nom d'usuari",
    "LINKEDIN": "Nom d'usuari",
}

ORG_SCOPES = [
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
    ("PARTICIPATION", "Participació ciutadana i dinamització comunitària"),
    ("DESIGN", "Disseny i comunicació"),
    ("TRAINING", "Formació i recerca"),
    ("HOUSING", "Habitatge i gestió de l’entorn"),
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
]

ORG_SCOPES_NAMES_MAP = {}
for scope in ORG_SCOPES:
    ORG_SCOPES_NAMES_MAP[scope[0]] = scope[1]

ORG_TYPES = [
    ("ASSOCIATION", "Associació"),
    ("COOPERATIVE", "Cooperativa"),
    ("NONPROFIT_COOPERATIVE", "Cooperativa sense ànim de lucre"),
    ("FOUNDATION", "Fundació"),
    ("LABOR_SOCIETY", "Societat laboral"),
    ("MUTUALITY", "Mutualitat"),
    ("INSERTION_COMPANY", "Empresa d’inserció"),
    ("SPECIAL_WORK_CENTER", "Centre especial de treball"),
]

ORG_TYPES_NAMES_MAP = {}
for org_type in ORG_TYPES:
    ORG_TYPES_NAMES_MAP[org_type[0]] = org_type[1]

RESOURCES = [
    ("PLACE", "Local"),
    ("TRAINING", "Formació"),
    ("SERVICE", "Servei"),
    ("EQUIPMENT", "Equipaments"),
    ("OTHER", "Altres"),
]

RESOURCE_NAMES_MAP, RESOURCES_ORDER = {}, []
for resource in RESOURCES:
    RESOURCE_NAMES_MAP[resource[0]] = resource[1]
    RESOURCES_ORDER.append(resource[0])

RESOURCE_ICONS_MAP = {
    "PLACE": "bi-house-fill",
    "SERVICE": "bi-person-check-fill",
    "TRAINING": "bi-book-half",
    "EQUIPMENT": "bi-gear-fill",
    "OTHER": "bi-three-dots",
}

RESOURCE_OPTIONS_MAP = {
    "PLACE": (
        ("DAILY_USAGE", "Ús diari"),
        ("PUNCTUAL_USAGE", "Ús puntual"),
        ("PUNCTUAL_MEETINGS", "Puntualment per a reunions"),
        ("PUNCTUAL_EVENTS", "Puntualment per a actes"),
    ),
    "TRAINING": (
        ("TRAINING_DIGITAL", "Digitalització"),
        ("TRAINING_BUREAUCRACY", "Relacions amb l'administració"),
        ("TRAINING_EQUALITY", "Igualtat"),
        ("TRAINING_ENERGY_SAVING", "Estalvi energètic"),
        ("TRAINING_HISTORICAL_MEMORY", "Memòria històrica"),
    ),
    "SERVICE": (
        ("COMMUNITY_MANAGER", "Gestió de la comunicació (web, xarxes socials, etc.)"),
        ("INSURANCE", "Assegurança"),
        ("AGENCY", "Gestoria"),
        ("PROJECT_WRITING", "Redacció de projectes"),
        ("DIGITAL_BUREAUCRACY", "Relacions digitals amb l'administració"),
    ),
    "EQUIPMENT": (
        ("SOUND_SYSTEM_ACOUSTIC", "Equip de so per a xerrades"),
        ("SOUND_SYSTEM_CONCERT", "Equip de so per a concerts"),
        ("PROJECTOR", "Projector"),
        ("VEHICLE", "Vehicle"),
        ("STAGE", "Escenari"),
        ("CHAIRS_TABLES", "Cadires i taules"),
        ("DISHES", "Plats, gots i coberts"),
        ("KITCHEN_EQUIPMENT", "Material de cuina"),
        ("CAMPING_EQUIPMENT", "Material d'acampada"),
    ),
    "OTHER": (),
}

RESOURCE_OPTIONS_READABLE_MAP = {
    ("PLACE", "DAILY_USAGE"): "local per a ús diari",
    ("PLACE", "PUNCTUAL_USAGE"): "local per a ús puntual",
    ("PLACE", "PUNCTUAL_MEETINGS"): "local per fer servir puntualment per a reunions",
    ("PLACE", "PUNCTUAL_EVENTS"): "local per fer servir puntualment per a actes",
    ("TRAINING", "TRAINING_DIGITAL"): "formació en igitalització",
    ("TRAINING", "TRAINING_BUREAUCRACY"): "formació en relacions amb l'administració",
    ("TRAINING", "TRAINING_EQUALITY"): "formació en igualtat",
    ("TRAINING", "TRAINING_ENERGY_SAVING"): "formació en estalvi energètic",
    ("TRAINING", "TRAINING_HISTORICAL_MEMORY"): "formació en memòria històrica",
    ("SERVICE", "COMMUNITY_MANAGER"): "ajuda amb la gestió de la comunicació (web, xarxes socials, etc.)",
    ("SERVICE", "INSURANCE"): "servei d'assegurança",
    ("SERVICE", "AGENCY"): "servei de gestoria",
    ("SERVICE", "PROJECT_WRITING"): "ajuda amb la redacció de projectes",
    ("SERVICE", "DIGITAL_BUREAUCRACY"): "ajuda amb les relacions digitals amb l'administració",
    ("EQUIPMENT", "SOUND_SYSTEM_ACOUSTIC"): "equip de so per a xerrades",
    ("EQUIPMENT", "SOUND_SYSTEM_CONCERT"): "equip de so per a concerts",
    ("EQUIPMENT", "PROJECTOR"): "projector",
    ("EQUIPMENT", "VEHICLE"): "vehicle",
    ("EQUIPMENT", "STAGE"): "escenari",
    ("EQUIPMENT", "CHAIRS_TABLES"): "cadires i taules",
    ("EQUIPMENT", "DISHES"): "plats, gots i coberts",
    ("EQUIPMENT", "KITCHEN_EQUIPMENT"): "material de cuina",
    ("EQUIPMENT", "CAMPING_EQUIPMENT"): "material d'acampada",
}

RESOURCES_LIST, RESOURCE_OPTIONS = [], []
for k in RESOURCE_OPTIONS_MAP:
    RESOURCES_LIST.append(k)
    v = RESOURCE_OPTIONS_MAP[k]
    for vv in v:
        if vv not in RESOURCE_OPTIONS:
            RESOURCE_OPTIONS.append(vv)

RESOURCE_OPTIONS_DEF_MAP = {}
for option in RESOURCE_OPTIONS:
    RESOURCE_OPTIONS_DEF_MAP[option[0]] = option[1]

RESOURCE_NEED_DESCRIPTIONS = {
    "PLACE": "Esteu buscant un local on poder desenvolupar la vostra activitat?",
    "SERVICE": "Esteu buscant algú que us proporcione aquests serveis?",
    "TRAINING": "Voleu rebre formació en algun d'aquests temes?",
    "EQUIPMENT": "Necessiteu alguna d'aquestes coses?",
    "OTHER": (
        "Podeu indicar qualsevol altra necessitat que tingueu."
        "Tindrem en compte les vostres suggerències per incloure-les a l'aplicació."
    ),
}

RESOURCE_NEED_ACTIONS = {
    "PLACE": ("No n'estem buscant", "Sí que n'estem buscant"),
    "SERVICE": ("No n'estem buscant", "Sí que n'estem buscant"),
    "TRAINING": ("No volem formació", "Sí que volem formació"),
    "EQUIPMENT": ("No en necessitem", "Sí que en necessitem"),
    "OTHER": ("No tenim altres necessitats", "Sí que tenim altres necessitats"),
}

RESOURCE_OFFER_DESCRIPTIONS = {
    "PLACE": "Teniu un local que estigueu disposats a compartir amb altres entitats?",
    "SERVICE": "Oferiu algun d'aquests serveis per a altres entitats, o podeu recomanar-ne proveïdors?",
    "TRAINING": "Oferiu formació en algun d'aquests temes?",
    "EQUIPMENT": "Teniu alguna d'aquestes coses que pugueu compartir?",
    "OTHER": (
        "Podeu indicar qualsevol altre servei o material que oferiu."
        "Tindrem en compte les vostres suggerències per incloure-les a l'aplicació."
    ),
}

RESOURCE_OFFER_ACTIONS = {
    "PLACE": ("No en tenim", "Sí que en tenim"),
    "SERVICE": ("No oferim serveis", "Sí que oferim serveis"),
    "TRAINING": ("No oferim formació", "Sí que oferim formació"),
    "EQUIPMENT": ("No en tenim cap", "Sí que en tenim alguna"),
    "OTHER": ("No oferim altres coses", "Sí que oferim altres coses"),
}

RESOURCE_ADD_IMAGE_LABEL = {
    "PLACE": "Afegeix imatge del local",
    "SERVICE": "Afegeix imatge del servei",
    "TRAINING": "Afegeix imatge de la formació",
    "EQUIPMENT": "Afegeix imatge d'aquestes coses",
    "OTHER": "Afegeix imatge del que oferiu",
}

RESOURCE_OPTIONS_QUESTION_MAP = {
    "PLACE": "Quan necessitarieu fer servir el local?",
    "SERVICE": "Quins serveis concrets necessiteu?",
    "TRAINING": "De quins temes us interessa formar-vos?",
    "EQUIPMENT": "Quina d'aquestes coses necessiteu?",
}

