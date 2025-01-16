from fastapi import APIRouter

from app.services.hit_service import clear_previous_hits

# Инициализация маршрута
router = APIRouter()


@router.post("/clear_hits")
async def clear_hits():
    """
    Очистка сохранённых попаданий.
    """
    clear_previous_hits()
    return {
        "message": (
            "Предыдущие попадания не будут учитываться "
            "при следующих загрузках мишени."
        )
    }
