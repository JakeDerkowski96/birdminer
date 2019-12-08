#!/usr/bin/python3
import os, sys, subprocess
import platform
import errno
import csv
from pandas import DataFrame, read_csv
import pandas as pd
import sqlite3
from sqlite3 import Error

import sqlite3 as lite
from sqlite3 import Error

project_dir = "project_files"

def welcome_view():
    print("""
                 ____  _         _ __  __ _
                | __ )(_)_ __ __| |  \/  (_)_ __   ___ _ __
                |  _ \| | '__/ _` | |\/| | | '_ \ / _ \ '__|
                | |_) | | | | (_| | |  | | | | | |  __/ |
                |____/|_|_|  \__,_|_|  |_|_|_| |_|\___|_|

  Dig and view the data that BirdMiner has collected --- this utility provides
  viewing the data in the terminal, the default application (per file type), or
  open a db file in a database browser. For more information: "help()" now.

            To continue with Birdminer, hit "Enter" now.
                  """)

def view_help():
    help = '''
    View mode is used to see and analyze the data that has been collected. When
    this mode is ran, it will automatically open to the project_folders directory
    and print the contents to choose from. You will simply type the directory in
    which you would like to explore, then chose the file and the method of viewing.

    This mode must be ran outside of the virtual environment if viewing in a system app

    Database files must either be used with option 2 or 3 becuase it cannot be
    printed to the terminal. It is recommended to use DB browser for SQLite to view
    all of the db files for it has been tested and is ensured to work.

              1. View in terminal
              2. View in default application
              3. Query a database file
              4. View the directory contents again/switch to sub-directory
              0. To exit

              '''
    print(help)
    print("This help screen will be saved in the 'Docs' of this main directory.")
    try:
        os.chdir("docs")
        help_doc = open("view_help.txt", "w")
        help_doc.writelines(help)
        sys.exit()
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Help document has succesfully been saved in the 'docs' folder.")
    except:
        print("File has already been created.")

# move to project_files
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

# print contents of current_dir
def dir_list():
    current_dir = os.getcwd()
    dir_ls = os.listdir(current_dir)
    print(*dir_ls, sep="\n")

    return list

def cd_dir():
    cd_dir = input("\nType the name of the directory you wish to view:  ")
    # pick dir to view
    try:
        os.chdir(cd_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("This directory does not exist.")
            raise
    # ls files in project
    print(f"\n{cd_dir}'s contents:\n")

    return dir

# print to terminal
def read_profile(file):
    df = pd.read_csv(file, usecols=["name", "username", "join_date", 'tweets', 'likes','following','followers'])
    print("\n")
    print(df)

# prints output from word searches -- tweets -- favorites
def read_CSV(file):
    df = pd.read_csv(file, usecols = ['date', 'username', 'name', 'tweet'])
    print(df)

def csv_read_as_is(file):
    df = pd.read_csv(file)
    print(df)

def read_smallcsv(file):
    df = pd.read_csv(file, usecols=['username'])
    print(df)

def db_connect(file):
    try:
        conn = sqlite3.connect(file)
        return conn
    except Error as e:
        print(e)

    return None

def db_display(file):
    word = input("Query word :  ")
    var = (word + "%")
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute("SELECT name, date, tweet FROM tweets")
    # c.execute("SELECT tweet FROM tweets WHERE tweet like ? and tweet = ?", ('%'+var+'%'))
    all_rows = c.fetchall()
    for rows in all_rows:
        print(rows)
    conn.close()

def error_file(file):
    try:
        print(f"{file} has been selected.")
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("File does not exist")

def application_open(file):
    if platform.system() == 'Windows':    # Windows
        os.startfile(file)
    else:                                   # linux variants
        subprocess.call(('xdg-open', file))


def main():
    project_dir = "project_files"

    welcome_view()
    cont = input(":  ")
    if cont == "help()":
        view_help()
        sys.exit()
    else:

            # move to prject_files
        project_files_ensure()
        # print(project_path)
        project_path = os.getcwd()
        print(f"\nProject Files: @ ({project_path})")
        # ls project-files
        dir_list()
        # cd
        cd_dir()

        dir_list()
        # user picks a file to view
        file = input("\nWhich file would you like to view?  :  ")
        try:
            print(f"{file} has been selected.")
        except OSError as e:
            if e.errno != errno.EEXIST:
                print("File does not exist")
                # add try agin
                raise

        file_action = input("""
            What would you like to do with this file?
            Enter the number:

              1. View in terminal
              2. View in default application
              3. Query a database file
              4. View the directory contents again/switch to subdirectory
              0. To exit

        :  """)

        if file_action == "1":
            if file == "profile_info.csv":
                read_profile(file)
            elif file == 'target_favorites.csv' or 'targets_tweets.csv':
                read_CSV(file)
            elif file == "target_IMPinfo.csv":
                csv_read_as_is(file)
            else:
                read_smallcsv(file)
            print("\n")
        elif file_action == "2":
            # print(file-path)
            application_open(file)
        elif file_action == "3":
            db_connect(file)
            db_display(file)
            # import query
        elif file_action == "4":
            cd_dir()
            dir_list()
            print("Would you like to view any of these files?")
            file = input(": ")
            action = input("""
                  1. terminal
                  2. application
                  3. Database table
                  0. exit birdminer
                  """)
            if action == "1":
                if file == "profile_info.csv":
                    read_profile(file)
                elif file == 'target_favorites.csv' or 'targets_tweets.csv':
                    read_CSV(file)
                elif file == "target_IMPinfo.csv":
                    csv_read_as_is(file)
                else:
                    read_smallcsv(file)
                    print("\n")
            elif action == "2":
                application_open(file)
            elif actions == "3":
                import query
                db_connect(file)
                db_display(file)
            elif action == "0":
                print("Closing birdminer.py.....")
                sys.exit()
            else:
                print("Error: invalid input")
                sys.exit()
        elif file_action == "0":
            print("Closing birdminer.py.....")
            sys.exit()
        else:
            print("Error: invalid input")
            sys.exit()

main()
