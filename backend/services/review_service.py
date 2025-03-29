from backend.models.db_session import create_session
from backend.models.review import Review
from typing import List

class ReviewService:
    @staticmethod
    def create_review(text: str, user_id: int, painting_id: int = None,
                    rating: int = None, is_exhibition: bool = False) -> Review:
        """Создание отзыва"""
        session = create_session()
        try:
            review = Review(
                text=text,
                user_id=user_id,
                painting_id=painting_id,
                rating=rating,
                is_about_exhibition=is_exhibition
            )
            session.add(review)
            session.commit()
            return review
        finally:
            session.close()

    @staticmethod
    def get_for_painting(painting_id: int) -> List[Review]:
        """Получение отзывов для картины"""
        session = create_session()
        try:
            return session.query(Review).filter(
                Review.painting_id == painting_id
            ).all()
        finally:
            session.close()