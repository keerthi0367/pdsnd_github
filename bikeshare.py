import time
import pandas as pd
import numpy as np

CITY_DATA = { 
    'chicago': 'chicago.csv',
    'new york city': 'new_york_city.csv',
    'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify  month, and day to analyze.

    Returns:
        city (str): name of the city to analyze
        month (str): month name to filter by, or "all"
        day (str): day of week to filter by, or "all"
    """
    print("Hello! Let's explore some US bikeshare data!")

    # ----- Get user input for city -----
    while True:
        city = input("Choose a city (Chicago, New York City, Washington): ").strip().lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please try again.\n")

    # ---- Get user input for month -----
    valid_months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    while True:
        month = input("Choose a month (January–June) or 'all': ").strip().lower()
        if month in valid_months:
            break
        else:
            print("Invalid month. Please try again.\n")

    # ----- Get user input for day -----
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
    while True:
        day = input("Choose a day of week or 'all': ").strip().lower()
        if day in valid_days:
            break
        else:
            print("Invalid day. Please try again.\n")

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the chosen city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])

    # Convert Start Time to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Extract month, day_of_week, and hour
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # Filter by month
    if month != 'all':
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month_num = months_list.index(month) + 1
        df = df[df['month'] == month_num]

    # Filter by day
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    print("Most common month:", df['month'].mode()[0])
    print("Most common day of week:", df['day_of_week'].mode()[0])
    print("Most common start hour:", df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print("Most commonly used start station:", df['Start Station'].mode()[0])
    print("Most commonly used end station:", df['End Station'].mode()[0])

    df['trip_combo'] = df['Start Station'] + " → " + df['End Station']
    print("Most frequent trip:", df['trip_combo'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    print("Total travel time:", df['Trip Duration'].sum())
    print("Average travel time:", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # User type counts
    print("User Types:")
    print(df['User Type'].value_counts(), "\n")

    # Gender (Only available for Chicago & NYC)
    if 'Gender' in df.columns:
        print("Gender Counts:")
        print(df['Gender'].value_counts(), "\n")
    else:
        print("Gender data not available for this city.\n")

    # Birth year stats (Only Chicago & NYC)
    if 'Birth Year' in df.columns:
        print("Earliest birth year:", int(df['Birth Year'].min()))
        print("Most recent birth year:", int(df['Birth Year'].max()))
        print("Most common birth year:", int(df['Birth Year'].mode()[0]))
    else:
        print("Birth year data not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def display_raw_data(df):
    """Displays raw data 5 rows at a time upon user request."""
    i = 0
    while True:
        show = input("Would you like to see 5 rows of raw data? yes/no: ").strip().lower()
        if show == 'yes':
            print(df.iloc[i:i + 5])
            i += 5
            if i >= len(df):
                print("No more data to display.")
                break
        elif show == 'no':
            break
        else:
            print("Please enter 'yes' or 'no'.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
    

