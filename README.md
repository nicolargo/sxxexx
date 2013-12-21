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

    $ sxxexx -t homeland -s 3 -e 12 -V

    21/12/2013 11:06:26 DEBUG - Running SxxExx version 0.2
    21/12/2013 11:06:26 DEBUG - Debug mode is ON
    21/12/2013 11:06:26 DEBUG - Search for title Homeland
    21/12/2013 11:06:26 DEBUG - Search for season 3
    21/12/2013 11:06:26 DEBUG - Search for episode 12
    21/12/2013 11:06:26 DEBUG - Download mode is OFF
    21/12/2013 11:06:26 DEBUG - Piracy Bay URL (use -p to overwrite): https://thepiratebay.se
    21/12/2013 11:06:26 DEBUG - Connected to the Piracy Bay
    21/12/2013 11:06:26 DEBUG - Search regexp: .*homeland.*((s[0]*3.*e[0]*12)|[0]*3x[0]*12).*
    21/12/2013 11:06:26 DEBUG - Search homeland in the category TV shows...
    21/12/2013 11:06:29 DEBUG - Search homeland in the category HD TV shows...
    21/12/2013 11:06:32 DEBUG - 8 torrent(s) found
    21/12/2013 11:06:32 DEBUG - Best match is Homeland S03E12 WEBRip x264-KYR[ettv]
    Title:   Homeland S03E12 WEBRip x264-KYR[ettv]
    Seeders: 7792
    Magnet:  magnet:?xt=urn:btih:d728fb44446e6c16e...

