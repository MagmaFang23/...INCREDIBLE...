import pygame, random, sys

pygame.init()
screen = pygame.display.set_mode((1440,810))
clock = pygame.time.Clock()

subtitle_font = pygame.font.Font("perpetua.ttf", 42)
title_font = pygame.font.Font("trajanpro.ttf", 69)

score = 0

# load assets and frames
jelly_0 = pygame.image.load('sprites/jelly_0.png')
jelly_1 = pygame.image.load('sprites/jelly_1.png')
jelly_2 = pygame.image.load('sprites/jelly_2.png')
ship_down = pygame.image.load('sprites/ship_down.png')
ship_up = pygame.image.load('sprites/ship_up.png')
ship_left_0 = pygame.image.load('sprites/ship_left_0.png')
ship_left_1 = pygame.image.load('sprites/ship_left_1.png')
ship_right_0 = pygame.image.load('sprites/ship_right_0.png')
ship_right_1 = pygame.image.load('sprites/ship_right_1.png')
bg_surface = pygame.image.load('sprites/bg_wallpaper.png')

bg_surface = pygame.transform.scale_by(bg_surface, 0.75)

bg_track = pygame.mixer.Sound('sounds/reflection_lofi.wav')
bg_track.set_volume(0.25)

jelly_pop = pygame.mixer.Sound('sounds/jellyfish_mini_death.wav')
jelly_pop.set_volume(0.5)

'''JELLY ANIMATION THINGS'''
jelly_0 = pygame.transform.scale_by(jelly_0, 1.5)
jelly_1 = pygame.transform.scale_by(jelly_1, 1.5)
jelly_2 = pygame.transform.scale_by(jelly_2, 1.5)

jelly_frames = [jelly_0, jelly_1, jelly_2]

def create_jellyfish(number_of_jellies):
    for jelly in range(number_of_jellies):
        jelly_position_x = random.randint(50, 1200)
        jelly_position_y = random.randint(120, 600)
        initial_frame = random.randint(0, len(jelly_frames) - 1)
        jelly_list.append([jelly_position_x, jelly_position_y, initial_frame, pygame.time.get_ticks()])
    return len(jelly_list)


#animation list
jelly_list = []
jelly_animation_speed = 400

def animate_jellyfish():
    current_time = pygame.time.get_ticks()
    for jelly in jelly_list:
        if current_time - jelly[3] >= jelly_animation_speed:
            jelly[2] = (jelly[2] + 1) % len(jelly_frames)
            jelly[3] = current_time
def render_jellyfish():
    for jelly in jelly_list:
        jelly_x, jelly_y, current_frame = jelly[:3]
        jelly_rect = jelly_frames[current_frame].get_rect(topleft=(jelly_x, jelly_y))
        screen.blit(jelly_frames[current_frame], jelly_rect.topleft)


'''SHIP ANIMATION THINGS'''
ship_down = pygame.transform.scale_by(ship_down, 2)
ship_up = pygame.transform.scale_by(ship_up, 2)
ship_left_0 = pygame.transform.scale_by(ship_left_0, 2)
ship_left_1 = pygame.transform.scale_by(ship_left_1, 2)
ship_right_0 = pygame.transform.scale_by(ship_right_0, 2)
ship_right_1 = pygame.transform.scale_by(ship_right_1, 2)

ship_frames = [ship_down, ship_up, ship_left_0, ship_left_1, ship_right_0, ship_right_1]
# ship_frames[] -- 0: down, 1: up, 2-3: left, 4-5: right

ship_initial_x = 720
ship_initial_y = 405

ship_x = ship_initial_x
ship_y = ship_initial_y
ship_init_direction = "right"
ship_current_frame = 0
ship_speed = 10
ship_animation_timer = 0
ship_animation_speed = 50


def animate_ship():
    global ship_current_frame, ship_animation_timer
    current_time = pygame.time.get_ticks()
    if current_time - ship_animation_timer >= ship_animation_speed:
        if ship_init_direction == "left":
            # left movement
            ship_current_frame = 2 + (ship_current_frame - 2 + 1) % 2
        elif ship_init_direction == "right":
            # right movement
            ship_current_frame = 4 + (ship_current_frame - 4 + 1) % 2
        ship_animation_timer = current_time
        # no need for up and down as they are one frame each.

def move_ship():
    global ship_x, ship_y, ship_init_direction, ship_current_frame
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        ship_init_direction = "up"
        ship_current_frame = 1
        ship_y -= ship_speed
    elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
        ship_init_direction = "down"
        ship_current_frame = 0
        ship_y += ship_speed
    elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
        ship_init_direction = "left"
        animate_ship()
        ship_x -= ship_speed
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        ship_init_direction = "right"
        animate_ship()
        ship_x += ship_speed

    # despawns and respawns ship whenever it touches the edge of the screen
    if ship_x < 0 or ship_x > screen.get_width() - ship_frames[0].get_width() or \
       ship_y < 0 or ship_y > screen.get_height() - ship_frames[0].get_height():
        reset_ship()

def reset_ship():
    global ship_x, ship_y, ship_init_direction, ship_current_frame
    ship_x, ship_y = ship_initial_x, ship_initial_y
    ship_init_direction = "right"
    ship_current_frame = 0


'''GAME MECHANICS'''
def collisions():
    global score, jelly_list
    ship_rect = ship_frames[ship_current_frame].get_rect(topleft=(ship_x, ship_y))
    for jelly in jelly_list[:]:
        jelly_x, jelly_y, current_frame = jelly[:3]
        jelly_rect = jelly_frames[current_frame].get_rect(topleft=(jelly_x, jelly_y))
        if ship_rect.colliderect(jelly_rect):
            jelly_pop.play()
            jelly_list.remove(jelly)  # remove jelly on collision
            score += 1

game_start_surface = pygame.image.load('sprites/title_screen.png').convert_alpha()
game_start_surface = pygame.transform.scale_by(game_start_surface, 0.75)
game_start_rect = game_start_surface.get_rect(topleft = (0,0))


game_active = False
show_credits = False

#colours r    g    b
BLACK = (0,   0,   0)
WHITE = (255, 255, 255)


title_x, title_y = 400, 90  # main title location
play_button_x, play_button_y = 1080, 105 # title screen play button location
credits_button_x, credits_button_y = 1080, 160 # title screen credits button location
quit_button_x, quit_button_y = 1080, 215 # title screen quit button location

def place_text(text, font, colour, x, y):
    surface = font.render(text, True, colour)
    rect = surface.get_rect(center=(x, y))
    return surface, rect

def render_title_screen():
    # render the title screen background
    screen.blit(game_start_surface, game_start_rect)
    # render the title text
    title_surface, title_rect = place_text('...INCREDIBLE...™', title_font, WHITE, title_x, title_y)
    screen.blit(title_surface, title_rect)
    # render the interactable buttons
    buttons = {}
    play_button_surface, play_button_rect = place_text('Play', subtitle_font, WHITE, play_button_x, play_button_y)
    credits_button_surface, credits_button_rect = place_text('Credits', subtitle_font, WHITE, credits_button_x, credits_button_y)
    quit_button_surface, quit_button_rect = place_text('Quit', subtitle_font, WHITE, quit_button_x, quit_button_y)
        # add terms to 'buttons' dictionary
    buttons['play'] = play_button_rect
    buttons['credits'] = credits_button_rect
    buttons['quit'] = quit_button_rect

    screen.blit(play_button_surface, play_button_rect)
    screen.blit(credits_button_surface, credits_button_rect)
    screen.blit(quit_button_surface, quit_button_rect)

    return buttons

def render_credits_screen():
    credits_lines = [
        "Developed by MagmaFang",
        "All sprites created by MagmaFang(hand-drawn)",
        "In-game background photo credit: Cristian Palmer (unsplash.com/@cristianpalmer)",
        "Background music credit: 'Reflection but it's lofi beats' by bits & hits",
        "(youtube.com/@FantasyLofi)",
        "Jelly pop sound credit: from in-game audio files of Hollow Knight"
    ]
    screen.fill(BLACK)
    line_spacing = 60
    base_x = 720
    base_y = 300

    # line spacing
    for index, line in enumerate(credits_lines):
        y_position = base_y + index * line_spacing
        credits_surface, credits_rect = place_text(line, subtitle_font, WHITE, base_x, y_position)
        screen.blit(credits_surface, credits_rect)

    back_button_surface, back_button_rect = place_text('Back', subtitle_font, WHITE, 720, base_y + len(credits_lines) * line_spacing + 50)
    screen.blit(back_button_surface, back_button_rect)
    return back_button_rect

def click_buttons(buttons, cursor_pos, click):
    for key, rect in buttons.items():
        if rect.collidepoint(cursor_pos) and click:
            return key

def score_display():
    score_surface = subtitle_font.render('Score: ' + str(score), True, (255, 255, 255))
    score_rect = score_surface.get_rect(center=(368, 69))
    screen.blit(score_surface, score_rect)


'''MAIN COMMAND'''
def run(game_active):
    global show_credits
    bg_track.play(loops=-1)
    while True:
        cursor_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if game_active:
            screen.blit(bg_surface, (0, 0))

            move_ship()
            screen.blit(ship_frames[ship_current_frame], (ship_x, ship_y))
            animate_jellyfish()
            collisions()
            render_jellyfish()
            score_display()

            if not jelly_list:
                global score
                score = 0
                game_active = False
                reset_ship()

        elif show_credits:
            back_button_rect = render_credits_screen()
            if back_button_rect.collidepoint(cursor_pos) and click:
                show_credits = False
        else:
            buttons = render_title_screen()
            choice = click_buttons(buttons, cursor_pos, click)
            if choice == 'play':
                game_active = True
                reset_ship()
                create_jellyfish(15)
            elif choice == 'credits':
                show_credits = True
            elif choice == 'quit':
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

run(game_active)


'''
Credits (copied from in-game credits screen):
All sprites created by MagmaFang (hand-drawn)
In-game background photo credit: Cristian Palmer (unsplash.com/@cristianpalmer)
Background music credit: 'Reflection but it's lofi beats' by bits & hits (youtube.com/@FantasyLofi)",
Jelly pop sound credit: from in-game audio files of the Hollow Knight game by Team Cherry

'''

# Input Instructions:
# Use the WASD or arrow keys to control the submarine ship! (& text buttons are self-explanatory)