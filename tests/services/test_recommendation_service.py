import pandas as pd
import pytest

from app.services.recommendation_service import get_recommendations_for_sectors


@pytest.fixture
def mock_data(mocker):
    # Мокаем метод чтения Excel файла
    mock_read_excel = mocker.patch("pandas.read_excel")
    mock_read_excel.return_value = pd.DataFrame(
        {
            "Пример набора секторов пробоин с 10м": ["С1, С2", "С3, С4"],
            "Рекомендаци": ["Recommendation 1", "Recommendation 2"],
        }
    )
    return mock_read_excel


def test_get_recommendations_for_sectors_found(mock_data):
    result = get_recommendations_for_sectors("С1, С2")
    assert result == "Recommendation 1"


def test_get_recommendations_for_sectors_not_found(mock_data):
    result = get_recommendations_for_sectors("С5, С6")
    assert result == "Рекомендация не найдена для текущего набора секторов."
