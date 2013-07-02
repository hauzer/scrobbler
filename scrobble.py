import argparse
from tokenize_args.tokenize_args import tokenize_args
import lfm


scrobble_parser = argparse.ArgumentParser(usage = "A scrobble consists of three or more\n" \
                                                  "options specified below. Pass these " \
                                                  "quoted,\nand as you would to a program.",
                                          add_help = False)

scrobble_parser.add_argument("artist", metavar = "Artist")
scrobble_parser.add_argument("track", metavar = "Track")
scrobble_parser.add_argument("timestamp", metavar = "Timestamp")
scrobble_parser.add_argument("-a", "--album", metavar = "Album")
scrobble_parser.add_argument("-d", "--duration", metavar = "Duration")
scrobble_parser.add_argument("-m", "--mbid", metavar = "MBID")
scrobble_parser.add_argument("-t", "--track-number", metavar = "TrackNumber", dest="tracknumber")
scrobble_parser.add_argument("-aa", "--album-artist", metavar = "AlbumArtist", dest="albumartist")
scrobble_parser.add_argument("-s", "--stream-id", metavar = "StreamID", dest="streamid")
scrobble_parser.add_argument("-c", "--chosen-by-user", metavar = "ChosenByUser?",
                             choices = ["0", "1"], dest="chosenbyuser")
scrobble_parser.add_argument("-cx", "--context", metavar = "Context")


parser = argparse.ArgumentParser(description = "A Last.fm scrobbler and a now-playing status updater.",
                                 formatter_class = argparse.RawTextHelpFormatter)

parser.add_argument("-s", "--scrobble", action = "append", metavar = "\"Artist Track Tstamp ...\"",
                    dest = "scrobbles", help = scrobble_parser.format_help())


args = parser.parse_args()

scrobbles = []
for scrobble in args.scrobbles:
    scrobbles.append(lfm.Scrobble(**vars(scrobble_parser.parse_args(tokenize_args(scrobble)))))


app = lfm.App("b3e7abc138f65a43803f887aeb36b9f6", "d60a1a4d704b71c0e8e5bac98d793969")
app.activate()

lfm.api.track.scrobble(scrobbles)
