import pandas as pd


def get_recommendations_for_sectors(sectors):
    """
    Возвращает рекомендации на основе секторов.
    """

    def replace_dashes_with_c10(cell):
        if "-" in cell:
            cell = cell.replace(",", "")
            parts = [part.strip() for part in cell.split() if part.strip()]
            updated_parts = ["С10" if part == "-" else part for part in parts]
            return ", ".join(updated_parts)
        return cell.strip()

    def sort_sectors(cell):
        if not cell:
            return cell
        sectors = [s.strip() for s in cell.split(",")]
        sectors.sort(
            key=lambda s: int(s[1:]) if s.startswith("С") else float("inf")
        )
        return ", ".join(sectors)

    # Загрузка данных
    df = pd.read_excel("data/recommendations.xlsx")

    # Обработка данных
    df["Пример набора секторов пробоин с 10м"] = (
        df["Пример набора секторов пробоин с 10м"]
        .apply(replace_dashes_with_c10)
        .apply(sort_sectors)
    )

    matched_row = df[df["Пример набора секторов пробоин с 10м"] == sectors]

    if matched_row.empty:
        return "Рекомендация не найдена для текущего набора секторов."

    return matched_row.iloc[0]["Рекомендаци"]
