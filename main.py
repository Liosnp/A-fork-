from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.commons.utils import JsCode
from streamlit_echarts import st_pyecharts
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import streamlit as st
import wash_data
import get_data

#Author:HuXintong
def Page_selected():
    st.text("Choose your situation")
    df=wash_data.wash_data()
    choice_App=st.selectbox('Applicant Income',["<5000","<10000","<15000","<=20000",">20000"])
    choice_App=(choice_App.replace('<',''))
    choice_App=(choice_App.replace('=',''))
    choice_App=float(choice_App.replace('>',''))
    if choice_App==5000:
        df=df[df['ApplicantIncome']<=5000]
    elif choice_App==10000:
        df=df[5000<df['ApplicantIncome']][df['ApplicantIncome']<=10000]
    elif choice_App==15000:
        df=df[10000<df['ApplicantIncome']][df['ApplicantIncome']<=15000]
    elif choice_App==20000:
        df=df[15000<df['ApplicantIncome']][df['ApplicantIncome']<=20000]
    else:
        df=df[df['ApplicantIncome']>20000]
    choice_Coapp=st.selectbox('CoApplicant Income',["0","<3000","<6000","<=10000",">10000"])
    choice_Coapp=(choice_Coapp.replace('<',''))
    choice_Coapp=(choice_Coapp.replace('=',''))
    choice_Coapp=float(choice_Coapp.replace('>',''))
    if choice_Coapp==0:
        df=df[df['CoapplicantIncome']==0]
    elif choice_Coapp==3000:
        df=df[0<df['CoapplicantIncome']][df['CoapplicantIncome']<=3000]
    elif choice_Coapp==6000:
        df=df[3000<df['CoapplicantIncome']][df['CoapplicantIncome']<=6000]
    elif choice_Coapp==10000:
        df=df[6000<df['CoapplicantIncome']][df['CoapplicantIncome']<=10000]
    else:
        df=df[df['CoapplicantIncome']>10000]
    df_success=df[df['Loan_Status']==1].shape[0]
    df_all=df.shape[0]
    if df_all==0:
        st.text("empty dataset")
        return None
    df_how=df_success*100/df_all
    st.text("The probability of your loan success is:"+str(df_how)+"%")
    st.dataframe(df)
    return None

#Author:Tianqi Liu
#To show the mean/max/min value of ApplicantIncome/CoapplicantIncome/LoanAmount under the selection of whether it is succesfully loaned.
def page_question2():
    st.title('question2')
    info=[0,1]
    select_loan=st.selectbox('Please enter whether the applicant has successfully borrowed (0 represents unsuccessful, 1 represents successful) ',info.columns.tolist())
    df_selected_new=get_data.select_Loan_Status(select_loan)
    info2=['ApplicantIncome','CoapplicantIncome','LoanAmount']
    select_line=st.selectbox('Please enter the data you want to view',info2.columns.tolist())
    mean=df_select_new[select_line].mean()
    min=df_select_new[select_line].min()
    max=df_select_new[select_line].min()
    data = {'mean': [mean],
        'min': [min],
        'max': [max]}
    df = pd.DataFrame(data)
    st.write(df)

#Author:Yuxi Guo
def data_selected():
    '''
    This section is to get the dataset selected and transfer the dataset to plots function that works in different pages.
    '''
    x = st.sidebar.slider('The size of data:', 0.0, 1.0, 1.0, 0.01)
    df = wash_data.wash_data()
    is_graduate = st.sidebar.selectbox('Graduate', [None, True, False])
    is_married = st.sidebar.selectbox('Married', [None, True, False])
    is_female = st.sidebar.selectbox('Female', [None, True, False])
    is_self_employed = st.sidebar.selectbox('Self_employed', [None, True, False])
    is_urban = st.sidebar.selectbox('Urban', [None, True, False])
    credit_history = st.sidebar.selectbox('Credit_History', [None, True, False])
    df_selected = get_data.select_data(x, is_graduate, is_married, is_female, is_self_employed, is_urban,
                                       credit_history)
    return df_selected

#Author:Yuxi Guo
#To implement the home page and make our dataset visible.
def page_home(): 
    df_selected = data_selected() 
    # Display the welcome message in the center, bold, and larger font 
    st.markdown("<h1 style='text-align: center; color: black; font-size: 2em; font-weight: bold;'>Welcome to our app</h1>", unsafe_allow_html=True) # Display the DataFrame below the welcome message 
    st.markdown("<h2 style='font-weight: bold;'>APP Introduction:</h2>\n" "After analyzing the customer's own information, the customer will judge the likelihood of the success of the loan based on our analysis results.", unsafe_allow_html=True) 
    st.markdown("<h2 style='font-weight: bold;'>Dataset Source:</h2>\n" "About the company Dream Housing Finance Corporation. They have a presence in all urban, semi-urban and rural areas. They would like to present the relevant charts based on the details of the customer provided when filling out the online application form. These details include the borrower's gender, marital status, educational background, employment situation, income situation, co-applicant income, loan amount required, repayment time, number of loans, place of residence, etc. Here, they provide a partial data set.", unsafe_allow_html=True) 
    st.dataframe(df_selected) # Display the introduction text 
    return None

#Author:Yuxi Guo
#To plot the mean value of the variables and make it visible in a bar plot.
def page_plot_bar():
    plt.style.use("ggplot")
    df_selected=data_selected()
    df_x=df_selected[['Is_Female','Is_graduate','Is_married','Is_urban','Is_self_employed','Loan_Status','Credit_History','Dependents']]
    df_y=df_selected.drop(['Is_Female','Is_graduate','Is_married','Is_urban','Is_self_employed','Loan_Status','Credit_History','Dependents','Loan_ID'],axis=1)
    choice_x=st.selectbox('x variable',df_x.columns.tolist())
    choice_y=st.selectbox('y variable',df_y.columns.tolist())
    df_selected_g=df_selected.groupby(choice_x)
    df=df_selected_g[[choice_y]].mean()
    st.text("Average Values of y variables")
    st.bar_chart(df)
    return None

#Author:Yuxi Guo
#This function is to implement the box plot in our app.
def page_plot_box():
    plt.style.use("ggplot")
    st.title('Boxplot')
    df_selected = data_selected().drop('Loan_ID',axis=1)
    df_x=df_selected[['Is_Female','Is_graduate','Is_married','Is_urban','Is_self_employed','Loan_Status','Credit_History','Dependents']]
    df_y=df_selected.drop(['Is_Female','Is_graduate','Is_married','Is_urban','Is_self_employed','Loan_Status','Credit_History','Dependents'],axis=1)
    choice_x=st.selectbox('x variable',df_x.columns.tolist())
    choice_y=st.selectbox('y variable',df_y.columns.tolist())
    s=sns.catplot(x=choice_x,y=choice_y,kind='box',data=df_selected)
    st.pyplot(s)
    return None

#Author:Yuxi Guo
#This section is to design pie chart of our dataset.
def page_plot_pie():
    plt.style.use("ggplot")
    df_selected = data_selected()
    df_x=df_selected[['Is_Female','Is_graduate','Is_married','Is_urban','Is_self_employed','Loan_Status','Credit_History','Dependents']]
    choice_x=st.selectbox('Ways to classify',df_x.columns.tolist())
    df_selected_g=df_selected.groupby(choice_x)
    df=df_selected_g.count()
    fig,ax=plt.subplots()
    labels=[]
    #to implement the labels' length is the same to the number of rows
    if df.shape[0]==0:
        st.text('The dataset that you selected is empty, please give up some selectors.')
        return None
    else:
        for i in range(0,df.shape[0]):
            labels.append(f'{choice_x}:{df.index.tolist()[i]}')
    ax.pie(df['Loan_ID'],labels=labels,autopct="%1.1f%%")
    st.pyplot(fig)
    return None

#Author:Yuxi Guo
#This function is to design the heatmap page and plot it with the dataset selected.
def page_plot_heatmap():
    plt.style.use("ggplot")
    fig,ax=plt.subplots()
    df_selected=data_selected()
    df=df_selected.drop(['Loan_ID'],axis=1)
    cols=df.corr().abs().nlargest(9, 'Loan_Status')['Loan_Status'].index
    cm=df_selected[cols].corr()
    variables=cols.tolist()
    for v in range(0,len(variables)):
        variables[v]=variables[v][0:3]
    labels=cols.tolist()
    cax=ax.matshow(cm,cmap='hot_r')
    fig.colorbar(cax)
    tick_spacing=1
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    ax.set_xticklabels(['']+variables)
    ax.set_yticklabels(['']+labels)    
    st.pyplot(fig)
    return None

#-----------------------------------------------------------------
# def plot_pie_LiuYanLin():
   

    
#     # 获取筛选后的数据
#     data = data_selected()
#     # 转换数据格式以符合pyecharts饼图的要求
#     loan_status = data['Loan_Status'].value_counts(normalize=True)

#     data_pair = [list(z) for z in zip(loan_status.index, loan_status.values)]
    
#     # 创建饼图
#     pie_chart = (
#         Pie()
#         .add(
#             series_name="示例系列",
#             data_pair=data_pair,
#             radius=["40%", "75%"],
#             label_opts=opts.LabelOpts(
#                 position="outside",
#                 formatter="{b|{b}: }{c}  ({d}%)",
#                 rich={
#                     "b": {"fontSize": 16, "lineHeight": 33},
#                     "per": {"color": "#eee", "backgroundColor": "#334455", "padding": [2, 4], "borderRadius": 2},
#                 },
#             ),
#         )
#         .set_global_opts(title_opts=opts.TitleOpts(title="饼图示例"))
#         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
#     )
    
#     # 使用st_pyecharts在Streamlit中渲染饼图
#     st_pyecharts(pie_chart)
#-------------------------------------------------------------------------


# from pyecharts.faker import Faker
# def plot_pie_LiuYanLin():
#     c = (
#         Pie()
#         .add("", [list(z) for z in zip(Faker.choose(), Faker.values())])
#         .set_global_opts(title_opts=opts.TitleOpts(title="Pie-基本示例"))
#         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
#         .render("pie_base.html")
#         )
    
#     st_pyecharts(c)

#---------------------------------------------------------------
def plot_pie_LiuYanLin():
    # 加载数据集
    df_selected = data_selected()
    # 计算每个地区贷款成功的比例
    loan_status_by_area = df_selected.groupby('Property_Area')['Loan_Status'].value_counts(normalize=True).unstack()
    
    
    # 选择一个地区进行可视化，例如 'Urban'
    urban_data = loan_status_by_area['Urban'].to_dict()
    urban_data_pair = [list(item) for item in urban_data.items()]
    
    # 生成饼图数据
    pie_chart = (
        Pie()
        .add("", urban_data_pair)
        .set_global_opts(title_opts=opts.TitleOpts(title="Urban Area Loan Approval Rates"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
      
    )
    
    
        
     st_pyecharts(pie_chart)

#-------------------------------------------------------------
# def main():
#     # 创建一个侧边栏选择器，用于选择饼图的显示方式
#     chart_type = st.sidebar.selectbox("选择图表类型", ["饼图", "其他图表"])
    
#     # 根据选择的图表类型来显示相应的图表
#     if chart_type == "饼图":
#         plot_pie_chart()
#     # 可以添加更多elif来添加其他图表类型的处理
#     # elif chart_type == "其他图表":
#         # 其他图表的函数调用

# # 运行主函数

#     main()

# def plot_pei_LiuYanLin():
#     # 用户选择地区类型
#     area_options = ['Urban', 'Semiurban', 'Rural']
#     selected_areas = st.multiselect('选择地区类型', options=area_options)
    
#     # 获取并清洗数据
#     df_selected = data_selected(is_urban=selected_areas)
    
#     # 如果数据不为空，则绘制饼图
#     if not df_selected.empty:
#         loan_status_counts = df_selected['Loan_Status'].value_counts().rename(index={1: 'Yes', 0: 'No'})
#         data_pair = [list(z) for z in zip(loan_status_counts.index, loan_status_counts.values)]
#         pie_chart = (
#             Pie()
#             .add("", data_pair)
#             .set_global_opts(title_opts=opts.TitleOpts(title="贷款成功率"))
#             .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"))
#         )
#         st_pyecharts(pie_chart)
#     else:
#         st.error("根据所选地区没有找到数据，请重新选择。")


#Author:Yuxi Guo
def main():
    #This section is to implement the control flow of our app, where the pages designing are implemented.
    session_state=st.session_state
    if 'page' not in session_state:
        session_state['page']='Home'
    page=st.sidebar.radio('Navigate',['Home','Plot_bar','Plot_box','Plot_pie','Plot_heatmap','LiuYanLin_pie','LiuTianqi','HuXintong'])
    #to implement multi-pages
    if page=='Home':
        page_home()
    elif page=='Plot_bar':
        page_plot_bar()
    elif page=='Plot_box':
        page_plot_box()
    elif page=='Plot_pie':
        page_plot_pie()
    elif page=='Plot_heatmap':
        page_plot_heatmap()
    elif page=='LiuYanlin_pie':
        plot_pie_LiuYanLin()    
    elif page=='LiuTianqi':
        page_question2()
    elif page=='HuXintong':
        Page_selected()
main()
