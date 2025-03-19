from backend.database import db_session
from backend.models.review import Review

class ReviewService:
    """
    Сервис для работы с отзывами.

    Методы:
    - add_review: Добавляет новый отзыв
    - get_reviews_by_painting: Получает все отзывы для указанной картины
    """

    def add_review(self, painting_id: int, user_name: str, comment: str, rating: int) -> dict:
        """
        Добавляет новый отзыв к картине.

        Параметры:
        - painting_id (int): ID картины
        - user_name (str): Имя пользователя
        - comment (str): Текст отзыва
        - rating (int): Оценка (1-5)

        Возвращает:
        - dict: Данные добавленного отзыва
        """
        new_review = Review(
            painting_id=painting_id,
            user_name=user_name,
            comment=comment,
            rating=rating
        )
        db_session.add(new_review)
        db_session.commit()
        return {
            "id": new_review.id,
            "painting_id": new_review.painting_id,
            "user_name": new_review.user_name,
            "comment": new_review.comment,
            "rating": new_review.rating
        }

    def get_reviews_by_painting(self, painting_id: int) -> list:
        """
        Получает список всех отзывов для указанной картины.

        Параметры:
        - painting_id (int): ID картины

        Возвращает:
        - list: Список словарей с отзывами
        """
        reviews = db_session.query(Review).filter(Review.painting_id == painting_id).all()
        return [
            {
                "id": review.id,
                "painting_id": review.painting_id,
                "user_name": review.user_name,
                "comment": review.comment,
                "rating": review.rating
            }
            for review in reviews
        ]
