from fastapi import FastAPI, HTTPException, Body
from services.artist_service import ArtistService
from services.painting_service import PaintingService
from services.review_service import ReviewService

app = FastAPI()

artist_service = ArtistService()
painting_service = PaintingService()
review_service = ReviewService()

@app.get("/artists/")
async def get_artists():
    """
    Получить каталог художников, представленных на данной выставке.

    Возвращает:
    - list: Список художников с их ID, именем и краткой биографией.
    """
    artists = artist_service.get_all_artists()
    if not artists:
        raise HTTPException(status_code=404, detail="Каталог художников пуст.")
    return artists

@app.get("/artist/{artist_id}")
async def get_artist(artist_id: int):
    """
    Получить информацию о конкретном художнике по его ID.

    Параметры:
    - artist_id (int): ID художника

    Возвращает:
    - dict: Информация о художнике
    """
    artist = artist_service.get_artist_info(artist_id)
    if not artist:
        raise HTTPException(status_code=404, detail="Художник не найден.")
    return artist

@app.get("/paintings/")
async def get_paintings():
    """
    Получить каталог картин, представленных на выставке.

    Возвращает:
    - list: Список картин с их ID, названием и именем художника.
    """
    paintings = painting_service.get_all_paintings()
    if not paintings:
        raise HTTPException(status_code=404, detail="Каталог картин пуст.")
    return paintings

@app.post("/review/")
async def add_review(
    painting_id: int = Body(..., embed=True),
    reviewer_name: str = Body(..., embed=True),
    rating: int = Body(..., embed=True, ge=1, le=5),
    comment: str = Body(..., embed=True)
):
    """
    Добавить отзыв о картине или выставке.

    Параметры:
    - painting_id (int): ID картины или выставки
    - reviewer_name (str): Имя оставившего отзыв
    - rating (int): Оценка (от 1 до 5)
    - comment (str): Текст отзыва

    Возвращает:
    - dict: Успешное сообщение об оставленном отзыве
    """
    review_service.add_review(painting_id, reviewer_name, rating, comment)
    return {"message": "Отзыв успешно добавлен."}
