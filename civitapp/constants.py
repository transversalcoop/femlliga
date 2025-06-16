from civitapp.models import Topic, Question, Answer, Content


TOPICS = []
topic1 = {
    "topic": Topic(
        name="Establiment d'objectius",
        description="Per engegar qualsevol procés, necessitem elegir un entorn delimitat d'acord amb uns criteris clars i, posteriorment, definir en claredat els objectius del procés de dinamització comunitària que volem dur a terme en eixe entorn.",
    ),
}

OBJECTIUS_ZONA_SIMILAR = "A l'hora de definir aquests límits és important considerar que la zona tinga unes característiques i necessitats similars, ja que si no ho son serà molt difícil consensuar i prioritzar els objectius posteriorment."
OBJECTIUS_NECESSITATS_CONCRETES = "Dins de les necessitats detectades també és important concretar quines seran les que es volen cobrir amb el procés de dinamització; això permetrà evitar generar falses expectatives i desviar esforços cap a necessitats que no s'hagen considerat prioritàries."
OBJECTIUS_NECESSITATS_BASIQUES = "Cal tindre en compte que en zones amb mancances clares d'inversió i manteniment és possible que aquestes deficiències siguen considerades prioritàries per la majoria de la població i que aquesta no vulga abordar altres necessitats sense haver resolt abans les primeres. Moltes vegades aquest tipus de mancances es poden saber consultant dades ja registrades, com els canals oficials de queixes de l'ajuntament, les mocions fetes al ple, etc."

questions1 = []
questions1.append(
    {
        "question": Question(
            question="Per què hem escollit este entorn? Quines necessitats prèvies hem detectat que ens han dut a triar-ho?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="L'entorn ens ve donat, no l'hem escollit nosaltres (ens han fet un encàrrec)"
                ),
                "content": Content(
                    description="Cal consensuar l'entorn on es treballarà",
                    content=[
                        "Independentment de que l'entorn vinga donat, s'ha d'especificar molt bé quines zones entren (i quines no). És necessari acordar bé amb qui ha fet l'encàrrec quins seran els límits, especialment per evitar malentesos més endavant.",
                        OBJECTIUS_ZONA_SIMILAR,
                        OBJECTIUS_NECESSITATS_CONCRETES,
                        OBJECTIUS_NECESSITATS_BASIQUES,
                    ],
                ),
            },
            {
                "answer": Answer(answer="L'hem escollit perquè és l'entorn on vivim"),
                "content": Content(
                    description="No totes tenim la mateixa idea del nostre barri",
                    content=[
                        "Malgrat que una persona puga tindre molt clar quina és la zona a la que pertany, aquesta idea no té perquè coincidir amb la que tenen altres persones implicades amb el procés o les persones a qui es dirigirà la dinamització. Cal deixar clar i per escrit quins son els límits a considerar i les raons per les que unes zones s'han inclòs i unes altres no.",
                        OBJECTIUS_ZONA_SIMILAR,
                        OBJECTIUS_NECESSITATS_CONCRETES,
                        OBJECTIUS_NECESSITATS_BASIQUES,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="L'hem escollit perquè hem detectat unes necessitats importants que pensem que podem cobrir"
                ),
                "content": Content(
                    description="Cal delimitar l'entorn on es treballarà",
                    content=[
                        "Tindre clares les necessitats que es volen afrontar és molt bon començament! Però no per això s'ha de descuidar la zona sobre la que es treballaran aquestes necessitats. Cal deixar clar i per escrit quins son els límits a considerar, tenint en compte no només en quines zones es donen les necessitats detectades, sinó també que les característiques de l'entorn siguen similars, ja que si no ho son serà molt difícil consensuar i prioritzar els objectius posteriorment.",
                        "Sabent quines son les necessitats que es poden cobrir, també és molt important ser transparents en comunicar-les; si no es fa, es poden generar falses expectatives de persones que esperen altres resultats del procés.",
                        OBJECTIUS_NECESSITATS_BASIQUES,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="L'hem escollit perquè creiem que és un entorn amb molta potencialitat per a la dinamització comunitària"
                ),
                "content": Content(
                    description="Cal definir les necessitats que s'afrontaran",
                    content=[
                        "Tindre un entorn amb un bon caldo de cultiu és molt bon punt de partida per a la dinamització, però alhora fa més important definir correctament quines son les necessitats que es volen abordar. Justament en un entorn actiu és més probable que diferents persones tinguen iniciativa per voler dur a terme els seus propis projectes, i si no es defineixen clarament els objectius del procés poden sorgir conflictes.",
                        "Si no s'han detectat necessitats clares encara, és necessari començar amb un procés de detecció i priorització de les necessitats durant les fases inicials del procés, de manera que totes les participants tinguen unes expectatives realistes dels resultats que es poden obtindre.",
                        OBJECTIUS_NECESSITATS_BASIQUES,
                    ],
                ),
            },
        ],
    },
)

OBJECTIUS_CAL_DEFINIR = "Independentment de quins siguen els objectius del procés, és imprescindible que aquests objectius estiguen definits clarament i que estiguen adaptats a les necessitats detectades i al públic que se'n beneficiarà. Si els objectius no estan definits clarament es poden produir conflictes entre persones que vulguen guiar el procés en direccions diferents segons els seus interessos diversos."
OBJECTIUS_CONTRADICCIONS = "També cal tindre en compte que els objectius definits poden entrar en contradicció amb els interessos d'algunes persones concretes, per exemple, la peatonalització dels carrers pot entrar en conflicte amb l'interès d'una persona d'aparcar davant de casa. Cal ser conscient d'això i tindre clars els beneficis que es volen aconseguir, per poder comunicar-ho de manera adequada, especialment a les persones que puguen quedar afectades"

questions1.append(
    {
        "question": Question(
            question="Quins són els objectius del procés de dinamització comunitària que volem engegar?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="Generar teixit social en un entorn en el que n'hi ha poc"
                ),
                "content": Content(
                    description="Els moviments necessiten una raó de ser",
                    content=[
                        "Malgrat que, en abstracte, pot resultar interessant motivar la interacció entre les persones, sempre és més efectiu fer-ho baix algun objectiu concret que puga interessar a aquestes persones. Per tant, malgrat que no hi haja cap objectiu concret que es vulga perseguir, val la pena definir-ne un que puga aglutinar a persones diverses que acaben formant aquest teixit social que realment interessa.",
                        OBJECTIUS_CAL_DEFINIR,
                        OBJECTIUS_CONTRADICCIONS,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Augmentar la col·laboració entre un teixit social ja existent"
                ),
                "content": Content(
                    description="La col·laboració necessita confiança",
                    content=[
                        "Si en el nostre entorn ja existeix teixit social però hi ha poca interacció entre les diferents organitzacions, és possible que hi haja un problema de coneixement o confiança. Un primer pas hauria de ser la trobada i coneixença dels diferents actors, que potser simplement desconeixen l'existència dels altres. Un segon pas hauria de ser l'aprofundiment en la confiança entre aquestes persones, el qual es podria fer a través de la facilitació de grups. Existeixen professionals amb experiència en la facilitació de grups als quals es pot recórrer en aquest cas.",
                        OBJECTIUS_CAL_DEFINIR,
                        OBJECTIUS_CONTRADICCIONS,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Dur a terme reivindicacions d'un col·lectiu concret"
                ),
                "content": Content(
                    description="Cal implicar a tota la societat",
                    content=[
                        "Malgrat que els objectius que es persegueixen puguen afectar especialment a un col·lectiu concret, un procés difícilment tindrà èxit si es du a terme aïllant aquest col·lectiu de la resta del seu entorn. Cal exposar les reivindicacions de manera que apelen a la resta de la població i que aquesta puga veure que les millores per a un col·lectiu no van en detriment de la resta. Per exemple, moltes persones poden pensar que les millores en accessibilitat com les rampes només beneficien a les persones amb diversitat funcional, però es pot fer veure que aquestes també ajuden a mares i pares amb carros, a una persona que carregue pes, o a qualsevol persona que un dia es trenque una cama.",
                        OBJECTIUS_CAL_DEFINIR,
                        OBJECTIUS_CONTRADICCIONS,
                    ],
                ),
            },
            {
                "answer": Answer(answer="Atacar una problemàtica concreta de l'entorn"),
                "content": Content(
                    description="Les problemàtiques es poden enfrontar de diferents maneres",
                    content=[
                        "Tindre clara la problemàtica que es vol abordar és un molt bon primer pas, però saber la problemàtica i pensar els objectius son dos coses diferents. Qualsevol problemàtica es pot abordar des de diferents òptiques que donarien lloc a objectius diferents. Fins i tot si hi ha un objectiu clar, com «aturar el projecte X», aquest objectiu pot ser massa ambiciós per abordar-lo directament i és millor començar definint objectius més menuts que es puguen assolir un a un.",
                        OBJECTIUS_CAL_DEFINIR,
                        OBJECTIUS_CONTRADICCIONS,
                    ],
                ),
            },
        ],
    },
)

OBJECTIUS_BENEFICIA = "És important definir el públic beneficiari del procés, ja que això facilitarà planificar la resta d'aspectes (les activitats, la estratègia comunicativa...). No és el mateix organitzar activitats per a persones joves que per a persones amb responsabilitats familiars."

questions1.append(
    {
        "question": Question(question="A qui beneficia el procés?"),
        "answers": [
            {
                "answer": Answer(answer="A tota la població, de manera indistinta"),
                "content": Content(
                    description="Sempre hi ha excepcions",
                    content=[
                        OBJECTIUS_BENEFICIA,
                        "Malgrat que es puga pensar que un procés és totalment positiu, sempre hi ha persones que en poden resultar afectades, o que poden pensar que en resultaran afectades malgrat que no siga cert. Cal fer l'esforç d'imaginar quines poden ser aquestes persones per anticipar-se a les seues reticències i tindre preparats els arguments de perquè, malgrat tot, el procés val la pena. Per exemple, en casos de peatonalització de carrers és habitual tindre la oposició del comerç local, malgrat que els estudis mostren increments del consum en zones peatonalitzades. Cal tindre aquesta informació preparada per respondre quan siga necessari.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="A un col·lectiu concret (dones, infància, persones migrants, persones majors...)"
                ),
                "content": Content(
                    description="Cal trobar aliades dins de cada col·lectiu",
                    content=[
                        OBJECTIUS_BENEFICIA,
                        "Quan un procés vol impactar especialment en un col·lectiu és molt important que aquest procés estiga liderat per persones del mateix col·lectiu. En cas que inicialment no ho estiga, és imprescindible trobar aliades dins del col·lectiu que prenguen com a propis els objectius i els impulsen de cara a la resta de persones del col·lectiu. Sense aquest suport intern, el procés sempre quedarà curt i perdrà credibilitat.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="A persones que pateixen d'una problemàtica concreta (dificultat d'accés a l'educació, a l'habitatge, pobresa energètica, accessibilitat...)"
                ),
                "content": Content(
                    description="Cal involucrar a les afectades per la problemàtica",
                    content=[
                        OBJECTIUS_BENEFICIA,
                        "Quan un procés vol impactar especialment en persones que pateixen una problemàtica és molt important que el procés estiga liderat per persones en aquesta situació. En cas que inicialment no ho estiga, és imprescindible trobar a aliades dins del col·lectiu que prenguen com a propis els objectius i els impulsen de cara a la resta de persones afectades. Aquest suport intern resulta imprescindible per impulsar accions realment efectives i assumibles per aquestes persones.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="A societat organitzada i entitats (associacions, altres entitats sense ànim de lucre, serveis públics, comerços...)"
                ),
                "content": Content(
                    description="Cal involucrar a les bases",
                    content=[
                        OBJECTIUS_BENEFICIA,
                        "És habitual que les organitzacions tinguen una dinàmica presa i una inèrcia que fa difícil canviar la manera de fer; aquesta inèrcia afecta especialment a les persones que es troben en la direcció de les entitats, que moltes vegades porten molts anys funcionant igual i es troben desconnectades de les problemàtiques de la resta de la organització. Per això és important involucrar a les bases, que seran les que es veuran més beneficiades, i que poden fer pressió perquè els seus equips directius estiguen oberts a noves propostes.",
                    ],
                ),
            },
        ],
    },
)

OBJECTIUS_IMPLICAR = "Independentment dels resultats esperats, recomanem realitzar el procés de manera col·lectiva, implicant a altres entitats coneixedores de l'entorn en la planificació, execució i avaluació de tot el procés"


topic1["questions"] = questions1
TOPICS.append(topic1)

topic2 = {
    "topic": Topic(
        name="Coneixement de l'entorn i els actors",
        description="Per començar un procés de dinamització comunitària, necessitem conéixer l'entorn elegit i els seus agents clau: quines entitats hi ha i com funcionen. Conéixer l'entorn ens permetrà apropar-nos als seus agents clau, i estos al seu torn ens permetran conéixer els espais participatius ja existents i generar confiança més ràpidament amb altres col·lectius i entitats que ens interesse involucrar en el procés.",
    ),
}

CONEIXEMENT_DIVERSITAT = "Independentment de la quantitat d'entitats existents en l'entorn, és important conéixer el màxim de diversitat possible. Persones amb diferents perfils en quant a gènere, edat, procedència, llengua, cultura, etc. Aporten en molts casos informació i punts de vista impossibles de detectar si, per exemple, només es fa contacte amb homes nadius de mitjana edat. Una major diversitat de contactes també permetrà posteriorment arribar a un major nombre de persones que participen del procés. Per tot això, cal sempre intentar convocar a persones amb el perfil més divers possible dins de les possibilitats trobades, i preguntar per persones amb perfils diferents quan s'entra en contacte amb qualsevol agent."

questions2 = []
questions2.append(
    {
        "question": Question(
            question="Quantes entitats operen en l'entorn que hem escollit dinamitzar?"
        ),
        "answers": [
            {
                "answer": Answer(answer="No existeixen entitats creades en l'entorn"),
                "content": Content(
                    description="Cal identificar agents clau",
                    content=[
                        "En cas de no saber de l'existència de cap entitat en l'entorn, cal identificar d'alguna manera agents clau que puguen servir en substitució seua. Aquests agents de vegades son persones molt conegudes en la zona, o que regenten establiments de referència. En absència d'altres entitats més representatives, aquestes persones podran servir per descobrir i fer d'enllaç amb altres persones que puguen estar interessades en el procés.",
                        CONEIXEMENT_DIVERSITAT,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Les úniques entitats existents provenen de l'administració"
                ),
                "content": Content(
                    description="Aprofiteu els recursos de l'administració",
                    content=[
                        "Les entitats que formen part de l'administració, malgrat tindre menys llibertat de moviments en general, també disposen de molts recursos que es poden aprofitar, com el contacte directe amb els mecanismes de participació oficials i el control de la difusió institucional. En aquest cas, val la pena aprofitar aquestes possibilitats perquè l'administració contribuisca a la difusió del procés.",
                        CONEIXEMENT_DIVERSITAT,
                    ],
                ),
            },
            {
                "answer": Answer(answer="Hi ha poques entitats operant en l'entorn"),
                "content": Content(
                    description="Aprofundiu en el seu coneixement",
                    content=[
                        "En cas d'haver poques entitats a les que dirigir-se, es disposa de la oportunitat d'aprofundir en el seu coneixement de l'entorn. Això es pot fer a través de reunions o entrevistes presencials amb les persones que participen activament en aquestes entitats. Aquestes entrevistes s'haurien de fer seguint un guió amb pautes clares de la informació que es vol obtenir, però alhora deixant oberta la possibilitat de rebre aportacions espontànies amb informacions no previstes.",
                        CONEIXEMENT_DIVERSITAT,
                    ],
                ),
            },
            {
                "answer": Answer(answer="Hi ha moltes entitats operant en l'entorn"),
                "content": Content(
                    description="De vegades no es pot abastar tot",
                    content=[
                        "En cas d'haver moltes entitats a les que dirigir-se, pot ser impossible conéixer-les de primera mà i aprofundir en el seu coneixement. Dos opcions alternatives per cobrir el màxim d'informació possible son les enquestes i els mapatges. Les enquestes permeten obtindre informació numèrica que guie les decisions posteriors, a més de poder arribar a moltes més persones i permetre identificar els punts més interessants en els que centrar-se. Els mapatges per la seua banda consisteixen en la identificació de les entitats existents sobre un plànol i de les relacions entre elles. Aquesta opció, més visual, permet identificar punts buits en el plànol, entitats amb poca relació amb la resta, o entitats amb una posició central en la interacció amb les altres.",
                        CONEIXEMENT_DIVERSITAT,
                    ],
                ),
            },
        ],
    },
)


CONEIXEMENT_DIVERSOS_CANALS = "Independentment dels canals de comunicació utilitzats per les entitats, és important trobar un equilibri en els que es facen servir per al procés: han de ser suficients per arribar a un percentatge important del públic objectiu, i suficientment pocs per no tindre una dispersió i divergència de continguts que facen dubtar a les persones que els reben de quin és el bo. Una manera d'evitar aquesta dispersió és tindre un canal «oficial» i a través d'altres canals enviar missatges breus amb un enllaç a la informació oficial."

questions2.append(
    {
        "question": Question(
            question="Quins canals de comunicació utilitzen les entitats? Com podem arribar a elles?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="Comunicació presencial, telèfon i boca-orella"
                ),
                "content": Content(
                    description="Una arma de doble fil",
                    content=[
                        "La comunicació verbal té avantatges i inconvenients molt marcats. Quan es necessita fer un procés deliberatiu o donar informació complexa, una conversa presencial no té rival en quant al nivell de comprensió que permet. Per altra banda, deixar la transmissió d'informacions complexes o de decisions al boca-orella pot generar un efecte de «telèfon trencat» en el que cada persona acaba amb una impressió diferent de la realitat.",
                        "Tenint en compte això, cal fer servir la comunicació presencial i el telèfon amb moderació, en aquells moments que realment ho requerisquen, i cal tindre sempre com a mínim un canal de comunicació per escrit. Per escrit haurien de quedar sempre totes les decisions i la informació de referència del procés, com per exemple les actes de les reunions, els objectius oficials del procés, etc. El boca-orella només convé fer-lo servir per fer arribar missatges molt concrets, com per exemple la convocatòria d'un acte.",
                        "Si les entitats fan servir preferentment aquest tipus de comunicació caldrà fer un esforç addicional per tindre aquesta presencialitat en els seus espais, i alhora caldrà ser especialment atent en evitar que puga haver malentesos derivats de la falta d'evidència escrita.",
                        CONEIXEMENT_DIVERSOS_CANALS,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Xarxes socials massives (Whatsapp, Instagram...)"
                ),
                "content": Content(
                    description="El mitjà més utilitzat té les seues limitacions",
                    content=[
                        "Actualment, les xarxes socials son el mitjà més utilitzat per comunicar-se, incloent per fer difusió dels projectes. Aquestes tenen molts avantatges, principalment el fet que un percentatge molt elevat de la població els fa servir, però també tenen uns inconvenients que els fan útils només per certs objectius.",
                        "En el cas de Whatsapp i altres plataformes de comunicació bidireccional, es poden fer servir amb dos propòsits. Per a la presa de decisions només funcionen amb grups menuts, per decisions molt concretes i que requereixen rapidesa; per a més persones o debats complexos, son totalment inviables i resulta imprescindible una trobada presencial (o una videotrucada). Per a la difusió d'activitats poden ser molt útils però cal calibrar bé el text i la freqüència amb que s'envia, ja que en aquestes plataformes els textos llargs s'acostumen a ignorar, i també s'ignoren quan el volum rebut és excessiu.",
                        "En el cas d'Instagram i altres plataformes de comunicació bàsicament unidireccional, la opció del debat resulta impossible. Resulten molt útils per fer difusió, però encara aixina tenen limitacions com no tindre la possibilitat d'adjuntar documents i similar.",
                        "Si les entitats fan servir preferentment aquest tipus de comunicació caldrà crear els comptes necessaris a les plataformes més utilitzades, i habituar-se a citar a les entitats involucrades per incloure-les.",
                        CONEIXEMENT_DIVERSOS_CANALS,
                    ],
                ),
            },
            {
                "answer": Answer(answer="Llocs web pròpis o premsa tradicional"),
                "content": Content(
                    description="Allò tradicional, de vegades la millor opció",
                    content=[
                        "Malgrat que cada vegada s'utilitzen menys, els llocs web pròpis d'un projecte permeten una llibertat que no es troba en cap de les altres opcions. En un lloc web es poden penjar notícies, imatges, calendaris, actes de les reunions, etc. I tot amb el disseny i organització que es considere convenient, donant prioritat al que es vulga destacar. El preu d'aquesta llibertat és que cal dedicar molt de temps, i de vegades ajuda professional, per poder-ho fer. Per a processos complexos, allargats en el temps, arriba un moment en que es torna imprescindible tindre un lloc web que centralitze tota la informació generada.",
                        "La premsa tradicional, per la seua banda, permet moltes vegades arribar a un públic totalment diferent al de les opcions digitals, i justament per això, i segons el públic objectiu, pot ser interessant considerar-ho.",
                        "Si les entitats fan servir preferentment aquest tipus de comunicació caldrà tindre-ho en compte per referenciar els seus llocs web o articles publicats rellevants quan es faça comunicació sobre el procés",
                        CONEIXEMENT_DIVERSOS_CANALS,
                    ],
                ),
            },
            {
                "answer": Answer(answer="Correu electrònic"),
                "content": Content(
                    description="Una opció sempre present",
                    content=[
                        "El correu electrònic té l'avantatge que, com el telèfon mòbil, gairebé totes les persones en tenen, i com les xarxes socials, es pot enviar una comunicació massiva a moltes persones alhora. Pateix, però, molts problemes de correu brossa, i per tant és probable que si la freqüència amb que s'envia informació és massa elevada o el recipient no ens coneix, decidisca ignorar directament el correu. En dosis baixes, pot servir per fer certs debats o prendre decisions complexes, donat que es presta més a la reflexió i als textos llargs que les plataformes de xat.",
                        "Si les entitats fan servir preferentment aquest tipus de comunicació, la millor manera de fer arribar la informació a les persones que interessen serà enviar la informació a cada entitat i que aquesta la remeta als seus associats, per evitar haver de gestionar llistes de correu.",
                        CONEIXEMENT_DIVERSOS_CANALS,
                    ],
                ),
            },
        ],
    },
)

CONEIXEMENT_COM_CONEIXER = "Si no es pot respondre amb profunditat a les preguntes anteriors, caldrà preguntar-se a través de qui es pot arribar a aquesta informació. La prospecció prèvia a l'inici de qualsevol procés és necessària per poder abordar-lo amb garanties, i com fer-la depèn de les persones concretes amb coneixements sobre l'entorn escollit."

questions2.append(
    {
        "question": Question(
            question="Qui té tots eixos coneixements? (quines entitats hi ha, a què es dediquen, i quins canals de comunicació utilitzen)"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="Persones que integren les entitats però no participen d'altres espais"
                ),
                "content": Content(
                    description="Cal fer un apropament gradual",
                    content=[
                        CONEIXEMENT_COM_CONEIXER,
                        "Si de la prospecció es detecta que hi ha agents clau amb informació que ens interessa però que estan centrades en la seua activitat o la de la seua entitat, caldrà fer un apropament gradual a aquests espais per poder conéixer-les.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Persones que integren les entitats i les representen en algun altre espai compartit"
                ),
                "content": Content(
                    description="Aprofitem els espais existents",
                    content=[
                        CONEIXEMENT_COM_CONEIXER,
                        "Quan existeixen espais compartits, com coordinadores, on participen agents clau, és imprescindible aprofitar-los. És habitual que aquests espais compartits estiguen oberts a la participació de noves persones, i moltes vegades el seu objectiu és justament compartir informació. Una sola reunió en un espai similar pot estalviar moltes hores i trucades per aconseguir la mateixa informació.",
                    ],
                ),
            },
            {
                "answer": Answer(answer="Persones treballadores de les entitats"),
                "content": Content(
                    description="Una jornada laboral dóna per molt",
                    content=[
                        CONEIXEMENT_COM_CONEIXER,
                        "Malgrat que no és habitual, algunes entitats disposen de suficients recursos per contractar a personal. Aquestes persones contractades també solen resultar claus per a l'obtenció d'informació, encara que en alguns casos la seua activitat està purament centrada en l'entitat que han de gestionar i tenen un coneixement molt limitat de la resta de les entitats existents.  Altres vegades, però, el fet de dedicar una jornada laboral completa a la seua activitat fa que tinguen un coneixement profund de tot el que existeix en la zona, així com també confiança personal amb molts agents clau. En aquest cas, un intercanvi de correus electrònics o trucades pot servir per estalviar moltes hores d'investigacions.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Persones treballadores de l'administració pública que es relacionen directament amb les entitats"
                ),
                "content": Content(
                    description="Aprofiteu els recursos de l'administració",
                    content=[
                        CONEIXEMENT_COM_CONEIXER,
                        "L'administració pública, malgrat tindre menys llibertat de moviments en general, també disposa de molts recursos que es poden aprofitar, com els canals de difusió oficials. Si és possible, es poden aprofitar aquests canals per arribar a més gent i detectar ràpidament els agents clau.",
                    ],
                ),
            },
        ],
    },
)

topic2["questions"] = questions2
TOPICS.append(topic2)

topic3 = {
    "topic": Topic(
        name="Disseny i execució de les activitats",
        description="Per a qualsevol procés de dinamització, cal planificar i dissenyar les activitats que s'organitzaran partint d'una sèrie de criteris d'ordre i format més enllà de les activitats. Cal pensar també el perfil de les entitats participants i les seues necessitats particulars.",
    ),
}

ACTIVITATS_ACCESSIBILITAT = "És habitual que les persones que organitzen un procés no tinguen un coneixement expert dels criteris d'accessibilitat, conciliació, llenguatge inclusiu, etc. En aquest sentit, és molt recomanable contactar amb entitats que treballen visibilitzant este tipus de qüestions o contractar ajuda professional per tal de dissenyar correctament les activitats i no segregar cap persona."
ACTIVITATS_ACCESSIBILITAT_2 = "Algunes consideracions a tindre en compte per als espais accessibles és que siguen accessibles en cadira de rodes sense necessitat d'elevador o ascensor (que poden avariar-se) o que el seu entorn en si siga accessible i arribe el transport públic. També és important considerar que siguen espais propers i familiars al públic objectiu, ja que espais desconeguts poden desincentivar la participació."

questions3 = []
questions3.append(
    {
        "question": Question(
            question="Els espais on s'organitzen les activitats compleixen els principis d'accessibilitat universal? I els materials que volem utilitzar?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="No ens haviem plantejat el tema i no sabem si els compleixen"
                ),
                "content": Content(
                    description="Sempre és bon moment per començar",
                    content=[
                        ACTIVITATS_ACCESSIBILITAT,
                        ACTIVITATS_ACCESSIBILITAT_2,
                        "El tema de l'accessibilitat és complex i requereix d'una atenció contínua, però progressivament es pot aconseguir millorar l'accessibilitat de tots els espais i materials utilitzats.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="No compleixen els principis perquè no trobem alternatives viables per al que volem fer"
                ),
                "content": Content(
                    description="Imaginació al poder",
                    content=[
                        ACTIVITATS_ACCESSIBILITAT,
                        ACTIVITATS_ACCESSIBILITAT_2,
                        "Disposar d'espais accessibles a tota la població és un deure fonamental de qualsevol ajuntament. Si una població no disposa d'espais accessibles universalment és important reclamar-li que esmene la situació. Mentrestant, es pot consultar amb les pròpies persones que es veuen afectades per aquesta falta d'alternatives per saber com voldrien ells que es resolguera el problema. De vegades, fer un acte ocupant la via pública és alhora una solució al problema de l'accessibilitat i una oportunitat de denunciar la falta d'alternatives.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="En alguns casos si, però no sempre és possible"
                ),
                "content": Content(
                    description="Cal oferir alternatives",
                    content=[
                        ACTIVITATS_ACCESSIBILITAT,
                        ACTIVITATS_ACCESSIBILITAT_2,
                        "En els casos en que no siga possible aconseguir espais accessibles, cal fer tot el possible per oferir alternatives a les persones que es vegen afectades. Una opció, per exemple, és retransmetre en directe l'acte perquè qualsevol persona el puga seguir des de casa. En aquest cas, és important disposar de la opció que qualsevol persona en remot puga fer preguntes i interactuar com la resta del públic presencial.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Si, sempre compleixen els principis d'accessibilitat universal"
                ),
                "content": Content(
                    description="Aneu per bon camí!",
                    content=[
                        "Enhorabona pel vostre compromís amb l'accessibilitat! Tanmateix, qualsevol activitat o material sempre es pot millorar per fer-lo més accessible. Hi ha espais que malgrat ser tècnicament accessibles requereixen més esforç per a les persones amb diversitat funcional que altres (per exemple, espais en pisos superiors respecte a altres a nivell de carrer, o espais estrets respecte a altres més amplis). Les xerrades es poden fer més accessibles proporcionant interpretació en llengua de signes, i els vídeos afegint subtítols. Algunes persones pateixen de sensibilitat química o son sensibles als espais amb molt de soroll, pel que necessiten ser informats per avançat de si l'espai i l'activitat respecten els seus límits abans de plantejar-se anar.",
                        "És impossible fer-ho perfecte, però amb voluntat i assessorament expert sempre es pot millorar.",
                    ],
                ),
            },
        ],
    },
)

ACTIVITATS_CONCILIACIO = "Cal planificar les activitats intentant facilitar l'assistència del màxim de persones possibles, tenint en compte les seues necessitats de conciliació personal, familiar i laboral. Una manera de fer-ho és aprofitar els espais organitzatius ja existents, com els espais de reunió periòdica, ja que les persones involucrades ja han adaptat els seus horaris per poder anar. Si no es disposa d'opcions clares similars, cal fer prospeccions o enquestes, intentant arribar a la major diversitat possible de persones per no deixar cap col·lectiu fora. Per norma general, les activitats no haurien d'acabar més tard de les 19.30h per conciliació familiar. La opció que sol permetre la màxima assistència és el cap de setmana, com el dissabte de matí."

questions3.append(
    {
        "question": Question(
            question="Quines són les necessitats de determinades persones per conciliar l'assistència a les activitats amb la seua vida personal i familiar?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="El nostre públic objectiu no té problemes de conciliació"
                ),
                "content": Content(
                    description="Tothom té coses a fer",
                    content=[
                        "Malgrat que puguem pensar que el nostre públic en particular no tindrà problemes en adaptar-se al nostre horari, tothom té compromisos on anar, encara que siga per quedar amb els amics. És important no prejutjar i en cas de dubte fer una consulta.",
                        ACTIVITATS_CONCILIACIO,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="La majoria de les persones tenen un treball remunerat"
                ),
                "content": Content(
                    description="Activitats de vesprada",
                    content=[
                        "Generalment, els treballs remunerats tenen horari de matí, pel que en aquest cas seria preferible fer les activitats de vesprada, a partir de les 17.30h, però això podria variar, pel que és preferible no prejutjar i en cas de dubte fer una consulta.",
                        ACTIVITATS_CONCILIACIO,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="La majoria de les persones tenen responsabilitats familiars i/o domèstiques"
                ),
                "content": Content(
                    description="Activitats de matí",
                    content=[
                        "En el cas de persones responsables de menors i sense treball remunerat, possiblement el millor moment és el matí. Tanmateix, aquest rarament és el cas, ja que les responsabilitats familiars i domèstiques tenen una variabilitat molt major que les del treball remunerat, de manera que pot ser complicat trobar un moment que convinga a la majoria de les persones. Un possible compromís, si això passa, és fer dos o més grups i alternar els horaris que més li convenen a cada grup.",
                        ACTIVITATS_CONCILIACIO,
                    ],
                ),
            },
            {
                "answer": Answer(answer="Desconeixem les necessitats de conciliació"),
                "content": Content(
                    description="Cal informar-se primer",
                    content=[
                        "Independentment de quina siga la resposta, és imprescindible fer un mínim d'indagació per poder escollir els moments de les activitats facilitant la màxima assistència.",
                        ACTIVITATS_CONCILIACIO,
                    ],
                ),
            },
        ],
    },
)

ACTIVITATS_DIVERSITAT = "Quan es realitza un procés participatiu que pretèn implicar a tota la població d'un territori, cal aconseguir la participació dels diferents sectors socials tenint en compte els principals eixos de desigualtat i els col·lectius més vulnerables per garantir que la seua veu estiga representada en els espais de presa de decisions."
ACTIVITATS_DIVERSITAT_2 = "Els diferents sectors socials requereixen atencions diferents, ja que alguns estan sobre o infrarepresentats, i alguns tenen problemes específics que els dificulten la participació. La perspectiva de gènere interseccional dona ferramentes per tractar amb la consideració que es mereix aquesta diversitat i incloure-la sense excloure a ningú."

questions3.append(
    {
        "question": Question(
            question="Estem tenint en compte la diversitat de perfils socials en l'organització de les activitats? Com prioritzem les entitats i les persones que les integren?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="No tenim en compte els diferents perfils socials"
                ),
                "content": Content(
                    description="És important tindre en compte la diversitat existent",
                    content=[
                        ACTIVITATS_DIVERSITAT,
                        ACTIVITATS_DIVERSITAT_2,
                        "Afrontar aquesta problemàtica requereix, primer de tot, voluntat per part de qui està impulsant el procés per prendre's seriosament el repte que això suposa. Suposant que hi haja voluntat, existeixen nombroses associacions amb experiència en el tema que poden guiar a l'hora de tindre en compte els seus col·lectius concrets. També pot ser interessant, si és possible, contractar l'acompanyament de persones expertes en introduir la perspectiva de gènere interseccional en projectes, per realitzar un plantejament que no deixe cap veu fora del procés.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Coneixem la diversitat de perfils socials, però no fem una priorització entre aquests"
                ),
                "content": Content(
                    description="Alguns perfils requereixen més atenció que altres",
                    content=[
                        ACTIVITATS_DIVERSITAT,
                        ACTIVITATS_DIVERSITAT_2,
                        "Conéixer els diferents perfils socials existents és un primer pas, però és igualment important fer una priorització en quant a l'esforç que es dedicarà a cadascun. En igualtat de tractament, hi haurà col·lectius que, per un major accés a la informació o una major disponibilitat de temps, participaran en sobremesura, mentre que altres estaran infrarepresentats. En cas de no poder revertir aquesta situació i de trobar-se amb que el perfil dels participants no és divers, cal fer un esforç per donar més veu als perfils més desafavorits.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Volem prioritzar la participació de col·lectius discriminats, però no sabem com fer-ho"
                ),
                "content": Content(
                    description="Hi ha molts recursos disponibles",
                    content=[
                        ACTIVITATS_DIVERSITAT,
                        ACTIVITATS_DIVERSITAT_2,
                        "Sabent que hi ha voluntat, es pot contactar amb les nombroses associacions amb experiència en el tema que poden guiar a l'hora de tindre en compte els seus col·lectius concrets. També pot ser interessant, si és possible, contractar l'acompanyament de persones expertes en introduir la perspectiva de gènere interseccional en projectes, per realitzar un plantejament que no deixe cap veu fora del procés.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Fem accions concretes per assegurar una participació diversa"
                ),
                "content": Content(
                    description="La diversitat s'ha de treballar de manera contínua",
                    content=[
                        ACTIVITATS_DIVERSITAT,
                        ACTIVITATS_DIVERSITAT_2,
                        "Si ja teniu en compte la perspectiva de gènere interseccional per assegurar una participació diversa, enhorabona! És un primer pas imprescindible. Però no oblideu que en aquest tema, com en qualsevol tema complex, sempre és possible seguir millorant. No dubteu a seguir qüestionant si podeu fer millor les accions que ja feu, i consulteu amb associacions de col·lectius discriminats o amb persones expertes que us puguen acompanyar en aquest camí de millora.",
                    ],
                ),
            },
        ],
    },
)


ACTIVITATS_RELACIO = "S'ha d'evitar abastar massa objectius en una única jornada: les activitats curtes i disteses afavoreixen la continuïtat de les entitats en el procés"
ACTIVITATS_RELACIO_2 = "Una activitat que funciona bé per trencar el gel és una passejada per l'entorn del procés, durant la qual es visite als diferents actors que participaran. A cada parada del camí, una persona representant de l'entitat visitada es presenta i explica breument en què consisteix la seua activitat. D'aquesta manera es fan les presentacions d'una manera més relaxada que en una reunió, alhora que mentre es camina es desenvolupen altres converses que creen més confiança."

questions3.append(
    {
        "question": Question(
            question="Hi ha una relació de confiança prèvia entre les entitats o persones que participaran del procés?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="Les entitats que participen del procés no es coneixien en absolut anteriorment"
                ),
                "content": Content(
                    description="Cal començar per conèixer-se",
                    content=[
                        "En els casos en els que no hi ha relació de confiança prèvia entre les participants en el procés, cal dissenyar les activitats de manera que els primers contactes esdevinguen en un ambient distés que afavorisca l'apropament i la participació entre elles",
                        ACTIVITATS_RELACIO,
                        ACTIVITATS_RELACIO_2,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Les entitats es coneixen entre si només per referències"
                ),
                "content": Content(
                    description="Creem vincles i confiança",
                    content=[
                        "Quan les entitats es coneixen només per referències, cal actuar pràcticament com si no es conegueren en absolut. Cal dissenyar les activitats de manera que els primers contactes esdevinguen en un ambient distés que afavorisca l'apropament i la participació entre elles",
                        ACTIVITATS_RELACIO,
                        ACTIVITATS_RELACIO_2,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Les entitats fan col·laboracions i intercanvis puntuals entre elles"
                ),
                "content": Content(
                    description="Enfortim la relació existent",
                    content=[
                        "Si ja existeix una relació prèvia, però aquesta no és molt profunda, es poden limitar les presentacions al mínim (encara que segueix sent important fer-les, per cortesia) i passar directament a treballar en els objectius del procés en si.",
                        "De totes maneres, és important evitar abastar massa objectius en una única jornada: les activitats curtes i disteses afavoreixen la continuïtat de les entitats en el procés",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Les entitats han generat espais de col·laboració i xarxes de suport entre elles"
                ),
                "content": Content(
                    description="Aprofitem els espais existents",
                    content=[
                        "Que les entitats es coneguen i col·laboren activament entre elles és un molt bon primer pas per afrontar un procés de dinamització comunitària. Cal aprofitar les estructures que ja estan creades, ja que degut al fet que ja tenen una inèrcia pròpia, poden servir per afrontar directament els objectius del procés sense la burocràcia prèvia que requereixen espais acabats de crear",
                        "És important, però, remarcar i saber diferenciar en tot moment les estructures que ja existien i el procés que es porta a terme actualment. Si la comunicació no és clara, les persones poden confondre d'on sorgeixen les propostes o qui està liderant el procés. També poden interferir, si s'abusa d'elles, en el funcionament normal de les xarxes de suport: el procés que s'inicia hauria de ser respectuós amb les dinàmiques existents",
                    ],
                ),
            },
        ],
    },
)

topic3["questions"] = questions3
TOPICS.append(topic3)

topic4 = {
    "topic": Topic(
        name="Disseny del pla de comunicació",
        description="En tot procés de dinamització és molt important la comunicació tant per convocar a les entitats participants com per a fer-ne ressò d'este. En aquest sentit, cal tindre en compte que segons el context social, la importància o l'eficàcia de determinats canals de comunicació pot canviar i hem de saber adaptar-nos.",
    ),
}

COMUNICACIO_CANVI_ESTRATEGIA = "A més, sempre cal deixar un marge de maniobra per canviar d'estratègia en cas que ens adonem que algun dels canals de comunicació que hem escollit no funciona. Si s'ha de canviar la manera de fer les comunicacions, és preferible fer-ho al principi del procés que quan aquest ja està consolidat."

questions4 = []
questions4.append(
    {
        "question": Question(
            question="A quin públic va dirigida la comunicació del procés? Estem tenint en compte l'escletxa digital en la comunicació? Podem involucrar agents clau en alguna de les etapes del pla de comunicació?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="No tenim clar a quin públic ens dirigim ni quins coneixements té"
                ),
                "content": Content(
                    description="Cal conéixer el públic objectiu",
                    content=[
                        "Cap estratègia comunicativa pot funcionar sense conéixer el públic objectiu: aquest és el primer pas per poder definir tota la resta, des dels canals que es faran servir fins a la freqüència amb què s'enviarà la informació o el to que tindran els missatges (més formal o més informal).",
                        "Cal considerar de manera sistemàtica els objectius del procés, les necessitats que es volen cobrir, les persones a les que beneficiarà o perjudicarà, i els resultats que s'esperen. Tenint en compte tot això, cal definir el públic objectiu, i a partir d'ahi definir la estratègia comunicativa.",
                        COMUNICACIO_CANVI_ESTRATEGIA,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim clar a quin públic ens dirigim, però desconeixem les seues habilitats i els possibles agents clau"
                ),
                "content": Content(
                    description="Cal considerar l'escletxa digital",
                    content=[
                        "Conéixer les habilitats del públic objectiu és fonamental per aconseguir una comunicació efectiva. Si no es té en compte l'escletxa digital, es poden deixar fora de les comunicacions a sectors molt grans de població, que podrien ser imprescindibles per a l'èxit del procés. En cas de detectar-se, caldrà recórrer a formes de comunicació més físiques, com publicacions en la premsa tradicional o penjades de cartells.",
                        COMUNICACIO_CANVI_ESTRATEGIA,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim clar el públic objectiu i els seus coneixements, però no coneixem agents a qui involucrar en la comunicació"
                ),
                "content": Content(
                    description="Cal localitzar agents clau",
                    content=[
                        "Tindre clar el públic objectiu i els seus coneixements és fonamental per fer una bona comunicació, però aquesta serà molt més efectiva si es troben agents clau, persones o entitats amb arrelament a l'entorn on s'executa el procés de dinamització comunitària i que ja tenen una comunicació habitual amb la seua població.",
                        "Com ja s'ha indicat anteriorment, un procés previ de coneixement de l'entorn és imprescindible per aconseguir un procés que funcione. A través d'enquestes o d'entrevistes a diferents persones es pot anar estirant del fil fins trobar aquells agents més centrals en l'entorn on es treballarà.",
                        COMUNICACIO_CANVI_ESTRATEGIA,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim clar a qui dirigir-nos i com, i també coneixem agents clau en contacte amb el nostre públic"
                ),
                "content": Content(
                    description="Aprofiteu els agents clau",
                    content=[
                        "Encara que es tinga clar a qui va dirigida la comunicació i quins son els canals a fer servir, sempre convé recolzar-se en els agents clau. Aquestes persones, que ja tenen relacions de confiança amb la població i s'hi comuniquen de manera habitual, seran molt més efectives en transmetre la informació que missatges rebuts des de fonts desconegudes.",
                        "Progressivament, si es demostra que la estratègia de comunicació funciona, es pot dependre progressivament menys dels agents clau i més dels canals oficials de comunicació que s'hagen establert.",
                        COMUNICACIO_CANVI_ESTRATEGIA,
                    ],
                ),
            },
        ],
    },
)

COMUNICACIO_FREQUENCIA = "Sempre és recomanable no enviar comunicacions supèrflues a les entitats, ja que és habitual que aquestes ja estiguen saturades de missatges i poden acabar decidint ignorar-los. És recomanable fer un cronograma previ de les comunicacions per temàtiques que es volen tractar; d'aquesta manera s'ajustarà millor què, com, i quan es vol comunicar."
COMUNICACIO_CONTRACTAR = "En cas de tindre dubtes o no saber com fer alguna d'aquestes coses, i si es disposa de recursos econòmics, es pot subcontractar la comunicació del procés a una entitat experta en aquest tipus de feina, o contractar una assistència tècnica que oferisca unes nocions sobre com crear o millorar el pla de comunicació"

questions4.append(
    {
        "question": Question(
            question="Quin tipus de comunicacions realitzarem? Quin en serà el contingut? Variarà el contingut de les comunicacions en funció del canal que usem? I segons el públic al què ens dirigim? Amb quina freqüència es volen fer les comunicacions?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="No tenim clar quines comunicacions farem ni quan, improvitzarem"
                ),
                "content": Content(
                    description="Cal tindre un pla, encara que se l'ignore",
                    content=[
                        "Fins i tot si es considera que es té capacitat d'improvització suficient per a dur a terme la comunicació sense planificar o si es pensa que no cal fer cap pla perquè no se li farà cas, val la pena fer-lo igualment. L'exercici de fer un pla de comunicació fa sortir a la superfície temes que no es consideraven de manera conscient i obliga a justificar les decisions inconscients a un mateix. No cal que el pla siga molt detallat, només amb respondre breument a les preguntes anteriors ja és un bon primer pas. Fer un calendari ràpid de les principals comunicacions que es volen fer també permetrà veure si hi ha prou de temps per fer totes les comunicacions, o a l'inrevés, si hi ha períodes llargs del procés durant el qual no es preveu comunicar res, el qual pot fer pensar que el procés s'ha paralitzat.",
                        COMUNICACIO_FREQUENCIA,
                        COMUNICACIO_CONTRACTAR,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="No tenim planificades les comunicacions, però tenim experts en els diferents canals de comunicació que les adaptaran"
                ),
                "content": Content(
                    description="A mig procés ja és massa tard",
                    content=[
                        "Cal planificar, encara que siga breument, les comunicacions que es volen realitzar, des del principi del procés. Si no es fa d'aquesta manera, es pot trobar quan ja s'ha fet la meitat del procés que algunes coses s'haurien d'haver comunicat al principi, o que tot el que es vol comunicar fins al final del procés és una quantitat excessiva d'informació per al temps que queda.",
                        "Tindre experts en els diferents canals de comunicació és una bona manera de fer que els missatges arriben de manera òptima, però de totes maneres també cal tindre en compte la variable temporal. Per exemple, un missatge a través de xarxes socials arriba molt més ràpidament que a través d'un cartell físic, i per tant el cartell s'ha de penjar amb un marge de temps superior per aconseguir el mateix efecte.",
                        COMUNICACIO_FREQUENCIA,
                        COMUNICACIO_CONTRACTAR,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim clar quines comunicacions volem fer i quan, però no les pensàvem adaptar al canal i al públic de cada cas"
                ),
                "content": Content(
                    description="Cada canal i públic tenen les seues peculiaritats",
                    content=[
                        "Com s'ha explicat anteriorment, cada canal de comunicació (la comunicació presencial, les xarxes socials, els llocs web o el correu electrònic) té els seus avantatges i inconvenients. També tenen cadascú les seues pròpies convencions: hi ha xarxes socials més serioses, com Linkedin, i altres més informals, com Instagram. En altres, com en TikTok, s'ignoraria qualsevol missatge que no fóra bàsicament visual. És per tant imprescindible conéixer els canals que es volen fer servir i adaptar els missatges a cadascun; si no es controla un canal, millor no fer-lo servir.",
                        "El mateix passa per al públic: els missatges els percebran de manera molt diferent adolescents que persones de més de 60 anys, i també persones nadiues que migrants. El to, la longitud, la llengua utilitzada... S'han d'escollir pensant en el públic en cada cas.",
                        COMUNICACIO_FREQUENCIA,
                        COMUNICACIO_CONTRACTAR,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Hem dissenyat un calendari de comunicacions i publicacions on especifiquem a qui van dirigides, quins missatges volem transmetre, quins canals utilitzarem i quan les farem"
                ),
                "content": Content(
                    description="Aneu per bon camí!",
                    content=[
                        "Amb tota aquesta planificació és molt probable que la comunicació acabe sent exitosa. De totes maneres, cal no oblidar que s'ha de ser flexibles, i anar adaptant la planificació feta segons les necessitats canviants del procés de dinamització, donat que és molt probable que siga necessari fer-ho (per canvis en la programació d'activitats, en els objectius, en els agents implicats, etc.)",
                        COMUNICACIO_FREQUENCIA,
                        COMUNICACIO_CONTRACTAR,
                    ],
                ),
            },
        ],
    },
)

COMUNICACIO_PLANER = "Sempre és recomanable fer servir un llenguatge clar, planer, sense excés de tecnicismes. El llenguatge tècnic és útil i necessari entre persones tècniques; en un procés de dinamització comunitària, la comprensió mútua és prioritària respecte a la exactitud"
COMUNICACIO_DIVERS = "També és recomanable fer servir un llenguatge inclusiu i respectuós, que no faça sentir fora del procés a ningú. En general, això requerirà adaptar el registre segons el canal que fem servir o a qui ens dirigim."

questions4.append(
    {
        "question": Question(
            question="Estem utilitzant un llenguatge clar, respectuós i que puguen entendre totes les persones? El llenguatge que hem utilitzat és inclusiu respecte a la diversitat de col·lectius?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="No hem fet una reflexió sobre el llenguatge que utilitzem"
                ),
                "content": Content(
                    description="El llenguatge determina la realitat",
                    content=[
                        "Si no s'ha fet una reflexió sobre el llenguatge que es fa servir, és recomanable fer-la. El llenguatge determina en bona part les percepcions que tenen les persones sobre la realitat, i per tant influeix de manera decisiva, per a bé i per a mal, en les decisions que es prenen.",
                        COMUNICACIO_PLANER,
                        COMUNICACIO_DIVERS,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Intentem fer servir un llenguatge inclusiu, però el tema que tractem és altament tècnic i requereix de coneixements per entendre'l"
                ),
                "content": Content(
                    description="La comprensió mútua té preferència",
                    content=[
                        COMUNICACIO_PLANER,
                        "Això no significa que s'hagen d'evitar per complet els tecnicismes, sinó que s'han de fer servir només quan siguen imprescindibles, i sempre prèvia explicació del que signifiquen, aquesta també, en llenguatge planer",
                        COMUNICACIO_DIVERS,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Intentem fer servir un llenguatge clar i senzill, però no sabem com fer-lo inclusiu"
                ),
                "content": Content(
                    description="Recolzeu-vos en els recursos existents",
                    content=[
                        "Existeixen multitud d'entitats que treballen per fer un mon més inclusiu, des de diferents perspectives; és important conéixer-les i posar-se en contacte amb elles, que podran donar bones indicacions o referir a altres recursos. També existeixen moltes guies de llenguatge inclusiu disponibles de manera gratuïta, també des de diferents perspectives: d'igualtat de gènere, antiracistes, anticapacitistes, etc. En última instància, i si es disposa de recursos, es pot contractar un acompanyament expert en aquests temes perquè revisen els textos i els facen més inclusius."
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Treballem en profunditat els missatges perquè estiguen adaptats en cada moment al col·lectiu al que ens dirigim i siguen fàcilment comprensibles"
                ),
                "content": Content(
                    description="Aneu per bon camí!",
                    content=[
                        "Treballar els missatges per fer-los fàcilment comprensibles i adaptats al públic objectiu és una base genial per tindre una bona comunicació. Tanmateix, recordeu que sempre es pot millorar, i que els missatges es poden revisar periòdicament per anar actualitzant-los i redactant-los encara millor, tal com evolucione el procés. A més, és recomanable contrastar amb les persones participants si realment els missatges s'han adaptat de manera efectiva, o malgrat l'esforç segueixen sense ser comprensibles."
                    ],
                ),
            },
        ],
    },
)

COMUNICACIO_LLENGUES_DIGLOSSIA = "cal tindre en compte les situacions de diglòssia i prioritzar les llengües minoritzades. De la mateixa manera que cal incloure a les persones discriminades amb actuacions pensades específicament per a elles, cal considerar les llengües com un pla més on es produeixen discriminacions que cal combatre."
COMUNICACIO_LLENGUES = (
    "Sovint, cal traduir els continguts a diverses llengües per arribar a diferents perfils socials. Cal tindre en compte que les persones valorem més els missatges que rebem en la nostra llengua materna, i per tant per arribar al màxim de gent possible la traducció és la única opció. A més d'això, "
    + COMUNICACIO_LLENGUES_DIGLOSSIA
)
COMUNICACIO_TRADUCCIONS = "Cal tindre en compte que fer les traduccions requereix temps, i per tant és especialment important planificar les comunicacions per poder-les traduir abans d'enviar-les. Aquestes traduccions les poden fer persones que participen del procés, en cas que tinguen els coneixements necessaris i voluntat per fer-ho, o també serveis de traducció professionals, dels quals n'hi ha en pràcticament totes les llengües."

questions4.append(
    {
        "question": Question(
            question="En quina llengua hem de fer els materials de comunicació del procés? Hem tingut en compte la diversitat lingüística de les entitats del territori? Estem tenint en compte la situació de diglòssia per protegir les llengües minoritzades?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="Cada persona fa els materials segons la llengua en què se sent més còmoda"
                ),
                "content": Content(
                    description="Sempre es pot traduir després",
                    content=[
                        COMUNICACIO_LLENGUES,
                        "Una bona manera de fer això és que cadascú escriga en la llengua en que se sent més còmode, i posteriorment fer les traduccions necessàries abans d'enviar les comunicacions.",
                        COMUNICACIO_TRADUCCIONS,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tots els materials es fan utilitzant la llengua que coneix la majoria de la població objectiu"
                ),
                "content": Content(
                    description="Conéixer la llengua no és el mateix que preferir-la",
                    content=[
                        COMUNICACIO_LLENGUES,
                        "És habitual escollir la llengua que coneix la majoria de la població per estalviar recursos, però s'ha de tindre en compte que conèixer una llengua no és el mateix que preferir-la, i a més, que fer servir certes llengües és un missatge en si mateix. Per exemple, una persona que parla àrab, rebent un cartell en àrab, pensarà (encertadament) que qui ha organitzat l'activitat la té en compte de manera especial, i que per tant li val la pena anar. Altres persones poden ignorar sistemàticament processos en els que es fa servir una única llengua, ignorant la diversitat existent.",
                        COMUNICACIO_TRADUCCIONS,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Els materials es fan en les llengües principals dels col·lectius a qui ens dirigim"
                ),
                "content": Content(
                    description="Cal tindre en compte les llengües minoritzades",
                    content=[
                        "Fer els materials en les llengües principals dels col·lectius als que es dirigeix el projecte és un bon punt de partida, però també "
                        + COMUNICACIO_LLENGUES_DIGLOSSIA,
                        COMUNICACIO_TRADUCCIONS,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Els materials es fan en diverses llengües, prioritzant les llengües minoritzades"
                ),
                "content": Content(
                    description="Aneu per bon camí!",
                    content=[
                        "Realitzar els materials en les principals llengües del públic objectiu, prioritzant les minoritzades, és una base genial per a la comunicació. Tanmateix, recordeu que sempre es pot millorar, incloent llengües addicionals en la mesura que siga factible, o segmentant els públics de manera que cada persona reba les comunicacions en la llengua que prefereix, és a dir, per exemple, no enviant el mateix correu a tothom, sinó preguntar prèviament la llengua de comunicació de preferència, i enviar a cadascú el correu amb la llengua indicada.",
                        COMUNICACIO_TRADUCCIONS,
                    ],
                ),
            },
        ],
    },
)

COMUNICACIO_FEEDBACK = "Si es disposa dels recursos necessaris, és important fixar un canal de comunicació invers, que servisca per a que les persones i entitats participants comuniquen els seus dubtes, demandes i suggeriments a l'equip dinamitzador."
COMUNICACIO_RESPONDRE = "Aquest canal ha de ser àgil, no ha de requerir esforç d'utilitzar (com descarregar-se una APP, registrar-se a una web, etc.) i s'ha de respondre sempre i en un temps raonable (pocs dies)."
COMUNICACIO_RESPONDRE_CONSEQUENCIES = "De fet, si els comentaris no es responen, és preferible directament no oferir cap via de contacte, ja que el fet d'oferir-la genera unes expectatives que, en veure's falses, suposen un major descontent amb la organització"
COMUNICACIO_UNA_PERSONA = "És recomanable que aquesta via de comunicació l'atenga una única persona, ja que aquesta tindrà més controlats tant els punts forts com les mancances del procés, i oferirà una resposta uniforme a totes les persones que contacten (o a la mateixa persona si contacta diverses vegades)."

questions4.append(
    {
        "question": Question(
            question="Hem oferit alguna via de contacte funcional que pose en comú l'agent dinamitzador amb els agents participants en cas que estos últims tinguen algun dubte o suggeriment? Podem garantir un temps reduït de resposta als dubtes, demandes, queixes i suggeriments? Hi ha una persona responsable de coordinar la comunicació del procés?"
        ),
        "answers": [
            {
                "answer": Answer(answer="No tenim cap via de contacte oficial"),
                "content": Content(
                    description="Cal tindre un mecanisme de retorn de la informació",
                    content=[
                        COMUNICACIO_FEEDBACK,
                        f"{COMUNICACIO_RESPONDRE} {COMUNICACIO_RESPONDRE_CONSEQUENCIES}",
                        COMUNICACIO_UNA_PERSONA,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim una via de contacte oficial, però no té un encarregat concret i no sempre es respon"
                ),
                "content": Content(
                    description="Sempre s'ha de respondre",
                    content=[
                        "Tindre una via de contacte oficial és un bon primer pas, però aquesta ha de ser funcional i respondre's sempre. "
                        + COMUNICACIO_RESPONDRE_CONSEQUENCIES
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim diverses vies de contacte, però cadascuna té un encarregat de respondre que té un criteri diferent de la resta"
                ),
                "content": Content(
                    description="És preferible tindre una única via de contacte",
                    content=[
                        "Tindre diverses vies de contacte pot ser necessari en alguns casos, però no és la opció més recomanable. En cas de rebre comunicacions a partir de diversos canals (com per exemple les diferents xarxes socials) el millor que es pot fer és redirigir aquestes persones al canal oficial",
                        COMUNICACIO_UNA_PERSONA,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim una via de contacte oficial, amb un encarregat de les respostes que la revisa cada dia"
                ),
                "content": Content(
                    description="Aneu per bon camí!",
                    content=[
                        "Tindre una via de contacte oficial amb respostes coherents i ràpides és una base genial per a una bona experiència per part de les persones que volen aportar comentaris. Tanmateix, recordeu que sempre es pot millorar, en aquest cas per exemple creant respostes estàndard a preguntes habituals, de manera que es reduisca el temps necessari per gestionar els comentaris rebuts, o recollint les preguntes habituals i adaptant la comunicació sortint perquè les coses sobre les que es pregunta siguen més clares, o fins i tot recollint aquestes preguntes en una pàgina de «Preguntes freqüents» que tothom puga consultar abans d'enviar la consulta."
                    ],
                ),
            },
        ],
    },
)

topic4["questions"] = questions4
TOPICS.append(topic4)


topic5 = {
    "topic": Topic(
        name="Posada en marxa de les activitats",
        description="És imprescindible per a tot procés de dinamització que generem una relació creixent de confiança entre les entitats participants i l'equip dinamitzador i entre elles mateixes. És, per això, que cal una bona planificació i començar per activitats més disteses per, a poc a poc, anar-ne augmentant la implicació. Cal que argumentem perquè estem duent a terme aquest procés i hem de saber transmetre els beneficis del mateix per a la comunitat.",
    ),
}


EXECUCIO_DISCURS = "Cal ser capaços de crear un context comú sobre allò que estem fent i dotar-lo d'arguments; deixar clar el punt del que es parteix, els objectius plantejats i per tant on es vol arribar. Cal assegurar-se que les persones participants son conscients de la utilitat del procés per a la comunitat i també que ho saben transmetre a la resta de la població."

questions5 = []
questions5.append(
    {
        "question": Question(
            question="Tenim un discurs articulat per explicar els objectius del procés?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="No hem plantejat un discurs comú per explicar el procés"
                ),
                "content": Content(
                    description="És imprescindible tindre una mínima base comú",
                    content=[
                        EXECUCIO_DISCURS,
                        "Si aquest discurs no s'ha preparat, cal fer-ho abans de començar el procés, i que totes les persones implicades el tinguen clar, a poder ser en un document compartit i sempre actualitzat que no deixe dubtes en cas de discrepància d'opinions i interpretacions.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim molt clar els objectius del procés, no ens cal preparar com explicar-lo"
                ),
                "content": Content(
                    description="Explícit és millor que implícit",
                    content=[
                        EXECUCIO_DISCURS,
                        "Per més que parega que tothom està en el mateix punt, si aquesta informació no s'ha fet explícita és possible que hi haja divergència d'interpretacions, que posteriorment puguen dur a problemes interns i discussions. El mateix procés de fer explícits els objectius i el discurs per explicar-los pot fer eixir a la llum algunes d'aquestes divergències.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim un discurs preparat per explicar el procés, però no el fa servir tothom"
                ),
                "content": Content(
                    description="La coherència és fonamental",
                    content=[
                        EXECUCIO_DISCURS,
                        "Rebre missatges contradictoris per part de les persones que porten a terme un procés de dinamització comunitària és una de les pitjors coses que els pot passar als participants, que un dia poden estar il·lusionats amb el projecte i el següent replantejar-se la seua participació. Si no tothom fa servir el discurs que s'ha preparat, això pot ser senyal que no estan completament d'acord amb aquest, i és impresdindible posar sobre la taula aquestes divergències i resoldre-les el més pronte possible en el procés, abans que els problemes es facen grans i més difícils de tractar.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim un discurs preparat que totes les persones del procés fan servir de manera consistent"
                ),
                "content": Content(
                    description="Aneu per bon camí!",
                    content=[
                        "Tindre un discurs preparat que es comunica de manera consistent i habitual és una bona base per a generar una imatge externa que no done lloc a confusions. Tanmateix, recordeu que sempre es pot millorar, per exemple, refinant progressivament el discurs, adaptant-lo a les novetats del procés i fent-lo més planer i fàcil d'entendre. A més, es pot publicar el discurs de manera que quede especialment clar quina és la versió oficial, i alhora donar-li una autoritat major que quan el discurs el fa una persona que no se sap fins a quin punt representa el procés."
                    ],
                ),
            },
        ],
    },
)

EXECUCIO_FLEXIBILITAT = "El procés de dinamització s'ha de poder adaptar per deixar espai a possibles canvis que puguen donar-se al llarg de l'execució de les activitats. És a dir, cal reservar temps i espais de coordinació per fer seguiment i avaluació continua del procés de dinamització i estar obertes a possibles canvis en la planificació d'este, per exemple, per programar noves activitats que puguen sorgir de les inquietuds dels col·lectius o introduir en el contingut de les activitats ja programades les necessitats detectades durant les primeres trobades."
EXECUCIO_CLIMA = "El pla d'activitats ha de garantir que es genere un clima de confiança entre les entitats participants i l'equip dinamitzador per evitar la pèrdua d'interès o l'abandonament del procés. Les primeres activitats han de servir per trencar el gel, establir relacions de confiança, generar relat comú, destacar bons exemples, informar, etc. Poc a poc, a mesura que avance el procés i es genere una dinàmica de treball, es pot demanar més implicació a les entitats participants i marcar objectius més ambiciosos per a cada activitat."

questions5.append(
    {
        "question": Question(
            question="Tenim un pla d'activitats que continga una bona progressió en les activitats des de la presentació fins a jornades que requereixen més dedicació? El pla permet gestionar l'aparició de nous objectius sorgits al llarg del procés a partir de les necessitats i inquietuds de les persones participants?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="No tenim un pla d'activitats clar, les activitats es van fent segons apareixen les idees"
                ),
                "content": Content(
                    description="Cal tindre un pla, encara que se l'ignore",
                    content=[
                        "Fins i tot si es considera que es té capacitat d'improvització suficient per a dur a terme les activitats sense planificar o si es pensa que no cal fer cap pla perquè no se li farà cas, val la pena fer-lo igualment. L'exercici de fer un pla d'activitats fa sortir a la superfície temes que no es consideraven de manera conscient i obliga a justificar les decisions inconscients a un mateix. No cal que el pla siga molt detallat, només amb tindre una aproximació de quantes activitats es faran i quins continguts aproximats tindran ja permet veure si hi ha períodes llargs de temps sense activitat, si hi ha objectius que queden descuidats dins del pla d'activitats, o si l'activitat és tan intensa que no hi haurà marge de maniobra si canvien els objectius o hi ha imprevistos.",
                        EXECUCIO_CLIMA,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim un pla d'activitats preparat i tancat des del principi"
                ),
                "content": Content(
                    description="Sempre s'ha de ser flexible",
                    content=[
                        EXECUCIO_FLEXIBILITAT,
                        "Aquests canvis no s'han de fer a la lleugera, improvisant, sinó de la mateixa manera que es va preparar el pla inicialment: a partir dels objectius, tenint en compte els precedents i el temps disponible fins a la fi del procés, per tornar a tindre un pla que siga coherent però que reflexe els canvis de la realitat.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim un pla d'activitats preparat, però no el seguim"
                ),
                "content": Content(
                    description="Si no s'utilitza, millor reformular-lo",
                    content=[
                        "El fet que existisca un pla que no es segueix és una indicació clara que aquest pla no està ben formulat o no és útil. En aquest cas, val la pena tornar-lo a fer: és probable que, amb l'experiència obtinguda i tenint clares les raons per les que el pla no estava sent útil, es puga millorar considerablement el pla fet inicialment.",
                        EXECUCIO_CLIMA,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim un pla d'activitats preparat, que inclou revisions periòdiques segons l'evolució del procés"
                ),
                "content": Content(
                    description="Aneu per bon camí!",
                    content=[
                        "Tindre un pla preparat i revisar-lo periòdicament és una base genial perquè les activitats es puguen fer i funcionen. Tanmateix, recordeu que sempre es pot millorar, per exemple, augmentant progressivament l'exigència que se li posa a les activitats a mesura que augmenta la confiança entre les entitats i a mesura que l'equip dinamitzador millora la seua habilitat en gestionar-les."
                    ],
                ),
            },
        ],
    },
)

EXECUCIO_INCLUSIO = "Per facilitar la inclusió de totes les mirades en els processos de dinamització comunitària cal incloure la perspectiva de gènere interseccional, és a dir, invertir temps en dissenyar processos, programes i intervencions que incloguen la diversitat i els diferents eixos de desigualtat, on es tenen en compte factors com el gènere, l'edat, la raça, la procedència, la llengua, la religió, el patrimoni, l'orientació sexual i la condició física i mental."
EXECUCIO_ENQUESTES = "Es poden recollir dades desagregades de participació en el procés en general i en cada activitat a partir d'enquestes estadístiques anònimes, on s'incloga informació del gènere, edat, procedència, ètnia i diversitat funcional de cada participant."

questions5.append(
    {
        "question": Question(
            question="Totes les persones i entitats participen per igual en les activitats? S'ha escoltat la veu de totes les persones implicades?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="No fem un seguiment de qui ha participat més o menys en el procés"
                ),
                "content": Content(
                    description="Si no sabem, no podem saber",
                    content=[
                        "El fet de no conéixer informació bàsica com per exemple la de participació, impedeix posteriorment saber si el procés ha complert els seus objectius, ja que es podria donar el cas que pensem que si que s'han aconseguit, quan en realitat s'han aconseguit només per a un sector de població molt concret que potser no és el més rellevant.",
                        EXECUCIO_INCLUSIO,
                        EXECUCIO_ENQUESTES,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Hi ha entitats i/o persones que han participat molt més que la resta"
                ),
                "content": Content(
                    description="Cal limitar les intervencions excessives",
                    content=[
                        "Cal assegurar-se d'escoltar la veu de totes les persones que acudeixen a les activitats, especialment al principi del procés. Sovint, hi ha persones que monopolitzen les converses, demanant la paraula quan ja han intervingut i altres persones no, allargant massa les intervencions i interrompent a altres persones. És imprescindible limitar aquestes intervencions, de manera respectuosa però ferma, per dos raons principalment. La primera, per respecte a la resta de persones que també es volen expressar. I la segona, perquè mentre una persona repeteix els mateixos arguments s'està perdent la informació que hagueren pogut aportar altres persones.",
                        EXECUCIO_INCLUSIO,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Hi ha entitats i/o persones que han participat molt menys que la resta"
                ),
                "content": Content(
                    description="Cal animar a la participació",
                    content=[
                        "Cal assegurar-se d'escoltar la veu de totes les persones que acudeixen a les activitats, especialment al principi del procés. Sovint, hi ha persones que malgrat acudir assíduament a les activitats, no prenen mai la paraula. És imprescindible animar a aquestes persones a participar, donat que molt probablement poden aportar punts de vista no escoltats fins al moment. En cas que no vulguen fer-ho en públic per vergonya, cal igualment detectar la situació i recollir les seues aportacions posteriorment en privat, per assegurar-se que se senten escoltades i aprofitar el que tenen a dir.",
                        EXECUCIO_INCLUSIO,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="La participació ha estat diversa i equilibrada"
                ),
                "content": Content(
                    description="Aneu per bon camí!",
                    content=[
                        "Enhorabona per aconseguir una participació diversa i equilibrada, no és gens fàcil! Com en tot, sempre es pot anar més enllà, discriminant positivament cap a col·lectius tradicionalment discriminats, o, en cas que les dades de participació hagen sigut basades en percepcions, recollint dades reals.",
                        EXECUCIO_ENQUESTES,
                    ],
                ),
            },
        ],
    },
)

EXECUCIO_RETORN = "És recomanable fer un retorn dels resultats del procés de dinamització comunitària a les entitats i persones participants. Aquesta devolució permet presentar el treball fet, els objectius assolits i la participació de les entitats. Aquest pas serveix tant per fer un xicotet reconeixement a les persones per la seua dedicació i esforç en el procés com per informar a persones que no han participat d'aquest"

questions5.append(
    {
        "question": Question(
            question="Com compartim els resultats del procés comunitari amb les entitats implicades al llarg del procés?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="Una vegada acabat el procés no es fan més activitats amb les participants"
                ),
                "content": Content(
                    description="Tot procés necessita un tancament",
                    content=[
                        EXECUCIO_RETORN,
                        "Si no es fa cap tipus de tancament, les participants es poden veure confoses o defraudades de la confiança dipositada en l'equip dinamitzador, pensant que potser s'ha abandonat el procés sense més o que s'ha deixat de comptar amb elles sense explicació.",
                    ],
                ),
            },
            {
                "answer": Answer(answer="Els resultats s'envien per correu electrònic"),
                "content": Content(
                    description="Tothom té dret a conéixer els resultats",
                    content=[
                        "Malgrat que enviar els resultats a les participants és un pas bàsic i imprescindible, després d'un procés amb diverses activitats presencials, fer un tancament per correu queda fred. A més, hi poden haver persones que no han participat del procés però que poden estar interessades en els seus resultats, pel que és preferible organitzar un acte de retorn presencial.",
                        EXECUCIO_RETORN,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Es fa un informe dels resultats que es comparteix per xarxes"
                ),
                "content": Content(
                    description="Un acte presencial llueix més",
                    content=[
                        "Malgrat que publicar l'informe de resultats perquè el puga veure tothom és un bon primer pas, després d'un procés amb diverses activitats presencials, fer un tancament en remot queda fred. És preferible organitzar un acte de retorn presencial.",
                        EXECUCIO_RETORN,
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Es fa una presentació pública dels resultats on es conviden a les participants del procés"
                ),
                "content": Content(
                    description="Aneu per bon camí!",
                    content=[
                        "Fer una presentació presencial dels resultats amb les participants és la millor manera de tancar un procés de dinamització comunitària. Per fer-la més efectiva, és interessant reservar un espai per al reconeixement i comentaris per part de les participants, i explicar tant el treball fet com els objectius assolits."
                    ],
                ),
            },
        ],
    },
)

topic5["questions"] = questions5
TOPICS.append(topic5)

topic6 = {
    "topic": Topic(
        name="Avaluació de l'impacte",
        description="Per arrodonir el procés participatiu hem de ser capaços de fer una correcta avaluació de l'impacte, sobretot, tenint en compte que aquest ha de poder continuar. Encara més, podem utilitzar la preparació del retorn a les entitats com a base per a l'informe d'avaluació de l'impacte. Tanmateix, podem aprofundir-ne més i incloure dades de caràcter més útil per a l'entitat dinamitzadora.",
    ),
}

questions6 = []
questions6.append(
    {
        "question": Question(
            question="Què ha canviat arran de la dinamització del procés? Podem comparar la situació de partida amb l'actual?"
        ),
        "answers": [
            {
                "answer": Answer(
                    answer="No tenim clar si s'ha donat un canvi arrel del procés"
                ),
                "content": Content(
                    description="Cal recollir dades",
                    content=[
                        "Poder comparar la situació anterior amb l'actual és fonamental per poder avaluar l'impacte del procés i determinar si s'han acomplert els objectius. Sempre hi ha temps per fer algun tipus de comparativa: encara que no s'hagen recollit dades d'abans de començar el procés, es poden recollir de després. A més, es poden realitzar enquestes a les persones participants en les que se'ls pregunte per les seues percepcions en quant a l'acompliment dels objectius del procés."
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Tenim dades sobre com és la situació ara, però no de com era abans (o viceversa)"
                ),
                "content": Content(
                    description="Es pot fer un anàlisi de percepcions",
                    content=[
                        "Si no es disposa de dades de partida, es pot realitzar una enquesta a les persones participants en la que se'ls pregunte per les seues percepcions en quant a l'acompliment dels objectius del procés. Malgrat que les dades siguen subjectives, son millors que no tindre'n cap."
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Hem detectat canvis significatius en l'entorn, però seria necessari seguir dinamitzant-ho per a enfortir i consolidar les iniciatives ciutadanes sorgides"
                ),
                "content": Content(
                    description="Busqueu suport professional",
                    content=[
                        "Els inicis dels projectes solen ser moments d'il·lusió que funcionen bé amb voluntarietat i assumint entorns més precaris, pensant que seran temporals. Quan els projectes s'allarguen i es volen consolidar, es fa més necessari abandonar aquesta precarietat i dotar-se d'estructures més fortes i coneixements més profunds. Per a tot això és convenient comptar amb l'ajuda de persones expertes que puguen guiar en aquest procés de consolidació, ja siga formant a les persones de les iniciatives perquè siguen autònomes o externalitzant les tasques més tècniques."
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Donat que partíem d'un entorn molt dinamitzat, hem pogut centrar-nos en consolidar espais de participació i generar noves iniciatives ciutadanes"
                ),
                "content": Content(
                    description="Enhorabona!",
                    content=[
                        "La consolidació dels espais de participació és un èxit molt important per als processos de dinamització comunitària. És fonamental seguir en aquesta línia, i recollir dades periòdicament, tant estadístiques com subjectives, de les persones que participen d'aquests espais, per poder avaluar si efectivament els espais segueixen consolidant-se o en canvi comencen a perdre força. També és fonamental fer un seguiment de les noves iniciatives ciutadanes, perquè no desapareguen poc després de crear-se, com sol ser habitual en projectes incipients."
                    ],
                ),
            },
        ],
    },
)


AVALUACIO_SINERGIES = "Tot i que el procés no haja suposat grans canvis estructurals, cal ser capaços de detectar canvis com el fet que hagen aparegut noves sinèrgies entre entitats, que s'hagen fet propostes de col·laboració entre elles, que les entitats haguen detectat interessos comuns sobre els que treballar o hagen arribat a algun tipus d'acord, etc."

questions6.append(
    {
        "question": Question(
            question="Han sorgit noves iniciatives o entitats a partir del procés? Alguns exemples podrien ser: xarxa d'espais compartits, xarxes de suport mutu, xarxes d'intercanvi de materials, grups de consum, projectes conjunts o col·laboracions puntuals entre diverses entitats, nous convenis o acords amb algun servei públic..."
        ),
        "answers": [
            {
                "answer": Answer(answer="Ho desconeixem"),
                "content": Content(
                    description="Cal indagar",
                    content=[
                        AVALUACIO_SINERGIES,
                        "Si es desconeix si hi ha hagut algun tipus de canvi a partir del procés, encara s'està a temps de descobrir-ho. La millor manera de fer-ho és realitzar entrevistes als agents clau amb els que s'haja treballat durant el procés, que probablement hagen pogut detectar canvis diferents als detectats per les dinamitzadores.",
                    ],
                ),
            },
            {
                "answer": Answer(answer="No s'han creat noves iniciatives o entitats"),
                "content": Content(
                    description="Les novetats no ho son tot",
                    content=[
                        AVALUACIO_SINERGIES,
                        "Encara que no s'hagen creat noves iniciatives o entitats, es poden haver donat altres canvis tant o més importants, com la consolidació d'espais o la millora en el funcionament intern d'entitats ja existents. La millor manera de detectar aquest tipus de coses és realitzar entrevistes als agents clau amb els que s'haja treballat durant el procés, que probablement hagen pogut detectar canvis diferents als detectats per les dinamitzadores.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="S'han creat iniciatives o entitats, però han deixat de funcionar quan ha acabat la dinamització"
                ),
                "content": Content(
                    description="La llavor ja s'ha plantat",
                    content=[
                        "Encara que és molt frustrant veure com la feina feta i el progrés aconseguit desapareixen, cal veure les coses amb perspectiva i procurar minimitzar les pèrdues. Encara que les iniciatives desapareguen, no desapareixen les persones que hi van participar, les coses que van aprendre o les altres persones que van conèixer. Tot això és un bon caldo de cultiu per, en el futur, tindre una base sobre la que tornar a començar sense partir desde zero. Per això és important fer una bona avaluació i un bon tancament del procés, perquè aquesta informació quede registrada i, si algú ve després, ho tinga tot preparat per fer un altre procés de dinamització."
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="S'han creat iniciatives o entitats, que segueixen actives després del procés de dinamització"
                ),
                "content": Content(
                    description="Enhorabona!",
                    content=[
                        "No és fàcil aconseguir que noves entitats sorgides a partir d'un suport inicial siguen capaces de funcionar per elles mateixes, de manera que enhorabona! En aquest cas, també és important fer un bon tancament i avaluació del projecte, perquè tota la informació quede ben registrada i els contactes sorgits durant la dinamització inicial puguen continuar en endavant. Tindre aquest tancament ben fet també servirà perquè futurs possibles processos de dinamització coneguen la història i puguen reprendre la tasca feta, en cas que les iniciatives comencen a decaure o necessiten d'una consolidació."
                    ],
                ),
            },
        ],
    },
)

questions6.append(
    {
        "question": Question(
            question="Quin ha sigut l'impacte de les publicacions fetes en xarxes socials o en altres mitjans?"
        ),
        "answers": [
            {
                "answer": Answer(answer="Desconeixem l'impacte que han tingut"),
                "content": Content(
                    description="Moltes plataformes permeten medir l'impacte",
                    content=[
                        "Encara que no es conega, moltes plataformes de comunicació permeten saber amb bastanta exactitud l'impacte que han tingut les publicacions.",
                        "En el cas de les xarxes socials, com Twitter o Instagram, generalment proporcionen informes bastant detallats tant de les visualitzacions de les publicacions com de les interaccions rebudes, de vegades incloent informació sobre l'evolució temporal o la desagregació per diverses variables com el gènere i l'edat. Aquest tipus d'informacions permetran avaluar amb bastanta exactitud no només si l'impacte és l'esperat, sinó també si el públic al que s'ha arribat és el públic objectiu",
                        "En el cas del correu electrònic, és difícil saber l'impacte si els correus s'han enviat directament, però si s'han fet a través de plataformes de campanyes de comunicació, com ListMonk o MailChimp, aquestes acostumen a proporcionar dades sobre l'impacte aconseguit, com a mínim la quantitat de visualitzacions i la quantitat de «clics» (visites a enllaços). Aquesta informació, malgrat que no és tan detallada com la de les xarxes socials, també pot ser molt útil per avaluar l'impacte",
                        "En el cas de disposar de web propi, generalment qualsevol plataforma on el tinguem allotjat permetrà conéixer informació sobre les visites, desagregades per pàgina visitada, el qual permetrà saber quines de les informacions generen més interès. En cas de voler dades més detallades, es pot configurar un servei d'analítiques com Matomo o Google Analytics. Aquesta opció pot ser bastant complicada de fer tècnicament, però permet el màxim nivell de detall en les dades recollides, si se sap exactament la informació que es vol saber",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Han tingut poques visualitzacions i interaccions"
                ),
                "content": Content(
                    description="La reputació es guanya amb temps i esforç",
                    content=[
                        "Un error habitual en molts processos és el de crear nous perfils per al procés, que comencen des de zero i s'abandonen en acabar aquest. Aquesta no sol ser una bona opció, ja que requereixen molt d'esforç de posar en marxa, que es desaprofita molt pronte quan es tanquen. En comptes d'això, és preferible recolzar-se en comptes ja existents i amb un compromís de permanència en el futur. D'aquesta manera, no es desaprofita l'esforç, sinó al contrari, el projecte existent prèviament i el procés s'ajuden mútuament a guanyar projecció i seguidors."
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Han tingut moltes visualitzacions però poques interaccions"
                ),
                "content": Content(
                    description="Les interaccions tenen més valor",
                    content=[
                        "Malgrat que les visualitzacions tenen la seua importància, la clau real de l'èxit de la comunicació està en les interaccions: els «likes» en menor mesura, i, especialment, els comentaris. Quan les publicacions fetes generen reacció en els comentaris és quan realment han tingut un impacte real, que ha fet que l'interès de les persones haja sigut suficient per prendre's la molèstia de respondre.",
                        "Aconseguir interaccions és complicat i normalment requereix d'una atenció especial a l'estratègia de comunicació, alhora que estar al dia i aprofitar certs moments concrets per mesclar els objectius del projecte amb l'actualitat. És recomanable, si es disposa de recursos, buscar ajuda professional per millorar l'impacte en xarxes.",
                    ],
                ),
            },
            {
                "answer": Answer(
                    answer="Han tingut moltes visualitzacions i interaccions"
                ),
                "content": Content(
                    description="Enhorabona!",
                    content=[
                        "Aconseguir un bon impacte a xarxes és un bon primer pas per tindre un procés que funcione. Tanmateix, cal tindre present que l'impacte real s'obté en persona, amb l'implicació en el dia a dia i amb accions concretes que milloren la vida de les veïnes. Cal revisar contínuament que l'expectativa creada en xarxes es tradueix en activitat real, i preguntar-se el perquè si això no passa."
                    ],
                ),
            },
        ],
    },
)

topic6["questions"] = questions6
TOPICS.append(topic6)
