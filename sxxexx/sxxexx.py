#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# SxxExx
# Thk to Piracy Bay, search and download series.
# Command line only. No GUI bulshit.
#
# Copyright (C) 2014 Nicolargo <nicolas@nicolargo.com>
#
# Distributed under the MIT license (MIT)

__appname__ = "SxxExx"
__version__ = "0.5"
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
    -q             Add a filter for HD quality
    -p <url>       Overwrite default Piracy Bay URL
    -a             Display all results (not only the best choice)
    -d             Download best choice using Transmission (RPC)
    -c <host:port> Overwrite Transmission RPC address (default localhost:9091)
    -i             Disable access to the TVDB database
    -V             Switch on verbose mode (verbose like a man)
    -D             Switch on debug mode (verbose like a woman)
    -h             Display help and exit
    -v             Display version and exit

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

# Import ext lib (mandatory)
try:
    import tpb
except:
    print("Error: Sorry but SxxExx need ThePirateBay Python lib")
    print("Install it using: # pip install thepiratebay")
    sys.exit(1)

# Import ext lib (optionnal)
try:
    import tvdb_api
except:
    tvdbapi_tag = False
else:
    tvdbapi_tag = True
try:
    import transmissionrpc
except:
    transmissionrpc_tag = False
else:
    transmissionrpc_tag = True

# Global variables
tpb_url = "https://thepiratebay.se"
tpb_categories = {}
tpb_categories_ld = { tpb.CATEGORIES.VIDEO.TV_SHOWS: 'TV shows' }
tpb_categories_hd = { tpb.CATEGORIES.VIDEO.HD_TV_SHOWS: 'HD TV shows' }
transmission_rcp = "localhost:9091"

# Classes

class tvdb(object):
    """
    Class to manage connection to the TVDB database
    In the current version, TVDB is optionnal
    """

    def __init__(self, title=""):
        self.tvdb_tag = tvdbapi_tag
        if (self.tvdb_tag):
            self.tvdb = tvdb_api.Tvdb()
            try:
                self.tvdb_serie = self.get_serie(title)
            except:
                self.tvdb_serie = None
        self.tvdb_season = None
        self.tvdb_episode = None


    def get_serie(self, title=""):
        if (self.tvdb_tag):
            self.tvdb_serie = self.tvdb[title]
            self.data = self.tvdb_serie.data
        return self.tvdb_serie


    def get_season(self, season=0):
        if (self.tvdb_tag and (self.tvdb_serie != None)):
            self.tvdb_season = self.tvdb_serie[season]
        return self.tvdb_season


    def get_season_number(self):
        if (self.tvdb_tag and (self.tvdb_serie != None)):
            return len(self.tvdb_serie)-1
        return -1


    def get_episode(self, season, episode):
        if (self.tvdb_tag and (self.tvdb_serie != None)):
            self.tvdb_episode = self.tvdb_serie[season][episode]
        return self.tvdb_episode


    def get_episode_number(self, season):
        if (self.tvdb_tag and (self.tvdb_serie != None)):
            return len(self.tvdb_serie[season])
        return -1


class series(object):
    """
    Main class: search and download series
    """

    def __init__(self, tpb_url= "",
                 title="", season="", episode="", seeders_min=0):
        self.tpb_url = tpb_url
        # TPB is the "source" for SxxExx
        self.source = self.__readsource__()
        self.title = title
        self.season = season
        self.episode = episode
        self.seeders_min = seeders_min
        logging.info("Get serie information from TVDB")
        self.tvdb = tvdb(self.title)
        self.regexp = self.search_regexp()
        logging.debug("Search regexp: %s" % self.regexp)
        self.list = []
        for c in tpb_categories.keys():
            self.list += self.buildlist(category=c)
        self.list.sort(key=lambda torrent: torrent[1], reverse=True)
        logging.info("%s torrent(s) found" % len(self.list))


    def __tpb_error_(self):
        # logging.error("Communication problem with the Piracy Bay")
        logging.info("Check if the Piracy Bay Web site is online: %s" % self.tpb_url)
        logging.debug("You can change the Piracy Bay URL with the -p tag")


    def __readsource__(self):
        """
        Connect to the Piracy Bay
        """
        try:
            s = tpb.TPB(self.tpb_url)
        except:
            logging.error("Can not connect to the Piracy Bay Web site")
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
            try:
                print("%s has %s seasons (the serie is %s)" % (self.tvdb.data['seriesname'], self.tvdb.get_season_number(), self.tvdb.data['status'].lower()))
                # print self.tvdb.data
            except:
                pass
            regexp = '^%s.*' % self.title.lower()
        elif (self.episode == ""):
            # Find season
            try:
                print("%s has %s episodes in season %s" % (self.tvdb.data['seriesname'], self.tvdb.get_episode_number(int(self.season)), self.season))
            except:
                pass
            regexp = '^%s.*(s[0]*%s|season[\s\_\-\.]*%s).*' % (self.title.lower(), self.season, self.season)
        else:
            # Find season and episode
            try:
                print("%s S%sE%s name is \"%s\"" % (self.tvdb.data['seriesname'], self.season, self.episode, self.tvdb.get_episode(int(self.season), int(self.episode))['episodename']))
            except:
                pass
            regexp = '^%s.*((s[0]*%s.*e[0]*%s)|[0]*%sx[0]*%s).*' % (self.title.lower(), self.season, self.episode, self.season, self.episode)
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
            logging.error("Can not send search request to the Piracy Bay")
            self.__tpb_error_()
            sys.exit(1)

        logging.info("Search %s in the category %s..." % (self.title.lower(), tpb_categories[category]))

        try:
            for t in s.items():
                pass
        except:
            logging.error("The Piracy Bay return an invalid result")
            self.__tpb_error_()
            sys.exit(1)

        torrentlist = []
        for t in s.items():
            # logging.debug("Compare regex to: %s" % t.title.lower())
            if (re.search(self.regexp, t.title.lower()) and (t.seeders >= self.seeders_min)):
                # logging.debug("Matched")
                torrentlist.append((t.title, t.seeders, t.magnet_link, t.torrent_link))
        logging.debug("Found %s matching items in category %s" % (len(torrentlist), tpb_categories[category]))

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
    global tpb_categories
    global transmission_rcp
    global tvdbapi_tag

    # Init locals variables
    serie_title = None
    serie_season = ""
    serie_episode = ""
    seeders_min = 0
    download_tag = False
    display_all_tag = False
    hd_tag = False

    # Manage args
    try:
        opts, args = getopt.getopt(sys.argv[1:], "t:s:e:l:qdc:p:aiVDhv")
    except getopt.GetoptError as err:
        # Print help information and exit:
        print("Syntax error, %s" % str(err))
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
        elif opt in ("-q"):
            hd_tag = True
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
        elif opt in ("-i"):
            tvdbapi_tag = False
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
                level=logging.INFO,
                format='%(asctime)s %(levelname)s - %(message)s',
                datefmt='%d/%m/%Y %H:%M:%S',
            )
            logging.debug("Verbose mode is ON")
        elif opt in ("-D"):
            _DEBUG_ = True
            # Debug mode is ON
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s %(levelname)s - %(message)s',
                datefmt='%d/%m/%Y %H:%M:%S',
            )
            logging.debug("Debug mode is ON")
        # Add others options here...
        else:
            printSyntax()
            sys.exit(1)

    if (not _DEBUG_):
        # Set default logging message to ERROR
        logging.basicConfig(
            level=logging.ERROR,
            format='%(asctime)s %(levelname)s - %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
        )

    logging.info("Running %s version %s" % (__appname__, __version__))

    # Test args
    if (serie_title is None):
        # A serie's title is needed... always
        logging.error("Need a serie's title. Use the -t tag.")
        sys.exit(1)
    else:
        logging.info("Search for title %s" % serie_title)
    if (serie_season != ""):
        # Optionnal season number
        logging.info("Search for season %s" % serie_season)
    if (serie_episode != ""):
        # Optionnal episode number
        logging.info("Search for episode %s" % serie_episode)
    if (download_tag and not transmissionrpc_tag):
        logging.error("-d tag need the TransmissionRPC Python lib")
        sys.exit(1)
    if (hd_tag):
        # HD tag is True: search only in the HD category
        tpb_categories.update(tpb_categories_hd)
        logging.info("Filter HD series")
    else:
        # By default search on all categories (SD and HD)
        tpb_categories.update(tpb_categories_ld)
        tpb_categories.update(tpb_categories_hd)
    if (download_tag and display_all_tag):
        logging.error("-d tag can not be used with the -a tag")
        sys.exit(1)
    if (download_tag and not display_all_tag):
        logging.info("Download mode is ON")
        try:
            transmission_rcp_host, transmission_rcp_port = transmission_rcp.split(':')
            transmission_rcp_port = int(transmission_rcp_port)
        except:
            logging.error("Transmission RPC adress should be host:port")
            sys.exit(1)
        else:
            logging.info("Transmission RPC: host=%s / port=%s" % (transmission_rcp_host, transmission_rcp_port))
    else:
        logging.info("Download mode is OFF")
    if (display_all_tag):
        logging.info("Display all tag is ON")

    if (tvdbapi_tag):
        logging.info("TVDB API is installed")
    else:
        logging.info("TVDB API is not installed")

    logging.info("Piracy Bay URL (use -p to overwrite): %s" % tpb_url)

    # Main loop
    serie = series(tpb_url = tpb_url, title=serie_title, season=serie_season, episode=serie_episode, seeders_min=seeders_min)
    best = serie.getbest()

    # Display result
    if (best is not None):
        if (display_all_tag):
            logging.info("Display all results")
            for r in serie.getall():
                print("*"*79)
                print("Title:   %s" % r[0])
                print("Seeders: %s" % r[1])
                print("Magnet:  %s" % r[2])
                # print("Torrent: %s" % r[3])
        else:
            logging.info("Best match is %s" % best[0])
            print("Title:   %s" % best[0])
            print("Seeders: %s" % best[1])
            print("Magnet:  %s" % best[2])
            # print("Torrent: %s" % best[3])
    else:
        print("No torrent found for %s..." % serie_title)

    # Download
    if ((best is not None) and download_tag):
        logging.info("Send best magnet to Transmission")
        try:
            tc = transmissionrpc.Client(transmission_rcp_host, port=transmission_rcp_port)
        except:
            print("Error: Can not connect to Transmission (%s:%s)" % (transmission_rcp_host, transmission_rcp_port))
            print("Info: Transmission remote control access should be enabled on host %s, port %s" % (transmission_rcp_host, transmission_rcp_port))
            logging.info("Can not connect to Transmission (%s:%s)" % (transmission_rcp_host, transmission_rcp_port))
            sys.exit(1)
        else:
            logging.debug("Transmission connection completed")
        try:
            tc.add_uri(best[2])
        except:
            logging.error("Error while sending download request to Transmission")
            sys.exit(1)
        else:
            print("Transmission start downloading...")

    # End of the game
    sys.exit(0)

# Main
#=====

if __name__ == "__main__":
    main()

# The end...
