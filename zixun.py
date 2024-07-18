import streamlit as st
import akshare as ak
import pandas as pd
import matplotlib.pyplot as plt

# 上海金属网-快讯
def get_shmet_news(symbol, start_date, end_date):
    futures_news_shmet_df = ak.futures_news_shmet(symbol=symbol)
    futures_news_shmet_df['发布时间'] = pd.to_datetime(futures_news_shmet_df['发布时间']).dt.tz_convert('Asia/Shanghai')
    start_date = pd.to_datetime(start_date + " 00:00:00").tz_localize('Asia/Shanghai')
    end_date = pd.to_datetime(end_date + " 23:59:59").tz_localize('Asia/Shanghai')
    mask = (futures_news_shmet_df['发布时间'] >= start_date) & (futures_news_shmet_df['发布时间'] <= end_date)
    filtered_news_df = futures_news_shmet_df.loc[mask]
    return filtered_news_df

# 百度股市通-期货-新闻
def get_baidu_news(symbol, start_date, end_date):
    futures_news_baidu_df = ak.futures_news_baidu(symbol=symbol)
    futures_news_baidu_df['发布时间'] = pd.to_datetime(futures_news_baidu_df['发布时间'])
    start_date = pd.to_datetime(start_date + " 00:00:00")
    end_date = pd.to_datetime(end_date + " 23:59:59")
    mask = (futures_news_baidu_df['发布时间'] >= start_date) & (futures_news_baidu_df['发布时间'] <= end_date)
    filtered_news_df = futures_news_baidu_df.loc[mask]
    return filtered_news_df

# 美联储利率决议报告
def get_interest_rate_data(start_year):
    macro_bank_usa_interest_rate_df = ak.macro_bank_usa_interest_rate()
    macro_bank_usa_interest_rate_df['日期'] = pd.to_datetime(macro_bank_usa_interest_rate_df['日期'])
    filtered_df = macro_bank_usa_interest_rate_df[macro_bank_usa_interest_rate_df['日期'].dt.year >= start_year]
    return filtered_df

# 美国 CPI 月率报告
def get_cpi_data(start_year):
    macro_usa_cpi_monthly_df = ak.macro_usa_cpi_monthly()
    macro_usa_cpi_monthly_df['日期'] = pd.to_datetime(macro_usa_cpi_monthly_df['日期'])
    filtered_df = macro_usa_cpi_monthly_df[macro_usa_cpi_monthly_df['日期'].dt.year >= start_year]
    return filtered_df

# 美国核心 CPI 月率报告
def get_core_cpi_data(start_year):
    macro_usa_core_cpi_monthly_df = ak.macro_usa_core_cpi_monthly()
    macro_usa_core_cpi_monthly_df['日期'] = pd.to_datetime(macro_usa_core_cpi_monthly_df['日期'])
    filtered_df = macro_usa_core_cpi_monthly_df[macro_usa_core_cpi_monthly_df['日期'].dt.year >= start_year]
    return filtered_df

# 美国非农就业人数报告
def get_non_farm_data(start_year):
    macro_usa_non_farm_df = ak.macro_usa_non_farm()
    macro_usa_non_farm_df['日期'] = pd.to_datetime(macro_usa_non_farm_df['日期'])
    filtered_df = macro_usa_non_farm_df[macro_usa_non_farm_df['日期'].dt.year >= start_year]
    return filtered_df

# 美国 ADP 就业人数报告
def get_adp_employment_data(start_year):
    macro_usa_adp_employment_df = ak.macro_usa_adp_employment()
    macro_usa_adp_employment_df['日期'] = pd.to_datetime(macro_usa_adp_employment_df['日期'])
    filtered_df = macro_usa_adp_employment_df[macro_usa_adp_employment_df['日期'].dt.year >= start_year]
    return filtered_df

# 伦敦金属交易所(LME)-库存报告
def get_lme_stock_data(start_date, end_date, commodity):
    macro_euro_lme_stock_df = ak.macro_euro_lme_stock()
    macro_euro_lme_stock_df['日期'] = pd.to_datetime(macro_euro_lme_stock_df['日期'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    mask = (macro_euro_lme_stock_df['日期'] >= start_date) & (macro_euro_lme_stock_df['日期'] <= end_date)
    filtered_df = macro_euro_lme_stock_df.loc[mask]
    stock_column = f"{commodity}-库存"
    registered_column = f"{commodity}-注册仓单"
    cancelled_column = f"{commodity}-注销仓单"
    if stock_column not in filtered_df.columns or registered_column not in filtered_df.columns or cancelled_column not in filtered_df.columns:
        st.error(f"数据中不存在品种 {commodity} 的库存、注册仓单或注销仓单信息。")
        return None, None
    return filtered_df, (stock_column, registered_column, cancelled_column)

# 全球宏观指标重大事件
def get_economic_events(date):
    news_economic_baidu_df = ak.news_economic_baidu(date=date)
    return news_economic_baidu_df

# 智能问答
def ask_question(question):
    answer = ak.nlp_answer(question=question)
    return answer

st.title("金融数据与新闻资讯获取")
st.write("created by 恒力期货上海分公司")

menu = [
    "上海金属网快讯",
    "伦敦金属交易所库存报告（20140702-至今）",
    "全球宏观指标重大事件",
    "美联储利率决议报告（从 19820927-至今）",
    "美国CPI月度报告（19700101-至今）",
    "美国核心CPI月度报告（19700101-至今）",
    "美国非农就业人数月度报告（19700102-至今）",
    "美国ADP就业人数报告（20010601-至今）",
    "百度期货新闻",
    "智能问答"
]
choice = st.sidebar.selectbox("选择功能", menu)

if choice == "上海金属网快讯":
    symbol = st.selectbox("请选择想要获取资讯的品种名", ['全部', '要闻', 'VIP', '财经', '铜', '铝', '铅', '锌', '镍', '锡', '贵金属', '小金属'])
    start_date = st.date_input("请输入开始日期:")
    end_date = st.date_input("请输入结束日期:")
    if st.button("获取资讯"):
        news_df = get_shmet_news(symbol, str(start_date), str(end_date))
        st.write(news_df)

elif choice == "百度期货新闻":
    symbol = st.text_input("请输入想要获取资讯的品种代码 (如 'AU', 'AG' 等):")
    start_date = st.date_input("请输入开始日期:")
    end_date = st.date_input("请输入结束日期:")
    if st.button("获取资讯"):
        news_df = get_baidu_news(symbol, str(start_date), str(end_date))
        st.write(news_df)

elif choice == "美联储利率决议报告（从 19820927-至今）":
    start_year = st.number_input("请输入想要获取数据的起始年代 (如 1990):", min_value=1900, max_value=2100, step=1)
    if st.button("获取数据"):
        data_df = get_interest_rate_data(start_year)
        st.write(data_df)

elif choice == "美国CPI月度报告（19700101-至今）":
    start_year = st.number_input("请输入想要获取数据的起始年代 (如 1990):", min_value=1900, max_value=2100, step=1)
    if st.button("获取数据"):
        data_df = get_cpi_data(start_year)
        st.write(data_df)

elif choice == "美国核心CPI月度报告（19700101-至今）":
    start_year = st.number_input("请输入想要获取数据的起始年代 (如 1990):", min_value=1900, max_value=2100, step=1)
    if st.button("获取数据"):
        data_df = get_core_cpi_data(start_year)
        st.write(data_df)

elif choice == "美国非农就业人数月度报告（19700102-至今）":
    start_year = st.number_input("请输入想要获取数据的起始年代 (如 1990):", min_value=1900, max_value=2100, step=1)
    if st.button("获取数据"):
        data_df = get_non_farm_data(start_year)
        st.write(data_df)

elif choice == "美国ADP就业人数报告（20010601-至今）":
    start_year = st.number_input("请输入想要获取数据的起始年代 (如 1990):", min_value=1900, max_value=2100, step=1)
    if st.button("获取数据"):
        data_df = get_adp_employment_data(start_year)
        st.write(data_df)

elif choice == "伦敦金属交易所库存报告（20140702-至今）":
    start_date = st.date_input("请输入开始日期:")
    end_date = st.date_input("请输入结束日期:")
    commodity = st.selectbox("请选择品种名", ['铜', '锡', '铅', '锌', '铝', '镍'])
    if st.button("获取数据"):
        data_df, columns = get_lme_stock_data(str(start_date), str(end_date), commodity)
        if data_df is not None:
            st.write(data_df)
            st.line_chart(data_df.set_index('日期')[list(columns)])

elif choice == "全球宏观指标重大事件":
    date = st.date_input("请选择日期:").strftime("%Y%m%d")
    if st.button("获取数据"):
        data_df = get_economic_events(date)
        st.write(data_df)

elif choice == "智能问答":
    question = st.text_input("请输入您的问题:")
    if st.button("获取答案"):
        answer = ask_question(question)
        st.write(f"问：{question}")
        st.write(f"答：{answer}")
