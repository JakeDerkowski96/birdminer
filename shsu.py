""" import modules """
import os, sys, subprocess, errno
from time import sleep
import pandas as pd
from pandas.io import sql
import sqlite3 as lite
import csv, re
import twint


''' global variables '''
# twint variable and initialize
c = twint.Config()
c.Hide_output = True
# variables used in gathering data
shsu_gps = "30.714279,-95.547366,3km"
spring_start = '2019-01-16'
spring_end = '2019-05-11'
# storage variables
dirName = "shsuSpring_2019study"
# dirName = "case-test"

rawDBfile = "birdminer.db"
info = 'case_study_report.txt'
word_list = ["drink", "drunk", "hungover", "hangover", "wasted",\
              "beer", "party", "byob", "bar", "club",\
               "weed", "high", "smoke", "stoned", "blazed", \
               "adderall", "vyvanse"]
# file imported as a list of stings
user_list = "user_list.csv"
tweet_list = 'tweet_list.csv'
# export the frequency of user's posts
num_tweets = "tweet_frequency.csv"

''' end of globals '''

def shsu_banner():
    banner = '''
                   ____  _         _ __  __ _
                  | __ )(_)_ __ __| |  \/  (_)_ __   ___ _ __
                  |  _ \| | '__/ _` | |\/| | | '_ \ / _ \ '__|
                  | |_) | | | | (_| | |  | | | | | |  __/ |
                  |____/|_|_|  \__,_|_|  |_|_|_| |_|\___|_|

            "BirdMiner: A user-friendly, forensic Twitter utility."
                Conducts a SHSU case study entirely on its own.

    Large computing power is necessary; to quit and save case study details:
           Enter (CTRL + C) now to quit -- saving case study details.


                BirdMiner will start digging in 3 seconds...
                '''

    print(banner)
    sleep(3)

# create the directory "shsu" where all data will be stored
def target_directory(dirName):
    os.chdir("project_files")
    try:
        os.mkdir(dirName)
        print("\nDirectory " + '"' + dirName + '"' +  " created. ")
    except FileExistsError:
        print("\nDirectory " + '"' + dirName + '"' + " already exists.")

    print(f"Moving to the {dirName} directory...")
    os.chdir(dirName)

# saves semester dates and criteria to verify against data collected
def back_info():
    intro = '''

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                    BIRDMINER: TWITTER DATA MINING AND REPORTING
                           CREATED BY:  JAKE DERKOWSKI
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                    INTRODUCTION
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Birdminer is a user-configurable program that allows the user to configure the
    way in which they would like to mine Twitter data. BirdMiner's different modes
    give the user efficiency for all search configurations; for all the parameters.

    This mode "birdminer.py --mode shsu" does not allow for configuration. Instead,
    it performs, conducts, and reports a case study on Sam Houston State University
    entirely on its own. For the conservation of computing power, the parameters in
    are reduced to allow for easy testing and presentation of the power Birdminer
    has.

    This case study shows the frequency in which students' posts contain keywords
    that indicate that they are "partying", or using drugs and/or drinking, and will
    be used to give a percentage approximation of the students that also partake in
    similar behaviors.

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                        BACKGROUND INFORMATION/DATA COLLECTION
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    There are only two search functions that collects all of the data that is user
    in this study. The main function that collects all of the raw data uses global
    positioning system (GPS) coordinates of Sam Houston State University as a focal
    point, then scraps all tweets posted during the 2019 spring semester that were
    posted within a 3 kilometer radius. This may limit the scope for BirdMiner by
    excluding those who commute to campus; however, it also returns a sample that is
    more concentrated of users that are actually students by capturing all of the
    tweets that were made on or near campus. This radius of searching is far more
    in- clusive then it initially sounds.

    This radius was calculated based on the distances from student living apartment
    complexes to campus. The distance from the Gateway apartments to campus was used
    in calculating the radius because this is the complex that is the furthest from
    campus but still provides a shuttle. This distance is 2.89km -- for simplicity
    the we use the rounded 3 kilometers.

    Sam Houston students (including those in graduate programs) equal to 20,938 -
    therefore, represent approximately 54.2% of Huntsville's population (38,548).
    With the given radius, the data collected should be primarily Sam Houston State
    students because most live near campus, and make up most of the population of
    the city.

    The data can also be further verified by the second function used by Birdminer.
    Birdminer export all of the data that was initially collected into a Database
    'birdminer.db' which stores all of the data in an organized and secure fashion
    (all data used in analysis will be drawn from this database). Birdminer selects
    all of the distinct users from the 'users' table and exports the list to a csv
    which the second function loops through and mines data for each user and then
    stored into the 'users' table. Queries executed on this table provides more
    certainty in verifying a user, but this will not be done for this program. This
    is not necessary because it has been shown that the data collected is reliable
    and this function takes a considerable amount of time to run. ***THIS FUNCTION
    DOES NOT RUN AUTOMATICALLY -- MUST BE UNCOMMENTED***


    Included within this directory will be the completed database file that
    Birdminer created, so mining has to be done to test this program. However, the
    results of a new search can possibly present different data analysis because
    data may removed/ added to twitter since time of original mining.

                                        ***sources cited at the end of document
        '''

    try:
        background_info = open(info, "w+")
        background_info.writelines(intro)
        background_info.close()
    except OSError as e:
        if e.errno != errno.EEXIST:
            background_info = open(info, "w+")
            background_info.writelines(intro)
            background_info.close()
            print('\nCreated "case_study_report.txt": detailed report and explanation.')
    except:
        print(f"Appending results to {info}.")

''' status/printing '''

def verbose_one():
        sleep(2)
        print("\nDONE.\n")
        sleep(1)
        print("Let the digging begin!")
        sleep(1)


''' data collection '''
# collect all tweets using GPS coordinates of SHSU
def gps_search(begin, end):
    c.Geo = shsu_gps
    c.Search = None
    c.Database = rawDBfile
    c.Since = begin
    c.Until = end
    c.Stats = True
    c.Count = True
    twint.run.Search(c)

# get files to be worked on from datab
def db_extract(rawDBfile):
    conn = lite.connect(rawDBfile)
    users = pd.read_sql_query("SELECT DISTINCT screen_name AS username \
                              FROM tweets GROUP BY screen_name, date;", conn)
    # used for profile lookup
    users.to_csv("user_list.csv", sep=",", header=None, index=False)

    tweets = pd.read_sql_query('SELECT tweet FROM tweets \
                                     ORDER BY screen_name, date;', conn)
    # used for analysis
    tweets.to_csv('tweet_list.csv', sep=',', header=None, index=None)


    tweets_freq = pd.read_sql_query("SELECT DISTINCT screen_name AS username, \
                                    Count(tweet) AS tweetsPosted FROM tweets \
                                    GROUP BY screen_name, date;", conn)
    tweets_freq.to_csv("tweet_frequency.csv", sep=",", index=False)

    users_num = len(users.index)
    tweets_num = len(tweets.index)

    return users_num, tweets_num

# list of usernames in strings for profile lookup
def user_ListData(user_list):
    with open(user_list) as f:
        users = f.readlines()
        # change [1:] to [:] if there is no header in csv file
    users = [x.strip() for x in users[:]]

    return users

# profile information
def lookup_profile(users):
    c.Hide_output = True
    c.Database = rawDBfile
    for u in users:
        user = u
        c.Username = user
        twint.run.Lookup(c)

# make raw tweet list
def create_tweet_df(rawDBfile):
    conn = lite.connect(rawDBfile)
    tweet_df = pd.read_sql_query('SELECT tweet\
                                 FROM tweets\
                                 ORDER BY screen_name, date;', conn)
    # tweetDFindex = tweet_df.to_csv('tweet_list.csv', sep=',')
    # for examination
    tweet_df.to_csv('tweet_list.csv', sep=',', header=None, index=None)

    return tweet_df

# import as variable
def tweet_ListData(tweet_list):
    with open(tweet_list) as f:
        tweets = f.readlines()
        # change [1:] to [:] if there is no header in csv file
    tweets = [x.strip() for x in tweets[:]]

    return tweets

def user_report(users, tweets):
    # connect to database file and query it using pandas
    conn = lite.connect(rawDBfile)
    # read query into a dataframe
    tweets_per_user = pd.read_sql_query("SELECT DISTINCT screen_name AS username, \
                                    Count(tweet) AS tweetsPosted FROM tweets \
                                    GROUP BY screen_name;", conn)
    tweets_per_user.to_csv("tweet_frequency.csv", sep=",", index=False)

    # variables for initial data analyis
    SHSU_students = 18416
    users_num = len(users)
    tweets_num = len(tweets)
    represent = round(users_num/SHSU_students*100, 2)
    tweet_p_user = int(tweets_num/users_num)
    sleep(2)
    res = f'''
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                   EXAMINATION
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        Data Summary of the Spring 2019 semester:

                {users_num} were used in this study
                {represent}% of the SHSU student population.

                Average post number: ~ {tweet_p_user};
                actual stored in: {num_tweets}

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
     '''
    print(res)
    sleep(3)
    try:
        examine = open(info, "a+")
        examine.writelines(res)
        examine.close()
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('\n"case_study_report.txt" gives detailed report the case study..')
    except:
        print(f"Appending results to {info}.")

def sources_case():
    sources = '''

    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                                   REFERENCES
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    1. Sam Houston State University GPS coordinates:
        https://www.findlatitudeandlongitude.com/?loc=Sam+Houston+State+University

    2. SHSU academic schedules & dates:
        https://www.shsu.edu/dept/registrar/calendars/academic-calendar.html

    3. SHSU campus size:
        https://www.usnews.com/best-colleges/sam-houston-state-3606

    4. Student population:
        https://www.collegetuitioncompare.com/edu/227881/sam-houston-state-university/enrollment/

    5. Huntsville population:
        https://suburbanstats.org/population/texas/how-many-people-live-in-huntsville

    6. twint module:
        https://github.com/twintproject/twint
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
'''

    try:
        ref = open(info, "a+")
        ref.writelines(sources)
        ref.close()
    except OSError as e:
        if e.errno != errno.EEXIST:
            print('The "case_study_report.txt":  detailed report and explanation.')
    except:
        print(f"Appending results to {info}.")


def main():
    ''' some lame user handling stuff'''
    shsu_banner()
    print("\nConfiguring environment to mine twitter...")
    sleep(2)
    # check shsu folder
    target_directory(dirName)
    sleep(2)
    # information for user saved in shsu dir
    back_info()

    verbose_one()

    print('\n\nData Collection:')
    print("\nDigging the tweets posted during Spring 2019 semester within 3 km from campus...\n")
    sleep(1)
    # gps_search(spring_start, spring_end)
    print(f"Data inserted into {rawDBfile} table:  'tweets'")
    sleep(1)
    # export queries to csv for  print of general info further investigation
    db_extract(rawDBfile)
    users = user_ListData(user_list)
    tweets = tweet_ListData(tweet_list)

    ''' UNCOMMENT THE FOLLOWING LINES TO RUN USER SEARCH'''
    sleep(1)
    print('\n***Skipping profile mining to save time...To run, uncomment in code.***\n')
    sleep(1)
    # iterates through the list of users and exports the profile information to db
    # print("\nDigging up profile information on these users...\n")
    # lookup_profile(users)
    # print(f"\nData inserted into {rawDBfile} table:  'users'\n")
    sleep(1)
    print("\nData Collection completed.\n\n")
    sleep(2)
    # finished with data collection


    print('\nBeginning analysis:')
    sleep(1)
    user_report(users, tweets)


    print('\nExtensive search through months of data:\n')
    print(f"""All tweets collected will now be scanned for a list of keywords;\nresults stored in: {info}:
              """)

    # seach through tweets for key words
    # word list to be searched
    wordlist = word_list
    tweets = tweets
    word_count = 0
    tweet_index = 0
    count = 0

    for tweet in tweets:
        tweet_index += 1
        for word in wordlist:
            s = re.search(word, tweet, re.I)
            # print(word, tweet)
            if s != None:
                word_count += 1
                final = f'''match: #{word_count}.'''
                print(final)
                # print(word_count)
                # word_count += 1
                count += 1
                element = s.group()
                res = f'''tweet index: {tweet_index} \t{word_count} contained: {element}\ntweet: {tweet}\n'''
                try:
                    save_data = open(info, "a+")
                    save_data.writelines(res)
                    save_data.close()
                    print(f'Saved results into {info}')
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        save_data = open(info, "a+")
                        save_data.writelines(res)
                        save_data.close()
                        print(f'Saved results into {info}')
                except:
                     print(f"Appending results to {info}.")


    sources_case()


main()
