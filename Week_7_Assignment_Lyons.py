#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Jun  20 19:16:48 2021

@author: earle

Title: Week 7 Assignment Lyons
Date: 20JUN2021
Author: Earle Lyons
Purpose: Create advancedd visuals for Week 7 Assignment
    - GeoPandas choropleth map #1
    - GeoPandas choropleth map #2
    - Seaborn heatmap
    
Inputs: 
Outputs: 
Notes:
     MSDS670 Data Visualization (Regis University)
     21M8W1: 05/03/21-06/27/21
     
Data Sources:
    https://www.cdc.gov/nceh/tracking/topics/SunlightUV.htm
    https://www.cdc.gov/nceh/tracking/topics/Cancer.htm
    https://www.census.gov/data/tables/time-series/demo/popest/intercensal-2000-2010-state.html
    https://www.census.gov/data/tables/time-series/demo/popest/intercensal-2000-2010-state.html
    https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html

Data Files: 
    https://github.com/elyons001/msds670_data_visualization/tree/main/data/week_7
    
References:
    https://geopandas.org/getting_started/introduction.html
    https://geopandas.org/docs/user_guide/io.html
    https://wenyandeng.wordpress.com/2017/07/20/maps-of-sri-lankan-army-deaths-with-geopandas/
    https://medium.com/@vworri/simple-geospacial-mapping-with-geopandas-and-the-usual-suspects-77f46d40e807
    https://wenyandeng.wordpress.com/2017/07/20/maps-of-sri-lankan-army-deaths-with-geopandas/
"""

#%% Import libraries
import pandas as pd
import geopandas
from geopandas import GeoDataFrame
import warnings
warnings.filterwarnings('ignore')
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns

#%% Set DPI
dpi = 300

#%% Reset Matplotlib rcParams to default
# https://matplotlib.org/stable/api/matplotlib_configuration_api.html#matplotlib.rc_file_defaults
mpl.rc_file_defaults()

#%% Create DataFrames

# Create two DataFrames for the UV irradiance levels for 2005 and 2015
# Read 'annual_avg_natl_by_state' sheet from the Excel workbook and create
# pandas DataFrames from 2005 and 2015
uv_df = pd.read_excel(r'C:\Users\earle\Documents\GitHub\msds670_data_visualization\data\week_7\UV IRRADIANCE AT NOON.xlsx', 
                    sheet_name='annual_avg_natl_by_state', 
                    usecols="A:D", converters={'stateFIPS':str})
uv_df_2005 = uv_df.loc[uv_df['Year'] == 2005].reset_index(drop=True)
uv_df_2015 = uv_df.loc[uv_df['Year'] == 2015].reset_index(drop=True)

# Create two DataFrames for the melanoma cases for 2005 and 2015
# Read 'annual_avg_natl_by_state' sheet from the Excel workbook and create
# pandas DataFrames from 2005 and 2015
melanoma_df = pd.read_excel(r'C:\Users\earle\Documents\GitHub\msds670_data_visualization\data\week_7\ANNUAL NUMBER OF CASES OF MELANOMA.xlsx', 
                    sheet_name='2005_2015_cases_by_state_pop', usecols="A:F", converters={'stateFIPS':str})
melanoma_df_2005 = melanoma_df.loc[melanoma_df['Year'] == 2005].reset_index(drop=True)
melanoma_df_2015 = melanoma_df.loc[melanoma_df['Year'] == 2015].reset_index(drop=True)
# Drop Alaska and Hawaii
melanoma_df_2005 = melanoma_df_2005.drop(melanoma_df_2005.index[[1, 11]])
melanoma_df_2015 = melanoma_df_2015.drop(melanoma_df_2015.index[[1, 11]])

# Create DataFrame (monthly) and Series (yearly average) for UV irradiance 
# levels for 2005 through 2015
# https://stackoverflow.com/questions/47523483/re-order-dataframe-based-on-month-not-alphabet
# Read 'monthly_avg_by_year' sheet from the Excel workbook and create
# pandas DataFrames
uv_df_by_month_2005_2015 = pd.read_excel(r'C:\Users\earle\Documents\GitHub\msds670_data_visualization\data\week_7\UV IRRADIANCE AT NOON.xlsx', 
                    sheet_name='monthly_avg_by_year', usecols="A:C")
month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
               'July', 'August', 'September', 'October', 'November', 
               'December']
uv_df_by_month_2005_2015 = pd.pivot_table(uv_df_by_month_2005_2015,
                    index='Month',
                    values='UV_Level',
                    columns='Year')
uv_df_by_month_2005_2015 = uv_df_by_month_2005_2015.reindex(month_order)
uv_df_by_month_2005_2015_mean = uv_df_by_month_2005_2015.agg('mean')
uv_df_by_month_2005_2015_mean

# Import shape file form Census.gov and create GeoPandas DataFrame
# https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html
url = "https://www2.census.gov/geo/tiger/GENZ2020/shp/cb_2020_us_state_500k.zip"
gdf_states = geopandas.read_file(url)
gdf_states = gdf_states[["STATEFP", "STUSPS", "NAME", "geometry"]]
gdf_states.rename(columns={'STATEFP': 'stateFIPS'}, inplace=True)
gdf_states['stateFIPS'] = gdf_states['stateFIPS'].str.lstrip('0')
gdf_states['stateFIPS'] = gdf_states['stateFIPS'].astype(str)
# Drop Guam, United States Virgin Islands, Puerto Rico, 
# Commonwealth of the Northern Mariana Islands,
# Alaska, American Samoa, and Hawaii
gdf_states = gdf_states.drop(gdf_states.index[[0, 5, 8, 17, 20, 41, 49]])
gdf_states.sort_values(by=['stateFIPS'])

#%% Merge DataFrames for values to geometry 

# Merge pandas DataFrames for UV irradiance levels for 2005 and 2015 to 
# GeoPandas DataFrame
uv_df_2005_states = uv_df_2005.merge(gdf_states, how='left')
uv_df_2005_states = GeoDataFrame(uv_df_2005_states)
uv_df_2005_states.sort_values(by=['UV_Level'])
uv_df_2015_states = uv_df_2015.merge(gdf_states, how='left')
uv_df_2015_states = GeoDataFrame(uv_df_2015_states)
uv_df_2015_states.sort_values(by=['UV_Level'])

# Merge pandas DataFrames for melanoma cases for 2005 and 2015 to 
# GeoPandas DataFrame
melanoma_df_2005_states = melanoma_df_2005.merge(gdf_states, how='left')
melanoma_df_2005_states = GeoDataFrame(melanoma_df_2005_states)
melanoma_df_2005_states.sort_values(by=['Cases_Per_100K'])
melanoma_df_2015_states = melanoma_df_2015.merge(gdf_states, how='left')
melanoma_df_2015_states = GeoDataFrame(melanoma_df_2015_states)
melanoma_df_2015_states.sort_values(by=['Cases_Per_100K'])

#%% Create first map visual

# Set a variable to the column to visualize the map
variable = 'UV_Level'
# Set the range for the choropleth
vmin, vmax = 80, 180

fig = plt.figure(figsize = (20, 4))
ax1 = fig.add_axes([0, 0.2, 0.4, 0.6])
ax2 = fig.add_axes([0.2, 0.2, 0.4, 0.6])

# Create plots for ax1 and ax2
uv_plt_2005 = uv_df_2005_states.plot(column=variable, cmap='coolwarm', 
                                     linewidth=0.8, 
                                     ax=ax1, edgecolor='white',
                                     vmin=vmin, vmax=vmax, 
                                     legend=False)
uv_plt_2015 = uv_df_2015_states.plot(column=variable, cmap='coolwarm', 
                                     linewidth=0.8, 
                                     ax=ax2, edgecolor='white',
                                     vmin=vmin, vmax=vmax, 
                                     legend=True)

# Set titles
fig.suptitle('Annual average UV irradiance at noon', 
             x=0.1, y=1.0, horizontalalignment='left', fontsize=16)
ax1.set_title('2005', fontsize = 12)
ax2.set_title('2015', fontsize = 12)

# Label legends
ax2.legend(title="mW/m2", loc=(0.92, 0.4), fontsize=14, frameon=False)

# Set axis off
ax1.axis('off')
ax2.axis('off')

# Show plot and save figure
plt.show()
plot1_filename = 'week_7_matplotlib_lyons_1_20JUN21.png'
fig.savefig(plot1_filename, dpi=dpi, bbox_inches='tight')

#%% Create second map visual

# Set a variable to the column to visualize the map
variable = 'Cases_Per_100K'
# Set the range for the choropleth
vmin, vmax = 0, 40

fig = plt.figure(figsize = (20, 4))
ax1 = fig.add_axes([0, 0.2, 0.4, 0.6])
ax2 = fig.add_axes([0.2, 0.2, 0.4, 0.6])

# Create plots for ax1 and ax2
melanoma_plt_2005 = melanoma_df_2005_states.plot(column=variable, 
                                                 cmap='YlOrRd', 
                                                 linewidth=0.8, ax=ax1, 
                                                 edgecolor='white',
                                                 vmin=vmin, vmax=vmax, 
                                                 legend=False)
melanoma_plt_2015 = melanoma_df_2015_states.plot(column=variable, 
                                                 cmap='YlOrRd', 
                                                 linewidth=0.8, ax=ax2, 
                                                 edgecolor='white',
                                                 vmin=vmin, vmax=vmax, 
                                                 legend=True)
# Set titles
fig.suptitle('Annual number of cases of Melanoma of the skin per 100K', 
             x=0.1, y=1.0, horizontalalignment='left', fontsize=16)
ax1.set_title('2005', fontsize = 12)
ax2.set_title('2015', fontsize = 12)

# Label legends
ax2.legend(title="Cases", loc=(0.94, 0.4), fontsize=14, frameon=False)
#ax2.legend(loc=(0.95, 0.4), fontsize=14, frameon=False, title="Cases")

# Set axis off
ax1.axis('off')
ax2.axis('off')

# Show plot and save figure
plt.show()
plot2_filename = 'week_7_matplotlib_lyons_2_20JUN21.png'
fig.savefig(plot2_filename, dpi=dpi, bbox_inches='tight')

#%% Create heatmap visual

fig = plt.figure(figsize=(10,5))
# [left, bottom, width, height]
ax1 = fig.add_axes([0.1, 1.0, 0.9, 0.9]) 
ax2 = fig.add_axes([0.1, 0.7, 0.9, 0.2])
fig.suptitle('Average UV irradiance at noon (mW/m2)', x=0.1, y=2, 
             horizontalalignment='left', fontsize=16)
sns.heatmap(uv_df_by_month_2005_2015, ax=ax1, cmap='coolwarm', 
                        vmin=80, vmax=190, annot=True, fmt=".1f", cbar=False, 
                        xticklabels=True, yticklabels=True)
# Set tick label colors to gray
# https://stackoverflow.com/questions/52392855/how-to-change-label-tick-color-in-seaborn
for tick_label in ax1.get_xticklabels():
    tick_label.set_color("gray")
for tick_label in ax1.get_yticklabels():
    tick_label.set_color("gray")

# Set ax1 title and labels
ax1.set_title('Monthly', loc='left')
ax1.set(xlabel='', ylabel='')

# Create ax2 plot and set title
ax2.plot(uv_df_by_month_2005_2015_mean.index, 
         uv_df_by_month_2005_2015_mean.values, 
         color='black')
ax2.set_title('Yearly', loc='left')

# Set ax2 spines invisible
ax2.spines.right.set_visible(False)
ax2.spines.left.set_visible(False)
ax2.spines.top.set_visible(False)
ax2.spines.bottom.set_visible(False)

# Set ax2 scatter and text
ax2.scatter(2005, 120.423469, s=40, color='black')
ax2.scatter(2012, 126.734694, s=40, color='#b40426')
ax2.scatter(2015, 120.634354, s=40, color='black')
ax2.text(2004.4, 121, '120.4', color='black')
ax2.text(2012.1, 127, '126.7', color='#b40426')
ax2.text(2015.1, 121, '120.6', color='black')

# Set ax2labels and ticks
ax2.xaxis.set_tick_params(which='both', labelbottom=False, colors='white')
ax2.set_xticks([])
ax2.set_xticklabels([])
ax2.set_yticks([])
ax2.set_yticklabels([])
ax2.set_ylim(110, 130)

# Show plot and save figure
plt.show()
plot3_filename = 'week_7_matplotlib_lyons_3_20JUN21.png'
fig.savefig(plot3_filename, dpi=dpi, bbox_inches='tight')