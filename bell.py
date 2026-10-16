import pygame, threading
import sys, os
from time import sleep
from datetime import datetime
running = True
pygame.init()
screen = pygame.display.set_mode((5120, 3200), pygame.SCALED | pygame.FULLSCREEN)
clock = pygame.Clock()

# hvala patrik
def find_real_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)

default_font = 'assets/Montserrat-Bold.ttf'
fullscreen = False
time_offset = 0

# postavke zvona
sound = pygame.mixer.Sound(find_real_path('assets/09once.wav'))
loops_left = 0
RING_BELL_EVENT = pygame.USEREVENT + 2
rings = [
    27000,
    29700,
    30000,
    32700,
    33600,
    36300,
    36600,
    39300,
    39600,
    42300,
    42600,
    45300
]

def set_rtc_variables():
    global rtc, h, mins, hm, current_time
    rtc = datetime.now().strftime("%H:%M:%S")
    h = int(datetime.now().strftime("%H"))
    mins = int(datetime.now().strftime("%M"))
    s = int(datetime.now().strftime("%S"))
    temp = datetime.now().strftime("%H:%M").split(':')
    hm[0] = int(temp[0])
    hm[1] = int(temp[1])
    current_time = s+mins*60+h*3600
    current_time += time_offset

def zzyzx():
    global bell_started
    for i in range(3):
        sound.play()
        sleep(4.2)
    threading.Event().set()
    bell_started = False
    return

def render_font(txt, color, x, y, size=36, font=default_font):
    screen.blit(pygame.font.Font(find_real_path(font), size*4).render(txt, True, color), (x*4, y*4))

def draw_bg():
    screen.fill((63, 63, 63))

t1 = threading.Thread(target=zzyzx)

def play_bell():
    global bell_started
    if not bell_started:
        bell_started = True
        t1.start()

bell_started = False
rtc, h, mins, hm, current_time = 0, 0, 0, [0, 0], 0

index_in_rings = 0
set_rtc_variables()
for i in rings:
    if current_time >= i:
        index_in_rings += 1
index_in_rings %= 13
print(index_in_rings)

render_font('ŠKOLSKO ZVONO: REKREACIJA\nSADA OFFLINE', (255, 255, 255), 100, 64, 128, 'assets/Comic Sans MS.ttf')
pygame.display.flip()
sleep(2.5)

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
    render_font(f'integer time: {current_time}', (255, 255, 255), 100, 64)
    render_font(f'rtc: {rtc}', (255, 255, 255), 100, 100)
    if current_time >= rings[-1]:
        render_font('NASTAVA JE ZAVRŠENA', (255, 255, 255), 100, 136)
    else:
        render_font(f'{rings[index_in_rings]-current_time}s do zvona', (255, 255, 255), 100, 136)
    if current_time in rings:
        play_bell()
    pygame.display.flip()

pygame.quit()
