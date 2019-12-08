# search a targets tweets for a specific word
import twint
import os, sys
import errno

def welcome_user_mode():
    print("""
                 ____  _         _ __  __ _
                | __ )(_)_ __ __| |  \/  (_)_ __   ___ _ __
                |  _ \| | '__/ _` | |\/| | | '_ \ / _ \ '__|
                | |_) | | | | (_| | |  | | | | | |  __/ |
                |____/|_|_|  \__,_|_|  |_|_|_| |_|\___|_|

    Dig through a targeted user's twitter account for a specific word.
    For more information: "help()" now.

         To continue with Birdminer, hit "Enter" now.
                  """)
welcome_user_mode()

def user_word_help():
    help = """
    This is nothing other than a combination of the "user" and "word" modes this
    is useful for running a quick search of a target (which is already known) to
    search through their tweets and retweets for a specific word.

    This is a very general mode of searching and should be used primarily as a
    method of checking data collected or in verifying parameters to be used in a
    larger/wider search.

    """
    try:
        os.chdir("docs")
        help_doc = open("user_word-help.txt", "w")
        help_doc.writelines(help)

    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Help document has succesfully been saved in the 'docs' folder.")
    except:
        print("File has already been created.")
        sys.exit()

cont = input(":  ")
if cont == "help()":
    user_word_help()
    sys.exit()


c = twint.Config()
# get target from user
target = input('Enter the username of the desired target: ')
target = target.lower()
# get search term, from user
word = str(input('Enter term which you would like to search by:  '))
word = word.lower()
c.Username = target
c.Search = word
# c.Since = begin_date
# c.Until = end_date


# create the directory where files will be saved
def combo_directory(target, word):
    target_dir = target
    word_search = word
    # SEARCHdir = user_dir + word_search
    # target user directory
    os.chdir("project_files")
    try:
        os.makedirs(target_dir)
        print("\nDirectory: " , target_dir,  " Created.\n")
    except FileExistsError:
        print("\nDirectory: " , target_dir ,  " already exists\n")
    # CD to the targeted user
    os.chdir(target_dir)
    print(f"Digging through {target} for {word}...")

# verify search with user
def combo_verification():
    print('\n\nYour search term is: ', word)
    # print('Your search will begin on:  ' + begin_date + '.')
    # print('Your Search will end on:  ' + end_date + '.')
    print('\nFor the following profile:\n')
    twint.run.Lookup(c)

    Search_check = input('Is this correct? Enter (y/n):  ')

    if Search_check == 'n':
        print("Please re-run BirdMiner.py mode -combo to try again.")
        sys.exit(0)

"""  the following functions have been set with a limit of 200 Tweets
         or entries for simplicity/test efficiency"""

# make the search
def combo_search():
    c.Hide_output = True
    c.Store_csv = True
    c.Store_object = True
    c.Output = f"{word}.csv"
    c.Limit = 200
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


    twint.run.Search(c)

    print(f'Data collected has been saved under "{word}.csv"\n')

def combo_main():

    combo_verification()
    combo_directory(target, word)

    combo_search()

    print("""TO VIEW:
          run:  python3 birdminer.py --mode [view][query]

          view: to browse through the project project_files project_folder
          query: to export to database and perform searches that can be saved.
          """)
    sys.exit(0)

combo_main()
