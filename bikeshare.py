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
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while city not in CITY_DATA:
        city = input('Specify the city you would like to look at: Chicago, New York City or Washington?').lower()

    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    month_day = input('Would you like to filter by month or by day? Type "m" for month or "d" for day').lower()

    if month_day == 'm':
        month = None
        months = ['all', 'january', 'febuary', 'march', 'april', 'may', 'june']
        while month not in months:
            month = input('Which month would you like to look at? All, January, Febuary, March, April, May or June?').lower()
        day = 'all'
    elif month_day == 'd':
        day = None
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        while day not in days:
            day = input('Which day would you like to look at? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday?').lower()
        month = 'all'
    else:
        print('Ooops. Your selection is not valid. Please try again.')


    # print statement for checks
    #print(city, month, day)
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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month']==month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week']==day.title()]

    return df


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Display the most common month only if not filtered by month
    months = ['january', 'febuary', 'march', 'april', 'may', 'june']
    if month not in months:
        popular_month = df['month'].mode()[0]
        print('The most popular month was: {}'.format(popular_month))


    # Display the most common day of week only if not filtered by day
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    if day in days:
        popular_day = df['day_of_week'].mode()[0]
        print('The most popular day of the week was: {}'.format(popular_day))

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular hour of the day to start a ride was: {}'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most popular start station was: {}'.format(popular_start_station))

    # Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most popular end station was: {}'.format(popular_end_station))

    # Display most frequent combination of start station and end station trip
    frequent_combo = df.groupby(['Start Station', 'End Station']).size().idxmax()
    frequent_combo_start = frequent_combo[0]
    frequent_combo_end = frequent_combo[1]
    print('The most frequent combination of start and end station was: Start from {} to {}'.format(frequent_combo_start, frequent_combo_end))


    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time in days, hours and minutes; neglects seconds
    total_travel_secs = df['Trip Duration'].sum()
    days = total_travel_secs // (60*60*24)
    hours_rest = total_travel_secs - (days*60*60*24)
    hours = hours_rest // (60*60)
    minutes_rest = total_travel_secs - (days*60*60*24) - (hours*60*60)
    minutes = minutes_rest // 60
    print('Total travel time wasm approx. {} days, {} hours and {} minutes and (probably a few seconds)'.format(days, hours, minutes))

    # Display mean travel time in minutes and seconds
    mean_travel = df['Trip Duration'].mean()
    mean_minutes = int(mean_travel // 60)
    mean_seconds = int(mean_travel - mean_minutes*60)
    print('The average trip duration was {} minutes and {} seconds.'.format(mean_minutes, mean_seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))

    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    num_user_types = df['User Type'].nunique()
    user_types = df['User Type'].value_counts()
    print('There a {} user types: \n{}'.format(num_user_types, user_types))

    # Display counts of gender with the exception of the Washington dataset
    if city != 'washington':
        num_gender = df['Gender'].nunique(dropna=False)
        gender = df['Gender'].value_counts(dropna=False)
        print('There a {} genders: \n{}'.format(num_gender, gender))

    # Display earliest, most recent, and most common year of birth
        first_birth = int(df['Birth Year'].min())
        last_birth = int(df['Birth Year'].max())
        common_birth = int(df['Birth Year'].mode())
        print('The oldest customer was born in {}, the youngest customer was born in {} and most customers were born in {}'.format(first_birth, last_birth, common_birth))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)




def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        details = input('Would you like to see details of the dataset? Please type "y" or "n"')
        if details == 'y':
            for i in range(0, len(df), 5):
                if details == 'y':
                    start = i
                    end = start + 5
                    print(df.iloc[start:end])
                    details = input('Would you like to see details of the dataset? Please type "y" or "n"')
                else:
                    break

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
