import pygame
from Presets import *

class SoundController:
    def __init__(self):
        self.music_volume = 1.0 # Full volume
        self.sfx_volume = 1.0 # Full volume
        self.mute_music = False
        self.mute_sfx = False
        self.current_song = None
        pygame.mixer.init()

    
    def update(self):
        self.playMusic(background_track)

    def playMusic(self, song_file, repeat=True, overwrite=False):
        """Plays a music file in an infinite loop, unless repeat is set to False"""
        if not pygame.mixer.get_busy():
            pygame.mixer.music.unpause()
        if self.current_song == song_file and not overwrite:
            return
        pygame.mixer.music.load(song_file)
        if self.mute_music:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(self.music_volume)
        pygame.mixer.music.play(-1 if repeat else 0)
        self.current_song = song_file
    
    def stopMusic(self):
        pygame.mixer.music.stop()

    def playSoundEffect(self, sfx_file):
        pygame.mixer.music.pause()
        if self.mute_sfx:
            return
        """Plays a sound effect once"""
        sfx = pygame.mixer.Sound(sfx_file)
        sfx.set_volume(self.sfx_volume)
        sfx.play()

    def setMusicVolume(self, volume):
        self.mute_music = False
        """Sets the volume of the music (0.0 to 1.0)"""
        if(volume < -0.04 or volume > 1.04):
            return
        self.music_volume = volume
        pygame.mixer.music.set_volume(volume)

    def setSfxVolume(self, volume):
        self.mute_sfx = False
        """Sets the volume of the sound effects (0.0 to 1.0)"""
        if(volume < -0.04 or volume > 1.04):
            return
        self.sfx_volume = volume
    
    def toggleMuteMusic(self):
        self.mute_music = not self.mute_music
        pygame.mixer.music.set_volume(0 if self.mute_music else self.music_volume)
    
    def toggleMuteSfx(self):
        self.mute_sfx = not self.mute_sfx
    
    def toggleMuteAll(self):
        if self.mute_music and not self.mute_sfx:
            self.toggleMuteSfx()
        elif not self.mute_music and self.mute_sfx:
            self.toggleMuteMusic()
        else:
            self.toggleMuteSfx()
            self.toggleMuteMusic()
    
    def getMusicState(self):
        if self.mute_music:
            return "MUTE"
        else:
            return str(round(100*self.music_volume))
    
    def getSfxState(self):
        if self.mute_sfx:
            return "MUTE"
        else:
            return str(round(100*self.sfx_volume))