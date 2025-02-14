# ./MLOps/altair/altair.install.test0.py

import altair as alt
import pandas as pd

# Sample data
data = {'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 1, 5, 3],
        }
df = pd.DataFrame(data)

# Create a simple scatter plot.
chart = alt.Chart(df).mark_circle().encode(
    x='x',
    y='y'
).properties(
    title='Altair Test Chart'
)

# Display the chart (this will open a browser window or display in a notebook).
chart.show() # Or chart.display() in some environments.

# To save the chart to a file.
chart.save('altair_test_chart.html')
chart.save('altair_test_chart.json')
chart.save('altair_test_chart.png')
