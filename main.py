#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram import InlineKeyboardButton,InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telegram.constants import ParseMode


from movie_info import MovieByImdb, MovieInfo

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    # await update.message.reply_text("Help!")
    keyboard = [[InlineKeyboardButton("Yes", callback_data="yes"),
             InlineKeyboardButton("No", callback_data="no")]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Do you like bots?", reply_markup=reply_markup)



async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    movie_name = update.message.text
    movie = MovieInfo(movie_name)

    keyboard = []

    for i in movie.data.get("Search"):
        keyboard.append([InlineKeyboardButton(f"{i.get('Title')} [{i.get('Year')}]",callback_data=i.get("imdbID"))])    

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Select the movie from this list", reply_markup=reply_markup)

async def selected_movie(update, context):
    query = update.callback_query
    await query.answer()  # This is required to stop the 'loading' animation on Telegram.

    search = MovieByImdb(query.data)

    CAPTION = f"""
Movie: <b><code>{search.Title}</code></b>
Genre: <b>{search.Genre}</b>
Imdb Rating: <b>{search.imdbRating}</b>
Director: <b>{search.Director}</b>
Duration: <b>{search.Runtime}</b>

Rated: {search.Rated}
Released: {search.Released}
Actors: {search.Actors}

Plot: 
<i>{search.Plot}</i>
    """
    keyboard = [
        [InlineKeyboardButton("IMDB", url=f"https://www.imdb.com/title/{query.data}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Send an image from a URL
    await query.delete_message()
    await context.bot.send_photo(
        chat_id=query.message.chat_id,
        photo=search.Poster,
        caption=CAPTION,
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup

    )

def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = "7085362036:AAEul6gY9YGuNzFiGeli_CDcfrGV2gXsk1g"
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.add_handler(CallbackQueryHandler(selected_movie))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()