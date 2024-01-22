import pygame
import os
pygame.font.init()
pygame.mixer.init()

# important stuff, variables
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("🚀Space Battles!🚀")

red_orientation = 270
yellow_orientation = 90


    #colours
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)

# Imported sound effects
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')
background_music = pygame.mixer.Sound('Assets/bgmusic.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 50)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Images

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), yellow_orientation)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), red_orientation)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'spacebg.webp')), (WIDTH, HEIGHT))

#GAME LOOP
def play():
    #FUNCTIONS TO ROTATE SPACESHIPS
    def rotate_red():
        rotated_red_ship = pygame.transform.rotate(RED_SPACESHIP_IMAGE, red_orientation)
        return pygame.transform.scale(rotated_red_ship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

    def rotate_yellow():
        rotated_yellow_ship = pygame.transform.rotate(YELLOW_SPACESHIP_IMAGE, yellow_orientation)
        return pygame.transform.scale(rotated_yellow_ship, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

    #puts stuff on the screen
    def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
        WIN.blit(SPACE, (0, 0))

        #ROCK
        #rockWIDTH = 20
        #rockLENGTH = 60
        #rock1 = pygame.Rect(500,100,rockWIDTH,rockLENGTH)
        #pygame.draw.rect(WIN,RED,rock1)
        

        red_health_text = HEALTH_FONT.render(
            "Health: " + str(red_health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render(
            "Health: " + str(yellow_health), 1, WHITE)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text, (10, 10))
        
        # replace the old red spaceship with the rotated one
        rotated_red_spaceship = rotate_red()
        rotated_yellow_spaceship = rotate_yellow()
        
        WIN.blit(rotated_yellow_spaceship, (yellow.x, yellow.y))
        WIN.blit(rotated_red_spaceship, (red.x, red.y))

        for bullet in red_bullets:
            pygame.draw.rect(WIN, RED, bullet)

        for bullet in yellow_bullets:
            pygame.draw.rect(WIN, YELLOW, bullet)

        pygame.display.update()

    #yellow keys
    def yellow_handle_movement(keys_pressed, yellow):
        if keys_pressed[pygame.K_w] and yellow.y-VEL>0: # Up
                yellow.y -= VEL
        if keys_pressed[pygame.K_s] and yellow.y+VEL +yellow.height<HEIGHT: # Down
                yellow.y += VEL
        if keys_pressed[pygame.K_a] and yellow.x-VEL>0: # Left
                yellow.x -= VEL
        if keys_pressed[pygame.K_d] and yellow.x+VEL + yellow.width<WIDTH: # Right
                yellow.x += VEL

    #Red keys
    def red_handle_movement(keys_pressed, red):
        if keys_pressed[pygame.K_UP] and red.y-VEL>0: # Up
                red.y -= VEL
        if keys_pressed[pygame.K_DOWN] and red.y+VEL +red.height<HEIGHT: # Down
                red.y += VEL
        if keys_pressed[pygame.K_LEFT] and red.x-VEL>0: # Left
                red.x -= VEL
        if keys_pressed[pygame.K_RIGHT] and red.x+VEL + red.width<WIDTH: # Right
                red.x += VEL

    #0 = down
    #90 = right
    #180 up
    #270 = left
            
    #the code to move the bullets
    def handle_bullets(yellow_bullets, red_bullets, yellow, red):

        for bullet in yellow_bullets:
            if bullet.x > WIDTH or bullet.x<0 or bullet.y<0 or bullet.y>HEIGHT:
                yellow_bullets.remove(bullet)

            elif yellow_orientation == 270:
                bullet.x -= BULLET_VEL

            elif yellow_orientation == 90:
                bullet.x += BULLET_VEL

            elif yellow_orientation == 180:
                bullet.y -= BULLET_VEL

            elif yellow_orientation == 0:
                bullet.y += BULLET_VEL

            if red.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                yellow_bullets.remove(bullet)
            
            #ROCK!!!!!!!!!!
            #if bullet.colliderect(rock1):
                #yellow_bullets.remove(bullet)
            

        for bullet in red_bullets:
            if bullet.x > WIDTH or bullet.x<0 or bullet.y<0 or bullet.y>HEIGHT:
                red_bullets.remove(bullet)

            elif red_orientation == 270:
                bullet.x -= BULLET_VEL

            elif red_orientation == 90:
                bullet.x += BULLET_VEL

            elif red_orientation == 180:
                bullet.y -= BULLET_VEL

            elif red_orientation == 0:
                bullet.y += BULLET_VEL

            if yellow.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                red_bullets.remove(bullet)

    #text for who won
    def draw_winner(text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                            2, HEIGHT/2 - draw_text.get_height()/2))
        
        pygame.display.update()
        pygame.time.delay(2000)
        background_music.stop()
        play()

    #the main loop
    def main():
        global yellow_orientation
        global red_orientation
        background_music.play()
        red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

        red_bullets = []
        yellow_bullets = []

        red_health = 10
        yellow_health = 10

        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()


                #0 = down
                #90 = right
                #180 up
                #270 = left
                 
                    
                #SPAWNING BULLETS
                if event.type == pygame.KEYDOWN:
                    #YELLOW!!!!!!!!!
                    if event.key == pygame.K_q and len(yellow_bullets) < MAX_BULLETS:
                        if yellow_orientation == 90 and len(yellow_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                            yellow_bullets.append(bullet)

                        if yellow_orientation == 270 and len(yellow_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(yellow.x, yellow.y + yellow.height//2 - 2, 10, 5)
                            yellow_bullets.append(bullet)

                        if yellow_orientation == 180 and len(yellow_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(yellow.x+yellow.width/2 -5, yellow.y + yellow.height//2 - 2, 10, 5)
                            yellow_bullets.append(bullet)

                        if yellow_orientation == 0 and len(yellow_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(yellow.x+yellow.width/2 -5, yellow.y - yellow.height//2 + 40, 10, 5)
                            yellow_bullets.append(bullet)

                        BULLET_FIRE_SOUND.play()

                    #RED!!!!!!!!!!!!
                    if event.key == pygame.K_SPACE and len(red_bullets) < MAX_BULLETS:
                        if red_orientation == 270 and len(red_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(red.x + red.width, red.y + red.height//2 - 2, 10, 5)
                            red_bullets.append(bullet)

                        if red_orientation == 90 and len(red_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5)
                            red_bullets.append(bullet)

                        if red_orientation == 180 and len(red_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(red.x+red.width/2 -5, red.y + red.height//2 - 2, 10, 5)
                            red_bullets.append(bullet)

                        if red_orientation == 0 and len(red_bullets) < MAX_BULLETS:
                            bullet = pygame.Rect(red.x+red.width/2 -5, red.y - red.height//2 + 40, 10, 5)
                            red_bullets.append(bullet)


                        BULLET_FIRE_SOUND.play()

            #TURNING SPACESHIP!!!!!!!!!!!!!!!!
                        
                    #YELLOW
                    if event.key == pygame.K_r: #turn right
                        yellow_orientation
                        yellow_orientation = (yellow_orientation - 90)
                        if yellow_orientation<0:
                            yellow_orientation = 360

                    if event.key == pygame.K_e: # Turn left
                        yellow_orientation = (yellow_orientation + 90)
                        if yellow_orientation>360:
                            yellow_orientation = 0

                    #RED
                    if event.key == pygame.K_RCTRL: # Turn right
                        red_orientation
                        red_orientation = (red_orientation - 90)
                        if red_orientation<0:
                            red_orientation = 360

                    if event.key == pygame.K_RALT: # Turn left
                        red_orientation = (red_orientation + 90)
                        if red_orientation>360:
                            red_orientation = 0


                # GETTING HIT
                if event.type == RED_HIT:
                    red_health -= 1
                    BULLET_HIT_SOUND.play()

                if event.type == YELLOW_HIT:
                    yellow_health -= 1
                    BULLET_HIT_SOUND.play()
    # Checks who won
            winner_text = ""
            if red_health <= 0:
                winner_text = "Yellow Wins!"

            if yellow_health <= 0:
                winner_text = "Red Wins!"

            if winner_text != "":
                draw_winner(winner_text)
                break

            keys_pressed = pygame.key.get_pressed()
            yellow_handle_movement(keys_pressed, yellow)
            red_handle_movement(keys_pressed, red)

            handle_bullets(yellow_bullets, red_bullets, yellow, red)

            draw_window(red, yellow, red_bullets, yellow_bullets,
                        red_health, yellow_health)
            

    if __name__ == "__main__":
        main()



MENU_FONT = pygame.font.SysFont('comicsans', 20)

#The text
def draw_menu(text):
        draw__menu_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw__menu_text, (WIDTH/2 - draw__menu_text.get_width() /
                            2, HEIGHT/2 - 100))
def draw_rules1(text):
        draw__menu_text = MENU_FONT.render(text, 1, WHITE)
        WIN.blit(draw__menu_text, (WIDTH/2 - draw__menu_text.get_width() /
                            2, HEIGHT/2 - 10))
def draw_rules_p1(text, xvalue):
        draw__menu_text = MENU_FONT.render(text, 1, WHITE)
        WIN.blit(draw__menu_text, (230, xvalue))
def draw_rules_p2(text, xvalue):
        draw__menu_text = MENU_FONT.render(text, 1, WHITE)
        WIN.blit(draw__menu_text, (500, xvalue))

MENUBG = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'start_bg.jpg')), (WIDTH, HEIGHT))
menu_bgm = pygame.mixer.Sound('Assets/menu_music.mp3')

#MENU SCREEN
def menu():
    WIN.blit(MENUBG, (0, 0))
    menu_bgm.play()

    draw_menu("SPACE BATTLE!")
    draw_rules1("Shoot the other player. Control the bullets using the force. You each have 10 lives.")
    draw_rules_p1("P1: WASD", 310)
    draw_rules_p1("Q = Shoot", 330)
    draw_rules_p1("E = Left Rotate", 350)
    draw_rules_p1("R = Right Rotate", 370)

    draw_rules_p2("P2: ARROW KEYS", 310)
    draw_rules_p2("SPACE = Shoot", 330)
    draw_rules_p2("RALT = Left Rotate", 350)
    draw_rules_p2("RCTRL = Right Rotate", 370)

    pygame.display.update()
    pygame.time.delay(6000)
    menu_bgm.stop()
    play()

menu()