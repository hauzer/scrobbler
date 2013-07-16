#
# A Last.fm scrobbler and a now-playing status updater.
# Copyright (C) 2013  Ð�Ð¸ÐºÐ¾Ð»Ð° "hauzer" Ð’ÑƒÐºÐ¾Ñ�Ð°Ð²Ñ™ÐµÐ²Ð¸Ñ›
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


from appdirs import AppDirs
import argparse
from datetime import datetime
import lfm
import os.path
import shlex
import sqlite3
import time
import webbrowser


class Error(Exception):
    pass


def user_exists(dbc, user):
    dbc.execute("select exists(select * from sessions where user == ?)", (user,))
    return bool(dbc.fetchone()[0])


def auth(app, dbc, user):
    if user_exists(dbc, user):
        dbc.execute("select key from sessions where user == ?", (args.user,))
        app.sk = dbc.fetchone()[0]
        
    else:
        raise Error("The user \"{}\" wasn't found in the database.\n" \
                    "Add a session via \"session-add\" first.".format(args.user))
    

def cmd_session_add(app, dbc, args):
    error = "Could not add user \"{}\" to the database; already exists."
    
    if args.user is not None:
        if user_exists(dbc, args.user):
            raise Error(error.format(args.user))
    
    if args.user is None or (args.user is not None and (args.pwd is None and args.sk is None)):
        token = app.auth.get_token()
        
        input("The Last.fm authentication page will be opened, or its URL printed here.\nPress enter to continue.")
        
        try:
            webbrowser.open(token.url)
        except webbrowser.Error:
            print(token.url)
    
        time.sleep(1)
        input("Press enter after granting access.")
        session = app.auth.get_session(token)
        
    elif args.pwd is not None:
        session = app.auth.get_mobile_session(args.user, args.pwd)
    
    elif args.sk is not None:
        session     = {
                       "name":  args.user,
                       "key":   args.sk,
                       }
    
    print()
    
    if not user_exists(dbc, session["name"]):
        dbc.execute("insert into sessions (user, key) values (?, ?)", (session["name"], session["key"]))
    else:
        raise Error(error.format(session["name"]))


def cmd_session_list(app, dbc, args):
    dbc.execute("select * from sessions")
    for (user, key) in dbc.fetchall():
        print("{} | {}".format(user, key))


def cmd_session_rm(app, dbc, args):
    dbc.execute("delete from sessions where user == ?", (args.user,))


def cmd_scrobble(app, dbc, args):
    auth(app, dbc, args.user)
    
    scrobbles = []
    for scrobble in args.scrobbles:
        scrobbles.append(lfm.Scrobble(**vars(parser_ascrobble.parse_args(shlex.split(scrobble)))))
        
    resp = app.track.scrobble(scrobbles)
    ignored = int(resp["@attr"]["ignored"])
    
    if ignored != 0:
        accepted = int(resp["@attr"]["accepted"])
        
        if accepted == 0:
            print("\nAll of the tracks have failed to scrobble:")
        else:
            print("\nSome of the tracks have failed to scrobble:")
            
        scrobbles = resp["scrobble"]
        # The above won't be an array if there's was a single scrobble sent, it'll be
        # the response for that single scrobble itself.
        for scrobble in scrobbles if isinstance(scrobbles, list) else [scrobbles]:
            code = int(scrobble["ignoredMessage"]["code"])
            
            if code != 0:
                message = scrobble["ignoredMessage"]["#text"]
                artist  = scrobble["artist"]["#text"]
                track   = scrobble["track"]["#text"]
                
                print("{} - {}: {}".format(artist, track, message))
                

def cmd_unp(app, dbc, args):
    auth(app, dbc, args.user)
    app.track.update_now_playing(args.artist, args.track, album = args.album, duration = args.duration,
                                 mbid = args.mbid, tracknumber = args.tracknumber,
                                 albumartist = args.albumartist, context = args.context)


API_KEY     = "b3e7abc138f65a43803f887aeb36b9f6"
SECRET      = "d60a1a4d704b71c0e8e5bac98d793969"

dirs = AppDirs("scrobbler", "hauzer", "1.0.0")
os.makedirs(dirs.user_data_dir, exist_ok = True)

DB_FILE     = os.path.join(dirs.user_data_dir, "sessions.db")
LFM_FILE    = os.path.join(dirs.user_data_dir, "lfm.dat")



parser = argparse.ArgumentParser(description = "A Last.fm scrobbler and a now-playing status updater.")
subparsers          = parser.add_subparsers()
parser_session_add  = subparsers.add_parser("session-add", aliases = ["sa"])
parser_session_list = subparsers.add_parser("session-list", aliases = ["sl"])
parser_session_rm   = subparsers.add_parser("session-remove", aliases = ["sr"])
parser_scrobble     = subparsers.add_parser("scrobble", aliases = ["sc"],
                                            formatter_class = argparse.RawTextHelpFormatter)
parser_unp          = subparsers.add_parser("update-now-playing", aliases = ["unp"])


parser_session_add.add_argument("-u", "--user", metavar = "user")
group = parser_session_add.add_mutually_exclusive_group()
group.add_argument("-p", "--password", metavar = "pwd", dest = "pwd")
group.add_argument("-s", "--session-key", metavar = "sk", dest = "sk")
parser_session_add.set_defaults(func = cmd_session_add)

parser_session_list.set_defaults(func = cmd_session_list)

parser_session_rm.add_argument("user")
parser_session_rm.set_defaults(func = cmd_session_rm)


class ParserAscrobbleFormatAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string = None):
        namespace.timestamp = int(datetime.strptime(namespace.timestamp, values).now().timestamp())
        del namespace.format

parser_ascrobble = argparse.ArgumentParser(usage =  "A scrobble consists of three or more\n"    \
                                                    "options specified below. Pass these "      \
                                                    "quoted,\nand as you would to a program.",
                                           add_help = False, formatter_class = argparse.RawTextHelpFormatter)
parser_ascrobble.add_argument("artist", metavar = "artist")
parser_ascrobble.add_argument("track", metavar = "track")
parser_ascrobble.add_argument("timestamp", metavar = "timestamp",
                              help = "\n{0}Time of scrobbling. Can be formatted with -f,\n{0}otherwise it's " \
                              "an UNIX timestamp.".format("\b" * 18))
parser_ascrobble.add_argument("-f", "--format", metavar = "format", action = ParserAscrobbleFormatAction,
                              help = "{0}Specifies the format of the timestamp. Uses\n{0}the same syntax " \
                              "as Python's strftime().".format("\b" * 18))
parser_ascrobble.add_argument("-a", "--album", metavar = "album")
parser_ascrobble.add_argument("-d", "--duration", metavar = "duration")
parser_ascrobble.add_argument("-m", "--mbid", metavar = "mbid")
parser_ascrobble.add_argument("-t", "--track-number", metavar = "track_number", dest = "tracknumber")
parser_ascrobble.add_argument("-aa", "--album-artist", metavar = "album_artist", dest = "albumartist")
parser_ascrobble.add_argument("-s", "--stream-id", metavar = "stream_id", dest = "streamid")
parser_ascrobble.add_argument("-c", "--chosen-by-user", action = "store_true", dest = "chosenbyuser")
parser_ascrobble.add_argument("-cx", "--context", metavar = "context")

parser_scrobble.add_argument("user")
parser_scrobble.add_argument("-s", "--scrobble", action = "append", metavar = "\"artist track tstamp ...\"",
                             dest = "scrobbles", help = parser_ascrobble.format_help())
parser_scrobble.set_defaults(func = cmd_scrobble)


parser_unp.add_argument("user")
parser_unp.add_argument("artist", metavar = "artist")
parser_unp.add_argument("track", metavar = "track")
parser_unp.add_argument("-a", "--album", metavar = "album")
parser_unp.add_argument("-d", "--duration", metavar = "duration")
parser_unp.add_argument("-m", "--mbid", metavar = "mbid")
parser_unp.add_argument("-t", "--track-number", metavar = "track_number", dest = "tracknumber")
parser_unp.add_argument("-aa", "--album-artist", metavar = "album_artist", dest = "albumartist")
parser_unp.add_argument("-cx", "--context", metavar = "context")
parser_unp.set_defaults(func = cmd_unp)



args = parser.parse_args()

app = lfm.App(API_KEY, SECRET, LFM_FILE)

db = sqlite3.connect(DB_FILE)
dbc = db.cursor()

dbc.execute("select exists(select * from sqlite_master " \
            "where type = \"table\" and name = \"sessions\")")
if not dbc.fetchone()[0]:
    dbc.execute("create table sessions (user text primary key, key text)")

try:
    args.func(app, dbc, args)
except Error as err:
    print(err)
    

db.commit()
dbc.close()
db.close()
