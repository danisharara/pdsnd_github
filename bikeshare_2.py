import time
import pandas as pd
import numpy as np


CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('\nWould you like to see data for New York, Chicago, or Washington?')

    city=input()

    while city.title() != "Chicago" and city != "New York" and city != "Washington":

        print('Invalid input. Please enter either Chicago, New York, or Washington')
        city=input()

   


    # get user input for month (all, january, february, ... , june)
    print('\nWhat month would you like to see data for (between January and June)? If you would like to see all, enter "all".')

    month=input()

    while month.title() != "January" and month != "February" and month != "March" and month != "April" and month != "May" and month != "June" and month != "all":

        print('Invalid input. Please enter a month between January and June or enter "all".')
        month=input()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nWhat day of the week would you like to see data for? If you would like to see all, enter "all".')

    day=input()

    while day != "Sunday" and day != "Monday" and day != "Tuesday" and day != "Wednesday" and day != "Thursday" and day != "Friday" and day != "Saturday" and day != "all":

        print('Invalid input. Please enter a valid day of the week or enter "all".')
        day=input()

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
    df=pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    

    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print("The most common month is ", most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    print("The most common day is ", most_common_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print("The most common hour is ", most_common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print("The most common Start Station is ", start_station)

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print("The most common End Station is ", end_station)

    # display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print("The most common combianation is ", combination)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    print("The total travel time was ", total_travel/60, " minutes")

    # display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print("The mean travel time was ", mean_travel/60 , " minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()

    print("The breakdown of user types is show below:\n", user_types)

    # Display counts of gender   
    if 'Gender' in df.columns:
          
          gender_types = df['Gender'].value_counts()
          print("\nThe breakdown of gender is show below:\n", gender_types)
          
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
          oldest_birth = int(df['Birth Year'].min())
          print('\nThe earliest year of birth was : ', oldest_birth)
          
          recent_birth =int(df['Birth Year'].max())
          print('The most recent year of birth was : ', recent_birth)
          
          common_birth = int(df['Birth Year'].mode()[0])
          print('The most common year  of birth was: ', common_birth)


    


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        start_loc = 0
        while (view_data.lower() == "yes"):
            print(df.iloc[start_loc:(start_loc+5)])
            start_loc += 5
            view_data = input("Do you wish to continue?: ").lower()
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break




if __name__ == "__main__":
    main()
