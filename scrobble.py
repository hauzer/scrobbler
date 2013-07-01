import lfm

app = lfm.App("b3e7abc138f65a43803f887aeb36b9f6", "d60a1a4d704b71c0e8e5bac98d793969")
app.activate()



print(lfm.api.album.get_info("hauzzer", "Metallica", "Kill 'em all"))

print("asdas")
