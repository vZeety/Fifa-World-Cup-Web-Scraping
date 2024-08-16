import requests
from bs4 import BeautifulSoup
import lxml
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class WorldCupDataAnalysis():
    def __init__(self, url='https://fbref.com/en/comps/1/possession/World-Cup-Stats#stats_possession::none'):
        self.data = None  # Stores the dataframe with the data scrapped from the website
        self.url = url  # Stores the url for the website
        self.ranked_col_names = []  # Stores the column names for which a rank is calculated (Check question 2)
        '''
        The following dictionary holds the color code for the plots for each team 
        '''
        self.team_colors = {
            'ar': '#97233f',
            'au': '#a71930',
            'be': '#241773',
            'br': '#00338d',
            'cm': '#0085ca',
            'ca': '#0b162a',
            'cr': '#fb4f14',
            'hr': '#311d00',
            'dk': '#041e42',
            'ec': '#002244',
            'eng': '#0076b6',
            'fr': '#203731',
            'de': '#03202f',
            'gh': '#002c5f',
            'ir': '#006778',
            'jp': '#e31837',
            'kr': '#002a5e',
            'mx': '#003594',
            'ma': '#008e97',
            'nl': '#4f2683',
            'pl': '#002244',
            'pt': '#d3bc8d',
            'qa': '#0b2265',
            'sa': '#125740',
            'sn': '#000000',
            'rs': '#004c54',
            'es': '#ffb612',
            'ch': '#aa0000',
            'tn': '#002244',
            'us': '#d50a0a',
            'uy': '#0c2340',
            'wls': '#174a3f'
        }

        '''
    Task 2: Populate this map to with the continents for the teams. Check https://en.wikipedia.org/wiki/2022_FIFA_World_Cup_qualification
    '''
        self.continent_map = {'ar': 'South America',
                              'au': 'Asia',
                              'be': 'Europe',
                              'br': 'South America',
                              'cm': 'Africa',
                              'ca': 'North America',
                              'cr': 'North America',
                              'hr': 'Europe',
                              'dk': 'Europe',
                              'ec': 'South America',
                              'eng': 'Europe',
                              'fr': 'Europe',
                              'de': 'Europe',
                              'gh': 'Africa',
                              'ir': 'Asia',
                              'jp': 'Asia',
                              'kr': 'Asia',
                              'mx': 'North America',
                              'ma': 'Africa',
                              'nl': 'Europe',
                              'pl': 'Europe',
                              'pt': 'Europe',
                              'qa': 'Asia',
                              'sa': 'Asia',
                              'sn': 'Africa',
                              'rs': 'Europe',
                              'es': 'Europe',
                              'ch': 'Europe',
                              'tn': 'Africa',
                              'us': 'North America',
                              'uy': 'South America',
                              'wls': 'Europe'}

    def scrape(self, url=None):  # Barry
        '''
        Task 3: Extracts the table of countries and their respective possession stats from the provided url.

        Input: url (string): If an url is not provided then the url from object initialization is used to scrape the data.
        Output: This method populates the data (check __init__) attribute of the object. Nothing is returned from this method.
        '''
        if url == None:
            url = self.url

        # requesting the html sourcecode from the website
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'lxml')

        # finding the html code for the table
        datable = soup.find('table', id='stats_squads_possession_for')

        # Retrieving columns headers from the HTML code
        col = []
        for i in datable.find_all('th', class_='poptip'):
            title = i.text
            col.append(title)

        # Create a pandas dataframe

        fifa22 = pd.DataFrame(columns=col)

        # populating the dataframe

        for j in datable.find_all('tr')[2:]:
            team_name = j.find('th')
            first_cell = [team_name.text]
            row_data = j.find_all('td')
            data = [i.text for i in row_data]
            final_data = first_cell + data
            length = len(fifa22)
            fifa22.loc[length] = final_data

        self.data = fifa22

    def rank(self):  # Barry
        '''
        Task 4: Create new columns that indicate the percentile (rank) of the data in each column except for the column name squad.For example, for the 'Succ' column, a new column is added called 'Succ_rank'.
        This method adds new columns to the data attribute of the object.
        This method also adds the columns (<col_name>) for which <col_name>_rank column is created to the list ranked_col_names.

        Input: None.
        Output:  Nothing is returned from this method.
        '''
        for col in self.data.columns:
            # iterate over all the columns except rank
            if col != 'Squad':
                # Store the column index
                index = self.data.columns.get_loc(col)
                # Add the string 'rank' to the original column name
                new_name = col + '_rank'
                # Apply the rank method over the data of the column
                new_data = self.data[col].rank(pct='True')
                # Insert the new column and data
                self.data.insert(index + 1, new_name, new_data)
                self.ranked_col_names.append(col)

    def preprocess(self):  # Aidan
        '''
        Task 5: Splits the 'Squad' column value into two new columns 'Squad' and 'Code'. For example, a value 'ar Argentina' will be have a code 'ar' and squad 'Argentina'.
        After adding these columns the old squad column is dropped from the dataframe.
        The method also converts the data type for all the columns (that should be numeric) to a numeric.
        All these changes must be reflected on the data attribute of the object.

        Input: None.
        Output:  Nothing is returned from this method.
        '''
        # Data type conversion
        dtype = {'Squad': str,
                 '# Pl': int,
                 'Poss': float,
                 '90s': float,
                 'Touches': int,
                 'Def Pen': int,
                 'Def 3rd': int,
                 'Mid 3rd': int,
                 'Att 3rd': int,
                 'Att Pen': int,
                 'Live': int,
                 'Att': int,
                 'Succ': int,
                 'Succ%': float,
                 'Tkld': int,
                 'Tkld%': float,
                 'Carries': int,
                 'TotDist': int,
                 'PrgDist': int,
                 'PrgC': int,
                 '1/3': int,
                 'CPA': int,
                 'Mis': int,
                 'Dis': int,
                 'Rec': int,
                 'PrgR': int}
        self.data = self.data.astype(dtype)

        # Splitting 'Squad'
        def code(x):
            result = ''
            for letter in x:
                if letter == ' ':
                    break
                result += letter
            return result

        self.data['Code'] = self.data['Squad'].apply(code)

        def squad(x):
            for letter in x:
                if letter == ' ':
                    x = x[1:]
                    break
                x = x[1:]
            return x

        self.data['Squad'] = self.data['Squad'].apply(squad)

    def continentBest(self):  # Aidan
        '''
        Task 6: Returns the best teams from each continent. The overall ranking for each team is calculated based on an aggregate function (e.g. sum or mean) of the Rank columns. Adds this new Rank column as overall_Rank to the DataFrame.

        Input: None.
        Output:  Returns a DataFrame with the best teams for each continent.
        '''
        # Creating overall_Rank
        rankcols = []
        for col in self.data:
            if col[-4:] == 'rank':
                rankcols.append(col)

        agg = 0
        for col in rankcols:
            agg += self.data[col]
        avg = agg / len(rankcols)
        self.data['overall_Rank'] = avg

        # Filtering best teams from each cont.
        temp = self.data.copy()

        def cont(x):
            return self.continent_map[x]

        temp['Continent'] = temp['Code'].apply(cont)

        temp.sort_values(by='overall_Rank', ascending=False, inplace=True)
        temp['not_best'] = temp.duplicated(subset=['Continent'])

        filtered = temp[temp['not_best'] == False]
        filtered = filtered.reset_index()

        return filtered[['Squad', 'Continent', 'overall_Rank']]

    def bestAttack(self):  # Aidan
        '''
        Task 7: Returns the name of the team that has the most number of touches in the attacking 3rd and attacking penalty area.

        Input: None.
        Output:  Returns a string denoting the best team for attacking.
        '''
        temp = self.data.copy()

        temp['total'] = temp['Att 3rd'] + temp['Att Pen']  # aggregate attacking 3rd and attacking pen
        return str(temp.sort_values(by='total', ascending=False, inplace=False).reset_index().at[
                       0, 'Squad'])  # sort and return first squad value as str

    def bestDefense(self):  # Aidan
        '''
        Task 8: Returns the name of the team that has the most number of touches in the defensive 3rd and defensive penalty area.

        Input: None.
        Output:  Returns a string denoting the best team for defense.
        '''
        temp = self.data.copy()

        temp['total'] = temp['Def 3rd'] + temp['Def Pen']  # aggregate defending 3rd and defending pen
        return str(temp.sort_values(by='total', ascending=False, inplace=False).reset_index().at[
                       0, 'Squad'])  # sort and return first squad value as str

    def bestMidfield(self):  # Aidan
        '''
        Task 9: Returns the name of the team that has the most number of touches in the midfield 3rd area.

        Input: None.
        Output:  Returns a string denoting the best team for midfield.
        '''
        temp = self.data.copy()

        return str(temp.sort_values(by='Mid 3rd', ascending=False, inplace=False).reset_index().at[
                       0, 'Squad'])  # sort and return first squad value as str

    def getRanksData(self, team):  # Aidan
        '''
        Task 10: Returns the rank data for the team passed as parameter.
        The rank data includes the ranks apart from the overall_Rank. This method also returns the color code for the team.

        Input: String specifying the name of the team (i.e. 'Squad').
        Output:  Returns a numpy array with the ranking data and string color code.
        '''
        # Filtering for rank columns
        rankcols = []
        for col in self.data:
            if col[-4:] == 'rank':
                rankcols.append(col)

        temp = self.data[self.data['Squad'] == team].copy().reset_index()
        result = [
            [team, self.team_colors[temp.at[0, 'Code']]]]  # first value in resultant array is in the form [team, color]

        for col in rankcols:
            result.append([col, temp.at[0, col]])  # append following rank values in form [column name, rank]

        nparray = np.array(result)
        return nparray

    def __drawRadarChart(self, ax, data, var_names=None, color=None):  # Jake
        '''
        Task 11: Draws a radar chart (on the axes passed as parameter) with the data, color code, and variable names passed as parameter.

        Input: A matplotlib axes object.
        An numpy array for the Data to plot.
        A list of var_names for which the function plots the data.
        A string specifying the color to use for the plot.
        Output:  Nothing is returned from this method.
        '''
        # You must set global variables a and as a list of axes named 'axes'
        axes[a] = fig.add_axes(ax,
                               polar=True)  # creates axis with names from 'axes' list with values passed into the method
        var_names = [*var_names, var_names[0]]  # Dublicates the first values of var_names and appends it to end of list
        data1 = [*data, data[0]]  # Duplicates first value of array and pushes it to end

        label_loc = np.linspace(start=0, stop=2 * np.pi,
                                num=len(data1))  # Sets locations of labels evenly around circle

        axes[a].plot(label_loc, data1, color=color)  # Plots data
        lines, labels = plt.thetagrids(np.degrees(label_loc),
                                       labels=var_names)  # Places labels according to locations we set

    def visualizeTeam(self, ax, team_name, var_names=None, color=None):  # Jake
        '''
        Task 12: Draws a radar chart (on the axes passed as parameter) for the team passed as parameter. If the var_names is None then uses the columns in the 'ranked_col_names' list for the radar chart.

        Input: A matplotlib axes object.
        A string specifying the team name (i.e. Squad).
        An optional list of variable names to be used in the radar chart and a string color code is also passed as input to this method.
        Output:  Nothing is returned from this method.
        '''
        if var_names == None:  # If no var_names are passed, use ranked_col_names class variable
            var_names = self.ranked_col_names
        # Gets data for passed team name and var_names, converts data to numpy array
        tempdf = self.data
        data = tempdf[tempdf['Squad'] == team_name][var_names]
        data = data.to_numpy()
        data = data[0]
        # Calls __drawRadarChart using passed axis, var_names, and color, as well as data coresponding to passed team
        self.__drawRadarChart(ax, data, var_names, color)


# Driver Code Starts Here. We wrote our code in Jupyter Notebook, so all driver code may not work properly in other IDEs.
if __name__ == '__main__':

    # Barry Driver Code
    tempdf1 = WorldCupDataAnalysis()
    tempdf1.scrape()
    tempdf2 = tempdf1.data
    print(tempdf2)

    tempdf = WorldCupDataAnalysis()
    tempdf.scrape()
    tempdf.preprocess()
    tempdf.rank()
    tempdf1 = tempdf.data
    print(tempdf2)

    # Aidan Driver Code
    test = WorldCupDataAnalysis()
    test.scrape()
    test.preprocess()
    test.rank()
    print('Task 6:')
    print(test.continentBest())
    print()
    print('Task 7:')
    print(test.bestAttack())
    print()
    print('Task 8:')
    print(test.bestDefense())
    print()
    print('Task 9:')
    print(test.bestMidfield())
    print()
    print('Task 10:')
    print(test.getRanksData('Croatia'))

    # Jake Driver Code
    cont = tempdf.continent_map
    Continents = []
    Cont_dict = {}
    for i in cont.keys():
        if cont[i] not in Continents:
            Continents.append(cont[i])

    for i in Continents:
        Cont_dict[i] = []

    for i in cont.keys():
        Cont_dict[cont[i]].append(i)

    print(tempdf2)

    TouchesList = ['Touches_rank',
                   'Def Pen_rank',
                   'Def 3rd_rank',
                   'Mid 3rd_rank',
                   'Att 3rd_rank',
                   'Att Pen_rank',
                   'Live_rank']

    # Q13a South America
    fig = plt.figure(figsize=(5, 5))
    SASquads = []
    colors = ['blue', 'red', 'green', 'purple']
    axes = ['ax1', 'ax2', 'ax3', 'ax4']
    a = 0
    ax = [[0, 1], [1, 1], [0, 0], [1, 0]]
    for i in Cont_dict['South America']:
        SASquads.append(tempdf1[tempdf1['Code'] == i]['Squad'].values[0])
    for i in zip(SASquads, ax, colors):
        tempdf.visualizeTeam(i[1] + [.8, .8], i[0], TouchesList, i[2])
        axes[a].set_title(i[0], color=i[2])
        a += 1

    # Q13a North America
    fig = plt.figure(figsize=(5, 5))
    NASquads = []
    colors = ['blue', 'red', 'green', 'purple']
    axes = ['ax1', 'ax2', 'ax3', 'ax4']
    a = 0
    ax = [[0, 1], [1, 1], [0, 0], [1, 0]]
    for i in Cont_dict['North America']:
        NASquads.append(tempdf1[tempdf1['Code'] == i]['Squad'].values[0])
    for i in zip(NASquads, ax, colors):
        tempdf.visualizeTeam(i[1] + [.8, .8], i[0], TouchesList, i[2])
        axes[a].set_title(i[0], color=i[2])
        a += 1

    # Q13a Africa
    fig = plt.figure(figsize=(9, 9))
    AfricaSquads = []
    colors = ['blue', 'red', 'green', 'purple', 'orange']
    axes = ['ax1', 'ax2', 'ax3', 'ax4', 'ax5']
    a = 0
    ax = [[0, 1], [.5, .5], [1, 1], [0, 0], [1, 0]]
    for i in Cont_dict['Africa']:
        AfricaSquads.append(tempdf1[tempdf1['Code'] == i]['Squad'].values[0])
    for i in zip(AfricaSquads, ax, colors):
        tempdf.visualizeTeam(i[1] + [.6, .6], i[0], TouchesList, i[2])
        axes[a].set_title(i[0], color=i[2], fontsize=20)
        a += 1

    # Q13a Asia
    fig = plt.figure(figsize=(7, 7))
    AsiaSquads = []
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'teal']
    axes = ['ax1', 'ax2', 'ax3', 'ax4', 'ax5', 'ax6']
    a = 0
    ax = [[0, 1], [.5, 1], [1, 1], [0, .5], [.5, .5], [1, .5]]
    for i in Cont_dict['Asia']:
        AsiaSquads.append(tempdf1[tempdf1['Code'] == i]['Squad'].values[0])
    for i in zip(AsiaSquads, ax, colors):
        tempdf.visualizeTeam(i[1] + [.37, .37], i[0], TouchesList, i[2])
        axes[a].set_title(i[0], color=i[2])
        a += 1

    # Q13a Europe part 1
    fig = plt.figure(figsize=(7, 7))
    EUSquads = []
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'teal']
    axes = ['ax1', 'ax2', 'ax3', 'ax4', 'ax5', 'ax6']
    a = 0
    ax = [[0, 1], [.5, 1], [1, 1], [0, .5], [.5, .5], [1, .5]]
    for i in Cont_dict['Europe']:
        EUSquads.append(tempdf1[tempdf1['Code'] == i]['Squad'].values[0])
    for i in zip(EUSquads[0:7], ax, colors):
        tempdf.visualizeTeam(i[1] + [.37, .37], i[0], TouchesList, i[2])
        axes[a].set_title(i[0], color=i[2])
        a += 1

    # Q13a Europe part 2
    fig = plt.figure(figsize=(7, 7))
    EUSquads = []
    colors = ['blue', 'red', 'green', 'purple', 'orange', 'teal', 'black']
    axes = ['ax1', 'ax2', 'ax3', 'ax4', 'ax5', 'ax6', 'ax7']
    a = 0
    ax = [[0, 1], [.5, 1], [1, 1], [0, .5], [.5, .5], [1, .5], [.5, 0]]
    for i in Cont_dict['Europe']:
        EUSquads.append(tempdf1[tempdf1['Code'] == i]['Squad'].values[0])
    for i in zip(EUSquads[6:], ax, colors):
        tempdf.visualizeTeam(i[1] + [.37, .37], i[0], TouchesList, i[2])
        axes[a].set_title(i[0], color=i[2])
        a += 1

    # Q13 b-d
    top9 = ['Argentina', 'France', 'Croatia', 'Morocco', 'Netherlands', 'England', 'Brazil', 'Portugal', 'Japan']
    fig = plt.figure(figsize=(7, 7))
    axes = ['ax1', 'ax2', 'ax3', 'ax4', 'ax5', 'ax6', 'ax7', 'ax8', 'ax9']
    # colors=['blue','red','green','purple','orange','teal','black','magenta','olivedrab']
    bestlist = ['Att 3rd_rank', 'Att Pen_rank', 'Def 3rd_rank', 'Def Pen_rank', 'Mid 3rd_rank']
    # bestlist=['Att 3rd','Att Pen','Def 3rd','Def Pen','Mid 3rd']
    ax = ax = [[0, 1], [.5, 1], [1, 1], [0, .5], [.5, .5], [1, .5], [0, 0], [.5, 0], [1, 0]]
    a = 0
    for i in zip(top9, ax, colors):
        tempdf.visualizeTeam(i[1] + [.37, .37], i[0], bestlist, i[2])
        axes[a].set_title(i[0], color=i[2])
        a += 1
