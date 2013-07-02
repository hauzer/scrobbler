import lfm
import argparse
from tokenize_args.tokenize_args import tokenize_args

parser = argparse.ArgumentParser(prog = "scrobble",
                                 description="A Last.fm scrobbler and a now-playing status updater.")

parser.add_argument("-s", "--scrobble", action="append")
args = parser.parse_args()

scrobble_parser = argparse.ArgumentParser()
scrobble_parser.add_argument("artist")
scrobble_parser.add_argument("track")
scrobble_parser.add_argument("timestamp")
scrobble_parser.add_argument("-a", "--album")
scrobble_parser.add_argument("-d", "--duration")
scrobble_parser.add_argument("-m", "--mbid")
scrobble_parser.add_argument("-t", "--tracknumber")
scrobble_parser.add_argument("-aa", "--albumartist")
scrobble_parser.add_argument("-s", "--streamid")
scrobble_parser.add_argument("-c", "--chosenbyuser")
scrobble_parser.add_argument("-cx", "--context")

scrobbles = []
for scrobble in args.scrobble:
    scrobbles.append(lfm.Scrobble(**vars(scrobble_parser.parse_args(tokenize_args(scrobble)))))


app = lfm.App("b3e7abc138f65a43803f887aeb36b9f6", "d60a1a4d704b71c0e8e5bac98d793969")
app.activate()

lfm.api.track.scrobble(scrobbles)
