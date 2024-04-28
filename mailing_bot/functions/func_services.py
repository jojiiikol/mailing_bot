import __main__
from aiogram import Router, F, types
from aiogram.filters import Command, ChatMemberUpdatedFilter, KICKED, MEMBER
from keyboards.user_kb import get_check_subscription_kb

services_router = Router()


@services_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: types.ChatMemberUpdated):
    await __main__.db.update_blocked__status_user(tg_id=event.from_user.id)


@services_router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_blocked_bot(event: types.ChatMemberUpdated):
    await __main__.db.update_unblocked__status_user(tg_id=event.from_user.id)
