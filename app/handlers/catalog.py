# # app/handlers/catalog.py
#
# from aiogram import Router
# from aiogram.types import Message
# from app.database import get_session
# from app.models import painting
# from app.service import get_all_paintings, get_all_artists
# from app.models.artist import Artist
# router = Router()
#
# @router.message(lambda msg: msg.text == "/catalog")
# async def catalog_handler(message: Message):
#     async for session in get_session():
#         paintings = await get_all_paintings(session)
#
#     if not paintings:
#         await message.answer("🔍 В каталоге пока нет картин.")
#         return
#
#     response = "🖼️ Каталог картин:\n\n"
#     for p in paintings:
#         response += f"🎨/art_{p.id} - {p.title}\n"
#
#     await message.answer(response)
#
#
# @router.message(lambda msg: msg.text and msg.text.startswith('/art_'))
# async def artist_detail_handler(message: Message):
#     try:
#         painting_id = int(message.text.split('_')[1])
#     except (IndexError, ValueError):
#         await message.answer("🚨 Неверный формат команды. Используйте /art_1")
#         return
#
#     async for session in get_session():
#         paintings = await get_all_paintings(session)
#         artists = await get_all_artists(session)
#         if not paintings:
#             await message.answer("🚨 Художник не найден")
#             return
#
#     for p in paintings:
#         artist_id = p.id
#         if p.id == painting_id:
#             for a in artists:
#                 if a.id == artist_id:
#                     response = (
#                     f"🖼 {p.title}\n\n"
#                     f"{a.name}\n"
#                     f"📖 Описание:\n{p.description}"
#                 )
#
#     await message.answer(response)