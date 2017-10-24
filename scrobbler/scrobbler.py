#!/usr/bin/env python
# coding=utf-8

#
# A command-line Last.fm scrobbler and a now-playing status updater.
# Copyright (C) 2013  Никола "hauzer" Вукосављевић
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
A command-line Last.fm scrobbler and a now-playing status updater.

usage: scrobbler [--sessions-file=<path>] [--liblfm-file=<path>]
                 [--help] [--version]
                 <command> [<args>...]

options:
    --sessions-file=<path>  Specify the path to the database holding known users.
    --liblfm-file=<path>    Specify the path which the lfm library should use for its file.

commands:
    add-user        Add a user to the list of known users.
    list-users      List all known users.
    remove-user     Remove a user from the list of known users.
    scrobble        Scrobble a track.
    now-playing     Update the now-playing status.
"""

import sys
if sys.version_info[0] != 3:
    print("Python 3 required.")
    exit()

from . import info

from appdirs import AppDirs
from docopt import docopt
from lastfm import lfm
import lastfm.exceptions

from getpass import getpass
from datetime import datetime
import time
import os.path
import re
import sqlite3
import webbrowser


API_KEY     = "b3e7abc138f65a43803f887aeb36b9f6"
SECRET      = "d60a1a4d704b71c0e8e5bac98d793969"

dirs            = AppDirs(info.NAME, info.AUTHOR_NICK, info.VERSION)
USERS_DB_FILE   = os.path.join(dirs.user_data_dir, "sessions.db")
LIBLFM_FILE     = os.path.join(dirs.user_data_dir, "lfm.db")


class Error(Exception):
    """
    An error intended to be printed for the user.
    """
    
    def __init__(self, msg):
        super().__init__("Error: {}.".format(msg))

    pass


def duration_to_seconds(string):
    if string is None:
        return None

    durations = re.findall("\d+[hms]", string)
    seconds = 0
    for duration in durations:
        time = int(duration[:-1])
        unit = duration[-1]

        if unit == "m":
            time *= 60
        elif unit == "h":
            time *= 60**2

        seconds += time

    return seconds


def db_table_exists_sessions(dbc):
    dbc.execute("select exists(select * from sqlite_master " \
                "where type = \"table\" and name = \"sessions\")")
    return dbc.fetchone()[0]


def db_create_table_sessions(dbc):
    dbc.execute("create table sessions (user text primary key, key text)")


def user_exists(dbc, user):
    dbc.execute("select exists(select * from sessions where user == ?)", (user,))
    return bool(dbc.fetchone()[0])


def exit_if_user_exists(dbc, user):
    if user_exists(dbc, user):
        raise Error("{} is already registered.".format(user))


def exit_if_user_not_exists(dbc, user):
    if not user_exists(dbc, user):
        raise Error("{} isn't in the list of known users.".format(user))


def auth(app, dbc, user):
    if not user_exists(dbc, user):
        pwd = getpass()
        session = app.auth.get_mobile_session(user, pwd)
        app.session_key = session["key"]

    else:
        dbc.execute("select key from sessions where user == ?", (user,))
        app.session_key = dbc.fetchone()[0]


def cmd_add_user(app, dbc, args):
    """
Add a user to the list of known users.
    
usage: scrobbler add-user [[<user> [--password=<password>]]|[--dont-invoke-browser]]

options:
    -p <password>,  --password=<password>
    -x, --dont-invoke-browser               When invoking the command without arguments,
                                            always show the authentication URL; never try
                                            to automatically open it.
    """
    
    if args["<user>"] is None:
        token = app.auth.get_token()
        
        if args["--dont-invoke-browser"]:
            print("Last.fm authentication URL: {}".format(token.url))
        else:
            input("The Last.fm authentication page will be opened, or its URL printed here.\nPress enter to continue.")
            try:
                webbrowser.open(token.url)
            except webbrowser.Error:
                print(token.url)
    
        input("Press enter after granting access.")
        session = app.auth.get_session(token)
    
        exit_if_user_exists(dbc, session["name"])

    else:
        exit_if_user_exists(dbc, args["<user>"])

        if args["--password"] is None:
            pwd = getpass()
        else:
            pwd = args["--password"]

        session = app.auth.get_mobile_session(args["<user>"], pwd)


    dbc.execute("insert into sessions (user, key) values (?, ?)", (session["name"], session["key"]))
    print("User {} added.".format(session["name"]))


def cmd_list_users(app, dbc, args):
    """
List all known users.

usage: scrobbler list-users
    """
   
    dbc.execute("select * from sessions")
    for (user, key) in dbc.fetchall():
        print("{}\t\t| {}".format(user, key))
    print()


def cmd_remove_user(app, dbc, args):
    """
Remove a user from the list of known users.

usage: scrobbler remove-user <user>
    """

    exit_if_user_not_exists(dbc, args["<user>"])
    dbc.execute("delete from sessions where user == ?", (args["<user>"],))
    print("User {} removed.".format(args["<user>"]))


def cmd_scrobble(app, dbc, args):
    """
Scrobble a track.

usage: scrobbler scrobble [--album=<name>] [--duration=<duration>] [--time-format=<format>]
                          [--] <user> <artist> <track> <time>


options:
    -f <format>, --time-format=<format>     [default: %Y-%m-%d.%H:%M]
    -a <name>, --album=<name>
    -d <duration>, --duration=<duration>    Has the format of XXhYYmZZs. At least one of
                                            those has to be present, but any number of them
                                            can be specified, and in any order.
    """

    auth(app, dbc, args["<user>"])

    if args["<time>"] == "now":
        timestamp = datetime.now().timestamp()
    else:
        timestamp = datetime.strptime(args["<time>"], args["--time-format"]).timestamp()

    scrobble = lfm.Scrobble(args["<artist>"], args["<track>"], int(timestamp),
                            album = args["--album"], duration = duration_to_seconds(args["--duration"]))

    resp = app.track.scrobble([scrobble]) 
    if int(resp["@attr"]["ignored"]) != 0:
        raise Error(resp["scrobble"]["ignoredMessage"]["#text"])

    print("Track scrobbled.")
    

def cmd_now_playing(app, dbc, args):
    """
Update the now-playing status.
    
usage: scrobbler now-playing [--album=<name>] [--duration=<duration>] [--] <user> <artist> <track>

options:
    -a <name>, --album=<name>
    -d <duration>, --duration=<duration>  Has the format of XXhYYmZZs. At least one of
                                          those has to be present, but any number of them
                                          can be specified, and in any order.
    """
    
    auth(app, dbc, args["<user>"])
    app.track.update_now_playing(args["<artist>"], args["<track>"],
                                 album = args["--album"], duration = duration_to_seconds(args["--duration"]))
    print("Status updated.")


def main():
    args = docopt(__doc__, version = "{} {}".format(info.NAME, info.VERSION), options_first = True)

    if args["--sessions-file"] is None:
        db_file = USERS_DB_FILE
    else:
        db_file = args["--sessions-file"]
   
    if args["--liblfm-file"] is None:
        liblfm_file = LIBLFM_FILE
    else:
        liblfm_file = args["--liblfm-file"]

    os.makedirs(dirs.user_data_dir, exist_ok = True)
    app = lfm.App(API_KEY, SECRET, liblfm_file, (info.NAME, info.VERSION))

    db = sqlite3.connect(db_file)
    dbc = db.cursor()
    
    if not db_table_exists_sessions(dbc):
        db_create_table_sessions(dbc)

    try:
        cmd_name = "cmd_{}".format(args["<command>"].replace("-", "_"))
        try:
            cmd = globals()[cmd_name]
        except KeyError as e:
            raise Error("Unknown command '{}'".format(args["<command>"]))

        cmd_args = docopt(cmd.__doc__, argv = [args["<command>"]] + args["<args>"])   

        try:
            cmd(app, dbc, cmd_args)
        except:
            raise

    except (Error, lastfm.exceptions.RequestError) as e:
        print(e)
    
    db.commit()
    db.close()


if __name__ == "__main__":
    main()
