import argparse
from tokenize_args.tokenize_args import tokenize_args
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
parser.add_argument("password")
parser.add_argument("-s", "--scrobble", action = "append", metavar = "\"artist track tstamp ...\"",
                    dest = "scrobbles", help = scrobble_parser.format_help())

args = parser.parse_args()


app = lfm.App("b3e7abc138f65a43803f887aeb36b9f6", "d60a1a4d704b71c0e8e5bac98d793969")
app.sk = lfm.api.auth.get_mobile_session(args.user, args.password)

scrobbles = []
for scrobble in args.scrobbles:
    scrobbles.append(lfm.Scrobble(**vars(scrobble_parser.parse_args(tokenize_args(scrobble)))))

lfm.api.track.scrobble(scrobbles)
