import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'
}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of the week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # Get user input for city (chicago, new york city, washington)
    while True:
        city = input("Enter the city name (chicago, new york city, washington): ").strip().lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please enter a valid city name.")

    # Get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    while True:
        month = input("Enter the month (all, january, february, ... , june): ").strip().lower()
        if month in months:
            break
        print("Invalid input. Please enter a valid month.")

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Enter the day of the week (all, monday, tuesday, ... sunday): ").strip().lower()
        if day in days:
            break
        print("Invalid input. Please enter a valid day of the week.")

    print('-' * 40)
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

    # Convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month and day of the week
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # Filter by month if applicable
    if month != 'all':
        month_index = ['january', 'february', 'march', 'april', 'may', 'june'].index(month) + 1
        df = df[df['month'] == month_index]

    # Filter by day if applicable
    if day != 'all':
        df = df[df['day_of_week'].str.lower() == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print(f"Most Common Month: {common_month}")

    # Display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print(f"Most Common Day: {common_day}")

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].mode()[0]
    print(f"Most Common Start Hour: {common_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print(f"Most Common Start Station: {common_start_station}")

    # Display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print(f"Most Common End Station: {common_end_station}")

    # Display most frequent combination of start station and end station trip
    common_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    print(f"Most Common Trip: {common_trip[0]} to {common_trip[1]}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total Travel Time: {total_travel_time} seconds")

    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print(f"Mean Travel Time: {mean_travel_time} seconds")

    # print("\nThis took %s seconds." % (time.time() - start_time)
    # print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(f"User Types:\n{user_types}")

    # Display counts of gender (if available)
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"\nGender Counts:\n{gender_counts}")

    # Display earliest, most recent, and most common year of birth (if available)
    if 'Birth Year' in df.columns:
        earliest_birth = int(df['Birth Year'].min())
        most_recent_birth = int(df['Birth Year'].max())
        most_common_birth = int(df['Birth Year'].mode()[0])

        print(f"\nEarliest Birth Year: {earliest_birth}")
        print(f"Most Recent Birth Year: {most_recent_birth}")
        print(f"Most Common Birth Year: {most_common_birth}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()  
        df = load_data(city, month, day)  

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').strip().lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
