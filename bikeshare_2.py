import time
import pandas as pd
import numpy as np
import sys
import os.path
from os import path

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

print('*'*80)
print('\nHello! This program aims to explore data related to bike share systems for three major cities')
print('in the United States — Chicago, New York City, and Washington.')
print('-'*40)
print('\nBefore we proceed, lets check if you have the data (.csv files) for the respective cities we intend to explore\n')
print('-'*10)
print('-'*20)
print('-'*40)
print('-'*60)

# to check if required files (for analysis) exists in the current working directory
if path.exists('chicago.csv') == True and path.exists('new_york_city.csv') == True and path.exists('washington.csv') == True:
    print("\n**********Great!!! files for this analysis are in place**********\n")
else:
    print("File not accessible")
    print("Please ensure you have the following files in your current working directory and then try again")
    print("chicago.csv\nnew_york_city.csv\nwashington.csv\n")
    print("if you do not have this files and you would like to download them, please use the link below\n")
    print("https://drive.google.com/file/d/1Bzi0Mm9fz0CwcMbJi9JbQw0Jc3XJ7pmc/view?usp=sharing\n")
    sys.exit("********The program has exited successfuly********")

def get_filters():
    while True:
        """
        Asks user to specify a city, month, and day to analyze.

        Returns:
            (str) city - name of the city to analyze
            (str) month - name of the month to filter by, or "all" to apply no month filter
            (str) day - name of the day of week to filter by, or "all" to apply no day filter
        """
        print('. '*20)
        print('Let\'s explore some US bikeshare data!')
        # get user input for city (chicago, new york city, washington).
        while True:
            print('. '*10)
            print('what city are we exploring? ')
            city  = input("would you like to explore chicago, new york city or washington? ").lower()
            city_val = ('chicago', 'new york city', 'washington')
            if city not in city_val:
                print()
                print("Sorry, I didn't understand that, kindly check your input and try again")
                print('. '*10)
                check = input("Please type YES to try again or type any other value to exit this program:  ")
                if check.lower()  != 'yes':
                    sys.exit("********The program has been exited successfuly********")
            else:
                break

        # get user input for month (all, jan, feb, mar, apr, may or jun)
        while True:
            print('. '*10)
            print('Would you like to filter data by month?')
            month = input("Which month? jan, feb, mar, apr, may or jun? (Type 'all' for no month filter): ").lower()
            month_val = ('all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun')
            if month not in month_val:
                print()
                print("Sorry, I didn't understand that, kindly check your input and try again")
                print('. '*10)
                check = input("Please type YES to try again or type any other value to exit this program:  ")
                if check.lower()  != 'yes':
                    sys.exit("********The program has been exited successfuly********")
            else:
                break

        # get user input for day of week (all, mon, tue, wed, thur, fri, sat or sun)
        while True:
            print('. '*10)
            print('Would you like to filter data by day of the week?')
            day = input("Which day? mon, tue, wed, thur, fri, sat or sun? (Type 'all' for no day filter): ").lower()
            day_val = ('all', 'mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun')
            if day not in day_val:
                print()
                print("Sorry, I didn't understand that, kindly check your input and try again")
                print('. '*10)
                check = input("Please type YES to try again or type any other value to exit this program:  ")
                if check.lower()  != 'yes':
                    sys.exit("********The program has been exited successfuly********")
            else:
                break

        # to display summary of input data, and confirm whether to continue of restart
        print('-'*40)
        print('Based on your input, see the details of data we are about to analyse\n')
        print('City: {}\nMonth: {}\nDay of the Week: {}'.format(city.title(),month.title(),day.title()))
        restart_filter = input('\nType YES to continue or type NO to restart.\n').lower()
        if restart_filter == 'yes':
            break
        
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
    df  = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month # The month as January=1, December=12.
    df['day_of_week'] = df['Start Time'].dt.dayofweek # The day of the week with Monday=0, Sunday=6
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'all':
        months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun')
        month = months.index(month) + 1
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        days = ('mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun')
        day = days.index(day)
        df = df[df['day_of_week'] == day] 

    return df


def fill_missing_values(df):
    """
    This function iterates through every coloumn in the data to detect missing values
    if missing value is found in any coloumn, this function also deals with the missing values
    based on the data type of the coloumn

    """
    print("Checked for missing values ...............")
    for i in range(1, df.columns.size):
        if df[df.columns[i]].isnull().sum() > 0:
            print('\nmissing values found in column:', df.columns[i])
            dtype = df[df.columns[i]].dtype
            if dtype == 'float' or dtype == 'int':
                print('we used the backward filling (backfill) method to replace missing values')
                df[df.columns[i]].fillna(method = 'backfill', axis = 0, inplace = True)
            else:
                print("we replaced missing values with 'not specified'")
                df[df.columns[i]].fillna('not specified', inplace = True)
    check = input("\nPlease type YES to continue or type any other value to exit this program:  ")
    if check.lower()  != 'yes':
        sys.exit("********The program has been exited successfuly********")

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if df['month'].unique().size > 1:
        popular_month = df['month'].mode()[0]
        count = df['month'].value_counts()[popular_month]
        months = ('jan', 'feb', 'mar', 'apr', 'may', 'jun')
        popular_month = months[popular_month - 1]
        print('The popular month is: {}, Count: {}'.format(popular_month.title(),count))

    # display the most common day of week
    if df['day_of_week'].unique().size > 1:
        popular_day = df['day_of_week'].mode()[0]
        count = df['day_of_week'].value_counts()[popular_day]
        days = ('mon', 'tue', 'wed', 'thur', 'fri', 'sat', 'sun')
        popular_day = days[popular_day]
        print('The popular day of the week is: {}, Count: {}'.format(popular_day.title(),count))

    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    count = df['hour'].value_counts()[popular_hour]
    print('The popular hour of the day is: {}, Count: {}'.format(popular_hour,count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    count = df['Start Station'].value_counts()[popular_start_station]
    print('The most commonly used start station: {}, Count: {}'.format(popular_start_station,count))

    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    count = df['End Station'].value_counts()[popular_end_station]
    print('The most commonly used end station: {}, Count: {}'.format(popular_end_station,count))

    # display most frequent combination of start station and end station trip
    df['Start_End_Trip'] = '('+ df['Start Station'] + ') TO (' + df['End Station'] + ')'
    popular_trip = df['Start_End_Trip'].mode()[0]
    count = df['Start_End_Trip'].value_counts()[popular_trip]
    print('The most frequent combination of start & end station trip: {}, Count: {}'.format(popular_trip,count))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = np.sum(df['Trip Duration'])
    print('The total travel time: {} secs'.format(total_travel_time))

    # display mean travel time
    mean_travel_time = np.mean(df['Trip Duration'])
    print('The average travel time: {} secs'.format(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('counts of user types:\n', df[['User Type']].value_counts())

    # Display counts of gender
    if 'Gender' in df.columns:
        print()
        print()
        print('counts of gender: \n', df[['Gender']].value_counts())

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print()
        print()
        print('earliest year of birth: ' , df['Birth Year'].min())
        print('most recent year of birth: ' , df['Birth Year'].max())
        print('common year of birth: ' , df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def gender_trip_duration_stats(df):
    """
    Displays addtional statistics on bikeshare users.
    Trip duration stats, by gender
    """
    
    print('\nCalculating User Stats...')
    start_time = time.time()
    if 'Gender' in df.columns:
        print('Gender-Trip duration stats')
        print()
        df_male = df[df['Gender'] == 'Male']
        total_travel_time_male = np.sum(df_male['Trip Duration'])
        mean_travel_time_male = np.mean(df_male['Trip Duration'])
        max_travel_time_male = df_male['Trip Duration'].max()
        min_travel_time_male = df_male['Trip Duration'].min()
        print("Male Stats")
        print("Total travel time - Male: ", total_travel_time_male, 'secs')
        print("Mean travel time - Male: ", mean_travel_time_male, 'secs')
        print("Maximum travel time - Male: ", max_travel_time_male, 'secs')
        print("Minimum travel time - Male: ", min_travel_time_male, 'secs')

        print()
        df_female = df[df['Gender'] == 'Female']
        total_travel_time_female = np.sum(df_female['Trip Duration'])
        mean_travel_time_female = np.mean(df_female['Trip Duration'])
        max_travel_time_female = df_female['Trip Duration'].max()
        min_travel_time_female = df_female['Trip Duration'].min()
        print("Female Stats")
        print("Total travel time - Female: ", total_travel_time_female, 'secs')
        print("Mean travel time - Female: ", mean_travel_time_female, 'secs')
        print("Maximum travel time - Female: ", max_travel_time_female, 'secs')
        print("Minimum travel time - Female: ", min_travel_time_female, 'secs')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def staion_user_type_stats(df):
    """
    Displays most frequent combination of start station and end station trip by user type
    """

    print('\nCalculating User Stats...')
    start_time = time.time()

    df['Start_End_Trip'] = '('+ df['Start Station'] + ') TO (' + df['End Station'] + ')'
    print('Most frequent combination of start station and end station trip by user type')
    print()
    subscriber = df[df['User Type'] == 'Subscriber']
    popular_trip_subscriber = subscriber['Start_End_Trip'].mode()[0]
    count = subscriber['Start_End_Trip'].value_counts()[popular_trip_subscriber]
    print('The most frequent combination of start & end station trip for subscribers: {}, Count: {}'.format(popular_trip_subscriber,count))

    print()
    customer = df[df['User Type'] == 'Customer']
    popular_trip_customer = customer['Start_End_Trip'].mode()[0]
    count = customer['Start_End_Trip'].value_counts()[popular_trip_customer]
    print('The most frequent combination of start & end station trip for customers: {}, Count: {}'.format(popular_trip_customer,count))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_raw_data(df):
    view_df = input('\nWould you like to view the bikeshare data? Type yes or no.\n')
    if view_df.lower()  == 'yes':
        print(df[0:5])
        view_more = input('\nWould you like to view more data? Type yes or no.\n')
        if view_more.lower() == 'yes':
            i = 5
            while i <= df.size and view_more.lower() == 'yes':
                print(df[i:i+5])
                i += 5
                view_more = input('\nWould you like to view more data? Type yes or no.\n')


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        df = fill_missing_values(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        gender_trip_duration_stats(df)
        staion_user_type_stats(df)
        view_raw_data(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
