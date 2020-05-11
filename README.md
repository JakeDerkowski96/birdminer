# Birdminer
twitter forensic suite

Research Topics in Comp Science (COSC 4340) project @ Sam Houston State University

This is twitter scraping program written in python for an independant study
course at Sam houston stata university. 
    This program utilizes the "twint" module to scrap twitter without the need of an API, which aids the users in
       forensic investigations. My case study done on the students of SHSU, but this program is highly configurable to any user's needs.

    Use "pip3 install -r requirements.txt" to install needed dependencies; 
    This program was built with python 3.7 -- therefore, may not be compatible with
    earlier versions.


usage: birdminer.py [-h] [--version] [--info]


                    [--mode {user,word,user-word,config-search,shsu,view,help}]

BirdMiner: An user-friendly, forensic Twitter utility. (Version 1.0.0)


optional arguments:

    -h, --help            show this help message and exit
  
    --version, -V         Display version information and dependencies.
  
    --info, --information, --how
  
                            Explanation of Program features and command-line
                            argruments
                        
    --mode {user,word,user-word,config-search,shsu,view,help}
  
                            Pick preconfigured search queries to speed
                            investigations.Also pick from other storing,
                            manipulating, and exporting utilties birdminer.py
                            offers
