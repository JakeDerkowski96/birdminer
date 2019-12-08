import twint
import os, sys
import errno
from pandas import DataFrame, read_csv
import pandas as pd


def welcome_user():
    print("""
                 ____  _         _ __  __ _
                | __ )(_)_ __ __| |  \/  (_)_ __   ___ _ __
                |  _ \| | '__/ _` | |\/| | | '_ \ / _ \ '__|
                | |_) | | | | (_| | |  | | | | | |  __/ |
                |____/|_|_|  \__,_|_|  |_|_|_| |_|\___|_|

  Dig through a specific users tweets with some preconfigured search queries.
  of these include: digging bio info, all user tweets, follwers/following,
  favorites and more For more information: "help()" now.

             To continue with Birdminer, hit "Enter" now.
                  """)
welcome_user()

def user_help():
    help = """
    User mode is used when there is a target that has already been located; and
    general, but extensive data is desired to be dug up on them. The following
    are the preconfigured searches:

          1. Save the general profile info that was just displayed.
          2. Dig:  all target's tweets (including retweets).
          3. Dig:  targets Favorites.
          4. Dig:  targets followers.
          5. Dig:  users that the target follows.
          6. Dig:  info on users the target follows.
          7. Dig:  info on the users that follow the target.


    All files can either be saved to csv files by default, but are also prompted
    if  a  database file is also targeted. All  files will be saved  within  the
    "targets"   directory in "project_files".

    """
    print(help)
    try:
        os.chdir("docs")
        help_doc = open("user_help.txt", "w")
        help_doc.writelines(help)

    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Help document has succesfully been saved in the 'docs' folder.")
    except:
        print("File has already been created.")
        sys.exit()

cont = input(":  ")
if cont == "help()":
    user_help()
    sys.exit()

c = twint.Config()
target = input('Enter the username of the desired target: ')
target = target.lower()
c.Username = target
# get target from user



def to_view():
    view_info = """
        run:   --mode [view][query]

        view: to browse through the project project_files project_folder
        query: to export to database and perform searches that can be saved.
        """

    print(view_info)
    print("\nThank you for using birdminer!")

def target_directory(target):
    dirName = target
    os.chdir("project_files")
    try:
        os.mkdir(dirName)
        print("Directory " , dirName ,  " Created. ")
    except FileExistsError:
        print("Directory " , dirName ,  " already exists")

    print("Moving to the target's working directory...\n")
    os.chdir(dirName)
    # print(os.getcwd()) # prints working directory -- ensures filies are written to target's dir


def target_verification():
    # c.Username = target
    print('This is the profile that we dug up:\n')
    twint.run.Lookup(c)
    target_check = input('Does this appear to be the correct target?\n\nEnter (y/n):  ')
    print("\n")

    if target_check == 'n':
        print("Please make sure you have the correct username, re-run BirdMiner to try again")
        sys.exit(0)

"""#1.1"""
# profile information
def lookup_profile():
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = "profile_info.csv"
    c.Username = target


    print("Data collected has been saved under profile_info.csv:\n")
    twint.run.Lookup(c)

"""  the following functions have been set with a limit of 200 Tweets
         or entries for simplicity/test efficiency"""

"""#1"""
# profile information used for grouping of sample
def profile_bio():
    all = "profile_info.csv"
    simple = "target_IMPinfo.csv"
    df = pd.read_csv(all, usecols = ["id", "name", "location", "bio", "verified"])
    export = df.to_csv(simple, index = None, header = True)
    print(export)

"""#2"""
# get all tweets
def tweets(target):
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = "targets_tweets.csv"
    c.Limit = 200
    c.Username = target
    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        C.Database = None
    elif db == 'y':
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")


    twint.run.Profile(c)
    print('Data collected has been saved under "targets_tweets.csv"')

"""#3"""
# targets favorites
def favorites(target):
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = "targets_favorites.csv"
    c.Limit = 200
    c.Username = target
    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        C.Database = None
    elif db == 'y':
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")


    twint.run.Favorites(c)
    print('Data collected has been saved under "targets_favorites.csv"')

"""#4"""
# followers of target
def followers(target):
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = "targets_followers.csv"
    c.Limit = 200
    c.Username = target
    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        C.Database = None
    elif db == 'y':
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")


    twint.run.Followers(c)
    print('Data collected has been saved under "targets_followers.csv"')

"""#5"""
# who the target follows
def following(target):
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = "target_following.csv"
    c.Limit = 200
    c.Username = target
    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        C.Database = None
    elif db == 'y':
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")

    twint.run.Following(c)
    print('Data collected has been saved under "target_following.csv"')

"""#6"""
# grab following info
def following_info(target):
    c.Username = target
    c.User_full = True
    c.Hide_output = True
    # c.Format = "Username: {username} | Bio: {bio} | Location: {location} | Url: {url}"
    c.Store_csv = True
    c.Store_object = True
    c.Output = "following_info.csv"

    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        c.Database = None
    elif db == 'y':
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")

    twint.run.Following(c)

"""#7"""
# grab following info
def followers_info(target):
    c.Username = target
    c.User_full = True
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = "followers_info.csv"

    db = input("""
      Save as a database file? Enter (y/n)

          """)
    if db == "n":
        c.Database = None
    elif db == 'y':
        c.Database = "tweets.db"
    else:
        c.Database = None
        print("Invalid entry; Birdminer will continue with default output.")

    twint.run.Followers(c)


''' the save variable is a test for collecting like-users and grouping them
based on information in their biography'''

def data_collection(jobs):
    for i in jobs:
            if i == 1:
                save = input('''Save all data? or Save minimum? (used for grouping users) \
                      \nEnter "min" to save the grouping data; else all data will be saved. \
                      \n:  ''')
                if save == "min":
                    lookup_profile()
                    profile_bio()
                    print("Saved as target_IMPinfo.csv")
                    continue
                else:
                    print('\nSaving general profile info...\n')
                    lookup_profile()
                    continue
            elif i == 2:
                print("\nDigging up all tweets + retweets from target's profile...\n")
                tweets(target)
            elif i == 3:
                print("\nDigging up the target's favorites...\n")
                favorites(target)
                continue
            elif i == 4:
                print("\nDigging up all of the users following the target...\n")
                followers(target)
                continue
            elif i == 5:
                print("\nDigging up all the users the target follows...\n")
                following(target)
                continue
            elif i == 6:
                print("\nDigging infomation of those the target follows...")
                following_info(target)
            elif i == 7:
                print("\nDigging infomation on the target's folllowers...")
                followers_info(target)
            elif jobs == 0:
                print(f"\nData has been saved '{target}' folder.")
                print("birdminer can also be used to view/query these files:")

""" FIX IndexError OUTPUT TO TERMINAL """

def user_mode_main():

        target_verification()

        # create directory for the given target
        target_directory(target)
        '''     #!!! or move to existing directory for the given target !!!# '''

        # main profile scraps
        print("""

      What information would you like BirdMiner dig for?
      Enter number of the job you would like to perform:

      1. Dig:  profile info (all/some of displayed info)
      2. Dig:  all target's tweets (including retweets).
      3. Dig:  favorites.
      4. Dig:  followers.
      5. Dig:  users that the target follows.
      6. Dig:  info on users the target follows.
      7. Dig:  info on the users that follow the target.

      Enter '0' when you have completed your job list.
      """)

        # empty list to be filled in with user raw_input
        # enumerate through list -- executing each item in list's corresponding function
        jobs = []
        raw_input = int(input("Enter first 'digsite':  "))
        while raw_input != 0:
            jobs.append(raw_input)
            raw_input = int(input("Next digsite:  "))

        # handles user input and executes their desired functions
        data_collection(jobs)

        print("""\n\nTO VIEW:
              run:  python3 birdminer.py --mode [view][query]

              view: to browse through the project project_files project_folder
              query: to export to database and perform searches that can be saved.
              """)

        sys.exit(0)

'''run user mode'''
user_mode_main()
