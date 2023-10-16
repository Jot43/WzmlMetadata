#!/usr/bin/env python3
from contextlib import suppress
from aiohttp import ClientSession
from requests import get as rget
from urllib.parse import quote as q
from pycountry import countries as conn
from urllib.parse import urlsplit
from pyrogram.filters import command, regex
from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.errors import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty, ReplyMarkupInvalid

from bot import LOGGER, bot, config_dict, user_data
from bot.helper.telegram_helper.filters import CustomFilters
from bot.helper.telegram_helper.message_utils import sendMessage, editMessage
from bot.helper.telegram_helper.bot_commands import BotCommands
from bot.helper.telegram_helper.button_build import ButtonMaker

LIST_ITEMS = 4
IMDB_GENRE_EMOJI = {"Action": "🚀", "Adult": "🔞", "Adventure": "🌋", "Animation": "🎠", "Biography": "📜", "Comedy": "🪗", "Crime": "🔪", "Documentary": "🎞", "Drama": "🎭", "Family": "👨‍👩‍👧‍👦", "Fantasy": "🫧", "Film Noir": "🎯", "Game Show": "🎮", "History": "🏛", "Horror": "🧟", "Musical": "🎻", "Music": "🎸", "Mystery": "🧳", "News": "📰", "Reality-TV": "🖥", "Romance": "🥰", "Sci-Fi": "🌠", "Short": "📝", "Sport": "⛳", "Talk-Show": "👨‍🍳", "Thriller": "🗡", "War": "⚔", "Western": "🪩"}
MDL_API = "http://kuryana.vercel.app/" #Public API ! Do Not Abuse !

async def mydramalist_search_url(_, message):
    if ' ' in message.text:
        temp = await sendMessage(message, '<i>Searching in MyDramaList ...</i>')
        title = message.text
        url_components = urlsplit(title)
        path_components = url_components.path.split('/')
        slug = path_components[-1]
        #title = message.text.split(' ', 1)[1]
        user_id = message.from_user.id
        async with ClientSession() as sess:
            async with sess.get(f'{MDL_API}/id/{q(slug)}') as resp:
                mdlurl = (await resp.json())["data"]
            plot = mdlurl.get('synopsis')
        if plot and len(plot) > 300:
            plot = f"{plot[:300]}..."
        return {
            'title': mdlurl.get('title'),
            'complete_title': mdlurl.get('complete_title'),
            'native_title': mdlurl['others'].get("native_title"),
            'score': mdlurl['details'].get('score'),
            'aka': mdlurl['others'].get("also_known_as"),
            'episodes': mdlurl['details'].get("episodes"),
            'type': mdlurl['details'].get("type"),
            "cast": list_to_str(mdlurl.get("casts"), cast=True),
            "country": list_to_hash([mdlurl['details'].get("country")], True),
            'aired_date': mdlurl['details'].get("aired", 'N/A'),
            'aired_on': mdlurl['details'].get("aired_on"),
            'org_network': mdlurl['details'].get("original_network"),
            'duration': mdlurl['details'].get("duration"),
            'watchers': mdlurl['details'].get("watchers"),
            'ranked': mdlurl['details'].get("ranked"),
            'popularity': mdlurl['details'].get("popularity"),
            'related_content': list_to_str(mdlurl['others'].get("related_content")),
            'native_title': list_to_str(mdlurl['others'].get("native_title")),
            'director': list_to_str(mdlurl['others'].get("director")),
            'screenwriter': list_to_str(mdlurl['others'].get("screenwriter")),
            'genres': list_to_hash(mdlurl['others'].get("genres"), emoji=True),
            'tags': list_to_str(mdlurl['others'].get("tags")),
            'poster': mdlurl.get('poster').replace('c.jpg?v=1', 'f.jpg?v=1').strip(),
            'synopsis': plot,
            'rating': str(mdlurl.get("rating"))+" / 10",
            'content_rating': mdlurl['details'].get("content_rating"),
            'url': mdlurl.get('link'),
        }
        template = config_dict['MDL_TEMPLATE']
        if mdlurl and template != "":
            cap = template.format(**mdlurl)
        else:
            cap = "<i>No Data Received</i>"
        if mdlurl.get('poster'):
            try: #Invoke Raw Functions
                await message.reply_to_message.reply_photo(mdlurl["poster"], caption=cap)
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                poster = mdlurl["poster"].replace('f.jpg?v=1', 'c.jpg?v=1')
                await sendMessage(message.reply_to_message, cap,  poster)
        else:
            await sendMessage(message.reply_to_message, cap)
        await message.delete()
    else:
        #await query.answer()
        await message.delete()
        await message.reply_to_message.delete()

              """
        for drama in mdl['results']['dramas']:
            #shortened_title = f[:15]}..." if len(drama.get('title')) > 15 else drama.get('title')
            # Check if the drama type is 'Korean Drama' before adding it to the buttons
            if drama.get('type') == 'Korean Drama':
                buttons.ibutton(f"🎬 {drama.get('title')} ({drama.get('year')})", f"mdl {user_id} drama {drama.get('slug')}")
        buttons.ibutton("🚫 Close 🚫", f"mdl {user_id} close")
        await editMessage(temp, '<b><i>Korean Dramas found on MyDramaList :</i></b>', buttons.build_menu(1))
    else:
        await sendMessage(message, f'<i>Send Movie / TV Series Name along with /{BotCommands.MyDramaListCommand} Command</i>')
"""
"""
async def extract_MDL(slug):
    async with ClientSession() as sess:
        async with sess.get(f'{MDL_API}/id/{slug}') as resp:
            mdlurl = (await resp.json())["data"]
    plot = mdl.get('synopsis')
    if plot and len(plot) > 300:
        plot = f"{plot[:300]}..."
    return {
        'title': mdl.get('title'),
        'complete_title': mdl.get('complete_title'),
        'native_title': mdl['others'].get("native_title"),
        'score': mdl['details'].get('score'),
        'aka': mdl['others'].get("also_known_as"),
        'episodes': mdl['details'].get("episodes"),
        'type': mdl['details'].get("type"),
        "cast": list_to_str(mdl.get("casts"), cast=True),
        "country": list_to_hash([mdl['details'].get("country")], True),
        'aired_date': mdl['details'].get("aired", 'N/A'),
        'aired_on': mdl['details'].get("aired_on"),
        'org_network': mdl['details'].get("original_network"),
        'duration': mdl['details'].get("duration"),
        'watchers': mdl['details'].get("watchers"),
        'ranked': mdl['details'].get("ranked"),
        'popularity': mdl['details'].get("popularity"),
        'related_content': list_to_str(mdl['others'].get("related_content")),
        'native_title': list_to_str(mdl['others'].get("native_title")),
        'director': list_to_str(mdl['others'].get("director")),
        'screenwriter': list_to_str(mdl['others'].get("screenwriter")),
        'genres': list_to_hash(mdl['others'].get("genres"), emoji=True),
        'tags': list_to_str(mdl['others'].get("tags")),
        'poster': mdl.get('poster').replace('c.jpg?v=1', 'f.jpg?v=1').strip(),
        'synopsis': plot,
        'rating': str(mdl.get("rating"))+" / 10",
        'content_rating': mdl['details'].get("content_rating"),
        'url': mdl.get('link'),
    }

"""
def list_to_str(k, cast=False):
    if not k:
        return ""
    elif len(k) == 1:
        return str(k[0])
    elif LIST_ITEMS:
        k = k[:int(LIST_ITEMS)]
    if cast:
        return ' '.join(f'''<a href="{elem.get('link')}">{elem.get('name')}</a>,''' for elem in k)[:-1]
    return ' '.join(f'{elem},' for elem in k)[:-1]

def list_to_hash(k, flagg=False, emoji=False):
    listing = ""
    if not k:
        return ""
    elif len(k) == 1:
        if not flagg:
            if emoji:
                return str(IMDB_GENRE_EMOJI.get(k[0], '')+" #"+k[0].replace(" ", "_").replace("-", "_"))
            return str("#"+k[0].replace(" ", "_").replace("-", "_"))
        try:
            conflag = (conn.get(name=k[0])).flag
            return str(f"{conflag} #" + k[0].replace(" ", "_").replace("-", "_"))
        except AttributeError:
            return str("#"+k[0].replace(" ", "_").replace("-", "_"))
    elif LIST_ITEMS:
        k = k[:int(LIST_ITEMS)]
        for elem in k:
            ele = elem.replace(" ", "_").replace("-", "_")
            if flagg:
                with suppress(AttributeError):
                    conflag = (conn.get(name=elem)).flag
                    listing += f'{conflag} '
            if emoji:
                listing += f"{IMDB_GENRE_EMOJI.get(elem, '')} "
            listing += f'#{ele}, '
        return f'{listing[:-2]}'
    else:
        for elem in k:
            ele = elem.replace(" ", "_").replace("-", "_")
            if flagg:
                conflag = (conn.get(name=elem)).flag
                listing += f'{conflag} '
            listing += f'#{ele}, '
        return listing[:-2]

"""
async def mdlurl_callback(_, query):
    message = query.message
    user_id = query.from_user.id
    data = query.data.split()
    if user_id != int(data[1]):
        await query.answer("Not Yours!", show_alert=True)
    elif data[2] == "data":
        await query.answer()
        mdl = await extract_MDL(data[3])
        buttons = ButtonMaker()
        buttons.ibutton("🚫 Close 🚫", f"mdlurl {user_id} close")
        
        template = config_dict['MDL_TEMPLATE']
        if mdlurl and template != "":
            cap = template.format(**mdlurl)
        else:
            cap = "<i>No Data Received</i>"
        if mdlurl.get('poster'):
            try: #Invoke Raw Functions
                await message.reply_to_message.reply_photo(mdlurl["poster"], caption=cap)
            except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
                poster = mdlurl["poster"].replace('f.jpg?v=1', 'c.jpg?v=1')
                await sendMessage(message.reply_to_message, cap, buttons.build_menu(1), poster)
        else:
            await sendMessage(message.reply_to_message, cap, buttons.build_menu(1), 'https://te.legra.ph/file/5af8d90a479b0d11df298.jpg')
        await message.delete()
    else:
        await query.answer()
        await message.delete()
        await message.reply_to_message.delete()
"""
bot.add_handler(MessageHandler(mydramalist_search_url, filters=command(BotCommands.MyDramaListURLCommand) & CustomFilters.authorized & ~CustomFilters.blacklisted))
#bot.add_handler(CallbackQueryHandler(mdlurl_callback, filters=regex(r'^mdlurl')))