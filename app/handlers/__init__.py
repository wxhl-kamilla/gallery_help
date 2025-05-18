# # app/handlers/__init__.py
#
# from aiogram import Router
# from .common import router as common_router
# from .catalog import router as catalog_router
# from .artist import router as artist_router
# from .qr import router as qr_router  # <- новое
#
# def setup_routers() -> Router:
#     router = Router()
#     router.include_router(common_router)
#     router.include_router(catalog_router)
#     router.include_router(artist_router)
#     router.include_router(qr_router)    # Подключаем обработчик для /qr
#     return router
