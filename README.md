SxxExx
======

A command line tool to search (and download) series from the Piracy Bay.

Examples:

1) Search and display best magnet (most seeded) Homeland season 3, episode 10

    $ sxxexx -t homeland -s 3 -e 10
    
    Title:   Homeland S03E10 HDTV x264-ASAP [eztv]
    Seeders: 5263
    Magnet:  magnet:?xt=urn:btih:522b99e066bf977...


2) Search and display all magnets Breaking bad season 5 (all episodes)

    $ sxxexx.py -t "Breaking bad" -s 5 -a

    *******************************************************************************
    Title:   Breaking Bad S05E10 HDTV x264-ASAP
    Seeders: 2310
    Magnet:  magnet:?xt=urn:btih:1a30f4646c7236c...
    *******************************************************************************
    Title:   Breaking Bad S05E09 HDTV x264-ASAP
    Seeders: 2303
    Magnet:  magnet:?xt=urn:btih:4ea50819447010f...
    *******************************************************************************
    ...


3) Search and start downloading (using Transmission) How i met your mother season 9, episode 9

    $ sxxexx -t "how i met your mother" -s 9 -e 9 -d

    Title:   How I Met Your Mother S09E09 HDTV x264-2HD [eztv]
    Seeders: 5037
    Magnet:  magnet:?xt=urn:btih:11633c741fe5e0a...
    Transmission start downloading...


4) Search and display best magnet (most seeded) Homeland season 3, episode 10 in verbose mode

    $ sxxexx -t homeland -s 3 -e 10

    19/12/2013 21:52:46 DEBUG - Running SxxExx version 0.1
    19/12/2013 21:52:46 DEBUG - Debug mode is ON
    19/12/2013 21:52:46 DEBUG - Search for title homeland
    19/12/2013 21:52:46 DEBUG - Search for season 3
    19/12/2013 21:52:46 DEBUG - Search for episode 10
    19/12/2013 21:52:46 DEBUG - Download mode is OFF
    19/12/2013 21:52:46 DEBUG - Piracy Bay URL (use -p to overwrite): https://thepiratebay.gy
    19/12/2013 21:52:46 DEBUG - Connected to the Piracy Bay
    19/12/2013 21:52:46 DEBUG - Search regexp: .*homeland.*s[0]*3.*e[0]*10.*
    19/12/2013 21:52:46 DEBUG - Start searching in the database (category 205)...
    19/12/2013 21:52:53 DEBUG - Found 3 matching items
    19/12/2013 21:52:53 DEBUG - 3 torrent(s) found
    19/12/2013 21:52:53 DEBUG - Best match is Homeland S03E10 HDTV x264-ASAP [eztv]
    Title:   Homeland S03E10 HDTV x264-ASAP [eztv]
    Seeders: 5263
    Magnet:  magnet:?xt=urn:btih:522b99e066bf977...
