# Copyright (C) 2026 Leon (MrUsername7)
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
# along with this program.  If not, see <https://gnu.org>.

import math

import pygame, threading, sys, os
from time import sleep
from datetime import datetime
running = True
pygame.init()

fullscreen = True

BASE_WIDTH = 1280
BASE_HEIGHT = 800
WH_MULTI = 4 # ovo ili manje

WIDTH = BASE_WIDTH*WH_MULTI
HEIGHT = BASE_HEIGHT*WH_MULTI

screen = pygame.display.set_mode((WIDTH, HEIGHT), (pygame.SCALED if WH_MULTI >= 1 or fullscreen else 0) | pygame.FULLSCREEN)
clock = pygame.Clock()

version_info = 'FAZA 3 DEV'

# hvala patrik
def find_real_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

baloo2_bold = 'Baloo2/Baloo2-Bold.ttf'          # 700, Danas (viši), veliki odmor oznaka
baloo2_extrabold = 'Baloo2/Baloo2-Extraold.ttf' # 800, status / onaj "badge"/"sticker" (6. SAT, ODMOR, i PAUZA), učionica
lexend_regular = 'Lexend/Lexend-Regular.ttf'    # 400, do kraja sata, "Zvono u {vrijeme} · sada je {vrijeme}" tekst
lexend_medium = 'Lexend/Lexend-Medium.ttf'      # 500, checklist vremena
lexend_semibold = 'Lexend/Lexend-SemiBold.ttf'  # 600, odbrojavanje, nedovršeni satovi u checklist, "Zvono u {vrijeme} · sada je {vrijeme}" vrijeme
default_font = 'Montserrat-Bold.ttf'
kill_thread = False
checker_border_size = 4*WH_MULTI

# postavke zvona
sound = pygame.mixer.Sound(find_real_path('assets/very_ethical.mp3'))
RING_BELL_EVENT = pygame.USEREVENT + 2
bell_colours = {
    'sat': {
        'puno': 0x2f6fe4,
        'prazno': 0xe3ecfd
    },
    'odmor': {
        'puno': 0x127a50,
        'prazno': 0xdcf2e7
    },
    'kraj': {
        'prazno': 0xf1ebdf
    },
    'tekst': {
        'puno': 0x1f2a44
    }
}
rings = [
    27000, # 7:30
    29700, # 8:15
    30000, # 8:20
    32700, # 9:05
    33600, # 9:20
    36300, # 10:05
    36600, # 10:10
    39300, # 10:55
    39600, # 11:00
    42300, # 11:45
    42600, # 11:50
    45300, # 12:35
    45600, # 12:40
    48300  # 13:25
]

def fetch_colour(field: str, full: bool = False):
    return bell_colours.get(field).get('puno' if full else 'prazno')

class TimeConversion:
    @staticmethod
    def int_to_time(int_time:int):
        return f'{(int_time//3600)%24:02}:{(int_time//60)%60:02}:{int_time%60:02}'

def set_rtc_variables():
    global rtc, current_time, offset_time, offset_int_time
    dtnstrf = datetime.now().strftime
    rtc = dtnstrf("%H:%M:%S")
    h = int(dtnstrf("%H"))
    mins = int(dtnstrf("%M"))
    s = int(dtnstrf("%S"))
    current_time = s+mins*60+h*3600
    offset_int_time = current_time-time_offset
    offset_time = TimeConversion.int_to_time(offset_int_time)

def bell_player():
    global bell_started
    while True:
        if bell_started:
            sound.play()
            sleep(13.668)
            bell_started = False
        if kill_thread: return

def render_font(txt: str, color, x, y, size: int = 36, font_file : str = default_font):
    screen.blit(pygame.font.Font(find_real_path(f'assets/{font_file}'), int(size*WH_MULTI)).render(txt, True, color), (x*WH_MULTI, y*WH_MULTI))

def draw_bg():
    screen.fill((159,159,159))
    for x in range(40):
        for y in range(25):
            pygame.draw.rect(screen, 0xffffff, (x*(32*WH_MULTI)+checker_border_size//2, y*(32*WH_MULTI)+checker_border_size//2, (32*WH_MULTI)-checker_border_size, (32*WH_MULTI)-checker_border_size))
    pygame.draw.line(screen, 0xff0000, (48*WH_MULTI, 0), ( 48*WH_MULTI, HEIGHT), int(2.5*WH_MULTI))
    pygame.draw.circle(screen, 0xe8e9ec, ((1500+128*1.25)/4*WH_MULTI, (1500+32*0.75)/4*WH_MULTI), 312.5*WH_MULTI)
    pygame.draw.circle(screen, 0xffffff, ((1500+128*1.25)/4*WH_MULTI, (1500+32*0.75)/4*WH_MULTI), 307.5*WH_MULTI)
    full_clr = ((fetch_colour('odmor', 1) if odmor else fetch_colour('sat', 1)) if not offset_int_time >= rings[-1] else fetch_colour('kraj'))
    r = 275*WH_MULTI
    pygame.draw.circle(screen, full_clr, (cx, cy), r)
    if not offset_int_time >= rings[-1]:
      try:
        a1 = math.radians(90)
        a2 = math.radians((max(0.0, min(1.0, (offset_int_time - rings[index_in_rings - 1]) / (rings[index_in_rings] - rings[index_in_rings - 1]))) if rings[index_in_rings] != rings[index_in_rings - 1] else 0.0) * 360 + 90)
        pygame.draw.arc(screen, ((fetch_colour('odmor') if odmor else fetch_colour('sat')) if not offset_int_time >= rings[-1] else fetch_colour('kraj')), pygame.Rect(((1500 + 128 * 1.25) / 4 * WH_MULTI) - r, ((1500 + 32 * 0.75) / 4 * WH_MULTI) - r, r*2, r*2), a1, a2, int(50*WH_MULTI))
        pygame.draw.circle(screen, full_clr, (cx + (r - 50*WH_MULTI/2) * math.cos(a1), cy - (r - 50*WH_MULTI/2) * math.sin(a1)), 50*WH_MULTI/2)
        pygame.draw.circle(screen, full_clr, (cx + (r - 50*WH_MULTI/2) * math.cos(a2), cy - (r - 50*WH_MULTI/2) * math.sin(a2)), 50*WH_MULTI/2)
      except IndexError:
          pass
    pygame.draw.circle(screen, 0xffffff, ((1500+128*1.25)/4*WH_MULTI, (1500+32*0.75)/4*WH_MULTI), 225*WH_MULTI)

bell_thread = threading.Thread(target=bell_player)

bell_started = False
bell_thread.start()

def play_bell():
    global bell_started
    bell_started = not bell_started

rtc, current_time, offset_time, time_offset, offset_int_time = 0, 0, 0, 0, 0
time_offset = ( 6 * 3600 + # sati
               44 * 60 +   # minute
                0)         # sekunde

index_in_rings = 0
set_rtc_variables()
for _ in rings:
    if offset_int_time >= _:
        index_in_rings += 1
index_in_rings %= len(rings)

render_font('ŠKOLSKO ZVONO: REKREACIJA\nSADA OFFLINE', (255, 255, 255), 100, 64, 128, 'Comic Sans MS.ttf')
pygame.display.flip()
sleep(1)

odmor = False

cx = (1500 + 128 * 1.25) / 4 * WH_MULTI
cy = (1500 + 32 * 0.75) / 4 * WH_MULTI

try:
    while running:
        set_rtc_variables()
        odmor = (index_in_rings-1)/2 != (index_in_rings-1)//2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    play_bell()
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), (pygame.SCALED if WH_MULTI >= 1 or fullscreen else 0) | (pygame.FULLSCREEN if fullscreen else 0))

        clock.tick(50)
        draw_bg()
        school_ended = offset_int_time >= rings[-1]
        bell_font_size = 100 if school_ended else 150
        temp = rings[index_in_rings]-offset_int_time
        bell_time = f'{(temp//60):02}:{temp%60:02}' if not school_ended else str(offset_time)
        countdown_font = pygame.font.Font(find_real_path(f'assets/{lexend_semibold}'), bell_font_size)
        countdown_dims = countdown_font.size(bell_time)
        render_font(bell_time, fetch_colour('tekst',1), cx/WH_MULTI-countdown_dims[0]/2, cy/WH_MULTI-countdown_dims[1]/2, bell_font_size, lexend_semibold)
        if offset_int_time in rings and not bell_started:
            index_in_rings += 1
            play_bell()
        render_font(version_info, 0, 0, 0, 25)
        pygame.display.flip()
except KeyboardInterrupt as e:
    print(f'{e}\n{type(e).__name__}')

kill_thread = True
pygame.quit()
