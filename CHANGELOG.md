# Changelog

Tots els canvis notables del projecte es documentaran en aquest arxiu.

El format es basa en el de [Keep
aChangelog](https://keepachangelog.com/en/1.0.0/), i el projecte s'adhereix al
[Versionat semàntic](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed


## [1.2.0] - 2024-09-XX

### Added

- S'han afegit converses tipus xat dins de l'aplicació, en substitució del funcionament
  fins al moment, corresponent a fer les converses per correu electrònic
- Es registra la pàgina d'origen de les peticions («Has lliga?» i «Descobreix») per poder
  saber quina es fa servir més a la pràctica
- Es registren tots els correus electrònics enviats per poder validar-ne el contingut
- Algunes necessitats es consideren «publicables»
- Es poden publicar anuncis de les necessitats publicables
- Una persona externa pot revisar tots els anuncis publicats en una pàgina pública
- Una persona externa pot enviar un missatge a una organització que ha publicat un anunci
- Una organització pot configurar si rebre un correu electrònic sempre que es rep un
  missatge per un anunci
- Una organització pot revisar els missatges rebuts pels seus anuncis
- Una usuària que intenta canviar el seu correu electrònic pot rectificar i tornar a
  l'actual
- Afegida la guia metodològica i el segell a la portada
- S'envia un correu de benvinguda a l'aplicació al cap de dos dies del registre, amb el
  segell adjunt

### Changed

- Revisats els estils de tota l'aplicació
- Les converses s'accepten automàticament, donat que es fan dins de l'aplicació i no
  impliquen els correus electrònics dels participants
- Les converses que estaven pendents d'acceptar s'accepten
- Les converses que s'havien rebutjat es marquen com a que no es va realitzar un
  intercanvi
- S'han afegit noves categories i etiquetes de recursos, mentre que altres s'han reagrupat
- Quan s'inicia una petició d'intercanvi, es premarquen les opcions indicades en
  necessitats
- L'informe de l'aplicació ara és configurable amb múltiples opcions

### Removed

- S'han retirat totes les referències a converses per correu electrònic
- S'han retirat totes les referències a converses rebutjades
- S'han retirat les opcions de preferències relacionades amb acceptar converses

### Fixed

- Substituïts alguns usos de `style` en línia per classes CSS


## [1.1.0] - 2024-05-13

### Added

- S'ha traduït l'aplicació completa al castellà
- S'ha afegit l'opció de canviar el correu electrònic amb el que es va fer el
  registre
- S'ha afegit una forma jurídica addicional
- S'ha afegit una nova categoria amb dos noves etiquetes
- S'han afegit notificacions immediates quan se sol·liciten o rebutgen peticions
- S'ha afegit més contingut a les notificacions periòdiques
- Arxius bàsics per a una _Progressive Web APP_
- Limitació de distància a la que es fan les lligues
- Indicació de si un Local és accessible
- _Tour_ de l'aplicació després de completar l'alta
- Opció d'esborrar per complet el compte d'usuari i l'organització creada

### Changed

- Millores en el disseny del procés d'alta d'una entitat
- Millores en el text del correu de petició d'un recurs
- Petites millores en la usabilitat de les pàgines de lligues, cerca i peticions
- Redisseny complet de la pàgina de preferències
- Corregida l'assignació de coordenades a partir d'una adreça
- Adaptació dels estils a pantalles mòvils

