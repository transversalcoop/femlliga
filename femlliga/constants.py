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
    ("HOUSING", _("Habitatge i gestió de l'entorn")),
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
    ("INSERTION_COMPANY", _("Empresa d'inserció")),
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
    ("EQUIPMENT", _("Materials")),
    ("ALLIANCES", _("Aliances")),
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
    "ALLIANCES": "bi-people-fill",
    "OTHER": "bi-three-dots",
}

RESOURCE_DESCRIPTIONS_MAP = {
    "PLACE": _("Espais on poder celebrar actes o desenvolupar l'activitat diària"),
    "SERVICE": _("Serveis necessaris per desenvolupar l'activitat"),
    "TRAINING": _("Formacions, assessoraments i acompanyaments"),
    "EQUIPMENT": _(
        "Material pedagògic i de sensibilització, d'exposicions, de fires, bibliogràfic, pamflets, cartells, material esportiu, de cuina, mobles, ferramentes o d'altres"
    ),
    "ALLIANCES": _("Intercooperació, col·laboracions i creació de xarxes"),
    "OTHER": _("Altres possibilitats que no encaixen en les categories anteriors"),
}

RESOURCE_OPTIONS_MAP = {
    "PLACE": (
        ("DAILY_USAGE", _("Espai de treball d'oficina")),
        # Former "PUNCTUAL_USAGE" was a different tag, now PUNCTUAL_MEETINGS + PUNCTUAL_EVENTS
        ("PUNCTUAL_MEETINGS", _("Espai per a reunions")),
        ("PUNCTUAL_EVENTS", _("Espai per a actes")),
        ("PLACE_TRAINING", _("Aula de formació")),
        ("PLACE_WORKSHOP", _("Taller")),
        ("PLACE_WAREHOUSE", _("Magatzem")),
    ),
    "TRAINING": (
        ("TRAINING_DIGITAL", _("Digitalització")),
        ("TRAINING_BUREAUCRACY", _("Relacions amb l'administració")),
        ("TRAINING_EQUALITY", _("Igualtat i Feminismes")),
        ("TRAINING_ENERGY_SAVING", _("Eficiència i estalvi energètic")),
        ("TRAINING_HISTORICAL_MEMORY", _("Memòria històrica")),
        ("TRAINING_ARTS", _("Arts i cultura")),
        ("TRAINING_PROJECTS", _("Redacció de projectes")),
    ),
    "SERVICE": (
        ("COMMUNITY_MANAGER", _("Comunicació")),
        ("INSURANCE", _("Assegurances")),
        ("AGENCY", _("Gestoria")),
        ("PROJECT_WRITING", _("Redacció de projectes")),
        ("DIGITAL_BUREAUCRACY", _("Relacions digitals amb l'administració")),
        ("SERVICE_PARTICIPATION", _("Participació")),
        ("SERVICE_REPAIR", _("Reparació, manteniment i reutilització")),
    ),
    "EQUIPMENT": (
        # Former: "SOUND_SYSTEM_ACOUSTIC", "SOUND_SYSTEM_CONCERT", "PROJECTOR", "STAGE"
        ("EQUIPMENT_EVENTS", _("Material d'esdeveniments, fires i exposicions")),
        ("VEHICLE", _("Vehicle")),
        ("CHAIRS_TABLES", _("Mobiliari")),
        # Former "DISHES" was a different tag, now inside KITCHEN_EQUIPMENT
        ("KITCHEN_EQUIPMENT", _("Material de cuina")),
        ("CAMPING_EQUIPMENT", _("Material d'acampada")),
        ("EQUIPMENT_DIY", _("Material de bricolatge")),
        ("EQUIPMENT_SPORTS", _("Material esportiu")),
        ("EQUIPMENT_EDUCATION", _("Material pedagògic i de sensibilització")),
    ),
    "ALLIANCES": (
        ("PROJECT_COLLABORATION", _("Col·laboració en projectes")),
        ("VOLUNTEERING", _("Voluntariat")),
        ("PUBLICITY", _("Difusió")),
        ("MONEY", _("Suport econòmic")),
        ("USERS_REFERRAL", _("Derivació d'usuàries")),
        ("SUPPORT_GROUPS", _("Xarxes i grups de suport")),
        ("COMMON_STRATEGY", _("Estratègia i protocols conjunts")),
    ),
    "OTHER": (),
}

NEEDS_PUBLISHABLE_OPTIONS_MAP = {
    "ALLIANCES": ("VOLUNTEERING",),
}

NEEDS_PUBLISHABLE_OPTIONS_LABELS_MAP = {
    ("ALLIANCES", "VOLUNTEERING"): _("Aliances - Crida a voluntariat"),
}

NEEDS_PUBLISHABLE_OPTIONS_LABELS_MAP_2 = {}
for k, value in NEEDS_PUBLISHABLE_OPTIONS_LABELS_MAP.items():
    NEEDS_PUBLISHABLE_OPTIONS_LABELS_MAP_2.setdefault(k[0], {})[k[1]] = value

NEEDS_PUBLISHABLE_OPTIONS_DESCRIPTION_MAP = {
    ("ALLIANCES", "VOLUNTEERING"): _(
        "Una bona descripció inclourà informació com on s'ha de desenvolupar el voluntariat, en quines dates, si hi ha algun tipus de requisit o inscripció necessària, i una breu descripció de la feina que es desenvoluparà"
    ),
}

NEEDS_PUBLISHABLE_OPTIONS_DESCRIPTION_MAP_2 = {}
for k, value in NEEDS_PUBLISHABLE_OPTIONS_DESCRIPTION_MAP.items():
    NEEDS_PUBLISHABLE_OPTIONS_DESCRIPTION_MAP_2.setdefault(k[0], {})[k[1]] = value

RESOURCE_OPTIONS_READABLE_MAP = {
    ("PLACE", "DAILY_USAGE"): _("espai de treball d'oficina"),
    ("PLACE", "PUNCTUAL_MEETINGS"): _("espai per a reunions"),
    ("PLACE", "PUNCTUAL_EVENTS"): _("espai per a actes"),
    ("PLACE", "PLACE_TRAINING"): _("aula de formació"),
    ("PLACE", "PLACE_WORKSHOP"): _("taller"),
    ("PLACE", "PLACE_WAREHOUSE"): _("magatzem"),
    ("TRAINING", "TRAINING_DIGITAL"): _("formació en digitalització"),
    ("TRAINING", "TRAINING_BUREAUCRACY"): _(
        "formació en relacions amb l'administració"
    ),
    ("TRAINING", "TRAINING_EQUALITY"): _("formació en igualtat i feminismes"),
    ("TRAINING", "TRAINING_ENERGY_SAVING"): _(
        "formació en eficiència i estalvi energètic"
    ),
    ("TRAINING", "TRAINING_HISTORICAL_MEMORY"): _("formació en memòria històrica"),
    ("TRAINING", "TRAINING_ARTS"): _("formació en arts i cultura"),
    ("TRAINING", "TRAINING_PROJECTS"): _("formació en redacció de projectes"),
    ("SERVICE", "COMMUNITY_MANAGER"): _("ajuda amb la comunicació"),
    ("SERVICE", "INSURANCE"): _("servei d'assegurances"),
    ("SERVICE", "AGENCY"): _("servei de gestoria"),
    ("SERVICE", "PROJECT_WRITING"): _("ajuda amb la redacció de projectes"),
    ("SERVICE", "DIGITAL_BUREAUCRACY"): _(
        "ajuda amb les relacions digitals amb l'administració"
    ),
    ("SERVICE", "SERVICE_PARTICIPATION"): _("ajuda amb projectes de participació"),
    ("SERVICE", "SERVICE_REPAIR"): _(
        "servei de reparació, manteniment i reutilització"
    ),
    ("EQUIPMENT", "EQUIPMENT_EVENTS"): _(
        "material d'esdeveniments, fires i exposicions"
    ),
    ("EQUIPMENT", "VEHICLE"): _("vehicle"),
    ("EQUIPMENT", "CHAIRS_TABLES"): _("mobiliari"),
    ("EQUIPMENT", "KITCHEN_EQUIPMENT"): _("material de cuina"),
    ("EQUIPMENT", "CAMPING_EQUIPMENT"): _("material d'acampada"),
    ("EQUIPMENT", "EQUIPMENT_DIY"): _("material de bricolatge"),
    ("EQUIPMENT", "EQUIPMENT_SPORTS"): _("material esportiu"),
    ("EQUIPMENT", "EQUIPMENT_EDUCATION"): _("material pedagògic i de sensibilització"),
    ("ALLIANCES", "PROJECT_COLLABORATION"): _("col·laboració en projectes"),
    ("ALLIANCES", "VOLUNTEERING"): _("voluntariat"),
    ("ALLIANCES", "PUBLICITY"): _("difusió"),
    ("ALLIANCES", "MONEY"): _("suport econòmic"),
    ("ALLIANCES", "USERS_REFERRAL"): _("derivació d'usuàries"),
    ("ALLIANCES", "SUPPORT_GROUPS"): _("xarxes i grups de suport"),
    ("ALLIANCES", "COMMON_STRATEGY"): _("estratègia i protocols conjunts"),
}

RESOURCES_LIST, RESOURCE_OPTIONS, RESOURCE_OPTIONS_WITH_PREFIX = [], [], []
for k in RESOURCE_OPTIONS_MAP:
    RESOURCES_LIST.append(k)
    v = RESOURCE_OPTIONS_MAP[k]
    for vv in v:
        if vv not in RESOURCE_OPTIONS:
            RESOURCE_OPTIONS.append(vv)
            RESOURCE_OPTIONS_WITH_PREFIX.append(
                (vv[0], RESOURCE_NAMES_MAP[k] + " - " + vv[1])
            )

RESOURCE_OPTIONS_DEF_MAP = {}
for option in RESOURCE_OPTIONS:
    RESOURCE_OPTIONS_DEF_MAP[option[0]] = option[1]

RESOURCE_OPTIONS_QUESTION_MAP = {
    "PLACE": _("Quin tipus de local necessiteu?"),
    "SERVICE": _("Quins serveis concrets necessiteu?"),
    "TRAINING": _("De quins temes us interessa formar-vos?"),
    "EQUIPMENT": _("Quina d'aquestes coses necessiteu?"),
    "ALLIANCES": _("Quina d'aquestes coses necessiteu?"),
}
