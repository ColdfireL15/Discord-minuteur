# Bot Discord - Minuteur

Un bot Discord simple et efficace pour gérer des minuteurs avec une interface visuelle propre.

## Fonctionnalités

- **Minuteur visuel** : Barre de progression qui se met à jour toutes les 30 secondes avec couleurs dynamiques
- **Interface propre** : Le channel se vide automatiquement à chaque nouveau minuteur
- **Commandes simples** : Tapez juste un nombre (ex: "5") pour lancer un minuteur
- **Arrêt manuel** : Tapez "stop" pour arrêter le minuteur en cours
- **Limite de sécurité** : Maximum 120 minutes (2 heures)
- **Notification** : Quand le minuteur est terminé le Bot affiche un message en notifiant l'utilisateur qui à initié le minuteur

## Prérequis

- Un bot Discord avec les permissions appropriées
- Les permissions suivantes pour le bot :
  - `Send Messages`
  - `Manage Messages` (pour nettoyer le channel)
  - `Embed Links`

## Installation

1. **Cloner le repository**

2. **Installer les dépendances**
   ```bash
   pip install -r app/requirements.txt
   ```

3. **Configuration**
   - Créer un fichier `.env` à la racine du projet
   - Ajouter vos tokens :
     ```
     DISCORD_BOT_TOKEN=votre_token_bot
     TIMER_CHANNEL_ID=id_du_channel_minuteur
     ```

4. **Lancer le bot**
   ```bash
   python app/app.py
   ```

## Utilisation

### Lancer un minuteur
Tapez simplement un nombre dans le channel dédié :
- `5` → Minuteur de 5 minutes
- `30` → Minuteur de 30 minutes
- `120` → Minuteur de 2 heures (maximum)

### Arrêter un minuteur
Tapez `stop` pour arrêter le minuteur en cours.

## Interface

Le bot affiche :
- **Barre de progression** visuelle avec pourcentage
- **Temps restant** et temps total
- **Couleurs dynamiques** :
  - 🟢 Vert : Plus de 5 minutes restantes
  - 🟠 Orange : Entre 1 et 5 minutes
  - 🔴 Rouge : Moins d'1 minute

## 🔧 Dépendances

- `discord.py` : API Discord
- `python-dotenv` : Gestion des variables d'environnement
