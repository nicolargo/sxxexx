#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SxxExx
# Thk to Piracy Bay, search and download series.
# Command line only. No GUI bulshit.
#
# Copyright (C) 2013 Nicolargo <nicolas@nicolargo.com>
#
# Distributed under the MIT license (MIT)

__appname__ = "SxxExx"
__version__ = "0.3"
__author__ = "Nicolas Hennion <nicolas@nicolargo.com>"
__license__ = "MIT"
# Syntax
__doc__ = '''\

Search (and download) series from the Piracy Bay.

Usage: sxxexx [options]

Options:
    -t <title>     Serie's title
    -s <season>    Season (optionnal)
    -e <episode>   Episode (optionnal)
    -l <min>       Minimum seeders (optionnal, default is 0)
    -p <url>       Overwrite default Piracy Bay URL
    -a             Display all results (not only the best choice)
    -d             Download best choice using Transmission (RPC)
    -c <host:port> Overwrite Transmission RPC address (default localhost:9091)
    -h             Display help and exit
    -v             Display version and exit
    -V             Switch on debug/verbose mode

Examples:

    # sxxexx -t homeland -s 3 -e 10 -a
    > Display all Homeland S03E10 torrents
    # sxxexx -t "the walking dead" -s 4 -e 8 -d
    > Download best torrent (most seeded) for The Walking Dead S04E08
    # sxxexx -t "how i met your mother" -s 9 -a
    > Display all HYMYM torrents of the season 9

'''

# Import std lib
import getopt
import sys
import logging
import re

# Import ext lib
try:
    import tpb
except:
    print("Error: Sorry but SxxExx need ThePiracyBay Python lib")
    sys.exit(1)
try:
    import transmissionrpc
except:
    transmissionrpc_tag = False
else:
    transmissionrpc_tag = True

# Global variables
tpb_url = "https://thepiratebay.se"
tpb_categories = { 205: 'TV shows', 208: 'HD TV shows' }
transmission_rcp = "localhost:9091"

# Limit import to class...
# __all__ = [ series ]

# Classes

class series(object):
    """
    Main class: search and download series
    """

    def __init__(self, tpb_url= "",
                 title="", season="", episode="", seeders_min=0):
        self.tpb_url = tpb_url
        self.source = self.__readsource__()
        self.title = title
        self.season = season
        self.episode = episode
        self.seeders_min = seeders_min
        self.regexp = self.search_regexp()
        logging.debug("Search regexp: %s" % self.regexp)
        self.list = self.buildlist(category=tpb.CATEGORIES.VIDEO.TV_SHOWS)
        self.list = self.list + self.buildlist(category=tpb.CATEGORIES.VIDEO.HD_TV_SHOWS)
        self.list.sort(key=lambda torrent: torrent[1], reverse=True)
        logging.debug("%s torrent(s) found" % len(self.list))        


    def __tpb_error_(self):
        print("Error: Communication problem with the Piracy Bay")
        print("Info: Check if the Piracy Bay Web site is online: %s" % self.tpb_url)            
        print("Note: You can change the Piracy Bay URL with the -p tag")            


    def __readsource__(self):
        """
        Connect to the Piracy Bay
        """
        try:
            s = tpb.TPB(self.tpb_url)
        except:
            logging.debug("Can not connect to the Piracy Bay")            
            self.__tpb_error_()
            sys.exit(1)
        else:
            logging.debug("Connected to the Piracy Bay")
            return s


    def search_regexp(self):
        """
        Define the regexp used for the search
        """
        if ((self.season == "") and (self.episode == "")):
            # Find serie
            regexp = '.*%s.*' % self.title.lower()
        elif (self.episode == ""):
            # Find season
            regexp = '.*%s.*(s[0]*%s|season[\s\_\-\.]*%s).*' % (self.title.lower(), self.season, self.season)
        else:
            # Find season and episode
            regexp = '.*%s.*((s[0]*%s.*e[0]*%s)|[0]*%sx[0]*%s).*' % (self.title.lower(), self.season, self.episode, self.season, self.episode)
        return regexp


    def buildlist(self, category=tpb.CATEGORIES.VIDEO.TV_SHOWS):
        """
        Build the torrent list
        Return list of list sorted by Seeders 
        [[<title>, <Seeders>, <MagnetURL>, <TorrentURL] ...]
        """

        try:
            s = self.source.search(self.title.lower(), category=category)
        except:
            logging.debug("Can not send search request to the Piracy Bay")            
            self.__tpb_error_()
            sys.exit(1)

        logging.debug("Search %s in the category %s..." % (self.title.lower(), tpb_categories[category]))

        try:
            for t in s.items():
                pass
        except:
            logging.debug("The Piracy Bay return an invalid result") 
            self.__tpb_error_()
            sys.exit(1)            

        torrentlist = []
        for t in s.items():
            # logging.debug("Compare regex to: %s" % t.title.lower())
            if (re.search(self.regexp, t.title.lower()) and (t.seeders >= self.seeders_min)):
                # logging.debug("Matched")
                torrentlist.append((t.title, t.seeders, t.magnet_link, t.torrent_link))
        # logging.debug("Found %s matching items" % len(torrentlist))

        # Return the list
        return torrentlist


    def getbest(self):
        """
        Return the best choice (or None if no serie founded)
        """
        if (len(self.list) > 0):
            return self.list[0]
        else:
            return None


    def getall(self):
        """
        Return all the matched series (or None if no serie founded)
        """
        if (len(self.list) > 0):
            return self.list
        else:
            return None


# Functions

def printSyntax():
    """
    Display the syntax of the command line
    """
    print(__doc__)


def printVersion():
    """
    Display the current software version
    """
    print(__appname__ + " version " + __version__)


def main():
    """
    Main function
    """

    global _DEBUG_
    _DEBUG_ = False

    global tpb_url
    global transmission_rcp

    # Init locals variables
    serie_title = None
    serie_season = ""
    serie_episode = ""
    seeders_min = 0
    download_tag = False
    display_all_tag = False

    # Manage args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:s:e:l:dc:p:ahvV")
    except getopt.GetoptError as err:
        # Print help information and exit:
        print("Error: " + str(err))
        printSyntax()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-t"):
            try:
                serie_title = arg
            except:
                printVersion()
                sys.exit(1) 
        elif opt in ("-s"):
            try:
                serie_season = arg
            except:
                printVersion()
                sys.exit(1) 
        elif opt in ("-e"):
            try:
                serie_episode = arg
            except:
                printVersion()
                sys.exit(1) 
        elif opt in ("-l"):
            try:
                seeders_min = int(arg)
            except:
                printVersion()
                sys.exit(1) 
        elif opt in ("-d"):
            download_tag = True
        elif opt in ("-c"):
            transmission_rcp = arg
        elif opt in ("-p"):
            try:
                tpb_url = arg
            except:
                printVersion()
                sys.exit(1) 
        elif opt in ("-a"):
            display_all_tag = True
        elif opt in ("-h"):
            printVersion()
            printSyntax()
            sys.exit(0)
        elif opt in ("-v"):
            printVersion()
            sys.exit(0) 
        elif opt in ("-V"):
            _DEBUG_ = True
            # Verbose mode is ON
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s - %(message)s',
                datefmt='%d/%m/%Y %H:%M:%S',
            )
        # Add others options here...
        else:
            printSyntax()
            sys.exit(1)

    # By default verbose mode is OFF
    if not _DEBUG_:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
        )
    logging.debug("Running %s version %s" % (__appname__, __version__))
    logging.debug("Debug mode is ON")

    # Test args
    if (serie_title is None):
        print("Error: Need a serie's title")
        printSyntax()
        sys.exit(1)
    else:
        logging.debug("Search for title %s" % serie_title)
    if (serie_season != ""):
        logging.debug("Search for season %s" % serie_season)
    if (serie_episode != ""):
        logging.debug("Search for episode %s" % serie_episode)
    if (download_tag and not transmissionrpc_tag):
        print("Error: -d tag need the TransmissionRPC Python lib")
        sys.exit(1)         
    if (download_tag and display_all_tag):
        print("Error: -d tag can not be used with the -a tag")
        printSyntax()
        sys.exit(1)         
    if (download_tag and not display_all_tag):
        logging.debug("Download mode is ON")
        try:
            transmission_rcp_host, transmission_rcp_port = transmission_rcp.split(':')
            transmission_rcp_port = int(transmission_rcp_port)
        except:
            print("Error: Transmission RPC should be host:port")
            printSyntax()
            sys.exit(1)
        else:
            logging.debug("Transmission RPC: host=%s / port=%s" % (transmission_rcp_host, transmission_rcp_port))
    else:
        logging.debug("Download mode is OFF")
    if (display_all_tag):
        logging.debug("Display all tag is ON")

    logging.debug("Piracy Bay URL (use -p to overwrite): %s" % tpb_url)

    # Main loop
    serie = series(tpb_url = tpb_url, title=serie_title, season=serie_season, episode=serie_episode, seeders_min=seeders_min)
    best = serie.getbest()

    # Display result
    if (best is not None):
        if (display_all_tag):
            logging.debug("Display all results")
            for r in serie.getall():
                print("*"*79)
                print("Title:   %s" % r[0])
                print("Seeders: %s" % r[1])
                print("Magnet:  %s" % r[2])
                # print("Torrent: %s" % r[3])
        else:
            logging.debug("Best match is %s" % best[0])
            print("Title:   %s" % best[0])
            print("Seeders: %s" % best[1])
            print("Magnet:  %s" % best[2])
            # print("Torrent: %s" % best[3])
    else:
        print("No torrent found for %s..." % serie_title)

    # Download
    if ((best is not None) and download_tag):
        logging.debug("Send best magnet to Transmission")
        try:
            tc = transmissionrpc.Client(transmission_rcp_host, port=transmission_rcp_port)
        except:
            print("Error: Can not connect to Transmission (%s:%s)" % (transmission_rcp_host, transmission_rcp_port))
            print("Info: Transmission remote control access should be enabled on host %s, port %s" % (transmission_rcp_host, transmission_rcp_port))
            logging.debug("Can not connect to Transmission (%s:%s)" % (transmission_rcp_host, transmission_rcp_port))
            sys.exit(1)
        else:
            logging.debug("Transmission connection completed")
        try:
            tc.add_uri(best[2])
        except:
            print("Error: Transmission can not start download")
            logging.debug("Error while sending download request to Transmission")
            sys.exit(1)
        else:
            print("Transmission start downloading...")
            logging.debug("SxxExx sent the magnet to Transmission")

    # End of the game
    sys.exit(0)

# Main
#=====

if __name__ == "__main__":
    main()

# The end...
