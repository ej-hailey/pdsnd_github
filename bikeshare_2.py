import time
import pandas as pd
import numpy as np

# dictionary for cities and respective data files
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

# set global variables
city = ""
month = ""
day = ""

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('\nFirst, let\'s enter the city name: ')
    global city
    city = str(input()).lower()
    while city not in CITY_DATA.keys():
        print('Try again. Choose from Chicago, New York City, or Washington.')
        print('Enter the city name: ')
        city = str(input()).lower()

    # get user input for month (all, january, february, ... , june)
    print('\nGreat! Now let\'s enter the month: ')
    global month
    month = str(input()).lower()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while month not in months:
        print('Try again. Choose a month between January - June or "All".')
        print('Enter a month or "all": ')
        month = str(input()).lower()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nFinally, let\'s enter the day of week: ')
    global day
    day = str(input()).lower()
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while day not in days:
        print('Try again. Choose a day of week from Monday to Sunday or "All".')
        print('Enter a day of week or "all": ')
        day = str(input()).lower()

    print('-'*40)
    return city, month, day


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
    
    # read the file
    df = pd.read_csv(CITY_DATA[city])
    
    # convert datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.day_name()
    
    # filter by month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if month != 'all':
        month = months.index(month) + 1
        df = df[df['Month'] == month]
    else:
        pass
    
    # filter by day of week
    if day != 'all':
        df = df[df['Day of Week'] == day.title()]
    else:
        pass
        
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    max_month = df['Month'].mode()[0]
    print(f'Most Common Month: {month}')

    # display the most common day of week
    max_day = df['Day of Week'].mode()
    print(f'Most Common Day of Week: {max_day}')

    # display the most common start hour
    df['Hour'] = df['Start Time'].dt.hour    
    max_hour = df['Hour'].mode()
    print(f'Most Common Hour: {max_hour}')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print(f'Most Common Start Station: {start_station}')

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print(f'Most Common End Station: {end_station}')
    
    # display most frequent combination of start station and end station trip
    df['Combined'] = df['Start Station'] + " + " + df['End Station']
    max_combined = df['Combined'].mode()[0]
    print(f'Most Common Month: {max_combined}')
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print(f"Total Trip Duration: {df['Trip Duration'].sum()}")

    # display mean travel time
    print(f"Average Trip Duration: {df['Trip Duration'].mean()}")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    users = df['User Type'].unique()
    for user in users:
        print(f"{user} Count: {df['User Type'][df['User Type'] == user].count()}")

    # Display counts of gender
    if 'Gender' in df:
        genders = df['Gender'].unique()
        for gender in genders:
            print(f"{gender} Count: {df['Gender'][df['Gender'] == user].count()}")
    else:
        print('Gender stats cannot be calculated because Gender does not appear in the dataframe.')
            
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        print(f"Earlier Birth Year: {int(df['Birth Year'].min())}")
        print(f"Most Recent Birth Year: {int(df['Birth Year'].max())}")
        print(f"Most Common Birth Year: {int(df['Birth Year'].mode())}")
    else:
        print('Birth Year stats cannot be calculated because Birth Year does not appear in the dataframe.')
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def display_data():
    """Prompts users to view 5 rows of data from dataframe"""
    
    view_data = str(input('Would you like to view 5 rows of individual trip data? Enter yes or no.')).lower()
    while view_data not in ['yes', 'no']:
        view_data = str(input('Please enter yes or no: ')).lower()
    start_loc = 0
    while view_data == 'yes':
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input('Do you wish to continue?: ').lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
