import pygame 
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Welome To The Rice Field!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH//2, 0, 10, HEIGHT)

bullet_hit_sound = pygame.mixer.Sound(os.path.join('Pygame/Assets/Grenade+1.mp3'))
bullet_fire_sound_1 = pygame.mixer.Sound(os.path.join('Pygame/Assets/TBMA.mp3'))
bullet_fire_sound_2 = pygame.mixer.Sound(os.path.join('Pygame/Assets/Gun+Silencer.mp3'))


health_font = pygame.font.SysFont('comicsans', 40)
winner_font = pygame.font.SysFont('comcsans', 100)

FPS = 60
VEL = 5
bullet_vel =   7
max_bullets = 3
space_witdh, spaceship_height = 100, 80

yellow_hit = pygame.USEREVENT + 1 
red_hit = pygame.USEREVENT + 2

yellow_spaceship_image = pygame.image.load(os.path.join('Pygame', 'Assets', 'trandan.png'))
yellow_spaceship = pygame.transform.rotate(pygame.transform.scale(yellow_spaceship_image, (space_witdh, spaceship_height)),  90)
red_spaceship_image = pygame.image.load(os.path.join('Pygame', 'Assets', 'dan2.png'))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(red_spaceship_image, (space_witdh, spaceship_height)),  270)
space = pygame.transform.scale(pygame.image.load(os.path.join('Pygame', 'Assets', 'rice-field-1.png')), (WIDTH, HEIGHT))

        
def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(space, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER )
    
    red_health_text = health_font.render('Health:   ' + str(red_health), 1, WHITE)
    yellow_health_text = health_font.render('Health:   ' + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, ( 10, 10))
    
    
    WIN.blit(yellow_spaceship, (yellow.x, yellow.y))
    WIN.blit(red_spaceship, (red.x, red.y))
    
    
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet )
        
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet )
        
        
    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: #LEFT
        yellow.x  -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x: #right
        yellow.x  += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: #up
        yellow.y  -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15: #down
        yellow.y  += VEL       
        
def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: #LEFT
        red.x  -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: #right
        red.x  += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: #up
        red.y  -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15: #down
        red.y  += VEL
        
        
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(red_hit))
            yellow_bullets.remove(bullet)
        elif bullet.x >WIDTH:
            yellow_bullets.remove(bullet)
            
    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(yellow_hit))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
            
def draw_winner(text):
    draw_text = winner_font.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/ 2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)
    



def main():
    red = pygame.Rect(700, 300, space_witdh, spaceship_height)
    yellow = pygame.Rect(100, 300, space_witdh, spaceship_height)
    
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
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    bullet_fire_sound_1.play()
                    
                    
                if event.key == pygame.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    bullet_fire_sound_2.play()
                    
                    
            if event.type == red_hit:
                red_health -= 1
                bullet_hit_sound.play()
            
            if event.type == yellow_hit:
                yellow_health -= 1
                bullet_hit_sound.play()
        
        winner_text = ""        
        if red_health <= 0:
            winner_text = "Tran Dan Wins!"
            
        if yellow_health <=0:
            winner_text = "Random Man Wins..."
            
        if winner_text != "":
            draw_winner(winner_text)
            break
            
        
        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)
            
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            
    pygame.quit()
    
    
if __name__  == "__main__":
    main()