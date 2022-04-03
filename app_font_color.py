import plotly.graph_objects as go

headerColor = '#e0e8ea'
rowEvenColor = '#f5f5f5'
rowOddColor = 'white'

fig = go.Figure(data=[go.Table(
    header=dict(
        values=['<b>EXPENSES</b>','<b>Q1</b>','<b>Q2</b>','<b>Q3</b>','<b>Q4</b>'],
        line_color='#eeeeee',
        fill_color=headerColor,
        align=['left','center'],
        font=dict(color='#5b5b5b', size=11, family="Courier New",)
    ),
    cells=dict(
        values=[
            ['Salaries', 'Office', 'Merchandise', 'Legal', '<b>TOTAL</b>'],
            [1200000, 20000, 80000, 2000, 12120000],
            [1300000, 20000, 70000, 2000, 130902000],
            [1300000, 20000, 120000, 2000, 131222000],
            [1400000, 20000, 90000, 2000, 14102000]],
        line_color='#eeeeee',
        # 2-D list of colors for alternating rows
        fill_color = [[rowOddColor,rowEvenColor,rowOddColor, rowEvenColor,rowOddColor]*5],
        align = ['left', 'center'],
        font = dict(color = '#4f4f4f', size = 12, family="Courier New",)
    ))
])

fig.show()