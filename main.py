import pygame
import random
import time
pygame.font.init()

#create a window
WIDTH, HEIGHT = 1200, 650
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Boo Kandy")

#load images
BG = pygame.transform.scale(pygame.image.load("bg.png"),(WIDTH,HEIGHT))
GHOST = pygame.image.load("Boo.png")
CANDY = pygame.image.load("Kandy.png")

#player
PLAYER_WIDTH = 120
PLAYER_HEIGHT = 160
PLAYER_VEL = 15

#font
FONT = pygame.font.SysFont("comicsans",30)

#candy
CANDY_WIDTH = 100
CANDY_HEIGHT = 120
CANDY_VEL = 10

def draw(player,elapsed_time,candies,count):
    WIN.blit(BG,(0,0))
    WIN.blit(GHOST,player)
    time_text = FONT.render(f"Time: {round(elapsed_time)}s",1,"black")
    WIN.blit(time_text,(10,10))
    for candy in candies:
        WIN.blit(CANDY,candy)
    count_text = FONT.render(f"Candy: {count}",1,"black")
    WIN.blit(count_text,(WIDTH-150,10))

    pygame.display.update()

def main():
    run = True

    player = pygame.Rect(200,HEIGHT-PLAYER_HEIGHT,
                         PLAYER_WIDTH,PLAYER_HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    candy_inc = 500
    candy_count = 0

    candies = []
    hit = True

    count = 0

    while run:
        candy_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if candy_count > candy_inc:
            candy_x = random.randint(0,WIDTH-CANDY_WIDTH)
            candy = pygame.Rect(candy_x,-CANDY_HEIGHT,CANDY_WIDTH,CANDY_HEIGHT)
            candies.append(candy)

            candy_inc = min(700,candy_count+50)
            candy_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x-PLAYER_VEL>=0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x+PLAYER_WIDTH+PLAYER_VEL<=WIDTH:
            player.x += PLAYER_VEL
        
        for candy in candies[:]:
            candy.y += CANDY_VEL
            if candy.y + candy.height >= player.height and candy.colliderect(player):
                count += 1
                candies.remove(candy)
            elif candy.y > HEIGHT:
                candies.remove(candy)
                hit = False
                break
        
        if not hit:
            lost_text = FONT.render("GAME OVER",1,"black")
            WIN.blit(lost_text,(WIDTH/2-lost_text.get_width()/2, HEIGHT/2-lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player,elapsed_time,candies,count)

    pygame.quit()

if __name__ == "__main__":
    main()