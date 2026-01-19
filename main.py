from media_player import MediaPlayer

current_song = f"music/{input('Enter song to play: ')}.mp3"

media_player = MediaPlayer()

media_player.play_song(current_song)

while True:
    pass