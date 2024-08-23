  # import libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import pickle
import json
from sklearn.decomposition import PCA
from tensorflow.keras.models import load_model
import time
import tensorflow




# Save Pipeline
with open('features.txt', 'r') as file_1:
    final_features = json.load(file_1)

with open('class_names.txt', 'r') as file_5:
    class_names = json.load(file_5)

with open('pca.pkl', 'rb') as file_2:
    pca = pickle.load(file_2)

with open('pipeline.pkl', 'rb') as file_3:
    pipeline = pickle.load(file_3)

with open('cluster.pkl', 'rb') as file_4:
    kmeans = pickle.load(file_4)

model = load_model('model_seq.keras')

def transform_value(x):
    if x == "Disagree":
        return 1
    elif x == "Agree":
        return 2
    elif x == "Neutral":
        return 3
    elif x == "Strongly Agree":
        return 4
    else:
        return 5

# Define the mapping for the responses
response_mapping = {
    1: "does not",
    2: "",
    3: "neutral about",
    4: "strongly",
    5: "very strongly"
}

# Define the questions and corresponding summaries
questions_summaries = {
    'q22': "The user {} puts money aside regularly for future needs,",
    'q26': "{} ensures they always have funds available in case an investment fails, highlighting a risk management strategy.",
    'q27': "{} actively plans their expenses to allocate funds for investment, showing a disciplined approach to financial management.",
    'q28': "{} consistently saves money with the intention to invest, demonstrating a commitment to growing their wealth.",
    'q30': "{} maintains investment accounts in both money and capital markets, reflecting a diversified investment portfolio."
}

# Function to generate descriptive summary for investment behavior
def generate_investment_behavior_summary(row):
    behavior_summary = []
    for question, summary in questions_summaries.items():
        response = row[question]
        behavior_summary.append(summary.format(response_mapping[response]))
    
    # Add a closing statement based on the user's responses
    closing_statement = "Overall, the user's investment behavior shows a {} approach to managing risks and opportunities in their financial strategy.".format(
        "conservative" if row['q26'] in [1, 2] and row['q28'] in [1, 2] else
        "balanced" if row['q22'] in [3, 4] and row['q27'] in [3, 4] else
        "aggressive"
    )
    
    summary_text = " ".join(behavior_summary) + " " + '\n' + closing_statement
    
    # Wrap the summary text in a div with justified text alignment
    return f"<div style='text-align: justify;'>{summary_text}</div>"


def get_instrument(category, value, previous_suggestions):
    # Define instrument options based on category
    instruments = {
        'Aggressive': {
            0.75: 'Stocks',
            0.5: 'Equity Mutual Funds',
            0.0: 'Hybrid Mutual Funds'
        },
        'Moderate': {
            0.75: 'Bonds',
            0.5: 'Money Market Mutual Funds',
            0.0: 'Fixed-Income Mutual Funds'
        },
        'Conservative': {
            0.75: 'Savings Account',
            0.5: 'Gold',
            0.0: 'Certificates of Deposit'
        }
    }

    # Get the category-specific instruments
    cat_instruments = instruments.get(category, {})

    # Sort instruments based on their value
    sorted_instruments = sorted(cat_instruments.items(), key=lambda x: x[0], reverse=True)
    
    # Avoid suggesting the same instrument
    for threshold, instrument in sorted_instruments:
        if value > threshold and instrument not in previous_suggestions:
            return instrument

    # Fallback in case all instruments have been suggested already
    return 'Others'

def calculate_result(y_pred_df):
    suggestions = []
    for _, row in y_pred_df.iterrows():
        sorted_row = row.sort_values(ascending=False)
        
        previous_suggestions = []

        first_suggestion = get_instrument(sorted_row.index[1], sorted_row.iloc[0], previous_suggestions)
        previous_suggestions.append(first_suggestion)
        second_suggestion = get_instrument(sorted_row.index[1], sorted_row.iloc[1], previous_suggestions)
        previous_suggestions.append(second_suggestion)
        third_suggestion = get_instrument(sorted_row.index[2], sorted_row.iloc[2], previous_suggestions)

        suggestions.append([first_suggestion, second_suggestion, third_suggestion])
        
        calculation = sorted_row.reset_index().rename(columns={0: 'percentage'})
        
        labels = [first_suggestion, second_suggestion, third_suggestion]

        # Generate percentage with donut pie chart
        sns.set(style="whitegrid")
        colors = ['lightgreen', 'skyblue', 'plum']

        fig, ax = plt.subplots(figsize=(8, 6))
        wedges, texts, autotexts = ax.pie(calculation['percentage'], labels=[''] * len(labels), autopct='%1.1f%%', startangle=150, wedgeprops=dict(width=0.3), pctdistance=1.2, colors=colors)
        
        # Extract the percentages used in the pie chart
        percentages = [float(autotext.get_text().replace('%', '')) for autotext in autotexts]

        ax.axis('equal')
        
        st.pyplot(fig)
        
        st.markdown(f"Suggestions Instruments for Investment")
        
        st.markdown(f"<span style='display: flex; align-items: center;'><span style='width: 12px; height: 12px; background-color: lightgreen; display: inline-block; margin-right: 5px;'></span>1. **{first_suggestion}**<span style='margin-left: auto; margin-right: 10px;'>{percentages[0]:.1f}%</span></span>", unsafe_allow_html=True)
        st.markdown(f"<span style='display: flex; align-items: center;'><span style='width: 12px; height: 12px; background-color: skyblue; display: inline-block; margin-right: 5px;'></span>2. **{second_suggestion}**<span style='margin-left: auto; margin-right: 10px;'>{percentages[1]:.1f}%</span></span>", unsafe_allow_html=True)
        st.markdown(f"<span style='display: flex; align-items: center;'><span style='width: 12px; height: 12px; background-color: plum; display: inline-block; margin-right: 5px;'></span>3. **{third_suggestion}**<span style='margin-left: auto; margin-right: 10px;'>{percentages[2]:.1f}%</span></span>", unsafe_allow_html=True)
def run():
    # Title
    st.title('Investment Instrument Suggestion')
    st.markdown('---')
    
    # Form
    with st.form(key='questions'):

        col1, col2 = st.columns(2)
        
        # with col1:
        
        with col1:
            age = st.number_input("Age", min_value=16, max_value=70, value=25, placeholder="Type a number...")
        
        with col2:
            allowance = st.number_input("Allowance (in IDR)", min_value=0, max_value=1000000000, value=100000, placeholder="Type a number...")
        
        gender = st.radio("Gender", ["Male", "Female"], index=1)

        container_1 = st.container(border=True)

        container_1.write("## Financial Literacy")
        options = ["Disagree", "Agree", "Neutral", "Strongly Agree", "Very Strongly Agree"]

        q1 = container_1.radio(f' 1 . I have a better understanding of how to invest my money \n \n *Saya memiliki cukup pemahaman tentang berinvestasi*', options, key=f'question_1', index=4)
        q2 = container_1.radio(f' 2 . I have a better understanding of how to manage my credit use \n \n *Saya memiliki pemahaman yang cukup dalam menggunakan kartu kredit*', options, key=f'question_2', index=3)
        q3 = container_1.radio(f' 3 . I have the ability to maintain financial records for my income and expenditure \n \n *Saya melakukan pencatatan keuangan saya terkait pemasukan dan pengeluaran*', options, key=f'question_3', index=1)
        q4 = container_1.radio(f'  4 . I can manage my money easily \n \n *Saya dapat mengatur keuangan dengan mudah*', options, key=f'question_4', index=2)
        q5 = container_1.radio(f'  5 . I have a better understanding of financial instruments (e.g. Bonds, stock, T-bill, time value of money, future contract, option, etc.) \n \n *Saya memiliki pemahaman yang cukup baik pada instrumen keuangan*', options, key=f'question_5', index=1)
        q6 = container_1.radio(f'  6 . I have the ability to prepare my own budget weekly and monthly \n \n *Saya memiliki kemampuan untuk membuat anggaran saya sendiri setiap minggu dan setiap bulan*', options, key=f'question_6', index=3)
        
        container_2 = st.container(border=True)

        container_2.write("## Self-Control")

        q7 = container_2.radio(f" 7 . I don't save, because I think it is too hard \n \n *Saya tidak menabung, karena menurut saya terlalu sulit.*", options, key=f'question_7', index=2)
        q8 = container_2.radio(f" 8 . I enjoy spending money on things that aren't practical. \n \n *Saya senang menghabiskan uang untuk hal-hal yang tidak praktis*", options, key=f'question_8', index=1)
        q9 = container_2.radio(f' 9 . When I get money, I always spend it immediately (within 1 or 2 days) \n \n *Ketika saya mendapat uang, saya selalu langsung membelanjakannya (dalam 1 atau 2 hari)*', options, key=f'question_9', index=1)
        q10 = container_2.radio(f'  10 . I see it, I like it, I buy its describe me	 \n \n *Saya melihatnya, saya menyukainya, saya membelinya, itu menggambarkan saya*', options, key=f'question_10', index=0)
        q11 = container_2.radio(f"  11 . 'Just do it' describes the way I buy things \n \n *'Lakukan saja dulu' menggambarkan cara saya membeli sesuatu*", options, key=f'question_11', index=1)
        q12 = container_2.radio(f"  12 . 'Buy now, think about it later' describe me \n \n *'Beli sekarang, pikirkan (konsekuensi) nanti' mendeskirpsikan saya*", options, key=f'question_12', index=1)
        q13 = container_2.radio(f'  13 . I always failed to control myself from spending money \n \n *Saya selalu gagal mengendalikan diri dalam membelanjakan uang*', options, key=f'question_13', index=0)
        q14 = container_2.radio(f'  14 . I am more concerned with what happens to me in short run than in long run	 \n \n *Saya lebih peduli dengan apa yang terjadi pada diri saya dalam jangka pendek daripada jangka panjang.*', options, key=f'question_14', index=2)
        q15 = container_2.radio(f'  15 . When I set having goals for myself, I rarely achieve them. \n \n *Ketika saya menetapkan tujuan untuk diri saya sendiri, saya jarang mencapainya.*', options, key=f'question_15', index=2)

        container_3 = st.container(border=True)

        container_3.write("## Peer-Influence")

        q16 = container_3.radio(f' 16 . As far I know, some of my friends regularly do save with a saving account \n \n *Sejauh yang saya tahu, beberapa teman saya rutin menabung dengan rekening tabungan*', options, key=f'question_16', index=2)
        q17 = container_3.radio(f' 17 . I always discuss financial management issue (saving) with my friends \n \n *Saya selalu mendiskusikan masalah pengelolaan keuangan (menabung) dengan teman-teman saya*', options, key=f'question_17', index=3)
        q18 = container_3.radio(f' 18 . I always discuss financial management issue (investment) with my friends \n \n *Saya selalu mendiskusikan masalah pengelolaan keuangan (investasi) dengan teman-teman saya*', options, key=f'question_18', index=2)
        q19 = container_3.radio(f'  19 . I always spend my leisure time with my friends \n \n *Saya selalu menghabiskan waktu senggang bersama teman-teman *', options, key=f'question_19', index=1)
        q20 = container_3.radio(f'  20 . I always involve in money spending activities with my friends \n \n *Saya selalu terlibat dalam kegiatan belanja uang bersama teman-teman*', options, key=f'question_20', index=1)
        q21 = container_3.radio(f'  21 .  I always follow the information about investment growth \n \n *Saya selalu mengikuti informasi tentang pertumbuhan investasi*', options, key=f'question_21', index=3)

        container_4 = st.container(border=True)

        container_4.write("## Investment Behavior")

        q22 = container_4.radio(f' 22 . I put money aside on a regular basis for the future \n \n *Saya menyisihkan uang secara teratur untuk masa depan*', options, key=f'question_22', index=2)
        q23 = container_4.radio(f' 23 . In order to invest, I often compare prices before I make purchase \n \n *Untuk berinvestasi, saya sering membandingkan harga sebelum melakukan pembelian*', options, key=f'question_23', index=2)
        q24 = container_4.radio(f' 24 . In order to invest, I often consider whether the stock prices are valuable when I sell it \n \n *Untuk berinvestasi, saya sering mempertimbangkan apakah harga saham berharga ketika saya menjualnya*', options, key=f'question_24', index=3)
        q25 = container_4.radio(f'  25 . In order to invest, I often understanding the fundamental analysis \n \n *Untuk berinvestasi, saya sering memahami analisa fundamental*', options, key=f'question_25', index=1)
        q26 = container_4.radio(f'  26 . I always have money available in the event of my failed investment \n \n *Saya selalu mempunyai uang jika investasi saya gagal*', options, key=f'question_26', index=1)
        q27 = container_4.radio(f'  27 . In order to invest, I plan to manage my expenses \n \n *Untuk berinvestasi, saya berencana mengatur pengeluaran saya*', options, key=f'question_27', index=2)
        q28 = container_4.radio(f'  28 . I save my money in order to do investment \n \n *Saya menabung uang saya untuk melakukan investasi*', options, key=f'question_28', index=4)
        q29 = container_4.radio(f'  29 . I invest to achieve certain goals \n \n *Saya berinvestasi untuk mencapai tujuan tertentu*', options, key=f'question_29', index=2)
        q30 = container_4.radio(f'  30 . I have some investment account in money market and also capital market \n \n *Saya mempunyai beberapa rekening investasi di pasar uang dan juga pasar modal*', options, key=f'question_30', index=2)
        
        submit_button = st.form_submit_button(label='Submit', use_container_width=True)

    
    data_inf = {
    "gender": gender,
    "age": age,
    "allowance": allowance,
    "q1": q1,
    "q2": q2,
    "q3": q3,
    "q4": q4,
    "q5": q5,
    "q6": q6,
    "q7": q7,
    "q8": q8,
    "q9": q9,
    "q10": q10,
    "q11": q11,
    "q12": q12,
    "q13": q13,
    "q14": q14,
    "q15": q15,
    "q16": q16,
    "q17": q17,
    "q18": q18,
    "q19": q19,
    "q20": q20,
    "q21": q21,
    "q22": q22,
    "q23": q23,
    "q24": q24,
    "q25": q25,
    "q26": q26,
    "q27": q27,
    "q28": q28,
    "q29": q29,
    "q30": q30
    }

    options = ["Disagree", "Agree", "Neutral", "Strongly Agree", "Very Strongly Agree"]


    if submit_button:
        progress_text = "Operation in progress. Please wait."
        my_bar = st.progress(0, text=progress_text)

        for percent_complete in range(100):
            time.sleep(0.01)
            my_bar.progress(percent_complete + 1, text=progress_text)
        time.sleep(1)
        my_bar.empty()

        # mapping result
        data_inf_df = pd.DataFrame([data_inf])
        data_inf_df['gender'] = data_inf_df['gender'].apply(lambda x: 0 if x == "Female" else 1)
        data_inf_df['age'] = data_inf_df['age'].apply(lambda x: 0 if 17 <= x < 21 else (1 if 21<= x < 26 else 2))
        data_inf_df['allowance'] = data_inf_df['allowance'].apply(lambda x: 0 if x < 500000 else (1 if 500000 < x <= 1000000 else 2))
        for col in data_inf_df.iloc[:,3:].columns.tolist():
            data_inf_df[col] = data_inf_df[col].apply(transform_value)
            
        # adjusting columns
        # data_inf_df[final_features]
        data_inf_df_adj = data_inf_df[final_features]

        # pca
        df_pca = pca.transform(data_inf_df_adj)

        # Predict Cluster
        pred = kmeans.predict(df_pca)    
        data_inf_df['cluster'] = pred
        data_inf_df['cluster'] = data_inf_df['cluster'].replace({0: 'Aggressive', 1: 'Conservative', 2: 'Moderate'})
        cluster = data_inf_df['cluster'].values[0]

        # Generate Description
        data_inf_df['description'] = data_inf_df.apply(generate_investment_behavior_summary, axis=1)
            
        # Handle Sparse Matrix
        data_inf_df_transformed = pipeline.transform(data_inf_df)
        if hasattr(data_inf_df_transformed, 'toarray'):
            data_inf_df_transformed = data_inf_df_transformed.toarray()

        # Predict Results
        y_pred = model.predict(data_inf_df_transformed)
        y_pred_df = pd.DataFrame(y_pred, columns=class_names)

        # Display cluster and description
        st.markdown(f"### {cluster}")
        st.markdown(f"{data_inf_df['description'].values[0]}", unsafe_allow_html=True)


        # Generate and display the result
        result = calculate_result(y_pred_df)        

if __name__ == '__main__':
    run()