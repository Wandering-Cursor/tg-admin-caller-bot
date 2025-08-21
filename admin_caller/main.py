import random
from admin_caller.settings import settings
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram.constants import ParseMode
from telegram import error as tg_errors


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:
    assert update.message is not None
    assert update.effective_chat is not None
    assert update.effective_user is not None

    if update.effective_chat.type != "private":
        try:
            await update.message.delete()
        except tg_errors.TelegramError:
            pass
        return

    await update.message.reply_text(
        f"Hello!\nDear {update.effective_user.first_name}, please add me to a group, so I can perform my duty."
    )


async def ping_admins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    assert update.message is not None
    assert update.effective_chat is not None
    assert update.effective_user is not None

    if update.effective_chat.type not in ["group", "supergroup"]:
        return


    main_text = f"{update.effective_user.mention_html()} is calling all admins!"

    message = await update.message.reply_text(
        main_text,
        parse_mode=ParseMode.HTML,
    )

    admins = list(await update.effective_chat.get_administrators())


    while True:
        mentions = ""
        
        if not admins:
            break

        selected_admins = random.sample(admins, k=min(50, len(admins)))

        for admin in selected_admins:
            if admin.user.is_bot:
                continue

            mentions += f"{admin.user.mention_html()}\n"
            admins.remove(admin)
        
        with_mentions = f"{main_text}\n\n{mentions}"

        await message.edit_text(
            with_mentions,
            parse_mode=ParseMode.HTML,
        )

    await message.edit_text(
        main_text,
        parse_mode=ParseMode.HTML,
    )



app = ApplicationBuilder().token(settings.bot_token).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("admin", ping_admins))

if settings.use_polling:
    app.run_polling()
else:
    assert settings.webhook_url is not None

    kwargs = {}

    if settings.listen_ip:
        kwargs["listen"] = str(settings.listen_ip)
    if settings.listen_port:
        kwargs["port"] = settings.listen_port
    if settings.listen_path:
        kwargs["url_path"] = settings.listen_path

    app.run_webhook(
        webhook_url=str(settings.webhook_url),
        **kwargs,
    )
