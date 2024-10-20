import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
import streamlit as st
import xlwings as xw
import time

# 로딩 시간 구현
with st.spinner('Wait for it...'):
    time.sleep(1)

# pandas
df = pd.read_csv('./제주도카드이용데이터/data/jeju_card.csv')

df['년도'] = df['연월'].str.split('-', expand=True)[0]
df['월'] = df['연월'].str.split('-', expand=True)[1]

df.groupby('연월').sum(numeric_only=True)

# 2017년과 2018년도만
df_1 = df[(df['년도']=='2017') | (df['년도']=='2018')]

# 이용자수
df_1_pivot = df_1.pivot_table(values='이용자수',
                          index='월',
                          columns='년도',
                          aggfunc='count')

# 이용금액
df_2_pivot = df_1.pivot_table(values='이용금액',
                          index='월',
                          columns='년도',
                          aggfunc='sum')

card_2017 = pd.read_csv('./읍면동단위/data/jeju_card_region_2017.csv')
card_2018 = pd.read_csv('./읍면동단위/data/jeju_card_region_2018.csv')
population = pd.read_csv('./읍면동단위/data/jeju_population.csv')
card = pd.concat([card_2017,card_2018])
card['지역'] = card['시군구명'] + card['읍면동명']
# population 전처리
# 1. 성별
population['성별'] = population['성별'].replace('남', '남성')
population['성별'] = population['성별'].replace('여', '여성')
# 2. 연월일
population['연월일'] = population['연월일'].astype(str)
population['연월일'] = pd.to_datetime(population['연월일']).astype(str)
# -- 칼럼명 통일
population.columns = ['연월', '시군구명', '읍면동명', '성별', '연령대', '방문인구']
# join
df5 = pd.merge(left=card, right=population, how='left', on=['연월','시군구명','읍면동명','성별'])

df7 = df5[df5['업종명']=='비알콜 음료점업']
df7 = df7.reset_index()
df7 = df7.drop('index', axis=1)
df7 = df7.groupby('지역').sum(numeric_only=True).sort_values('방문인구', ascending=False)
df7 = df7.reset_index()

# streamlit

# metrics
met_col1, met_col2, met_col3, met_col4 = st.columns(4)
met_col1.metric(label="Age", value="20대", delta="12명")
met_col2.metric(label="Age", value="30대", delta="-10명")
met_col3.metric(label="Age", value="40대", delta="-1명")
met_col4.metric(label="Age", value="50대 이상", delta="8명")

# tab
tab1, tab2 = st.tabs(['Tab A', 'Tab B'])

# layout
col1, col2 = st.columns(2)

col1.subheader('월별 카드 이용자수')
col1.line_chart(df_1_pivot)

col2.subheader('월별 카드 이용금액')
col2.line_chart(df_2_pivot) 

st.subheader('방문인구와 이용자수의 상관관계')
st.scatter_chart(df7, x='방문인구', y='이용자수')