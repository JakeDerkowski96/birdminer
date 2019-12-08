""" user configurated search """
# import all arguments
# print configure swarch screen w few variables printed to screen
# offer more options = print out all configureable options
# offer long config where all variable are asked one after another
# orgainze the questions strategically
    # the main options
    # the interesting options
    # how this would like to be saved/output

"""manuel search"""
import os, sys
import errno
import twint
from twint import config

project_dir = "project_files"

# basic welcome screen
def welcome():
    print("""
                   ____  _         _ __  __ _
                  | __ )(_)_ __ __| |  \/  (_)_ __   ___ _ __
                  |  _ \| | '__/ _` | |\/| | | '_ \ / _ \ '__|
                  | |_) | | | | (_| | |  | | | | | |  __/ |
                  |____/|_|_|  \__,_|_|  |_|_|_| |_|\___|_|

  Make your search as precise as you would like by specifying any/all of the
  configurable variables -- all of which can be viewed by typing: "help()" now.

      For Birdminer to assist you in your configuration hit: "Enter" now.
               """)

# make help menu
# def search config help screen
def search_config_help():
    options = """
This mode is the best for either large-scale and specific searches due to the
precision that it provides as well as the freedom. This can be used when digging
on a targeted user along with location/content parameters -- or search through
tweets between the years  2018-2019 in which contain certain words are were
posted from a certain city.

The possibilites are endless; configuration can be too specific - be careful not
to make them too broad either.

The following are the configurable variables for a user/manuel search. Use this
text document as reference while specifying search to avoid mistakes.

    Variable             Type       Description
--------------------------------------------
Username             (string) - Twitter user's username
Search               (string) - Search terms
Geo                  (string) - Geo coordinates (lat,lon,km/mi.)
Near                 (string) - Near a certain City (Example: london)
Output               (string) - Name of the output file.
Year                 (string) - Filter Tweets before the specified year.
Since                (string) - Filter Tweets sent since date, works only with twint.run.Search (Example: 2017-12-27).
Until                (string) - Filter Tweets sent until date, works only with twint.run.Search (Example: 2017-12-27).
Email                (bool)   - Set to True to show Tweets that _might_ contain emails.
Phone                (bool)   - Set to True to show Tweets that _might_ contain phone numbers.
Store_csv            (bool)   - Set to True to write as a csv file.
Store_json           (bool)   - Set to True to write as a json file.
Show_hashtags        (bool)   - Set to True to show hashtags in the terminal output.
Limit                (int)    - Number of Tweets to pull (Increments of 20).
Count                (bool)   - Count the total number of Tweets fetched.
Database             (string) - Store Tweets in a sqlite3 database. Set this to the DB. (Example: twitter.db)
To                   (string) - Display Tweets tweeted _to_ the specified user.
Images               (bool)   - Display only Tweets with images.
Videos               (bool)   - Display only Tweets with videos.
Media                (bool)   - Display Tweets with only images or videos.
Replies              (bool)   - Display replies to a subject.
Retweets             (bool)   - Display replies to a subject.
Hide_output          (bool)   - Hide output.
Get_replies          (bool)   - All replies to the tweet.
Popular_tweets       (bool)   - Scrape popular tweets, not most recent (default: False).
          """
    print(options)
    print("This help screen will be saved in the 'Docs' of this main directory.")
    try:
        os.chdir("docs")
        help_doc = open("search_config_help.txt", "w")
        help_doc.writelines(options)
        sys.exit()
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Help document has succesfully been saved in the 'docs' folder.")
    except:
        print("File has already been created.")

# ensure project file directory
def project_files_ensure():
    try:
        os.chdir(project_dir)
        project_path = os.getcwd()
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("""The default directory "project_files" does not exist.

                  One will be created -- this is the designated folder for projects.

                  Please replace your folder into this directory or birdminer WILL NOT
                  be able to access them, and will cause further, unpredictable issues.""")

            os.mkdir("project_files")

    return project_path

# create and move into the project folder
def config_directory(directory):
    try:
        os.mkdir(directory)
        print("Directory " , directory ,  " Created. ")
    except FileExistsError:
        print("Directory " , directory ,  " already exists.")

    print("Moving to the target's working directory...\n")
    os.chdir(directory)

def main():
    welcome()
    cont = input(":  ")
    if cont == "help()":
        search_config_help()
        sys.exit()
    else:
        # make sure there has been a project folder created
        project_files_ensure()
        directory = input("Enter the name of the folder you would like to save this in:\n")
        print("\n")
        # make directory to save the search
        config_directory(directory)

        # initialize c as config container for twint variables
        c = twint.config.Config()
        # what is the difference with this

        """
        c = twint.Config()
        """

        print("""If a configurable variable is denoted as "(boolean)" you must only Enter
              "True" if you want to include it in your search.
                             """)
        # main configuration
        c.Username = input("username:  ")
        if c.Username == "":
            c.Username = None
        c.To = bool(input("Tweets to target (boolean):  "))
        if c.To == "":
            c.To = None
        c.Retweets = bool(input("Retweets? (boolean):  "))
        if c.Retweets == "":
            c.Retweets = False
        c.Popular_tweets =  bool(input("Popular tweets? (boolean):  "))
        if c.Popular_tweets == "":
            c.Popular_tweets = False
        c.Replies = bool(input("Replies? (boolean):  "))
        if c.Replies == "":
            c.Replies = False
        c.Search = input("Word:  ")
        if c.Search == "":
            c.Search = None
        c.Show_hashtags = bool(input("hashtags? (boolean):  "))
        if c.Show_hashtags == "":
            c.Show_hashtags = False
        c.Geo = input("Geo coordinates (lat,lon,km/mi.):  ")
        if c.Geo == "":
            c.Geo = None
        c.Near = input("Search around a specific city:  ")
        if c.Near == "":
            c.Near = None

        print("\nNow for tweet-time parameteres\n")

        # search time parameters
        c.Year = input("Tweets only before year:  ")
        if c.Year == "":
            c.Year = None
        c.Since = input("Begin search on this date (ex. 2017-12-27)\n")
        if c.Since == "":
            c.Since = None
        c.Until = input("End search on this date (ex. 2017-12-27)\n")
        if c.Until == "":
            c.Until = None

        # content of tweets
        print("\n \n")
        c.Email = input("Dig tweets that may contain emails? (boolean)  ")
        if c.Email == "":
            c.Email = False
        c.Phone = input("Dig tweets that may contain phone numbers? (boolean)  ")
        if c.Phone == "":
            c.Phone = False
        c.Images = input("Dig tweets that may contain images (boolean)  ")
        if c.Images == "":
            c.Images = False
        c.Videos = input("Dig tweets that may contain videos (boolean)  ")
        if c.Videos == "":
            c.Videos = False
        c.Media = input("Dig tweets with both images and videos? (boolean)  ")
        if c.Media == "":
            c.Media = False

        # output of searches

        print("\nDeclare how you would like to output the data.\n")
        outvar = input("Would you like to save your output to file or print to the terminal?\n \
                       enter (save/print):  ")
        outvar = outvar.lower()
        if outvar == "print":
            c.Hide_output = False
        elif outvar == "save":
            c.Hide_output = True
            c.Database = input("Store as database file? (ex. twitter.db):  ")
            if c.Database == "":
                c.Database = None

            c.Output = input("Name of the file (string):  ")
            c.Store_csv = input("Store as csv? (boolean)  ")
            if c.Store_csv == "":
                c.Store_csv = False
            c.Store_json = input("Store as json? (boolean)  ")
            if c.Store_json == "":
                c.Store_json = False

        c.Count = input("Count the total number of tweets? (boolean)  ")
        if c.Count == "":
            c.Count = False
        # c.Limit = int(input("Set a limit to the number of tweets? (int)  "))
        # if c.Limit == int(""):
        #     c.Limit = None

        twint.run.Search(c)


main()
