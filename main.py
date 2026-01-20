from media_player import MediaPlayer

media_player = MediaPlayer("music/")

media_player.preview_song_titles()

current_song = media_player.song_title_to_song(input('Enter song to play: '))

media_player.play_song(current_song)

while True:
    pass