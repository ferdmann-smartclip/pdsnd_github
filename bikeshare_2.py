import time
import pandas as pd
import numpy as np

CITY_DATA = { 'c': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'w': 'washington.csv' }

def get_safe_str_input(question, check, cont = True):
    answer = ''
    while cont == True:
        try:
            answer = str(input(question).lower())
            if answer in check.split('/'):
                cont = False
            else:
                print('Your Answer wasnt valid!')
        except ValueError:
            print('Your Answer wasnt valid!')
        except (KeyboardInterrupt, EOFError):
            print('Exiting... Thanks for using this tool! CU soon.')
            exit()
    return answer

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
    city = get_safe_str_input("Would you like to see data for Chicago, New York, or Washington? (c/ny/w)", "c/ny/w")

    # get user filter granularity (by month, day, or not at all)
    granularity = get_safe_str_input("Would you like to filter the data by month, day, both, or not at all? (m/d/b/na)", "m/d/b/na")
    if granularity == "m":
        # get user input for month (all, january, february, ... , june)
        months = ['j', 'f', 'mar', 'a', 'may', 'ju']
        month = get_safe_str_input("Which month - January, February, March, April, May, or June? (j/f/mar/a/may/ju)","j/f/mar/a/may/ju")
        month = months.index(month)+1
        day = -1
    elif granularity == "d":
        # get user input for day of week (all, monday, tuesday, ... sunday)
        dayofweek = ['m', 't', 'w', 'thu', 'f', 'sa', 'su']
        day = get_safe_str_input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? (m/t/w/thu/f/sa/su)","m/t/w/thu/f/sa/su")
        day = dayofweek.index(day)
        month = -1
    elif granularity == "b":
        # get user input for both month(all, january, february, ... , june) and day of week (all, monday, tuesday, ... sunday)
        months = ['j', 'f', 'mar', 'a', 'may', 'ju']
        month = get_safe_str_input("Which month - January, February, March, April, May, or June? (j/f/mar/a/may/ju)","j/f/mar/a/may/ju")
        month = months.index(month)+1
        dayofweek = ['m', 't', 'w', 'thu', 'f', 'sa', 'su']
        day = get_safe_str_input("Which day - Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, or Sunday? (m/t/w/thu/f/sa/su)","m/t/w/thu/f/sa/su")
        day = dayofweek.index(day)
    else:
        day = -1
        month = -1

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
    #print("DEBUG: Loading Data for {} and Month {} and Day {}".format(city, month, day))
    try:
        df = pd.read_csv(CITY_DATA[city])
    except:
        print("Oops: Cant load Datafile {}. Please check location. Bye.".format(CITY_DATA[city]))
        exit()

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week and hour from Start Time to create new columns
    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['day_of_week'] = pd.DatetimeIndex(df['Start Time']).dayofweek
    df['hour'] = pd.DatetimeIndex(df['Start Time']).hour

    if month != -1 and day == -1:
        df = df[df['month'] == month]
    elif day != -1 and month == -1:
        df = df[df['day_of_week'] == day]
    else:
        df = df[df['month'] == month]
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = df.groupby(['month']).size().idxmax()
    print("The most common month is {}.".format(months [common_month-1].title()))

    # display the most common day of week
    dayofweek = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    common_day = df.groupby(['day_of_week']).size().idxmax()
    print("The most common day is {}.".format(dayofweek[common_day].title()))

    # display the most common start hour
    common_hour = df.groupby(['hour']).size().idxmax()
    print("The most common hour is {}h.".format(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df.groupby(['Start Station']).size().idxmax()
    print("The most common start station is \'{}\'.".format(common_start_station))

    # display most commonly used end station
    common_end_station = df.groupby(['End Station']).size().idxmax()
    print("The most common end station is \'{}\'.".format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_combination_station = df.groupby(['Start Station','End Station']).size().idxmax()
    print("The most frequent combination of start station and end station is between \'{}\' and \'{}\'.".format(common_combination_station[0],common_combination_station[1]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    duration = df["Trip Duration"].sum()
    print("The total travel time is {} days, {} hours, {} minutes, {} seconds".format(int(duration/86400), int(int(duration%86400)/3600), int(int(int(duration%86400)%3600/60)),int(int(int(int(duration%86400)%3600%60)))))

    # display mean travel time
    mean = df["Trip Duration"].mean()
    print("The mean travel time is {} days, {} hours, {} minutes, {} seconds".format(int(mean/86400), int(int(mean%86400)/3600), int(int(int(mean%86400)%3600/60)),int(int(int(int(mean%86400)%3600%60)))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("The count of user types is {} subsribers and {} customers.".format(user_types['Subscriber'], user_types['Customer']))

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts(dropna = False)
        print("There are {} male, {} female and unknown {} users in the dataset.".format(gender_counts[0],gender_counts[2],gender_counts[1]))
    except:
        print("There is no gender information in the dataset.")

    # Display earliest, most recent, and most common year of birth
    try:
        common_birth_year = df.groupby(['Birth Year']).size().idxmax()
        print("The earliest birth year is {}, the most recent birth year is {} and the most common birth year is {}.".format(str(df['Birth Year'].min()).replace(".0",""), str(df['Birth Year'].max()).replace(".0",""), str(common_birth_year).replace(".0","")))
    except:
        print("There is no birth year information in the dataset.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_info(df):
    see_rows = get_safe_str_input("Would you like to see raw data? (y/n)","y/n")
    iterate = True
    row_num = 0;
    print('\n')
    if see_rows == "y":
        while iterate:
            print(df.iloc[row_num:row_num+5,])
            row_num +=5
            print('-'*40)
            see_more_rows = get_safe_str_input("Would you like to see 5 more rows of raw data? (y/n)","y/n")
            print('\n')
            if see_more_rows == "n" or df.size < row_num:
                iterate = False
    print('-'*40)

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_info(df)

        restart = get_safe_str_input("Would you like to restart? (y/n)","y/n")
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
