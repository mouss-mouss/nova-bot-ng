import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

# ═══════════════════════════ CONFIG ═══════════════════════════
PREFIX = "Nova"

# Les 13 types d'entreprise NationsGlory (Java) d'après le wiki officiel.
COMPANY_TYPES = [
    {"name": "Construction", "emoji": "⚒️"},
    {"name": "Ingénieurs", "emoji": "💡"},
    {"name": "Terraform", "emoji": "⛏️"},
    {"name": "Journalisme", "emoji": "📰"},
    {"name": "Casino", "emoji": "🎲"},
    {"name": "Prêt d'argent", "emoji": "💲"},
    {"name": "Immobilier", "emoji": "🏢"},
    {"name": "Trader", "emoji": "📈"},
    {"name": "Paris", "emoji": "🎯"},
    {"name": "Réparation", "emoji": "🔧"},
    {"name": "Électricité", "emoji": "⚡"},
    {"name": "Pétrolière", "emoji": "🛢️"},
    {"name": "Agricole", "emoji": "🌾"},
]

# Catégories globales (créées une seule fois pour tout le serveur)
ARRIVAL_CHANNEL = "📥┃arrivée"
LEAVE_CHANNEL = "📤┃départ"
RULES_CHANNEL = "📜┃règlement"

GLOBAL_CATEGORIES = [
    {
        "name": "👋・ACCUEIL",
        "channels": [
            {"name": ARRIVAL_CHANNEL, "type": "text", "read_only": True},
            {"name": LEAVE_CHANNEL, "type": "text", "read_only": True},
            {"name": RULES_CHANNEL, "type": "text", "read_only": True, "rules": True},
            {"name": "📌┃informations", "type": "text", "read_only": True},
        ],
    },
    {
        "name": "🌍・GLOBAL",
        "channels": [
            {"name": "📢┃annonces", "type": "text", "read_only": True},
            {"name": "💬┃général", "type": "text", "read_only": False},
            {"name": "🖼️┃médias", "type": "text", "read_only": False},
            {"name": "🤖┃commandes-bot", "type": "text", "read_only": False},
            {"name": "🔊┃vocal-général", "type": "voice"},
            {"name": "🔊┃vocal-détente", "type": "voice"},
        ],
    },
]

# ⚠️ Texte du règlement : modifie-le comme tu veux
RULES = [
    "Respecte tous les membres, aucune insulte ni harcèlement.",
    "Pas de spam, de pub ni de liens non autorisés.",
    "Utilise chaque salon pour son usage.",
    "Les décisions du staff et des directions sont à respecter.",
    "Les règles de NationsGlory s'appliquent aussi ici.",
]

# read_only=True -> seuls les admins (et le bot) peuvent écrire
# panel -> le bot poste un bouton qui ouvre un TICKET privé
PUBLIC_CHANNELS = [
    {"name": "📢┃annonce", "type": "text", "read_only": True},
    {"name": "📈┃promotion", "type": "text", "read_only": True},
    {"name": "🏅┃rank", "type": "text", "read_only": True},
    {"name": "📉┃dérank", "type": "text", "read_only": True},
    {"name": "📝┃recrutement", "type": "text", "read_only": True, "panel": "recrutement"},
    {"name": "🛒┃commande", "type": "text", "read_only": True, "panel": "commande"},
]

EMPLOYEE_CHANNELS = [
    {"name": "📢┃annonce", "type": "text", "read_only": True},
    {"name": "📰┃news", "type": "text", "read_only": True},
    {"name": "💬┃chat", "type": "text", "read_only": False},
    {"name": "🔊┃voc", "type": "voice"},
]
# ══════════════════════════════════════════════════════════════
