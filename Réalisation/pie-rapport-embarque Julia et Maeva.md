# Rapport d'Activité : Pôle Embarqué

## 1. Contexte et Objectifs de l'Équipe
L'objectif principal de l'équipe était l'intégration du système de contrôle avec les composants physiques du bateau, afin de garantir un système fonctionnel et testé pour la compétition.

Dès le début du projet, une contrainte majeure a été identifiée : l'accès tardif au châssis physique du bateau. En conséquence, les efforts se sont concentrés sur la viabilité de la transition des fonctionnalités développées sur le **BlueBoat** vers le prototype final. Le BlueBoat, une plateforme robotique de surface préexistante, a été crucial comme banc d'essai : il a permis de simuler et de valider les algorithmes de contrôle et la communication logicielle en parallèle de la construction du châssis officiel, garantissant ainsi que le développement des autres parties du projet ne soit pas retardé par les contraintes matérielles.

Les étapes de travail ont été axées sur l'exploration technique, l'analyse des composants et la communication, tout en respectant l'évolution des exigences de l'organisation (changements concernant la présence ou l'absence d'un pilote, impactant directement la configuration du châssis).

## 2. Étapes Exécutées et Organisation

### Étape 1 : Recherche et Étude de Marché
* **Activités :** Réalisation d'un benchmarking sur les différents contrôleurs disponibles, incluant une analyse de viabilité technique, de difficulté d'intégration et une étude budgétaire.
* **Méthodologie :** Nous avons mis en place un processus de validation rigoureux basé sur les exigences de performance de la compétition, les contraintes d'étanchéité et le budget alloué. Cette analyse comparative a conduit au choix de conserver le système **BlueOS**. Ce choix est justifié par sa grande modularité, sa base solide sur **ArduPilot** et le fait que l'équipe disposait déjà d'une carte compatible, optimisant ainsi les ressources financières et techniques.
* **Décisions :** Confirmation de l'utilisation de BlueOS et de l'architecture ArduPilot.
* **Durée :** Environ 3 semaines.

### Étape 2 : Analyse de Viabilité de Communication
* **Activités :** Tests de communication (interfaces et difficultés techniques), incluant des essais sur le BlueBoat et sur le moteur disponible.
* **Point Critique :** Le moteur sélectionné pour ses performances ne possédait pas de support natif pour communiquer avec le firmware choisi. Après arbitrage, il a été décidé de maintenir ce moteur malgré cette absence de compatibilité immédiate, en allouant du temps au développement d'une interface de communication personnalisée.
* **Durée :** 4 semaines.

### Étape 3 : Intégration des Composants
* **Activités (En cours) :** Mise en œuvre des adaptations nécessaires pour le châssis final et préparation de l'intégration du moteur et des périphériques validés précédemment. Cette phase assure la transition concrète des acquis du BlueBoat vers la structure finale.
* **Durée :** Phase finale du développement.

### Étape 4 : Tests et Validation
* **Activités (En cours) :** Procédures de tests finaux, étalonnage des capteurs et ajustements en vue de la compétition.

## 3. Difficultés Rencontrées
Tout au long du projet, l'équipe a dû faire face à deux défis techniques majeurs :
1.  **Compatibilité logicielle :** Difficultés lors de l'intégration du système *BlueOS* avec le contrôleur *VESC*.
2.  **Interopérabilité matérielle :** Problèmes de communication avec le moteur et complexité de l'intégration des nouveaux composants sur le châssis officiel. Bien que ces risques aient été cartographiés dès le début, leur résolution a nécessité un investissement temporel important qui a impacté le calendrier global.