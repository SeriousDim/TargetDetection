from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Подключение шаблонов Jinja2
templates = Jinja2Templates(directory="templates")

# Инициализация маршрута
router = APIRouter()


# Маршрут для главной страницы
@router.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    """
    Возвращает стартовую HTML-страницу.
    """
    return templates.TemplateResponse("index.html", {"request": request})
