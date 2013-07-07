# A Last.fm scrobbler and a now-playing status updater.
# Copyright (C) 2013  Никола Вукосављевић
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

import argparse
import sqlite3
import webbrowser
from tokenize_args import tokenize_args
import lfm


scrobble_parser = argparse.ArgumentParser(usage = "A scrobble consists of three or more\n" \
                                                  "options specified below. Pass these " \
                                                  "quoted,\nand as you would to a program.",
                                          add_help = False)

scrobble_parser.add_argument("artist", metavar = "artist")
scrobble_parser.add_argument("track", metavar = "track")
scrobble_parser.add_argument("timestamp", metavar = "timestamp")
scrobble_parser.add_argument("-a", "--album", metavar = "album")
scrobble_parser.add_argument("-d", "--duration", metavar = "duration")
scrobble_parser.add_argument("-m", "--mbid", metavar = "mbid")
scrobble_parser.add_argument("-t", "--track-number", metavar = "track_number", dest="tracknumber")
scrobble_parser.add_argument("-aa", "--album-artist", metavar = "album_artist", dest="albumartist")
scrobble_parser.add_argument("-s", "--stream-id", metavar = "stream_id", dest="streamid")
scrobble_parser.add_argument("-c", "--chosen-by-user", action = "store_true", dest="chosenbyuser")
scrobble_parser.add_argument("-cx", "--context", metavar = "context")


parser = argparse.ArgumentParser(description = "A Last.fm scrobbler and a now-playing status updater.",
                                 formatter_class = argparse.RawTextHelpFormatter)

parser.add_argument("user")
parser.add_argument("-p", "--password", metavar = "password")
parser.add_argument("-s", "--scrobble", action = "append", metavar = "\"artist track tstamp ...\"",
                    dest = "scrobbles", help = scrobble_parser.format_help())

args = parser.parse_args()


scrobbles = []
for scrobble in args.scrobbles:
    scrobbles.append(lfm.Scrobble(**vars(scrobble_parser.parse_args(tokenize_args(scrobble)))))


app = lfm.App("b3e7abc138f65a43803f887aeb36b9f6", "d60a1a4d704b71c0e8e5bac98d793969", "lfm.dat")

dbconn = sqlite3.connect("sessions.db")
dbcur = dbconn.cursor()

try:
    dbcur.execute("create table sessions (user text primary key, key text)")
except sqlite3.OperationalError:
    pass

if args.password is not None:
    session = app.auth.get_mobile_session(args.user, args.password)
    
else:
    dbcur.execute("select * from sessions where user == ?", (args.user,))
    session = dbcur.fetchone()
    
    try:
        app.sk = session[1]
        
    except TypeError:
        token = app.auth.get_token()
        
        input("\nThe Last.fm authentication page will be opened now, or its URL printed here.\nPress enter to continue.\n")
        
        try:
            webbrowser.open(token.url)
        except webbrowser.Error:
            print(token.url)
    
        input("Press enter after granting access.")
        session = app.auth.get_session(token)

if app.sk is None:
    app.sk = session["key"]
    
    try:
        dbcur.execute("insert into sessions (user, key) values (?, ?)", (session["name"], session["key"]))
    except sqlite3.IntegrityError:
        pass

dbconn.commit()
dbcur.close()
dbconn.close()


app.track.scrobble(scrobbles)
