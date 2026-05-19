# Copyright (c) 2025 AxiomBots
# Licensed under the MIT License.
# This file is part of AxiomXMusic


from pyrogram import filters, types

from axiomm import axiom, app, db, lang
from axiomm.helpers import can_manage_vc


@app.on_message(filters.command(["skip", "next", "dusra", "agla"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _skip(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    await axiom.play_next(m.chat.id)
    await m.reply_text(m.lang["play_skipped"].format(m.from_user.mention))
