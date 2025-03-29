from backend.models.db_session import create_session
from backend.models.painting import Painting
from typing import List, Optional
import io
import qrcode


class PaintingService:
    @staticmethod
    def add_painting(title: str, artist_id: int, **kwargs) -> Painting:
        """Добавление новой картины"""
        session = create_session()
        try:
            painting = Painting(title=title, artist_id=artist_id, **kwargs)
            session.add(painting)
            session.commit()
            return painting
        finally:
            session.close()

    @staticmethod
    def get_by_artist(artist_id: int) -> List[Painting]:
        """Получение картин по ID художника"""
        session = create_session()
        try:
            return session.query(Painting).filter(Painting.artist_id == artist_id).all()
        finally:
            session.close()

    @staticmethod
    def generate_qr(painting_id: int) -> io.BytesIO:
        """Генерация QR-кода для картины"""
        session = create_session()
        try:
            painting = session.query(Painting).get(painting_id)
            if not painting:
                raise ValueError("Painting not found")

            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(f"Painting: {painting.title}\nArtist: {painting.artist.name}")
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            return img_io
        finally:
            session.close()