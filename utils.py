import discord

from config import PREFIX

PO = discord.PermissionOverwrite


def norm(name):
    """Discord met les noms de salons textuels en minuscules avec des tirets."""
    return name.lower().replace(" ", "-")


def role_names(type_name):
    return f"{PREFIX} Employé {type_name}", f"{PREFIX} Direction {type_name}"


def staff_roles(guild, kind, type_name):
    """Rôles qui ont accès aux tickets de cette branche."""
    emp_name, dir_name = role_names(type_name)
    emp = discord.utils.get(guild.roles, name=emp_name)
    direction = discord.utils.get(guild.roles, name=dir_name)
    roles = [direction] if kind == "recrutement" else [emp, direction]
    return [r for r in roles if r]


def build_overwrites(guild, roles, read_only, locked):
    ow = {}
    if locked:
        ow[guild.default_role] = PO(view_channel=False)
        for r in roles:
            ow[r] = PO(
                view_channel=True,
                send_messages=not read_only,
                connect=True,
                speak=True,
            )
    elif read_only:
        ow[guild.default_role] = PO(send_messages=False)
    if read_only or locked:
        # le bot doit pouvoir écrire (panneaux, messages d'accueil)
        ow[guild.me] = PO(view_channel=True, send_messages=True, embed_links=True, connect=True)
    return ow


async def ensure_category(guild, name, overwrites=None):
    cat = discord.utils.get(guild.categories, name=name)
    if cat:
        return cat, False
    cat = await guild.create_category(name, overwrites=overwrites or {})
    return cat, True


async def ensure_channel(guild, category, ch, roles, locked):
    """Crée le salon seulement s'il n'existe pas déjà dans la catégorie."""
    ow = build_overwrites(guild, roles, ch.get("read_only", False), locked)
    if ch["type"] == "voice":
        existing = discord.utils.get(category.voice_channels, name=ch["name"])
        if existing:
            return existing, False
        return await guild.create_voice_channel(ch["name"], category=category, overwrites=ow), True

    existing = discord.utils.get(category.text_channels, name=norm(ch["name"]))
    if existing:
        return existing, False
    return await guild.create_text_channel(ch["name"], category=category, overwrites=ow), True


async def post_once(channel, embed, view=None):
    """Poste un message seulement s'il n'a pas déjà été posté par le bot."""
    async for m in channel.history(limit=25):
        if m.author.id == channel.guild.me.id and m.embeds and m.embeds[0].title == embed.title:
            return False
    await channel.send(embed=embed, view=view)
    return True


def find_text_channel(guild, name):
    return discord.utils.get(guild.text_channels, name=norm(name))
