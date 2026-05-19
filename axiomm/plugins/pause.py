# Copyright (c) 2025 AxiomBots
# Licensed under the MIT License.
# This file is part of AxiomXMusic


from pyrogram import filters, types

from axiomm import axiom, app, db, lang
from axiomm.helpers import buttons, can_manage_vc


@app.on_message(filters.command(["pause", "ruk", "k"]) & filters.group & ~app.bl_users)
@lang.language()
@can_manage_vc
async def _pause(_, m: types.Message):
    if not await db.get_call(m.chat.id):
        return await m.reply_text(m.lang["not_playing"])

    if not await db.playing(m.chat.id):
        return await m.reply_text(m.lang["play_already_paused"])

    await axiom.pause(m.chat.id)
    await m.reply_text(
        text=m.lang["play_paused"].format(m.from_user.mention),
        reply_markup=buttons.controls(m.chat.id),
    )
