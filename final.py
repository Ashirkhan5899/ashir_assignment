#Necessary libraries 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns


def read_twb_data(filename, indicator_code):
    ''' 
    This function reads the data(worldbank format) from the given csv file in pandas Data Frame format.
    Because the first 4 rows in the world bank data format files doesn't include useful information so we skip them.
    Also extra columns are dropped.
    Finally the the dataframes with Years as column and the data frame with Country Names are both returned

    Parameters:
        filename - path of the file names which contains the dataset in worldbank data format
        indicator_code - the code for climate change indicator
    Returns:
        df_years - the data frame with Years as columns
        df_countries - the data frame with Countries as Columns for that specific indicator

    '''

    # It reads the data in a data frame from a .csv file, skips the first 4 rows and sets the first column as index
    df_wbdata = pd.read_csv(filename, skiprows=4)
    
    # It only extracts data for a specific indicator
    wbdata = df_wbdata.loc[df_wbdata["Indicator Code"] == indicator_code, :]

    wbdata.index = wbdata.iloc[:, 0]

    # Removes the Extra Columns which are not useful for us
    df_years = wbdata.drop(["Country Name", "Indicator Name", "Country Code", "Indicator Code" , "Unnamed: 66"], axis=1)

    # Transpose the DataFrame so that it has countries as its columns
    df_countries = df_years.T.copy()

    # Return both the Data frames
    return df_years, df_countries

# This function read the world bank data and returns the data for a specific country
def read_twb_data_country(filename, country=''):
    '''  
    This function reads the world bank data file and return the dataframe of a specifc country

    Parameters:
        filename - the path of the file which contains the dataset
        country - the name of the Country for which we want to return the data

    Returns:
        df_data - Data frame of the specific country
    '''
    df_data = pd.read_csv(filename, skiprows=4)             # read the file skipping the first 4 rows
    if country != 'World':
        df_data = df_data.loc[df_data["Country Name"] == country, :]    # extract data for a specific country 

    df_data.index = df_data.iloc[:, 3]
    df_data.drop(columns=["Country Name", "Country Code", "Indicator Code", "Unnamed: 66"], inplace=True) # Drop the unnecessar columns
    

    return df_data




    
def plot_bar_datay(data, countries, years, labelx="", labely = "Rate"):
    '''
    This Function takes the dataset as input and plots a bar graph for specified countries and year

    Parameters:
        data - The Data Frame with years as columns and Countries as index
        countries - a list of countries
        year - list of years
        labelx - (str) the label to be drawn on x-axis
        labely - (str) the label to be drawn on y-axis

    Returns:
        None
    '''

    datay = data.loc[data.index.isin(countries), years ]
    datay = datay.fillna(0)

    # set width of bar with respect to the input data
    barWidth = 10/(len(countries)  * (2*len(years)))
    
    fig = plt.subplots(figsize =(9, 7)) # create a figure of size 14x6
    
    # Set position of bars on X axis
    brs = [np.arange(datay.shape[0])]
    for i in range(0, len(brs[0])-1):
        brs.append([x + barWidth for x in brs[i]])
 
    # Make the plot of each bar
    for i in range(datay.shape[1]):
        plt.bar(brs[i], datay.loc[: , years[i]], width = barWidth, edgecolor ='grey', label =years[i])

    # Adding X and and Y labels
    plt.xlabel(labelx, fontweight ='bold', fontsize = 12)
    plt.ylabel(labely, fontweight ='bold', fontsize = 12)

    # Adding xTicks
    plt.xticks([r + barWidth for r in range(len(countries))], countries , rotation=45)
 
    plt.legend()
    plt.show()


# Function for drawing a line chart
def plot_line(data , countries, years):
    yrs = [str(1980+ i) for i in range(0,40,5)]
    data = data.loc[countries, yrs]

    fig = plt.subplots(figsize =(12, 8)) # create a figure of size 14x6
    plt.plot(data.T , scalex=10)

    # Adding X and and Y labels
    plt.xlabel("", fontweight ='bold', fontsize = 11)
    plt.ylabel("Electricity production from oil sources (% of total)", fontweight ='bold', fontsize = 14)
    plt.xticks(rotation = 35)
    plt.legend(countries, loc='upper left', fontsize = 12)
    plt.show()


#Function for draw a heatmap for a specific country or the world world
def plot_heatmap(file, country, i_codes, i_titles):
    pdata = read_twb_data_country(file, country=country)

    if(country == 'World'):
        pdata = pdata.groupby("Indicator Code").mean()
    
    pdata = pdata.T
    pdata = pdata.iloc[1:,:]
    pdata = pdata.loc[:, i_codes]

    pdata.fillna(0, inplace=True)
    pear = pdata.corr(method='pearson', )

    ax = plt.axes()
    # plot the heatmap
    sns.heatmap(pear, ax=ax, cmap="Blues", annot=True,  xticklabels=i_titles, yticklabels=i_titles)
    ax.set_title("Correlation heatmap: "+ country, fontsize=18)
    plt.show()



if __name__ == "__main__":
    #World Bank DataSet filename for Climate Change
    wbdata_filename = "data/world_bank_data.csv"

    #5 Selected Indicator codes
    urban_population= {"Code": "SP.URB.TOTL.IN.ZS", "Title": "Urban population (% of total population)"} # Urban population (% of total population)
    mortality_rate= {"Code": "SH.DYN.MORT", "Title": "Mortality rate, under-5 (per 1,000 live births)"} #Mortality rate, under-5 (per 1,000 live births)
    co2_emission= {"Code": "EN.ATM.CO2E.SF.ZS", "Title": "CO2 emissions from solid fuel consumption (% of total)"} # CO2 emissions from solid fuel consumption (% of total)
    electriciy_production= {"Code": "EG.ELC.PETR.ZS", "Title": "Electricity production from oil sources (% of total)"} # Electricity production from oil sources (% of total)
    forest_area = {"Code": "AG.LND.FRST.ZS", "Title": "Forest area (% of land area)"} # Forest area (% of land area)


    # Reading the data for those indicators into separate data frames
    df_urban_population, df_urban_population_c  = read_twb_data(wbdata_filename, urban_population["Code"])
    df_mortality_rate, df_mortality_rate_c  = read_twb_data(wbdata_filename, mortality_rate["Code"])
    df_co2_emission, df_co2_emission_c  = read_twb_data(wbdata_filename, co2_emission["Code"])
    df_electricity_production, df_electricity_production_c  = read_twb_data(wbdata_filename, electriciy_production["Code"])
    df_forest_area, df_forest_area_c  = read_twb_data(wbdata_filename, forest_area["Code"])

    #The list of countries for which the indicators are investigated
    countries = ["World", "Pakistan", "United States", "India", "France", "United Kingdom", "Cambodia", "China", "Afghanistan", "Brazil", "Indonesia"]
    years = ["1990","2000", "2010", "2020"] 

    # Urban Population (% of the population)
    df_urban_population["World"] = df_urban_population.mean(axis=1) # Average for the whole world
    plot_bar_datay(df_urban_population, countries, years, labely=urban_population["Title"]) # Draw the plot

    # CO2 emissions from solid fuel consumption (% of total)
    df_co2_emission["World"] = df_co2_emission.mean(axis=1) # Average for the whole world
    plot_bar_datay(df_co2_emission, countries, years, labely=co2_emission["Title"]) # Draw the plot

    # Forest area (% of land area)
    df_forest_area["World"] = df_forest_area.mean(axis=1) # Average for the whole world
    plot_bar_datay(df_forest_area, countries, years, labely=forest_area["Title"]) # Draw the plot

    #Mortality rate, under-5 (per 1,000 live births)
    df_mortality_rate["World"] = df_mortality_rate.mean(axis=1) # Average for the whole world
    plot_bar_datay(df_mortality_rate, countries, years, labely=mortality_rate["Title"]) # Draw the plot

    #draw a line chart for electricity production from oil sources
    plot_line(df_electricity_production, countries=countries, years=[str(1980 +i) for i in range(40)])



    #Create a list of Climate Indicator Codes and titles
    climate_indicators_codes = [co2_emission['Code'] , urban_population["Code"], mortality_rate["Code"], electriciy_production["Code"], forest_area["Code"]]
    climate_indicators_titles = ["CO2 emission" , "Urban Population", "Mortality Rate", "Electricity Production", "Forest Area"]


    #Plotting the heat map for the whole world
    plot_heatmap(wbdata_filename, "World", climate_indicators_codes, climate_indicators_titles)

    plot_heatmap(wbdata_filename, "Pakistan", climate_indicators_codes, climate_indicators_titles)
    plot_heatmap(wbdata_filename, "United States", climate_indicators_codes, climate_indicators_titles)
    plot_heatmap(wbdata_filename, "Brazil", climate_indicators_codes, climate_indicators_titles)