import streamlit as st
import pandas as pd
import pickle

st.set_page_config(page_title="ПСБ Machine Learning")
st.header("Machine Learning", divider='rainbow')


class MachineLearning:
    def __init__(self, page_type: str):
        self.page_type = page_type

    def main_container(self):

        new_scoring, model_characteristics = st.tabs(["Новый скоринг", "Характеристики модели"])

        loan, cred_cards, bki, mortgage = new_scoring.tabs(
            ["Потребительский кредит", "Кредитная карта", "Оптимизация БКИ", "Ипотека"]
        )

        pickled_model = pickle.load(open('ml_models/sns_titanic_model.pickle', 'rb'))
        uploaded_file = loan.file_uploader("Передайте .csv файл с необходимыми параметрами")
        if uploaded_file:
            dataframe = pd.read_csv(uploaded_file)
            loan.dataframe(dataframe)

            proba = pickled_model.predict_proba(dataframe)[:, 1]
            loan.write(f"Вероятность взять кредит: {proba}")

        # file = open("ml_models/data/sns_titanic_features.json", "r")
        # columns_data = file.read()
        # columns = json.loads(columns_data)
        # file.close()

        loan.title("Параметры")
        features = pd.read_json('ml_models/data/sns_titanic_features.json', orient='index') \
            .reset_index().rename(columns={'index': 'Признак', 0: 'Описание'})

        with loan.expander("Просмотреть необходимые параметры"):
            loan.dataframe(features, use_container_width=True)

        model_characteristics.write("ROC AUC: 0.71")
        feat_imp = pd.concat([features['Признак'], pd.Series(pickled_model.feature_importances_)], axis=1)\
            .rename(columns={0: 'Влияние'})

        feat_imp = feat_imp.sort_values('Влияние', ascending=False)

        model_characteristics.dataframe(feat_imp, use_container_width=True)
        model_characteristics.bar_chart(data=feat_imp, x='Признак', y='Влияние')


MachineLearning("ML").main_container()
