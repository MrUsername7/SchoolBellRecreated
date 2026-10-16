import pygame, threading
import sys, os
from time import sleep
from datetime import datetime
running = True
pygame.init()
screen = pygame.display.set_mode((5120, 3200), pygame.SCALED | pygame.FULLSCREEN)
clock = pygame.Clock()

version_info = 'FAZA 1'

# hvala patrik
def find_real_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

default_font = 'Montserrat-Bold.ttf'
fullscreen = False
kill_thread = False

# postavke zvona
sound = pygame.mixer.Sound(find_real_path('assets/09once.wav'))
loops_left = 0
RING_BELL_EVENT = pygame.USEREVENT + 2
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

class TimeConversion:
    @staticmethod
    def int_to_time(int_time:int):
        return f'{(int_time//3600)%24:02}:{(int_time//60)%60:02}:{int_time%60:02}'

def set_rtc_variables():
    global rtc, current_time, offset_time, offset_int_time
    rtc = datetime.now().strftime("%H:%M:%S")
    h = int(datetime.now().strftime("%H"))
    mins = int(datetime.now().strftime("%M"))
    s = int(datetime.now().strftime("%S"))
    current_time = s+mins*60+h*3600
    offset_int_time = current_time-time_offset
    offset_time = TimeConversion.int_to_time(offset_int_time)

def zzyzx():
    global bell_started
    while True:
        if bell_started:
            for i in range(3):
                sound.play()
                sleep(4.2)
            bell_started = False
        if kill_thread:
            return

def render_font(txt: str, color, x:int, y:int, size:int=36, font_file:str=default_font):
    screen.blit(pygame.font.Font(find_real_path(f'assets/{font_file}'), size*4).render(txt, True, color), (x*4, y*4))

def draw_bg():
    screen.fill((63, 63, 63))

t1 = threading.Thread(target=zzyzx)

bell_started = False
t1.start()

def play_bell():
    global bell_started
    bell_started = (True if not bell_started else False)

rtc, current_time, offset_time, time_offset, offset_int_time = 0, 0, 0, 0, 0
#time_offset = ( 3 * 3600 + # sati
#               50 * 60 +   # minute
#                0)         # sekunde

index_in_rings = 0
set_rtc_variables()
for i in rings:
    if offset_int_time >= i:
        index_in_rings += 1
index_in_rings %= len(rings)

render_font('ŠKOLSKO ZVONO: REKREACIJA\nSADA OFFLINE', (255, 255, 255), 100, 64, 128, 'Comic Sans MS.ttf')
pygame.display.flip()
sleep(1)

try:
    while running:
        set_rtc_variables()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    play_bell()

        clock.tick(50)
        draw_bg()
        render_font(version_info, (255, 255, 255), 0, 0, 25)
        render_font(f'current int time: {current_time}', (255, 255, 255), 100, 100)
        render_font(f'current time: {rtc}', (255, 255, 255), 100, 136)
        render_font(f'represented int time: {offset_int_time}', (255, 255, 255), 100, 172)
        render_font(f'represented time: {offset_time}', (255, 255, 255), 100, 208)
        if offset_int_time >= rings[-1]:
            render_font('NASTAVA JE ZAVRŠENA', (255, 255, 255), 100, 244)
        else:
            temp = rings[index_in_rings]-offset_int_time
            render_font(''
                       f'{(temp//60):02}:'
                       f'{temp%60:02} '
                        'do zvona', (255, 255, 255), 100, 244)
        if offset_int_time in rings:
            index_in_rings += 1
            play_bell()
        pygame.display.flip()
except BaseException as e:
    print(f'{e}\n{type(e).__name__}')

kill_thread = True
pygame.quit()
