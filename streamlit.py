import streamlit as st
from PIL import Image

from detection.recommendations.recomendations import get_recommendations
from views.test import primary_scenario

st.title("Распознавание попаданий")

uploaded_file = st.file_uploader("Загрузите изображение")

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    processed_image, target, hs = primary_scenario.process_image(image)

    st.image(processed_image, use_container_width=True)
    processed_image.save(f"./temp/мишень_1.jpg")
    with open(f"./temp/мишень_1.jpg", 'rb') as file:
        st.download_button(
            label='Скачать изображение',
            data=file,
            file_name=f'мишень_1.jpg'
        )

    target_name = target.name
    hits = len(hs)
    recommendations = get_recommendations(hs)
    sector_info = ", ".join([f"{'С'+sector.sector if sector.sector != 10 else '-'}" for sector in hs])
else:
    target_name, hits, recommendations, sector_info = "", 0, "", ""

# Поля для вывода значений
st.sidebar.markdown(f"**Мишень:** <span style=\"font-size: 2em\">№{target_name}</span>", unsafe_allow_html=True)
st.sidebar.write(f"**Кол-во попаданий:** <span style=\"font-size: 2em\">{hits}</span>", unsafe_allow_html=True)
st.sidebar.write(f"**Сектора:**")
st.sidebar.write(f"<span style=\"font-size: 2em\">{sector_info}</span>", unsafe_allow_html=True)
st.sidebar.write("**Рекомендации:**")
st.sidebar.write(recommendations)
