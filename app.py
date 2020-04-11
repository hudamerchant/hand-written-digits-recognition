import pygame
from  process_image import process
import os

black       = [0, 0, 0]
white       = [255, 255, 255]
active      = False
last_pos    = (0, 0)
color       = (255, 128, 0)
radius      = 4
font_size   = 500


# initializing screen
width   = 1240
height  = 300

screen = pygame.display.set_mode((width, height*2))
screen.fill(white)
pygame.font.init()



def show_output(img):
    bg = pygame.pixelcopy.make_surface(img)
    bg = pygame.transform.rotate(bg, -270)
    bg = pygame.transform.flip(bg, 0, 1)
    screen.blit(bg, (0, height+2))

def crop(img):
    cropped = pygame.Surface((width-5, height-5))
    cropped.blit(img, (0, 0), (0, 0, width-5, height-5))
    return cropped


def roundline(srf, color, start, end, radius=1):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = max(abs(dx), abs(dy))
    for i in range(distance):
        x = int(start[0] + float(i) / distance * dx)
        y = int(start[1] + float(i) / distance * dy)
        pygame.draw.circle(srf, color, (x, y), radius)

try:
    while True:

        e = pygame.event.wait()
        pygame.draw.line(screen, black, [0, height], [width,height ], 10)

        # clear screen after right click
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button == 3):
            screen.fill(white)

        # quit
        if e.type == pygame.QUIT:
            raise StopIteration

        # start drawing after left click
        if(e.type == pygame.MOUSEBUTTONDOWN and e.button != 3):
            color = black
            pygame.draw.circle(screen, color, e.pos, radius)
            active = True

        # stop drawing after releasing left click
        if e.type == pygame.MOUSEBUTTONUP and e.button != 3:
            active = False
            fname = "out.png"

            img = crop(screen)
            pygame.image.save(img, fname)

            output = process(fname)
            show_output(output)
           
        # start drawing line on screen if active is true
        if e.type == pygame.MOUSEMOTION:
            if active:
                pygame.draw.circle(screen, color, e.pos, radius)
                roundline(screen, color, e.pos, last_pos, radius)
            last_pos = e.pos

        pygame.display.flip()

except StopIteration:
    fname = "out.png"
    if os.path.exists(fname):
        os.remove(fname)

pygame.quit()