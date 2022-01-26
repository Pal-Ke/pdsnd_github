import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('-'*60)
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington, all)
    while True:
        city = input("Which city should we select? Please enter Chicago, New York City, Washington, or 'all' for an analysis based on all these three cities:\n")
        if city.strip().lower() in ('chicago', 'new york city', 'washington', 'all', 'nyc', 'dc'):
            if city.strip().lower() == 'dc':
                city = 'washington'
            elif city.strip().lower() == 'nyc':
                city = 'new york city'
            break
        else: print('Invalid entry - please try again.')
    # get user input for month (all, january, february, ... , june)
    while True:
        print('Data is available for the months January to June 2017.')
        month = input('Please enter the name of the month you are interested in or "all".\n')
        if month.strip().lower() in ('january','february','march', 'april', 'may', 'june', 'all'):
            break
        else: print('Invalid entry - please try again.')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Please enter the day of the week which should be investigated or "all".\n')
        if day.strip().lower() in ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all'):
            break
        else: print('Invalid entry - please try again.')
    print('-'*60)
    return city.strip().lower(), month.strip().lower(), day.strip().lower()


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    if city != 'all':
        df = pd.read_csv(CITY_DATA[city])
    else:
        df = pd.DataFrame()
        for city_name in CITY_DATA:
            #df = df.append(pd.read_csv(CITY_DATA[city]))
            df_new = pd.read_csv(CITY_DATA[city_name])
            df_new.insert(0,'City',city_name.title())
            df = df.append(df_new)
    # Convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Extract month and day of week from Start Time to create new columns
    # filter by month if applicable
    if month != 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['Month'] = df['Start Time'].dt.month_name()
        df = df[df['Month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['Weekday'] = df['Start Time'].dt.day_name()
        df = df[df['Weekday'] == day.title()]

    for extra_col in ['Weekday','Month']:
        try:
            df.drop([extra_col], axis = 1, inplace = True)
        except KeyError:
            print('')
            #print('Column {} not created...'.format(extra_col))

    return df

def data_summary(df):
    """Displays a short summary of the selected data/filtered dataframe."""

    print('')
    print('-'*60)
    msg = '\nAccording to your selection, the dataset has {} rows and contains the following {} columns:\n{}\n'
    print(msg.format(int(df.size/len(df.columns)), int(len(df.columns)),' '+"\n ".join(df.columns)))
    print("Here is a preview of the data table:\n", df,'\nYou can select raw data access from the main menu to go row-wise through the entire table.')
    input('[ENTER] to return to the selection menu.  ')

##
def raw_data(df):
    """Displays raw data table (unaltered imported data table after filtering).
       Allows to scroll down by 5 new lines each or by a selected number of rows.
    """

    print('-'*60)
    print('\nThis section will allow you to access the raw data table that is currently loaded.\n')
    print('\nYou will be able to go through the table by entering either the number of rows you would like to see next, [y]es for the default option (5 rows) or [n]o to abort.\n')
    print('\nPlease bear in mind that bigger numbers of rows may not be fully displayed on your screen, however, you will be able to skip/scroll through the table faster.')
    print('\nBy typing [df] you can select to show the condensed overview of the entire raw data table and return to the main menu.')
    print('\nThe currently selected data table has {} rows.'.format(len(df)))
    print('Here are the first 5 rows of that raw data table:')
    r_list = [0,1,2,3,4]
    limit = len(df) -1
    while True:
        print('-'*140)
        print(df.iloc[r_list])
        print('-'*140)
        #print('Please enter the number of rows [1...1,000,000] you would like to see next, [y]es for the |default| option (5 rows) or [n]o to abort.')
        print('Would you like to proceed?')
        print('Please enter the number of rows you would like to see next, [yes] for the |default| option (5 rows) or [no] to abort.')
        while True:
            try:
                x = str(input(''))
                if not (x in ('yes','no','df') or (int(x) > 0)): #(0 < int(x) <= 1000000)):
                    raise ValueError
            except (ValueError, IndexError):
                print("Invalid entry - Please enter a valid positive number, 'yes' or 'no' and hit [ENTER/RETURN].")
            else:
                if x.strip().lower() == 'no':
                    break
                if x == 'df':
                    print(df)
                    x = 'no'
                    break
                else:
                    if x == 'yes':
                         x = 5
                    if r_list[-1] >= (limit-int(x)): #if row number selection exceeds remaining rows
                        if int(x) > limit - r_list[-1]:
                            x = limit - r_list[-1]   # restrict selection to
                        n_list = list(range(int(x))) # number of remaining rows
                        r_list = [y + (limit - n_list[-1]) for y in n_list]
                        # show no of remaining rows from last row position to the last row of the table
                        print(df.iloc[r_list])
                        print('That displayed the last rows of the table!')
                        x = 'no'
                        break
                    else:
                        n_list = list(range(int(x)))
                        r_list = [y + r_list[-1]+1 for y in n_list]
                        break
        if x == 'no':
            break
    print('-'*60)
    input('[ENTER] to return to the selection menu.  ')


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('-'*60)
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #ensure datetime format
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # display the most common month
    df['Month'] = df['Start Time'].dt.month_name()
    count_table = df.groupby(['Month'])['Month'].count()
    popular_month = count_table[count_table == count_table.max()].index[0]
    print('\nThe most popular month is {}.\n'.format(popular_month))

    # display the most common day of week
    df['Weekday'] = df['Start Time'].dt.day_name()
    count_table = df.groupby(['Weekday'])['Weekday'].count()
    popular_dow = count_table[count_table == count_table.max()].index[0]
    print('\nThe most popular day of the week is {}.\n'.format(popular_dow))

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour
    count_table = df.groupby(['Hour'])['Hour'].count()
    popular_hour = count_table[count_table == count_table.max()].index[0]
    print('\nThe most popular hour of the day to start bike travel is {}.\n'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    input('[ENTER] to return to the selection menu.')


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('-'*60)
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Identify the most commonly used start station
    count_table = df.groupby(['Start Station'])['Start Station'].count()
    popular_start = count_table[count_table == count_table.max()].index[0]
    start_counts = count_table.max()
    # ... and the most common destination of trips starting from it
    #  >> cave: variable count_table is being reused <<
    count_table = df[df['Start Station'] == popular_start].groupby(['End Station'])['Start Time'].count()
    pop_start_destination = count_table[count_table == count_table.max()].index[0]
    start_desti_counts = count_table.max()
    # Print the results rgd the most common Start Station
    print("\nThe most popular station to start bike trips is '{}' ({} counts).".format(popular_start,start_counts))
    print("The most common destination to go from there is {} ({} counts).\n".format(pop_start_destination,start_desti_counts))

    # Identify the most commonly used end station
    count_table = df.groupby(['End Station'])['End Station'].count()
    popular_end = count_table[count_table == count_table.max()].index[0]
    end_counts = count_table.max()
    # ... and the most common start/origin of trips ending there
    count_table = df[df['End Station'] == popular_end].groupby(['Start Station'])['Start Time'].count()
    pop_desti_origin = count_table[count_table == count_table.max()].index[0]
    end_start_counts = count_table.max()
    # Print the results rgd the most common End Station
    print("\nThe most popular destination for bike trips is the station '{}' ({} counts).".format(popular_end, end_counts))
    print("Most trips that ended there started at station {} ({} counts)\n".format(pop_desti_origin,end_start_counts))

    # Display most frequent combination [bidirectional]
    # Identify return trips and round trips
    count_table1 = df[df['Start Station']!=df['End Station']].groupby(['Start Station', 'End Station'])['Start Time'].count()   # direction A > B
    count_table2 = df[df['Start Station']!=df['End Station']].groupby(['End Station', 'Start Station'])['Start Time'].count() # direction B > A
    count_table3 = df[df['Start Station']==df['End Station']].groupby(['End Station', 'Start Station'])['Start Time'].count() # round trips

    df_join = pd.DataFrame({'Start>End': count_table1 , 'End>Start':count_table2, 'Round': count_table3})

    df_join.fillna(0, inplace=True)
    df_join['sum'] = df_join['Start>End'] + df_join['End>Start'] + df_join['Round']
    df_join.sort_values(by = ['sum'], ascending = False)
    ## This approach will allow to identify the most popular combination of stations but it will leave double row entries, one for the directional label A > B and another for B > A "return" trips.

    popular_combo = df_join[df_join['sum'] == df_join['sum'].max()].index[0]
    if popular_combo[0] != popular_combo[1]:
        print("\nWith {} counts, the most popular bike trips were between the stations '{}' and '{}'.\n".format(int(df_join['sum'].max()),popular_combo[0], popular_combo[1]))
    else:
        print("\nThe most popular trips were round trips starting from and ending at station '{}' ({} counts).\n".format(popular_combo[0], int(df_join['sum'].max())))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    input('[ENTER] to return to the selection menu.  ')

def ret_time(total, unit = 'hrs'):
    """ Converts time in seconds to units hours + minutes + second, returns those as a string variable. Function for the analysis part regarding time duration.

    Arg:    total ... time in seconds
            unit .. a secondary argument defining the output
            (default = 'hrs', other option: 'min')
    Return: a string variable indicating converted input as hrs + mins + secs
    """
    if unit == 'hrs':   # will return result as hours + minutes + seconds
        hr = total // (60*60)
        min = (total % (60*60)) // 60
        sec = (total % (60*60)) % 60
        msg = str('{} hours, {} minutes, and {} seconds'.format(int(hr), int(min), round(sec,2)))
    elif unit == 'min': # will return result as minutes + seconds
        min = total // 60
        sec = total % 60
        msg = str('{} minutes, and {} seconds'.format(int(min),round(sec,2)))

    return msg

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('-'*60)
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total = df['Trip Duration'].sum()
    print('\nThe accumulated travel duration of all users in the selected period is {}.\n'.format(ret_time(total)))

    # display longest travel time
    longest = df['Trip Duration'].max()
    print('\nThe longest travel duration of bike trips in the selected period is {}.\n'.format(ret_time(longest)))


    # display mean travel time
    mean_dur = df['Trip Duration'].mean()
    print('\nThe average travel duration of bike trips is {}.\n'.format(ret_time(mean_dur, unit = 'min')))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    input('[ENTER] to return to the selection menu.')


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('-'*60)
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    ut_counts =  df[['Start Time','User Type']].dropna(axis=0).groupby(['User Type'])['Start Time'].count()
    if ut_counts.max() != 0:
        print('\nThe following number of bike trips were registered:')
        for count in ut_counts:
            print('   {} trips by {}s '.format(count,ut_counts[ut_counts == count].index[0], count))


    # Display counts of gender categories
    try:
        gt_counts =  df[['Start Time','Gender']].dropna(axis=0).groupby(['Gender'])['Start Time'].count()
        if gt_counts.max() != 0:
            print('\nGrouping by gender categories, the following number of bike trips were registered:')
            for count in gt_counts:
                print('   {} trips by {}s '.format(count,gt_counts[gt_counts == count].index[0], count))
    except:
        print('No data for gender categories are available in this data set.')


    # Display earliest, most recent, and most common year of birth (yob)
    try:
        mode_yob = df[['Start Time','Birth Year']].dropna(axis=0)['Birth Year'].mode()[0]
        ear_yob = df[['Start Time','Birth Year']].dropna(axis=0)['Birth Year'].min()
        lat_yob = df[['Start Time','Birth Year']].dropna(axis=0)['Birth Year'].max()
        print('\nThe oldest customer at the time was born in the year {} while the youngest customer was born in {}.'.format(int(ear_yob),int(lat_yob)))
        msg = 'The most common year of birth was {}.'
        print(msg.format(int(mode_yob)))
    except:
        print('No data for the year of birth are available in this data set.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*60)
    input('[ENTER] to return to the selection menu.')

def user_query(city, month, day):
    """ Starts an interaction with the user:
        a) presents current data selection according to passed arguments
        b) queries the user's choice for data access.

    Arguments: city, month, day

    Returns: a single string variable with one of the following values:
    'summary', 'raw', 'time', 'station', 'trip', 'user', 'restart', or 'exit'.
    """
    msg_main = "You can access bike sharing data in {} for {} in {} 2017."
    if city != 'all':
        msg_city = city.title()
    else:
        msg_city = 'Chicago, Washington, and New York City'
    if day != 'all':
        msg_day = 'all ' + day.title() +'s'
    else:
        msg_day = 'all weekdays'
    if month != 'all':
        msg_month = month.title()
    else:
        msg_month = 'all months (Jan - June) of'
    print('')
    print('-'*60)
    print(msg_main.format(msg_city, msg_day, msg_month))
    print("Please select one of the following options by typing in..:")
    print("\n> 'summary' - to access a short summary of the selected data")
    print("\n> 'raw'     - for raw data table access")
    print("\n> 'time'    - to access information on popular travel times")
    print("\n> 'station' - to access information on popular stations")
    print("\n> 'trip'    - to access information on trip durations")
    print("\n> 'user'    - to access information about user data")
    print("\n> 'restart' - if you would like to alter your selection")
    print("\n> 'exit'    - if you would like to exit this programm")
    print('-'*60)

    while True:
        user_input = input('')
        #day = input('Please enter the day of the week which should be investigated or "all".')
        if user_input.strip().lower() in ('summary', 'raw', 'time', 'station', 'trip', 'user', 'restart', 'exit'):
            return user_input.strip().lower()
            break
        else: print('Invalid entry - please try again.')


def main():
    while True:
        # Query loop requesting input: will get filter/selection arguments for the analysis/results part
        while True:
            city, month, day = get_filters()
            msg = 'Thank you! The following selection was registered:\n  City:            {}\n  Month:           {}\n  Day of the week: {}'
            print(msg.format(city.title(), month.title(), day.title()))
            print("\nPlease enter 'yes' if you agree to proceed with that selection:")
            while True:
                restart = input('')
                if restart.strip().lower() in ['yes']:
                    break
                elif restart.strip().lower() in ['no']:
                    break
                else:
                    print("Sorry, that was unclear - please enter 'yes' to proceed or 'no' to restart.")
            if restart.strip().lower() not in ['no']: #!= 'no':
                break
            else:
                print("Very well - let's restart:")

        # Load data according to arguments: city data, filter by month and weekday
        df = load_data(city, month, day)

        # interaction loop: show statistics/results as requested by the user
        while True:
            # returns a string var for the following selection
            user_input = user_query(city, month, day)
            if user_input == 'summary':
                data_summary(df)
            elif user_input == 'raw':
                raw_data(df)
            elif user_input == 'time':
                time_stats(df)
            elif user_input == 'station':
                station_stats(df)
            elif user_input == 'trip':
                trip_duration_stats(df)
            elif user_input == 'user':
                user_stats(df)
            elif user_input in ['exit','restart']:
                print('Alright...')
                break
            else:
                print('i really don\'t know what happened...')
        if user_input == 'exit':
            print('... thanks for using this data browser! Till next time!\n')
            break
        else:
            print('        ... restarting\n          ..\n           .')

if __name__ == "__main__":
	main()
