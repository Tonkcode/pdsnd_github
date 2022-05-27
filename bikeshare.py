'''
Analyze citywise bikeshare data to generate user, trip duration, station and time stats

'''

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
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while True:
        city = input('Please enter one of following cities : chicago, new york city, washington\n')
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Please enter a valid city')

    # get user input for month (all, january, february, ... , june)
    month = None
    while True:
        month = input('Please enter any of the following months : january, february, march, april, may, june or all\n')
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Please enter a valid month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while True:
        day = input('Please enter any of the following days : sunday, monday, tuesday, wednesday, thursday, '
                    'friday, saturday or all\n')
        day = day.lower()
        if day in ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'all']:
            break
        else:
            print('Please enter a valid day')

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
    df = pd.read_csv('./' + CITY_DATA[city])

    # Assumption : month and day filters are applied on the trips that started in a given month.
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    if month != 'all':
        month_map = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6}
        df = df[df['month'] == month_map[month]]

    df['day'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    if day != 'all':
        day_map = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5,
                   'sunday': 6}
        df = df[df['day'] == day_map[day]]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    month_map = {1: 'january', 2: 'february', 3: 'march', 4: 'april', 5: 'may', 6: 'june'}
    print('Most Common Month: ', month_map[df['month'].value_counts().idxmax()])

    # display the most common day of week
    day_map = {0: 'monday', 1: 'tuesday', 2: 'wednesday', 3: 'thursday', 4: 'friday', 5: 'saturday',
               6: 'sunday'}
    print('Most Common Day: ', day_map[df['day'].value_counts().idxmax()])

    # display the most common start hour
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour
    print('Most Common hour: ', df['hour'].value_counts().idxmax())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Most commonly used start station: ', df['Start Station'].value_counts().idxmax())


    # display most commonly used end station
    print('Most commonly used End station: ', df['End Station'].value_counts().idxmax())


    # display most frequent combination of start station and end station trip
    print('Most frequent combination of start station and end station trip: ', df.groupby(['Start Station', 'End Station']).size().nlargest(1))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total Trip Duration: ', sum(df['Trip Duration']))

    # display mean travel time
    print('Mean Trip Duration: ', sum(df['Trip Duration'])/len(df))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User types Counts: ', df['User Type'].value_counts())
    if city != 'washington':
        # Display counts of gender
        print('Gender Counts: ', df['Gender'].value_counts())

        # Display earliest, most recent, and most common year of birth
        print('Earliest Year: ', min(df['Birth Year']))
        print('Most Recent Year: ', max(df['Birth Year']))
        print('Most Common Year of Birth: ', df['Birth Year'].value_counts().idxmax())

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    
def view_raw_data(df):
    """Displays raw data as per user input."""
    raw_data_counter = 0 
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        if view_data.lower() == 'yes':
            print(df.iloc[raw_data_counter:raw_data_counter+5]) 
            raw_data_counter += 5  
        else : 
            break
            
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        view_raw_data(df)        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
