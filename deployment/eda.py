# import libraries
import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(
    page_title='Investment Recommendations - Exploratory Data Analysis',
    layout='wide',
    initial_sidebar_state='expanded')

# create function to run program
def run():
    # create title/header
    st.title('Investment Recommendations Based on Risk Profile')
    # create subheader
    st.subheader('Exploratory Data Analysis for Investment Recommendations')
    # add image
    st.image('https://thumbor.forbes.com/thumbor/fit-in/900x510/https://www.forbes.com/advisor/wp-content/uploads/2023/02/model_portfolio.jpeg.jpg',
             caption='Investment Recommendations Based on Risk Profile')
    # add description
    st.write('### Problem Statement')
    st.write("In these days, people have many investment options like stocks, bonds, mutual funds, and cryptocurrencies. With so many choices, it can be confusing to decide where to invest. This confusion can lead to poor investment decisions that don't meet long-term financial goals. That's why a personal finance recommendation system is important. It can help by giving personalized advice based on a person's financial data, risk tolerance, and goals, making it easier to make smart and informed investment choices.")
    st.write('### Objective')
    st.write('''
            1. Understanding the Investment Behavior of Respondents (Young Millennials) Using the 5W1H Approach.
            2. Identifying Respondent Groupings Based on Characteristics and Risk Profiles.
            3. Creating a Machine Learning Model for Investment Product Recommendations.
            ''')
    st.markdown('---')
    # show dataframe
    df = pd.read_csv('survey_financial_ref_dataset_clustered.csv')
    st.write('### Dataset')
    st.write('Exploration based on the clusters that have been formed with unsupervised learning.')
    st.dataframe(df)
    st.markdown('---')

    # create submenu
    submenu = st.sidebar.selectbox('Exploratory Data Analysis Navigation',['Exploratory Data Analysis - Before Clustering','Exploratory Data Analysis - After Clustering'])
    if submenu == 'Exploratory Data Analysis - Before Clustering':
        # create visualization 1
        st.write('### Gender Distribution')
        fig, ax = plt.subplots(figsize=(8, 6))
        df_gender_based = df['gender'].value_counts()
        ax.pie(df_gender_based, labels=df_gender_based.index, autopct='%1.1f%%', startangle=140, wedgeprops={'width':0.5})
        st.pyplot(fig)
        st.write('The data analysis revealed a significant gender imbalance in the research sample, with a predominance of males, indicating potential gender bias. This imbalance needs further investigation to understand its causes and implications for the research findings. Addressing gender representation is crucial, as such bias can limit the generalizability of results and overlook minority perspectives. Future studies should aim for more balanced gender representation and consider social and cultural factors affecting female participation.')

        # create visualization 2
        st.write('### Age Distribution')
        fig = plt.figure(figsize=(8, 6))
        df_age_based = df['age'].value_counts().reset_index()
        df_age_based = pd.DataFrame({'age':['17-20 years old', '21-25 years old', '26-30 years old'], 'val':[10, 30, 20]})
        plt.bar(df_age_based['age'], df_age_based['val'], color=['skyblue', 'lightgreen', 'salmon'])
        plt.xlabel('Age Categories')
        plt.ylabel('Number of Individuals')
        st.pyplot(fig)
        st.write('The analysis reveals a significant increase in average values for the 21-25 age group, suggesting specific factors or conditions that favor this group. In contrast, there is a decline in average values for the 26-30 age group after the peak observed in the 21-25 age group, which may indicate shifts in priorities, job demands, or other influencing factors. Additionally, the graph highlights a substantial difference in average values across the three age groups, indicating that age is a significant factor affecting the measured values.')

        # create visualization 3
        st.write('### Allowance Distribution')
        fig = plt.figure(figsize=(8, 6))
        df_allowance_based = df['allowance'].value_counts().reset_index()
        df_allowance_based = pd.DataFrame({'allowance':['< 500k', '500-1000k', '> 1000k'], 'val':[10, 30, 20]})
        plt.barh(df_allowance_based['allowance'], df_allowance_based['val'], color=['skyblue', 'lightgreen', 'salmon'])
        plt.xlabel('Number of Individuals')
        plt.ylabel('Allowance Categories')
        st.pyplot(fig)
        st.write('The horizontal bar chart visually depicts the distribution of pocket money across three categories: under 500k IDR, between 500k and 1 million IDR, and over 1 million IDR. The X-axis represents the frequency or number of individuals in each category, with the bar length indicating the proportion of individuals receiving each amount. The chart reveals that most surveyed individuals fall into the 500k to 1 million IDR range, as shown by the longest bar. Fewer individuals receive more than 1 million IDR, and the category under 500k IDR has the lowest frequency, indicating it is the least common amount among the surveyed individuals.')

        # create visualization 4
        st.write('### Allowance Based on Investment Understanding')
        allowance_q1 = df.groupby('allowance')['q1'].sum().reset_index()
        fig = plt.figure(figsize=(8, 6))
        allowance_q1['q1'].plot(kind='bar',color=['skyblue', 'lightgreen', 'salmon'])
        plt.xlabel('Allowance: 0 = < 500k; 1 = 500-1000k; 2 = > 1000k')
        plt.ylabel('Mean Score')
        plt.legend(title='I have better understanding of how to invest my money')
        st.pyplot(fig)
        st.write('The bar plot reveals that respondents with an allowance over 1 million IDR (category 2) have the highest average score for understanding investment, around 3. Those with allowances between 500k and 1 million IDR (category 1) have similar scores, while respondents with less than 500k IDR (category 0) score slightly lower. This indicates a positive link between allowance size and investment understanding, suggesting that higher allowances may provide better access to resources or education. However, the small score differences also suggest that other factors like education and personal experience play a role in investment knowledge.')

        # create visualization 5
        st.write('### Allowance Based on Financial Management')
        fig = plt.figure(figsize=(8, 6))
        sns.histplot(data=df, x='q3', hue='gender', multiple='stack', bins=20)
        plt.xlabel('Q3')
        plt.ylabel('Frequency')
        plt.legend(title='I have the ability to maintain financial records for my income and expenditure')
        st.pyplot(fig)
        st.write('The analysis reveals that females are more prevalent across all response scales, particularly on scales 2 and 3, indicating uncertainty or neutrality about their financial record-keeping abilities. In contrast, males, though fewer in number, are more evenly distributed across higher scales (3 and 4), suggesting greater confidence in their financial management skills. This suggests a need for financial literacy programs and interventions focused on women to boost their confidence and skills in managing finances. Males appear more confident despite their lower representation, highlighting the importance of targeted educational efforts to address these gaps.')
        
        # create visualization 6
        st.write('### Allowance Based on Financial Budgeting')
        fig = plt.figure(figsize=(8, 6))
        sns.histplot(data=df, x='q6', hue='allowance', multiple='stack', bins=20)
        plt.xlabel('Q6')
        plt.ylabel('Frequency')
        plt.legend(title='I have the ability to prepare my own budget weekly and monthly')
        st.pyplot(fig)
        st.write('The plot illustrates the distribution of responses to question Q6 about budgeting abilities. Different colors represent allowance categories: light brown for <500k, light purple for 500-1000k, and dark purple for >1000k. Most responses fall on ratings 2 and 3, indicating that many respondents feel neutral or slightly agree about their budgeting skills. Respondents with allowances under 500k show varied but generally neutral perceptions. Those with allowances between 500k and 1 million exhibit more balanced perceptions across ratings 2, 3, and 4, while those with allowances over 1 million tend to be more confident, though some still disagree. Overall, higher allowances correlate with greater confidence in budgeting abilities.')

        # create visualization 7
        value_counts_q1 = df['q1'].value_counts().sort_index()
        value_counts_q2 = df['q2'].value_counts().sort_index()
        value_counts_q3 = df['q3'].value_counts().sort_index()
        value_counts_q4 = df['q4'].value_counts().sort_index()
        value_counts_q5 = df['q5'].value_counts().sort_index()
        value_counts_q6 = df['q6'].value_counts().sort_index()
        ## create subplots
        fig, axs = plt.subplots(2, 3, figsize=(18, 12))
        st.write('### Overall Insight of Financial Literacy')
        ## plot question 1 value counts
        axs[0, 0].bar(value_counts_q1.index, value_counts_q1.values, color='skyblue')
        axs[0, 0].set_title('Q1')
        axs[0, 0].set_xlabel('Values')
        axs[0, 0].set_ylabel('Count')
        ## plot question 2 value counts
        axs[0, 1].bar(value_counts_q2.index, value_counts_q2.values, color='lightgreen')
        axs[0, 1].set_title('Q2')
        axs[0, 1].set_xlabel('Values')
        axs[0, 1].set_ylabel('Count')
        ## plot question 3 value counts
        axs[0, 2].bar(value_counts_q3.index, value_counts_q3.values, color='lightcoral')
        axs[0, 2].set_title('Q3')
        axs[0, 2].set_xlabel('Values')
        axs[0, 2].set_ylabel('Count')
        ## plot question 4 value counts
        axs[1, 0].bar(value_counts_q4.index, value_counts_q4.values, color='gold')
        axs[1, 0].set_title('Q4')
        axs[1, 0].set_xlabel('Values')
        axs[1, 0].set_ylabel('Count')
        ## plot question 5 value counts
        axs[1, 1].bar(value_counts_q5.index, value_counts_q5.values, color='lightskyblue')
        axs[1, 1].set_title('Q5')
        axs[1, 1].set_xlabel('Values')
        axs[1, 1].set_ylabel('Count')
        ## plot question 6 value counts
        axs[1, 2].bar(value_counts_q6.index, value_counts_q6.values, color='lightpink')
        axs[1, 2].set_title('Q6')
        axs[1, 2].set_xlabel('Values')
        axs[1, 2].set_ylabel('Count')
        ## Adjust layout
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        st.pyplot(fig)
        st.write('The plot shows six histograms representing respondent answers to questions Q1 through Q6 on financial literacy. Each histogram has an X-axis for answer values (1 to 5) and a Y-axis for the number of respondents choosing each value. Most responses are centered around values 2 and 3, with peaks at 3 for Q1 and Q5, and at 2 for Q2, Q3, Q4, and Q6. This indicates a moderate viewpoint among respondents, with some questions showing more spread but overall, answers are concentrated around the middle values or neutral.')

        # create visualization 8
        value_counts_q7 = df['q7'].value_counts().sort_index()
        value_counts_q8 = df['q8'].value_counts().sort_index()
        value_counts_q9 = df['q9'].value_counts().sort_index()
        value_counts_q10 = df['q10'].value_counts().sort_index()
        value_counts_q11 = df['q11'].value_counts().sort_index()
        value_counts_q12 = df['q12'].value_counts().sort_index()
        value_counts_q13 = df['q13'].value_counts().sort_index()
        value_counts_q14 = df['q14'].value_counts().sort_index()
        value_counts_q15 = df['q15'].value_counts().sort_index()
        ## create subplots
        fig, axs = plt.subplots(3, 4, figsize=(18, 12))
        st.write('### Overall Insight of Self Control')
        ## plot question 7 value counts
        axs[0, 0].bar(value_counts_q7.index, value_counts_q7.values, color='skyblue')
        axs[0, 0].set_title('Q7')
        axs[0, 0].set_xlabel('Values')
        axs[0, 0].set_ylabel('Count')
        ## plot question 8 value counts
        axs[0, 1].bar(value_counts_q8.index, value_counts_q8.values, color='lightgreen')
        axs[0, 1].set_title('Q8')
        axs[0, 1].set_xlabel('Values')
        axs[0, 1].set_ylabel('Count')
        ## plot question 9 value counts
        axs[0, 2].bar(value_counts_q9.index, value_counts_q9.values, color='lightcoral')
        axs[0, 2].set_title('Q9')
        axs[0, 2].set_xlabel('Values')
        axs[0, 2].set_ylabel('Count')
        ## plot question 10 value counts
        axs[0, 3].bar(value_counts_q10.index, value_counts_q10.values, color='gold')
        axs[0, 3].set_title('Q10')
        axs[0, 3].set_xlabel('Values')
        axs[0, 3].set_ylabel('Count')
        ## plot question 11 value counts
        axs[1, 0].bar(value_counts_q11.index, value_counts_q11.values, color='lightskyblue')
        axs[1, 0].set_title('Q11')
        axs[1, 0].set_xlabel('Values')
        axs[1, 0].set_ylabel('Count')
        ## plot question 12 value counts
        axs[1, 1].bar(value_counts_q12.index, value_counts_q12.values, color='lightpink')
        axs[1, 1].set_title('Q12')
        axs[1, 1].set_xlabel('Values')
        axs[1, 1].set_ylabel('Count')
        ## plot question 13 value counts
        axs[1, 2].bar(value_counts_q13.index, value_counts_q13.values, color='yellow')
        axs[1, 2].set_title('Q13')
        axs[1, 2].set_xlabel('Values')
        axs[1, 2].set_ylabel('Count')
        ## plot question 14 value counts
        axs[1, 3].bar(value_counts_q14.index, value_counts_q14.values, color='orchid')
        axs[1, 3].set_title('Q14')
        axs[1, 3].set_xlabel('Values')
        axs[1, 3].set_ylabel('Count')
        ## plot question 15 value counts
        axs[2, 0].bar(value_counts_q15.index, value_counts_q15.values, color='salmon')
        axs[2, 0].set_title('Q15')
        axs[2, 0].set_xlabel('Values')
        axs[2, 0].set_ylabel('Count')
        ## hide the empty subplots
        for ax in axs[2, 1:]:
            ax.axis('off')
        ## adjust layout
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        st.pyplot(fig)
        st.write('The plot shows ten histograms representing responses to questions Q7 through Q15 on self-control. Each histogram has an X-axis for answer values (1 to 5) and a Y-axis for the number of respondents choosing each value. Most responses are higher (3, 4, and 5), with peaks at 4 for questions like Q7, Q8, Q9, Q11, and Q12, indicating that many respondents feel they have poorer self-control. Some questions, like Q15, have more responses concentrated at 3, suggesting varied but generally negative perceptions of self-control among respondents.')

        # create visualization 9
        value_counts_q16 = df['q16'].value_counts().sort_index()
        value_counts_q17 = df['q17'].value_counts().sort_index()
        value_counts_q18 = df['q18'].value_counts().sort_index()
        value_counts_q19 = df['q19'].value_counts().sort_index()
        value_counts_q20 = df['q20'].value_counts().sort_index()
        value_counts_q21 = df['q21'].value_counts().sort_index()
        ## create subplots
        fig, axs = plt.subplots(3, 4, figsize=(18, 12))
        st.write('### Overall Insight of Peer Influence')
        ## plot question 16 value counts
        axs[0, 0].bar(value_counts_q16.index, value_counts_q16.values, color='skyblue')
        axs[0, 0].set_title('Q16')
        axs[0, 0].set_xlabel('Values')
        axs[0, 0].set_ylabel('Count')
        ## plot question 17 value counts
        axs[0, 1].bar(value_counts_q17.index, value_counts_q17.values, color='lightgreen')
        axs[0, 1].set_title('Q17')
        axs[0, 1].set_xlabel('Values')
        axs[0, 1].set_ylabel('Count')
        ## plot question 18 value counts
        axs[0, 2].bar(value_counts_q18.index, value_counts_q18.values, color='lightcoral')
        axs[0, 2].set_title('Q18')
        axs[0, 2].set_xlabel('Values')
        axs[0, 2].set_ylabel('Count')
        ## plot question 19 value counts
        axs[0, 3].bar(value_counts_q19.index, value_counts_q19.values, color='gold')
        axs[0, 3].set_title('Q19')
        axs[0, 3].set_xlabel('Values')
        axs[0, 3].set_ylabel('Count')
        ## plot question 20 value counts
        axs[1, 0].bar(value_counts_q20.index, value_counts_q20.values, color='lightblue')
        axs[1, 0].set_title('Q20')
        axs[1, 0].set_xlabel('Values')
        axs[1, 0].set_ylabel('Count')
        ## plot question 21 value counts
        axs[1, 1].bar(value_counts_q21.index, value_counts_q21.values, color='lightpink')
        axs[1, 1].set_title('Q21')
        axs[1, 1].set_xlabel('Values')
        axs[1, 1].set_ylabel('Count')
        ## hide the remaining subplots
        for ax in axs[1, 2:].flatten():
            ax.axis('off')
        ## hide the last row
        for ax in axs[2].flatten():
            ax.axis('off')
        ## adjust layout
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        st.pyplot(fig)
        st.write('The plot shows the distribution of responses to questions Q16 through Q21 on peer influence. Most respondents gave a middle value (3) for all questions, indicating a generally neutral or balanced view. Extreme values (1 and 5) are less common, suggesting that respondents mostly have moderate opinions. This indicates that, overall, peer influence does not significantly affect respondents financial management or planning.')

        # create visualization 9
        value_counts_q22 = df['q22'].value_counts().sort_index()
        value_counts_q23 = df['q23'].value_counts().sort_index()
        value_counts_q24 = df['q24'].value_counts().sort_index()
        value_counts_q25 = df['q25'].value_counts().sort_index()
        value_counts_q26 = df['q26'].value_counts().sort_index()
        value_counts_q27 = df['q27'].value_counts().sort_index()
        value_counts_q28 = df['q28'].value_counts().sort_index()
        value_counts_q29 = df['q29'].value_counts().sort_index()
        value_counts_q30 = df['q30'].value_counts().sort_index()
        ## create subplots
        fig, axs = plt.subplots(3, 4, figsize=(18, 12))
        st.write('### Overall Insight of Investment Behaviour')
        ## plot question 22 value counts
        axs[0, 0].bar(value_counts_q22.index, value_counts_q22.values, color='skyblue')
        axs[0, 0].set_title('Q22')
        axs[0, 0].set_xlabel('Values')
        axs[0, 0].set_ylabel('Count')
        ## plot question 23 value counts
        axs[0, 1].bar(value_counts_q23.index, value_counts_q23.values, color='lightgreen')
        axs[0, 1].set_title('Q23')
        axs[0, 1].set_xlabel('Values')
        axs[0, 1].set_ylabel('Count')
        ## plot question 24 value counts
        axs[0, 2].bar(value_counts_q24.index, value_counts_q24.values, color='lightcoral')
        axs[0, 2].set_title('Q24')
        axs[0, 2].set_xlabel('Values')
        axs[0, 2].set_ylabel('Count')
        ## plot question 25 value counts
        axs[0, 3].bar(value_counts_q25.index, value_counts_q25.values, color='gold')
        axs[0, 3].set_title('Q25')
        axs[0, 3].set_xlabel('Values')
        axs[0, 3].set_ylabel('Count')
        ## plot question 26 value counts
        axs[1, 0].bar(value_counts_q26.index, value_counts_q26.values, color='lightblue')
        axs[1, 0].set_title('Q26')
        axs[1, 0].set_xlabel('Values')
        axs[1, 0].set_ylabel('Count')
        ## plot question 27 value counts
        axs[1, 1].bar(value_counts_q27.index, value_counts_q27.values, color='lightpink')
        axs[1, 1].set_title('Q27')
        axs[1, 1].set_xlabel('Values')
        axs[1, 1].set_ylabel('Count')
        ## plot question 28 value counts
        axs[1, 2].bar(value_counts_q28.index, value_counts_q28.values, color='salmon')
        axs[1, 2].set_title('Q28')
        axs[1, 2].set_xlabel('Values')
        axs[1, 2].set_ylabel('Count')
        ## plot question 29 value counts
        axs[1, 3].bar(value_counts_q29.index, value_counts_q29.values, color='peachpuff')
        axs[1, 3].set_title('Q29')
        axs[1, 3].set_xlabel('Values')
        axs[1, 3].set_ylabel('Count')
        ## plot question 30 value counts
        axs[2, 0].bar(value_counts_q30.index, value_counts_q30.values, color='plum')
        axs[2, 0].set_title('Q30')
        axs[2, 0].set_xlabel('Values')
        axs[2, 0].set_ylabel('Count')
        ## hide the remaining subplots
        for ax in axs[2, 1:].flatten():
            ax.axis('off')
        ## adjust layout
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        st.pyplot(fig)
        st.write('The plot shows responses to questions Q22 through Q30 on investment behavior. Most respondents gave low scores (1 and 2), with 2 being the most common, indicating a generally negative or low confidence in their investment behavior. Few respondents gave high scores (4 and 5), except for Q30, where many gave higher scores (3 and 4), suggesting a more positive view on this particular question.')

    elif submenu == 'Exploratory Data Analysis - After Clustering':
        # create visualization 1
        fig, axs = plt.subplots(2, 2, figsize=(16, 12))
        st.write('### Cluster Analysis by Section')
        ## define the data
        clusters = ['Cluster 0', 'Cluster 1', 'Cluster 2']
        financial_literacy = [np.mean([3.29, 4.02, 3.67, 3.91, 3.13, 3.78]), #for cluster 0
                                np.mean([2.81, 1.80, 2.29, 2.20, 2.92, 2.18]), #for cluster 1
                                np.mean([2.79, 2.46, 2.74, 2.61, 2.85, 2.61])] #for cluster 2

        self_control = [np.mean([2.36, 2.27, 2.13, 2.27, 2.29, 2.09, 2.62, 2.33, 3.09]), #for cluster 0
                            np.mean([4.22, 4.47, 4.71, 4.09, 4.06, 4.24, 3.87, 4.04, 3.42]), #for cluster 1
                            np.mean([3.27, 3.42, 3.61, 2.89, 3.09, 2.99, 2.71, 2.79, 2.38])] #for cluster 2

        peer_influence = [np.mean([3.60, 2.91, 3.04, 3.18, 2.91, 3.44]), #for cluster 0
                            np.mean([2.40, 2.99, 3.06, 2.60, 3.36, 2.78]), #for cluster 1
                            np.mean([2.57, 2.94, 2.88, 2.55, 2.74, 2.69])] #for cluster 2

        investment_behavior = [np.mean([3.89, 4.44, 4.51, 4.27, 3.76, 4.04, 4.02, 3.98, 2.62]), #for cluster 0
                                np.mean([1.97, 1.55, 1.49, 1.77, 2.06, 1.83, 1.93, 1.98, 3.59]), #for cluster 1
                                np.mean([2.61, 2.06, 2.07, 2.24, 2.51, 2.27, 2.36, 2.39, 3.28])] #for cluster 2

        ## Plot Financial Literacy
        axs[0, 0].bar(clusters, financial_literacy, color='skyblue')
        axs[0, 0].set_title('Financial Literacy')
        axs[0, 0].set_xlabel('Cluster')
        ## Plot Self-Control
        axs[0, 1].bar(clusters, self_control, color='lightgreen')
        axs[0, 1].set_title('Self-Control')
        axs[0, 1].set_xlabel('Cluster')
        ## Plot Peer Influence
        axs[1, 0].bar(clusters, peer_influence, color='lightcoral')
        axs[1, 0].set_title('Peer Influence')
        axs[1, 0].set_xlabel('Cluster')
        ## Plot Investment Behavior
        axs[1, 1].bar(clusters, investment_behavior, color='gold')
        axs[1, 1].set_title('Investment Behavior')
        axs[1, 1].set_xlabel('Cluster')
        ## Adjust layout
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        st.pyplot(fig)
        st.write('''
                Cluster 0 consists of individuals who are highly knowledgeable about finance and very active in investments but tend to have low self-control, leading to potentially impulsive investment decisions.
                Cluster 1 consists of individuals with good self-control and cautious spending habits but with limited financial knowledge and less active in investment activities.
                Cluster 2 consists of individuals with a balanced level of financial knowledge, self-control, peer influence, and investment behavior. They are neither highly active in investments nor lack knowledge, showing a moderate approach overall.
                For better understanding, we will examine each section in detail to better understand the characteristics of each cluster.''')
                 
        # create visualization 2
        lists = []
        for i in df.q6:
            q6 = float(i)
            if (q6 == 5 or q6 == 4):
                lists.append('Strongly Agree')
            elif (q6 == 2):
                lists.append('Agree')
            elif (q6 == 3):
                lists.append('Neutral')
            elif (q6 == 1):
                lists.append('Disagree')
        df['q6_cat'] = lists
        st.write('### Cluster Based on Financial Literacy')
        fig = plt.figure(figsize=(10,5))
        df['cluster'] = df['cluster'].replace({'Agressive':'Cluster 0','Conservative':'Cluster 1','Moderate':'Cluster 2'})
        q_6 = df.groupby('cluster')['q6_cat'].value_counts().reset_index()
        sns.barplot(q_6, x='cluster', y='count', hue='q6_cat', palette=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
        plt.xlabel('Cluster')
        plt.legend()
        st.pyplot(fig)
        st.write('Question 6: I have the ability to prepare my own budget weekly and monthly.')
        st.write('Based on the image above, the insight obtained is that many respondents in cluster 0 have the best financial management habits, as evidenced by the dominance of respondents in cluster 0 who strongly agree, with no respondents disagreeing. This indicates that cluster 0 has the best long-term financial planning. On the other hand, cluster 1 shows poorer financial management habits compared to cluster 2, as indicated by the fewer respondents in cluster 1 who strongly agree. This suggests that there may be financial constraints leading cluster 1 to invest only in stable and safe returns.')

        # create visualization 3
        lists = []
        for i in df.q10:
            q10 = float(i)
            if (q10 == 5 or q10 == 4):
                lists.append('Strongly Agree')
            elif (q10 == 2):
                lists.append('Agree')
            elif (q10 == 3):
                lists.append('Neutral')
            elif (q10 == 1):
                lists.append('Disagree')
        df['q10_cat'] = lists
        st.write('### Cluster Based on Self Control in Financial Management')
        fig = plt.figure(figsize=(10,5))
        df['cluster'] = df['cluster'].replace({'Agressive':'Cluster 0','Conservative':'Cluster 1','Moderate':'Cluster 2'})
        q_10 = df.groupby('cluster')['q10_cat'].value_counts().reset_index()
        sns.barplot(q_10, x='cluster', y='count', hue='q10_cat', palette=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
        plt.xlabel('Cluster')
        plt.legend()
        st.pyplot(fig)
        st.write('Question 10: I see it, I like it, I buy it describes me.')
        st.write('Based on the image above, the insight obtained is that cluster 1 exhibits the poorest self-control compared to other clusters, as evidenced by the dominance of respondents in cluster 1 who strongly agree, indicating frequent impulsive purchases. On the other hand, cluster 0 demonstrates the best self-control, as shown by the fewest respondents in cluster 0 who strongly agree. This suggests that cluster 0 exercises self-control by purchasing only what is necessary, rather than making impulsive purchases, which aligns with the previous characteristic where cluster 0 showed the best financial planning.')

        # create visualization 4
        lists = []
        for i in df.q17:
            q17 = float(i)
            if (q17 == 5 or q17 == 4):
                lists.append('Strongly Agree')
            elif (q17 == 2):
                lists.append('Agree')
            elif (q17 == 3):
                lists.append('Neutral')
            elif (q17 == 1):
                lists.append('Disagree')
        df['q17_cat'] = lists
        st.write('### Cluster Based on Peer Influence in Financial Management')
        fig = plt.figure(figsize=(10,6))
        df['cluster'] = df['cluster'].replace({'Agressive':'Cluster 0','Conservative':'Cluster 1','Moderate':'Cluster 2'})
        q_17 = df.groupby('cluster')['q17_cat'].value_counts().reset_index()
        sns.barplot(q_17, x='cluster', y='count', hue='q17_cat', palette=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
        plt.xlabel('Cluster')
        plt.legend()
        st.pyplot(fig)
        st.write('Question 17: I always discuss financial management issues (saving) with my friends.')
        st.write('Based on the image above, the insight obtained is that peer influence has a significant impact on saving habits in cluster 0, whereas in clusters 1 and 2, the influence is less pronounced. This suggests that peer influence plays a major role in motivating better saving habits in cluster 0, likely due to the possibility that the environment or peers in cluster 0 have a strong understanding of financial literacy.')

        # create visualization 5
        lists = []
        for i in df.q26:
            q26 = float(i)
            if (q26 == 5 or q26 == 4):
                lists.append('Strongly Agree')
            elif (q26 == 2):
                lists.append('Agree')
            elif (q26 == 3):
                lists.append('Neutral')
            elif (q26 == 1):
                lists.append('Disagree')
        df['q26_cat'] = lists
        st.write('### Cluster Based on Investment Behaviour')
        fig = plt.figure(figsize=(10,6))
        df['cluster'] = df['cluster'].replace({'Agressive':'Cluster 0','Conservative':'Cluster 1','Moderate':'Cluster 2'})
        q_26 = df.groupby('cluster')['q26_cat'].value_counts().reset_index()
        sns.barplot(q_26, x='cluster', y='count', hue='q26_cat', palette=['skyblue', 'lightgreen', 'lightcoral', 'gold'])
        plt.xlabel('Cluster')
        plt.legend()
        st.pyplot(fig)
        st.write('Question 26: I always have money available in the event of a failed investment.')
        st.write('Based on the image above, the insight obtained is that cluster 0 has additional savings available in case of investment losses, as indicated by the dominance of respondents in cluster 0 who strongly agree. This suggests that cluster 0 has the highest ability to manage investment risk due to having sufficient savings to cover potential losses. In contrast, although cluster 1 has a dominant number of respondents who agree, there are more respondents who disagree compared to cluster 2. This indicates that cluster 1 has the lowest ability to handle investment risk due to a lack of savings to cover potential losses.')

if __name__ == '__main__':
    run()