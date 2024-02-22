import sqlite3

from db import main_db_interface
from db import user_db_tables

from aiogram import F, Router
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated

router = Router()
router.my_chat_member.filter(F.chat.type == "private")
router.message.filter(F.chat.type == "private")


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED))
async def user_blocked_bot(event: ChatMemberUpdated):
    conn = sqlite3.connect(user_db_tables.user_db_path)
    main_db_interface.DBInterface.remove_record(
        conn,
        user_db_tables.UserTable.user_id_field_name,
        event.from_user.id,
        user_db_tables.UserTable.table_name,
    )


@router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def user_unblocked_bot(event: ChatMemberUpdated):
    conn = sqlite3.connect(user_db_tables.user_db_path)
    main_db_interface.DBInterface.create_record(
        conn, user_db_tables.UserTable.fields_names_list, list(event.from_user.id)
    )
