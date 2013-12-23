[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/nicolargo/sxxexx/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

SxxExx
======

A command line tool to search (and download) series from the Piracy Bay.

# Install 

Easy way to install:

    pip install sxxexx

or upgrade:

    pip install --upgrade sxxexx

# Cookbook

1) Search and display best magnet (most seeded) Homeland season 3, episode 10

    $ sxxexx -t homeland -s 3 -e 10

    Homeland S3E10 name is "Good Night"
    Title:   Homeland S03E10 HDTV x264-ASAP [eztv]
    Seeders: 3567
    Magnet:  magnet:?xt=urn:btih:522b99e066bf97753a9c0


2) Search and display all magnets Breaking bad season 5 (all episodes)

    $ sxxexx.py -t "Breaking bad" -s 5 -a

    Breaking Bad has 16 episodes in season 5
    *******************************************************************************
    Title:   Breaking Bad - The Complete Season 5 [BDRip-HDTV] + EXTRAS
    Seeders: 2097
    Magnet:  magnet:?xt=urn:btih:82eb1fbb413038dd551eb8c5d4f6a891ff2d190f&dn=Breaking+Bad+-+The+Complete+Season+5+%5BBDRip-HDTV%5D+%2B+EXTRAS&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Ftracker.ccc.de%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337
    *******************************************************************************
    Title:   Breaking Bad S05E16 REPACK HDTV x264-ASAP[ettv]
    Seeders: 1928
    Magnet:  magnet:?xt=urn:btih:24d076e1c0f041977346e7bbf4277ceccf1086b0&dn=Breaking+Bad+S05E16+REPACK+HDTV+x264-ASAP%5Bettv%5D&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A80&tr=udp%3A%2F%2Ftracker.publicbt.com%3A80&tr=udp%3A%2F%2Ftracker.istole.it%3A6969&tr=udp%3A%2F%2Ftracker.ccc.de%3A80&tr=udp%3A%2F%2Fopen.demonii.com%3A1337
    *******************************************************************************
    ...


3) Search and start downloading (using Transmission) How i met your mother season 9, episode 9

    $ sxxexx -t "how i met your mother" -s 9 -e 9 -d

    How I Met Your Mother S9E9 name is "Platonish"
    Title:   How I Met Your Mother S09E09 HDTV x264-2HD [eztv]
    Seeders: 3631
    Magnet:  magnet:?xt=urn:btih:11633c741fe5e0a0774c2222cfa6c05


4) Search and display best magnet (most seeded) Homeland season 3, episode 10 in verbose mode

    $ sxxexx -t homeland -s 3 -e 12 -V

    23/12/2013 15:19:45 INFO - Running SxxExx version 0.4
    23/12/2013 15:19:45 INFO - Search for title homeland
    23/12/2013 15:19:45 INFO - Search for season 3
    23/12/2013 15:19:45 INFO - Search for episode 12
    23/12/2013 15:19:45 INFO - Download mode is OFF
    23/12/2013 15:19:45 INFO - TVDB API is installed
    23/12/2013 15:19:45 INFO - Piracy Bay URL (use -p to overwrite): https://thepiratebay.se
    23/12/2013 15:19:45 INFO - Get serie information from TVDB
    Homeland S3E12 name is "The Star"
    23/12/2013 15:19:47 INFO - Search homeland in the category HD TV shows...
    23/12/2013 15:19:49 INFO - Search homeland in the category TV shows...
    23/12/2013 15:19:53 INFO - 7 torrent(s) found
    23/12/2013 15:19:53 INFO - Best match is Homeland S03E12 WEBRip x264-KYR[ettv]
    Title:   Homeland S03E12 WEBRip x264-KYR[ettv]
    Seeders: 5924
    Magnet:  magnet:?xt=urn:btih:d728fb44446e6c16eafe2bbd2932dce10e272c87&dn=Homel
