# -*- coding: utf-8 -*-
"""
Created on Thu Apr  4 11:15:18 2024

@author: Ofir and Moshiko
"""

#%%
import sys
import os
import pandas as pd
import numpy as np
import skimage as ski
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot
import plotly.io as io
io.renderers.default='browser'
io.templates.default = "plotly"
import plotly.graph_objs as go
from plotly.offline import plot


df = pd.read_csv('C:\\Users\\User\\ofirBSC\\YearE\\ויזואליזציה\\visualization_project\\Merge_Data_py.csv')



#%%
#-----------------------------------------------------------------------------#
#////////////////////////// Chart 1 - Box Plot/////////////////////////////#
#-----------------------------------------------------------------------------#


columns_df_Box_Plot = ['LamasName', 'PriceForMeter', 'MarketingRep','DistrictHeb','hh_MidatDatiyut_Name']
df_Box_Plot = df[columns_df_Box_Plot]
df_Box_Plot = df_Box_Plot.sort_values(by='PriceForMeter')


df_Box_Plot['DistrictHeb'] = df_Box_Plot['DistrictHeb'].str.replace('אזור יהודה ושומרון', 'מחוז ירושלים').str.replace('מחוז תל אביב', 'מחוז המרכז').str.replace('מחוז חיפה', 'מחוז הצפון')

df_Box_Plot['hh_MidatDatiyut_Name'] = df_Box_Plot['hh_MidatDatiyut_Name'].str.replace('יישובים מסורתיים', 'יישובים דתיים').str.replace('יישובים חרדיים', 'יישובים דתיים')


df_Box_Plot_dati = df_Box_Plot[df_Box_Plot['hh_MidatDatiyut_Name'] == 'יישובים דתיים']
df_Box_Plot_hiloni = df_Box_Plot[df_Box_Plot['hh_MidatDatiyut_Name'] == 'יישובים חילוניים']


Region_dati = df_Box_Plot_dati['DistrictHeb']
Region_hiloni = df_Box_Plot_hiloni['DistrictHeb']

Price_dati = df_Box_Plot_dati['PriceForMeter']
Price_hiloni = df_Box_Plot_hiloni['PriceForMeter']

fig = go.Figure()

fig.add_trace(go.Box(
    y=Price_dati, 
    x=Region_dati,
    name='יישובים דתיים',
    marker_color='#008fb1'
))
fig.add_trace(go.Box(
    y=Price_hiloni,
    x=Region_hiloni,
    name='יישובים חילוניים',
    marker_color='#ff5555'
))


fig.update_layout(
    title="במחוז דרום נצפה הפער המשמעותי ביותר בתמחור הדירות בין יישובים דתיים ליישובים חילוניים",
    title_x=0.5,
    title_font=dict(size=24, family='Calibri', color='black'),  
    yaxis_title='מחיר למטר (ש"ח)',
    xaxis_title='מחוז',
    xaxis_title_font=dict(size=20 ,family='Calibri', color='black'),
    yaxis_title_font=dict(size=20 ,family='Calibri', color='black'),
    boxmode='group', 

    xaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(180, 180, 180)',
            linewidth=1.5,
            ticks='outside',
            tickfont=dict(
                family='Calibri',
                size=16,
                color='rgb(0, 0, 0)',
            ),
        ),
        yaxis=dict(
            showline=True,
            showgrid=False,
            showticklabels=True,
            linecolor='rgb(180, 180, 180)',
            linewidth=1.5,
            ticks='outside',
            tickfont=dict(
                family='Calibri',
                size=16,
                color='rgb(0, 0, 0)',
            ),
        ),
        autosize=True,
        margin=dict(
            autoexpand=True

        ),
        showlegend=True,  
        legend=dict(font=dict(size=16, family='Calibri', color='black')),
        plot_bgcolor='white'

)


fig.show()



#%%
#-----------------------------------------------------------------------------#
#////////////////////////// Chart 2 - Line Chart /////////////////////////////#
#-----------------------------------------------------------------------------#

columns_line_chart = ['LotteryExecutionDate', 'LamasName', 'Subscribers','Winners' ,'DistrictHeb']
df_line_chart = df[columns_line_chart]
df_line_chart['DistrictHeb'] = df_line_chart['DistrictHeb'].str.replace('אזור יהודה ושומרון', 'מחוז ירושלים').str.replace('מחוז תל אביב', 'מחוז המרכז').str.replace('מחוז חיפה', 'מחוז הצפון')

df_line_chart = df_line_chart[df_line_chart['LotteryExecutionDate'] != 'לא מוגדר']
df_line_chart.replace("-", np.nan, inplace=True)
df_line_chart = df_line_chart.dropna()

df_line_chart['LotteryExecutionDate'] = pd.to_datetime(df_line_chart['LotteryExecutionDate'])
df_line_chart['Quarter'] = df_line_chart['LotteryExecutionDate'].dt.to_period('Q')
df_line_chart['Quarter'] = df_line_chart['Quarter'].astype(str)
df_line_chart['Odds Of Winning'] = df_line_chart['Winners'] / df_line_chart['Subscribers'] 


line_chart_group_by = df_line_chart.groupby(['Quarter', 'DistrictHeb']).agg({
    'LotteryExecutionDate': 'min',
    'Odds Of Winning': 'mean',
}).reset_index()

line_chart_group_by = line_chart_group_by.sort_values(by='Quarter')
line_chart_group_by = line_chart_group_by[line_chart_group_by['Quarter'] != '2016Q1']


sub_line_chart_north = line_chart_group_by[line_chart_group_by['DistrictHeb'] == 'מחוז הצפון'][['Quarter', 'Odds Of Winning','LotteryExecutionDate']]
sub_line_chart_center = line_chart_group_by[line_chart_group_by['DistrictHeb'] == 'מחוז המרכז'][['Quarter', 'Odds Of Winning','LotteryExecutionDate']]
sub_line_chart_south = line_chart_group_by[line_chart_group_by['DistrictHeb'] == 'מחוז הדרום'][['Quarter', 'Odds Of Winning','LotteryExecutionDate']]
sub_line_chart_jerusalem = line_chart_group_by[line_chart_group_by['DistrictHeb'] == 'מחוז ירושלים'][['Quarter', 'Odds Of Winning','LotteryExecutionDate']]

trace1 = go.Scatter(x=sub_line_chart_center['LotteryExecutionDate'], y=sub_line_chart_center['Odds Of Winning'], mode='lines', name='מחוז המרכז', line=dict(color='mediumseagreen'), legendgroup="מחוז המרכז")
trace2 = go.Scatter(x=sub_line_chart_north['LotteryExecutionDate'], y=sub_line_chart_north['Odds Of Winning'], mode='lines', name='מחוז הצפון', line=dict(color='salmon'), legendgroup="מחוז הצפון")
trace3 = go.Scatter(x=sub_line_chart_south['LotteryExecutionDate'], y=sub_line_chart_south['Odds Of Winning'], mode='lines', name='מחוז הדרום', line=dict(color='mediumorchid'), legendgroup="מחוז הדרום")
trace4 = go.Scatter(x=sub_line_chart_jerusalem['LotteryExecutionDate'], y=sub_line_chart_jerusalem['Odds Of Winning'], mode='lines', name='מחוז ירושלים', line=dict(color='royalblue'), legendgroup="מחוז ירושלים")


def format_hover_text(df,DistrictHeb):
 hover_text = 'District: ' + DistrictHeb + '<br>' + \
              'Quarter: ' + df['Quarter'] + '<br>' + \
                 'Odds of Winning: ' + df['Odds Of Winning'].apply(lambda x: f'{x:.2f}')
 return hover_text

trace1['hovertext'] = format_hover_text(sub_line_chart_center,'מחוז המרכז' )
trace1['hovertemplate'] = '<b>%{hovertext}</b><extra></extra>'  

trace2['hovertext'] = format_hover_text(sub_line_chart_north, 'מחוז הצפון')
trace2['hovertemplate'] = '<b>%{hovertext}</b><extra></extra>'

trace3['hovertext'] = format_hover_text(sub_line_chart_south, 'מחוז הדרום')
trace3['hovertemplate'] = '<b>%{hovertext}</b><extra></extra>'

trace4['hovertext'] = format_hover_text(sub_line_chart_jerusalem, 'מחוז ירושלים')
trace4['hovertemplate'] = '<b>%{hovertext}</b><extra></extra>'

layout = go.Layout(
    title='בשנים האחרונות סיכויי הזכיה בהגרלות במחוז צפון הם הגבוהים ביותר',
    title_x=0.5,
    title_font=dict(size=18, family='Calibri', color='black'),  
    xaxis=dict(title='מועד ביצוע ההגרלה', showgrid=False, showline=True),
    yaxis=dict(title='סיכוי זכייה', showgrid=False, showline=True),
    xaxis_title_font=dict(size=16 ,family='Calibri', color='black'),
    yaxis_title_font=dict(size=16 ,family='Calibri', color='black'),
    legend=dict(x=0.8, y=1),
    plot_bgcolor='rgba(255, 255, 255, 1)'
)

fig = go.Figure(data=[trace1, trace2, trace3,trace4], layout=layout)

fig.update_layout(
    xaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(180, 180, 180)',
        linewidth=1.5,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(0, 0, 0)',
        ),
    ),
    yaxis=dict(
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(180, 180, 180)',
        linewidth=1.5,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=12,
            color='rgb(0, 0, 0)',
        ),
    ),
    autosize=False,
    margin=dict(
        autoexpand=False,
        l=100,
        r=20,
        t=110,
    ),
    showlegend=True,  
    plot_bgcolor='white'
)

fig.show()




#%%
#-----------------------------------------------------------------------------#
#////////////////////////// Chart 3 - bar chart /////////////////////////////#
#-----------------------------------------------------------------------------#

import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


columns_bar_chart = ['LotteryExecutionDate', 'LamasName', 'Subscribers','LotterySignupHousingUnits']
df_bar_chart = df[columns_bar_chart]


df_bar_chart.replace("-", np.nan, inplace=True)
df_bar_chart = df_bar_chart.dropna()
df_bar_chart = df_bar_chart[ df_bar_chart['LotterySignupHousingUnits'] > 9]

df_bar_chart['LotteryExecutionDate'] = pd.to_datetime(df_bar_chart['LotteryExecutionDate'])

df_bar_chart['Year'] = df_bar_chart['LotteryExecutionDate'].dt.year
df_bar_chart['Demands'] = df_bar_chart['Subscribers'] / df_bar_chart['LotterySignupHousingUnits'] 

bar_chart_group_by = df_bar_chart.groupby(['Year', 'LamasName']).agg({
    'Demands': 'mean',
}).reset_index()

mask = bar_chart_group_by['Year'].isin([2022, 2023])
filtered_df = bar_chart_group_by[mask]

pivot_df_bar_chart = filtered_df.pivot(index='LamasName', columns='Year', values='Demands').reset_index()

pivot_df_bar_chart.columns.name = None  
pivot_df_bar_chart.columns = ['city', 'value in 2022', 'value in 2023']

pivot_df_bar_chart = pivot_df_bar_chart.dropna()
pivot_df_bar_chart['change']= ((pivot_df_bar_chart['value in 2023']-pivot_df_bar_chart['value in 2022'])/pivot_df_bar_chart['value in 2022'])*100
pivot_df_bar_chart['change_abs']= abs(pivot_df_bar_chart['change'])
pivot_df_bar_chart = pivot_df_bar_chart.nlargest(10, 'change_abs')

pivot_df_bar_chart_positive =pivot_df_bar_chart['change'][pivot_df_bar_chart['change'] >= 0]
pivot_df_bar_chart_positive = pivot_df_bar_chart_positive.sort_values(ascending=True)

pivot_df_bar_chart_negative =pivot_df_bar_chart['change'][pivot_df_bar_chart['change'] < 0]

import plotly.io as io
io.templates.default = "none"
fig = go.Figure()

fig.add_trace(go.Bar(
    y=pivot_df_bar_chart['city'][pivot_df_bar_chart['change'] < 0],
    x=pivot_df_bar_chart_negative,
    name='Negative',
    marker_color='crimson',
    orientation='h',
    base=0  
))

fig.add_trace(go.Bar(
    y=pivot_df_bar_chart['city'][pivot_df_bar_chart['change'] >= 0],
    x=pivot_df_bar_chart_positive,
    name='Positive',
    marker_color='royalblue',
    orientation='h'  
))


# Update layout
fig.update_layout(
    
    
    title="עשרת הערים בהם נצפו השינויים המשמעותיים ביותר בביקושים (נרשמים לדירה שהוגרלה) בין השנים 2022-2023<br>נהריה בצמיחה וחיפה בצניחה",
    title_font=dict(size=26, family='Calibri', color='black'),
    xaxis_title='השינוי בביקוש (אחוז)',  
    yaxis_title='עיר',  
    barmode='relative',  
    bargap=0.1,  
    bargroupgap=0.1,  
    yaxis=dict(automargin=True, tickfont = dict(size=15)),
    xaxis=dict(tickfont = dict(size=15), range=[min(pivot_df_bar_chart['change']) - 10, max(pivot_df_bar_chart['change']) + 10]),  # Set x-axis range
    xaxis_showgrid=False,
    yaxis_showgrid=False,  
    showlegend=False,
    xaxis_title_font=dict(size=22 ,family='Calibri', color='black'),
    yaxis_title_font=dict(size=22 ,family='Calibri', color='black'),
)

fig.update_yaxes(title_standoff=8, showline=True , linewidth=0.2, linecolor='grey')
fig.update_xaxes(title_standoff=5,showline=True , linewidth=1, linecolor='grey')

# Show the plot
fig.show()



#%%
#-----------------------------------------------------------------------------#
#////////////////////////// Chart 4 - radar/////////////////////////////#
#-----------------------------------------------------------------------------#


import plotly.io as io
io.templates.default = "none"



column_df_spider = ['LotteryExecutionDate', 'LamasName', 'MarketingRep']
df_spider = df[column_df_spider]

df_spider = df_spider[df_spider['LotteryExecutionDate'] != 'לא מוגדר']
df_spider.replace("-", np.nan, inplace=True)

df_spider['LotteryExecutionDate'] = pd.to_datetime(df_spider['LotteryExecutionDate'])
df_spider['Month'] = df_spider['LotteryExecutionDate'].dt.month
month_names = {1: 'ינואר', 2: 'פברואר', 3: 'מרץ', 4: 'אפריל', 5: 'מאי', 6: 'יוני',
               7: 'יולי', 8: 'אוגוסט', 9: 'ספטמבר', 10: 'אוקטובר', 11: 'נובמבר', 12: 'דצמבר'}
df_spider['Month'] = df_spider['Month'].map(month_names)
df_spider['Year'] = df_spider['LotteryExecutionDate'].dt.year


df_spider_group_by = df_spider.groupby(['Year', 'Month', 'MarketingRep']).agg({
    'LamasName': 'count',
}).reset_index()

df_spider_group_by = df_spider_group_by.groupby(['Month', 'MarketingRep']).agg({
    'LamasName': 'mean',
}).reset_index()

df_spider_group_by.rename(columns={'LamasName': 'Average Lotteries'}, inplace=True)

df_pivot_spider = df_spider_group_by.pivot_table(index='Month', columns='MarketingRep', values='Average Lotteries')
df_pivot_spider.reset_index(inplace=True)


month_order = {'פברואר': 3, 'ינואר': 4, 'דצמבר': 5, 'נובמבר': 6, 'אוקטובר': 7, 'ספטמבר': 8,
               'אוגוסט': 9, 'יולי': 10, 'יוני': 11, 'מאי': 12, 'אפריל': 1, 'מרץ': 2}

df_pivot_spider['Month_order'] = df_pivot_spider['Month'].map(month_order)
df_pivot_spider = df_pivot_spider.sort_values(by='Month_order')

df_pivot_spider = df_pivot_spider.drop(columns='Month_order')

# Create categories for months
categories = df_pivot_spider['Month'].tolist()
categories.append(categories[0])

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
      r=df_pivot_spider['רמ"י'].tolist() + [df_pivot_spider['רמ"י'].iloc[0]],
      theta=categories,
      fill='toself',
      name='רשות מקרקעי ישראל',
      fillcolor='rgba(0,0,0,0)',
      line=dict(color='#DC143C'),
      hovertemplate='<b>MarketingRep:</b> רשות מקרקעי ישראל<br><b>Month:</b> %{theta}<br><b>Average Lotteries:</b> %{r}<extra></extra>'
))

fig.add_trace(go.Scatterpolar(
      r=df_pivot_spider['משב"ש'].tolist() + [df_pivot_spider['משב"ש'].iloc[0]],
      theta=categories,
      fill='toself',
      name='משרד הבינוי והשיכון',
      fillcolor='rgba(0,0,0,0)',
      line=dict(color='#3D59AB'),
      hovertemplate='<b>MarketingRep:</b> משרד הבינוי והשיכון<br><b>Month:</b> %{theta}<br><b>Average Lotteries:</b> %{r}<extra></extra>'

))


fig.update_layout(
  title="במחצית הראשונה של השנה, ישנו פער ניכר במספר ההגרלות הממוצע לחודש של פרוייקטים אותם משווק משרד הבינוי והשיכון <br>בהשוואה לפרויקטים שמשווקת רשות מקרקעי ישראל",
  title_y=0.97,
  title_font=dict(size=24, family='Calibri', color='black'),
  polar=dict(
      radialaxis=dict(
      visible=True,
      linecolor  = 'lightgrey',
      range=[0, 45],  
      showgrid=True,  
      gridcolor='#EDEDED',  
      gridwidth=1.0,  
      tickfont=dict(size=14)
    )),
  
    legend=dict(
      x=0.75, 
      y=0.5,  
      bgcolor='rgba(255, 255, 255, 0.7)',  
      font=dict(
          size=18  
      )
  ),
  showlegend=True,  
  font=dict(
        size=18 
    )
)

fig.show() 
