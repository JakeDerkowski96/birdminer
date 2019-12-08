''' Fetch Tweets using the search filters (Normal); '''
import twint
import os, sys
import errno
import datetime

def welcome_word():
    print("""
             ____  _         _ __  __ _
            | __ )(_)_ __ __| |  \/  (_)_ __   ___ _ __
            |  _ \| | '__/ _` | |\/| | | '_ \ / _ \ '__|
            | |_) | | | | (_| | |  | | | | | |  __/ |
            |____/|_|_|  \__,_|_|  |_|_|_| |_|\___|_|

  Dig through tweets for specific words given certain parameters which require
  only two parameters: begin/end date. For more information: "help()" now.

             To continue with Birdminer, hit "Enter" now.
                  """)
welcome_word()

def word_help():
    help = """
    Search mode is used when there is needed forensic investigation surround the
    use of a certain word or hashtag  --  rather it be around  a  specified area
    (including Geo  coordinates or near a city), if these word(s)  are  used  in
    conjunctions with  emails/phone numbers, or images/videos/both.  Ultimately,
    this  is used to determine  when/where/how certain key words are used  in  a
    simple; user-friendly manner.

        1. Dig:  all tweets that contain search-term.
        2. Dig:  search-term as a hashtag.
        3. Dig:  search-term + media(images/videos).
        4. Dig:  search-term + emails and/or phone #'s.
        5. Dig:  w/ search-term + GPS location.
        6. Dig:  search-term + general area (city).


    All files can either be saved to csv files by default, but are also prompted
    if a database file is also targeted. All files will be saved within the "word"
    directory in "project_files".

    """
    print(help)
    try:
        os.chdir("docs")
        help_doc = open("word-help.txt", "w")
        help_doc.writelines(help)

    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Help document has succesfully been saved in the 'docs' folder.")
    except:
        print("File has already been created.")
        sys.exit()
cont = input(":  ")
if cont == "help()":
    word_help()
    sys.exit()
# setup TWINT config variable
c = twint.Config()
# get search term, from user
word = str(input('\nEnter term which you would like to search by:  '))
word = word.lower()

print("Specify the timeframe in which you'd like the digging to take place!")
print('\tFormat: (YEAR-MM-DD)\t example: 2017-12-15 = December 15, 2017\n')
# time parameters
begin_date = input("Begin dig on: ")
end_date = input('Stop dig on:  ')


# global variables set --- must be includes on all digging methods
# twint configured variables
c.Search = word
c.Since = begin_date
c.Until = end_date



# make sure user is happy when their query
def Search_verification():
    print('\n\nYour search term is: ', word)
    print('Your search will begin on:  ' + begin_date + '.')
    print('Your Search will end on:  ' + end_date + '.')
    Search_check = input('\nIs this correct? Enter (y/n):  ')

    if Search_check == 'n':
        print("Please re-run BirdMiner.py --search to try again.")
        sys.exit(0)

# create a working directory -- cd to it"
def Search_directory(word):
    dirName = word
    os.chdir("project_files")
    try:
        os.makedirs(dirName)
        print("\nDirectory: " , dirName ,  " Created.\n")
    except FileExistsError:
        print("\nDirectory: " , dirName ,  " already exists.\n")

    print("Moving to the Search-term working directory...")
    os.chdir(dirName)
    # print(os.getcwd()) # prints working directory --
    # ensures filies are written to target's dir
    print("\n")

"""  the following functions have been set with a limit of 200 Tweets
         or entries for simplicity/test efficiency"""

# dig up all tweets that has the search term in it
''' #1 '''
def Search_term():
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = f"{word}_all.csv"
    c.Limit = 10
    c.Search = word
    c.Since = begin_date
    c.Until = end_date
    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        c.Database = None
    elif db == 'y':
        print(f'Your database will be saved as "{word}_all.db".')
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")

    twint.run.Search(c)
    print('Data collected has been saved under "all-w-search-term.csv"')

# dig for tweets that uses search term as a hashtag
''' #2 '''
def hashtag_word():
    c.Hide_output = True
    hashtag = '#' + word
    c.Store_csv = True
    c.Store_object = True
    c.Output = f"{word}_hashtags.csv"
    c.Limit = 10
    c.Search = hashtag
    c.Since = begin_date
    c.Until = end_date
    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        C.Database = None
    elif db == 'y':
        print(f'Your database will be saved as "{word}_hashtag.db".')
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")

    twint.run.Search(c)
    print('Data collected has been saved under "hashtag_only.csv"')

# dig for serch term where media (image/video) is part of tweet
''' #3 '''
def Search_media():
     c.Hide_output = True
     c.Store_csv = True
     c.Store_object = True
     c.Media = True
     c.Output = f"{word}_media.csv"
     # limit; where 1 = 20 post
     c.Limit = 10
     c.Search = word
     c.Since = begin_date
     c.Until = end_date
     db = input("""
       Save as a database file? Enter (y/n)

           """)
     if db == "n":
         c.Database = None
     elif db == 'y':
         print(f'Your database will be saved as "{word}_media.db".')
         c.Database = "tweets.db"
     else:
         c.Database = None
         print("Invalid entry; Birdminer will continue with default output.")

     twint.run.Search(c)
     print('Data collected has been saved under "Search-word_media.csv"')

# Digging up emails and phone #'s that have been associated with our Search-term
''' #4 '''
def Search_email_phone():
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Email = True
    c.Phone = True
    c.Output = "Search-Emails_phones.csv"
    c.Limit = 10
    c.Search = word
    c.Since = begin_date
    c.Until = end_date
    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        c.Database = None
    elif db == 'y':
        print(f'Your database will be saved as "{word}_contacts.db".')
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")

    twint.run.Search(c)
    print('Data collected has been saved under "Search-Emails_phones.csv"')

''' #5 '''
def Search_geo():
    # dig tweets that were posten at given geo-coordinalts
    user_geo = input("Enter your desired coordinates in the form: (lat,lon,km/mi.)\n :  ")
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = "Search_geo.csv"
    c.Limit = 200
    c.Geo = user_geo
    c.Search = word
    c.Since = begin_date
    c.Until = end_date
    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        c.Database = None
    elif db == 'y':
        print(f'Your database will be saved as "{word}_contacts.db".')
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")
    twint.run.Search(c)
    print('Data collected has been saved under "Search_geo.csv"')

# search by Search-term + near a location (city)
# example c.Search = 'baseball' c.Near = Houston
''' #6 '''
def Search_near_city():
    # dig tweet that are near a given city
    user_city = input("Enter a city name to dig tweets that contains your search-term:  ")
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = "Search_near-city.csv"
    c.Limit = 200
    c.Near = user_city
    c.Search = word
    c.Since = begin_date
    c.Until = end_date

    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        c.Database = None
    elif db == 'y':
        print(f'Your database will be saved as "{word}_near-city.db".')
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")

    twint.run.Search(c)
    print('Data collected has been saved under "Search_near_city.csv"')

def data_collection(methods):
    for i in methods:
            if i == 1:
                print('Digging for all tweets that include the search word...\n')
                Search_term()
                continue
            elif i == 2:
                print("\nDigging through all hashtags for matches with the Search-term...\n")
                hashtag_word()
                continue
            elif i == 3:
                print("\nDigging through tweets that have the search-term + media files...\n")
                Search_media()
                continue
            elif i == 4:
                print("Digging up emails and phone #'s that have been associated with our Search-term...\n")
                Search_email_phone()
                continue
            elif i == 5:
                print("\nDigging up the search-term around specific Geo-locations...\n")
                Search_geo()
                continue
            elif i == 6:
                print("Digging up the search-term tweets that were posted near a given city...\n")
                Search_near_city()
                continue
            elif methods == 0:
                print("Moving forward...")
                break

def Search_main():

    # prints search term to verifiy w/ user
    Search_verification()
    Search_directory(word)

    print("""
      What information would you like BirdMiner dig for?
      Enter number of the job you would like to perform:

      1. Dig:  all tweets that contain search-term.
      2. Dig:  search-term as a hashtag.
      3. Dig:  search-term + media(images/videos).
      4. Dig:  search-term + emails and/or phone #'s.
      5. Dig:  w/ search-term + GPS location.
      6. Dig:  search-term + general area (city).

      Enter '0' when you have completed your job list.""")

    # empty list to be filled in with user raw_input
    # enumerate through list -- executing each item in list's corresponding function
    methods = []
    raw_input = int(input("\nEnter first 'digsite':  "))

    while raw_input != 0:
        methods.append(raw_input)
        raw_input = int(input("Next digsite:  "))

    # handles user input and determines what methods/functions are to be called
    # based on the user's input


    data_collection(methods)

    print("""\nTO VIEW:
          run:  python3 birdminer.py --mode [view][query]

          view: to browse through the project project_files project_folder
          query: to export to database and perform searches that can be saved.
          """)

    sys.exit(0)


Search_main()
