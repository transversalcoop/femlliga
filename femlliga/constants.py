from django.utils.translation import gettext_lazy as _

APP_NAME = _("Fem lliga!")
FROM_EMAIL = f"{APP_NAME} <no-reply@femlliga.org>"

LANGUAGE_CHOICES = [
    ("ca", "Català"),
    ("es", "Castellano"),
]

NOTIFICATION_CHOICES = [
    ("DAILY", _("Diàriament")),
    ("WEEKLY", _("Setmanalment")),
    ("MONTHLY", _("Mensualment")),
    ("NEVER", _("Mai")),
]

SOCIAL_MEDIA_TYPES = [
    ("EMAIL", _("Correu electrònic")),
    ("WEBSITE", _("Lloc web")),
    ("FACEBOOK", _("Facebook")),
    ("INSTAGRAM", _("Instagram")),
    ("TWITTER", _("Twitter")),
    ("LINKEDIN", _("Linkedin")),
    ("WHATSAPP", _("Whatsapp")),
    ("PHONE", _("Telèfon")),
]

SOCIAL_MEDIA_TYPES_MAP, SOCIAL_MEDIA_TYPES_ORDER = {}, []
for mt in SOCIAL_MEDIA_TYPES:
    SOCIAL_MEDIA_TYPES_MAP[mt[0]] = mt[1]
    SOCIAL_MEDIA_TYPES_ORDER.append(mt[0])

SOCIAL_MEDIA_TYPES_PLACEHOLDERS = {
    "EMAIL": _("correu@example.com"),
    "WEBSITE": _("example.com"),
    "FACEBOOK": _("Nom d'usuari"),
    "INSTAGRAM": _("Nom d'usuari"),
    "TWITTER": _("Nom d'usuari"),
    "LINKEDIN": _("Nom d'usuari"),
}

ORG_SCOPES = [
    ("EQUALITY", _("Dona/Igualtat/Feminismes")),
    ("EDUCATION", _("Educació")),
    ("OLDER_PEOPLE", _("Persones majors")),
    ("NEIGHBORHOOD", _("Veïnal")),
    ("SPORTS", _("Activitat física i esportiva")),
    ("CULTURE", _("Cultura, patrimoni, territori, llengua...")),
    ("YOUTH", _("Infància, adolescència i joventut")),
    ("SOCIAL_ASSISTANCE", _("Benestar social")),
    ("COOPERATION", _("Cooperació i sensibilització")),
    ("ENVIRONMENT", _("Medi ambient i mobilitat sostenible")),
    ("TRADITIONS", _("Festa i tradicions")),
    ("RELIGIOUS", _("Religiosa")),
    ("PARTICIPATION", _("Participació ciutadana i dinamització comunitària")),
    ("DESIGN", _("Disseny i comunicació")),
    ("TRAINING", _("Formació i recerca")),
    ("HOUSING", _("Habitatge i gestió de l’entorn")),
    ("FOOD", _("Alimentació, restauració i hosteleria")),
    ("LOGISTICS", _("Logística i subministraments")),
    ("FINANCE", _("Finançament i Moneda Social")),
    ("PRODUCTION", _("Producció")),
    ("TRADE", _("Comerç")),
    ("HEALTH", _("Salut i Cures")),
    ("TECHNOLOGY", _("Tecnologia i electrònica")),
    ("TEXTILE", _("Textil")),
    ("ACCESSIBILITY", _("Accessibilitat")),
    ("FUNCTIONAL_DIVERSITY", _("Diversitat funcional")),
    ("OTHER", _("Altres")),
]

ORG_SCOPES_NAMES_MAP = {}
for scope in ORG_SCOPES:
    ORG_SCOPES_NAMES_MAP[scope[0]] = scope[1]

ORG_TYPES = [
    ("ASSOCIATION", _("Associació")),
    ("COOPERATIVE", _("Cooperativa")),
    ("NONPROFIT_COOPERATIVE", _("Cooperativa sense ànim de lucre")),
    ("FOUNDATION", _("Fundació")),
    ("LABOR_SOCIETY", _("Societat laboral")),
    ("MUTUALITY", _("Mutualitat")),
    ("INSERTION_COMPANY", _("Empresa d’inserció")),
    ("SPECIAL_WORK_CENTER", _("Centre especial de treball")),
    ("PUBLIC_PRIVATE_BASED", _("Entitat pública de base privada")),
]

ORG_TYPES_NAMES_MAP = {}
for org_type in ORG_TYPES:
    ORG_TYPES_NAMES_MAP[org_type[0]] = org_type[1]

RESOURCES = [
    ("PLACE", _("Local")),
    ("TRAINING", _("Formació")),
    ("SERVICE", _("Servei")),
    ("EQUIPMENT", _("Equipaments")),
    ("OTHER", _("Altres")),
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
        ("DAILY_USAGE", _("Ús diari")),
        ("PUNCTUAL_USAGE", _("Ús puntual")),
        ("PUNCTUAL_MEETINGS", _("Puntualment per a reunions")),
        ("PUNCTUAL_EVENTS", _("Puntualment per a actes")),
    ),
    "TRAINING": (
        ("TRAINING_DIGITAL", _("Digitalització")),
        ("TRAINING_BUREAUCRACY", _("Relacions amb l'administració")),
        ("TRAINING_EQUALITY", _("Igualtat")),
        ("TRAINING_ENERGY_SAVING", _("Estalvi energètic")),
        ("TRAINING_HISTORICAL_MEMORY", _("Memòria històrica")),
    ),
    "SERVICE": (
        ("COMMUNITY_MANAGER", _("Gestió de la comunicació (web, xarxes socials, etc.)")),
        ("INSURANCE", _("Assegurança")),
        ("AGENCY", _("Gestoria")),
        ("PROJECT_WRITING", _("Redacció de projectes")),
        ("DIGITAL_BUREAUCRACY", _("Relacions digitals amb l'administració")),
    ),
    "EQUIPMENT": (
        ("SOUND_SYSTEM_ACOUSTIC", _("Equip de so per a xerrades")),
        ("SOUND_SYSTEM_CONCERT", _("Equip de so per a concerts")),
        ("PROJECTOR", _("Projector")),
        ("VEHICLE", _("Vehicle")),
        ("STAGE", _("Escenari")),
        ("CHAIRS_TABLES", _("Cadires i taules")),
        ("DISHES", _("Plats, gots i coberts")),
        ("KITCHEN_EQUIPMENT", _("Material de cuina")),
        ("CAMPING_EQUIPMENT", _("Material d'acampada")),
    ),
    "OTHER": (),
}

RESOURCE_OPTIONS_READABLE_MAP = {
    ("PLACE", "DAILY_USAGE"): _("local per a ús diari"),
    ("PLACE", "PUNCTUAL_USAGE"): _("local per a ús puntual"),
    ("PLACE", "PUNCTUAL_MEETINGS"): _("local per fer servir puntualment per a reunions"),
    ("PLACE", "PUNCTUAL_EVENTS"): _("local per fer servir puntualment per a actes"),
    ("TRAINING", "TRAINING_DIGITAL"): _("formació en digitalització"),
    ("TRAINING", "TRAINING_BUREAUCRACY"): _("formació en relacions amb l'administració"),
    ("TRAINING", "TRAINING_EQUALITY"): _("formació en igualtat"),
    ("TRAINING", "TRAINING_ENERGY_SAVING"): _("formació en estalvi energètic"),
    ("TRAINING", "TRAINING_HISTORICAL_MEMORY"): _("formació en memòria històrica"),
    ("SERVICE", "COMMUNITY_MANAGER"): _("ajuda amb la gestió de la comunicació (web, xarxes socials, etc.)"),
    ("SERVICE", "INSURANCE"): _("servei d'assegurança"),
    ("SERVICE", "AGENCY"): _("servei de gestoria"),
    ("SERVICE", "PROJECT_WRITING"): _("ajuda amb la redacció de projectes"),
    ("SERVICE", "DIGITAL_BUREAUCRACY"): _("ajuda amb les relacions digitals amb l'administració"),
    ("EQUIPMENT", "SOUND_SYSTEM_ACOUSTIC"): _("equip de so per a xerrades"),
    ("EQUIPMENT", "SOUND_SYSTEM_CONCERT"): _("equip de so per a concerts"),
    ("EQUIPMENT", "PROJECTOR"): _("projector"),
    ("EQUIPMENT", "VEHICLE"): _("vehicle"),
    ("EQUIPMENT", "STAGE"): _("escenari"),
    ("EQUIPMENT", "CHAIRS_TABLES"): _("cadires i taules"),
    ("EQUIPMENT", "DISHES"): _("plats, gots i coberts"),
    ("EQUIPMENT", "KITCHEN_EQUIPMENT"): _("material de cuina"),
    ("EQUIPMENT", "CAMPING_EQUIPMENT"): _("material d'acampada"),
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

RESOURCE_ADD_IMAGE_LABEL = {
    "PLACE": _("Afegeix imatge del local"),
    "SERVICE": _("Afegeix imatge del servei"),
    "TRAINING": _("Afegeix imatge de la formació"),
    "EQUIPMENT": _("Afegeix imatge d'aquestes coses"),
    "OTHER": _("Afegeix imatge del que oferiu"),
}

RESOURCE_OPTIONS_QUESTION_MAP = {
    "PLACE": _("Quan necessitarieu fer servir el local?"),
    "SERVICE": _("Quins serveis concrets necessiteu?"),
    "TRAINING": _("De quins temes us interessa formar-vos?"),
    "EQUIPMENT": _("Quina d'aquestes coses necessiteu?"),
}

