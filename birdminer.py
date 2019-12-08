#!/usr/bin/env python3
'''
"BirdMiner: A user-friendly, forensic Twitter utility."

This module contains the power to search specific words, hashtags,
users and all of the info on their profiles; easy. -- does not use Twitter's API,
therefore never a need to login. Free scraping for everyone -- w/o limitations!

'''

import os
import sys, errno
import argparse
from argparse import ArgumentParser, RawDescriptionHelpFormatter
import platform
import twint

module_name = "BirdMiner: An user-friendly, forensic Twitter utility."
__version__ = "1.0.0"

# prints banner
def banner():
    BANNER = """
                                               ++++++++++++++++++++++++++++++++
  ____  _         _ __  __ _                   ++++++++++++++++++/:....-:+++//+
 | __ )(_)_ __ __| |  \/  (_)_ __   ___ _ __   ++:`:++++++++++++.        `` .++
 |  _ \| | '__/ _` | |\/| | | '_ \ / _ \ '__|  ++.   -/++++++++.           ``-+
 | |_) | | | | (_| | |  | | | | | |  __/ |     ++:      .-:/+++            .+++
 |____/|_|_|  \__,_|_|  |_|_|_| |_|\___|_|     ++/:`          `            -+++
                                               +o-                         /+++
    Twitter Forensics and Data Mining:         oo+-                       .oooo
     Jake Derkowski & Chris Aboshear           oooo/-`                   `+oooo
                                               oooo+`                   .+ooooo
          COSC 4340 -- Dr. Frank               oooooo/.`               :ooooooo
                                               ooooooo+:.            -+oooooooo
    USAGE: python3 birdminer.py --how          o+:-.`            `-/ooooooooooo
                                               oooo+/:-.....--:/+oooooooooooooo

            """
    print(BANNER)

# details about how to use program "--how"
def info():
    info = """
    BirdMiner: Twitter Forensics Investigation and reporting suite

    BirdMiner digs up all data that is stored by Twitter - no login necessary.

            RUN "shsu" MODE TO AUTOMOCATICALLY COLLECT DATA AND SORT

    There are various search parameters that allow for the scraping to be as
    specific or general as needed. These parameters can be found by running:

    Usage:    python3 birdminer.py [OPTIONS]
    Assisted data collection:            PROG --mode [user][word][user-word]
                                                    [config-search][shsu]

    Each mode has its own information/help doc that is offered when the mode is
    ran -- this is automatically saved into a folder for accessbility -- while
    running BirdMiner.

    Birdminer description/other info     PROG --how
    For help:                            PROG --help.

    Use "pip3 install -r requirements.txt" to install needed dependencies; This
    program was built with python 3.7 -- therefore, may not be compatible with
    earlier versions.

    """
    print(info)
    print("This help screen will be saved in the 'Docs' of this main directory.")
    try:
        os.chdir("docs")
        help_doc = open("info.txt", "w")
        help_doc.writelines(info)
        sys.exit()
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Help dopcument has succesfully been saved in the 'docs' folder.")
    except:
        print("File has already been created.")

# display mode help
def mode_info():
    print("""
          Usage: python3 birdminer.py --mode [MODE]

          MODE is the desired searching mode which must be in lower case.
                MODES[user][word][combo][config-search]
                            [shsu][view][help]
          example: python3 birdminer.py --mode user
          """)

# if there are no arguments passed -- print banner and exit
# creates project folder
def check_args(args):
    if len(sys.argv) == 1:
        banner()
        sys.exit()

# creates/checks project-files folder
def project_folder():
    try:
        os.makedirs("project_files")
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

# Parse arguments
def arguments():

    version_string = f"%(prog)s {__version__}\n" +  \
    f"Python:  {platform.python_version()}" + \
    "\nUse 'pip3 install -r requirements.txt' to install dependencies."

    p = argparse.ArgumentParser(formatter_class=RawDescriptionHelpFormatter,
                            description=f"{module_name} (Version {__version__})")
    p.add_argument("--version", "-V",
                    action="version",  version=version_string,
                    help="Display version information and dependencies.")
    p.add_argument("--info", "--information", "--how",
                    action="store_true", dest="info", default="False",
                    help="Explanation of Program features and command-line argruments")
    p.add_argument("--mode",
                    action="store",
                     choices=["user", "word", "user-word", "config-search",
                              "shsu", "view", "help"], dest="mode",
                    help="Pick preconfigured search queries to speed investigations."
                    "Also pick from other storing, manipulating, and exporting utilties birdminer.py offers")

    args = p.parse_args()

    return args


def main():
    # call and store agruments
    args = arguments()

    # ARGS CHECK
    check_args(args)

    # creates/checks project-files folder
    project_folder()

    current_dir = os.getcwd()

    try:
        os.mkdir("docs")
    except OSError as e:
        if e.errno != errno.EEXIST:
            print("Stored help documents can be found in the 'docs' folder.")

    if args.mode:
        if args.mode == "user":
            import user
        elif args.mode == "word":
            import word
        elif args.mode == "user-word":
            import user_word
        elif args.mode == "config-search":
            import user_config
        elif args.mode == "shsu":
             import shsu
        elif args.mode == "view":
            import view
        elif args.mode == "help":
            mode_info()


    # agruments for help and information
    ''' fix version arg '''
    if args.info == True:
        info()
        sys.exit()

main()

