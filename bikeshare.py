#Adding a starting comment
#Refactoring commit
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
    print('*'*74)
    print('*'*15,'Welcome to Purity\'s data analysis platform','*'*15)
    print('*','\t'*2,'Let\'s explore some US bikeshare data!','\t'*2,'  *')
    print('*'*74)

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    #Here we will make use of numbers for the user choose against typing the words
    while True:
        c = int(input("Which city would you like to explore? (Choose a number)\n1. Chicago\n2. New York City\n3. Washington\nYour response: "))
        #city = city.lower()
        city = ['chicago', 'new york city', 'washington']
        if (not(c < 1 or c > 3)):
            city = city[(c-1)]
            break
        else:
            print("\nError!\nPlease select a number form the options provided.")

    # get user input for month (all, january, february, ... , june)
    while True:    
        m = int(input("Select the month option from below...\n0. All\n1. January\n2. February\n3. March\n4. April\n5. May\n6. June\nYour response: "))
        #month = month.lower()
        month = ['all','january', 'february', 'march', 'april', 'may', 'june']
        if not (m < 0 or m > 12):
            month = month[m]
            break
        else:
            print("\nError!\nPlease select a number form the options provided.")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        d = int(input("What day would you ike to view?\n0. All\n1. Monday\n2. Tuesday\n3. Wednesday\n4. Thursday\n5. Friday\n6. Saturday\n7. Sunday\nYour response: "))
        #day = day.lower()
        day = ['all','monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        if not (d < 0 or d > 7):
            day = day[d]
            break
        else:
            print("\nError!\nPlease select a number form the options provided.")
    print('-'*75)
    
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
     # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: ", df['month'].mode()[0], "\n")

    # display the most common day of week
    print("The most common day of week  is: ", df['day_of_week'].mode()[0], "\n")

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print("The most common start hour is: ", df['hour'].mode()[0])

    print("\nThis operation took %.8f seconds." % (time.time() - start_time))
    print('-'*75)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is ", df['Start Station'].mode()[0], "\n")

    # display most commonly used end station
    print("The most commonly used end station is ", df['End Station'].mode()[0], "\n")

    # display most frequent combination of start station and end station trip
    df['combination'] = df['Start Station'] + " " + df['End Station']
    print("The most frequent combination of start station and end station trip is: ", df['combination'].mode()[0])

    print("\nThis operation took %.8f seconds." % (time.time() - start_time))
    print('-'*74)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is", df['Trip Duration'].sum(), "\n")

    # display mean travel time
    print("The total mean time is", df['Trip Duration'].mean())

    print("\nThis operation took %.8f seconds." % (time.time() - start_time))
    print('-'*74)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby(['User Type'])['User Type'].count()
    print(user_types, "\n")
    if city != 'washington':
        # Display counts of gender
        gen = df.groupby(['Gender'])['Gender'].count()
        print(gen)
        # Display earliest, most recent, and most common year of birth
        recent = sorted(df.groupby(['Birth Year'])['Birth Year'], reverse=True)[0][0]
        earliest = sorted(df.groupby(['Birth Year'])['Birth Year'])[0][0]
        common = df['Birth Year'].mode()[0]
        print("The earliest year of birth is: ", earliest, "\n")
        print("The most recent year of birth is: ", recent, "\n")
        print("The most common year of birth is: ", common, "\n")

    print("\nThis operation took %.8f seconds." % (time.time() - start_time))
    print('-'*40)
    x = 1
    while True:
        raw = input('\nWould you like to see some raw data? Enter y or n.\n')
        if raw.lower() == 'y':
            print(df[x:x+5])
            x = x+5
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        print(f'Your selected options are: \nCity: {city}\nMonth: {month}\nDay of week: {day}\n')

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter y or n.\n')
        if restart.lower() != 'y':
            break

if __name__ == "__main__":
	main()
