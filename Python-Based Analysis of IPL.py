import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Plotly to create interactive graph
# import chart_studio.plotly as py
from plotly import tools
from plotly.offline import init_notebook_mode, iplot
init_notebook_mode(connected=True)
import plotly.figure_factory as ff
import plotly.graph_objs as go

sns.set_style("whitegrid")
plt.style.use("fivethirtyeight")

# To remove unnecessary warnings
import warnings
warnings.filterwarnings("ignore")

deliveries = pd.read_csv('/Applications/Python 3.11/IPL Ball-by-Ball 2008-2020.csv')
matches = pd.read_csv('/Applications/Python 3.11/IPL Matches 2008-2020.csv')
