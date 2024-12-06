import pandas as pd

df = pd.read_excel('./recommendations.xlsx')


def get_recommendations(sectors):
    if len(sectors) != 4:
        return "Для получения рекомендаций сделайте ровно 4 выстрела"

    sectors_str = ", ".join([f"{'С'+sector.sector if sector.sector != 10 else '-'}" for sector in sectors])

    matched_row = df[
        df["Пример набора секторов пробоин с 10м"]
        == sectors_str
        ]

    try:
        return matched_row.iloc[0]["Рекомендаци"]
    except:
        return "Нет рекомендаций"
