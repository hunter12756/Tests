import pygame
import math
from pygame.math import Vector2
import time
import random
windowW = 800
windowH = 600

black= (0,0,0)
white= (255,255,255)
silver= (192,192,192)
maroon = (128,0,0)
olive = (128,128,0)
yellow= (219,219,26)
lime = (50,205,50)
class User(pygame.sprite.Sprite):
    def __init__(self, pos= (250,250)):
        super(User, self).__init__()
        self.image = pygame.Surface([20, 40], pygame.SRCALPHA)
        self.image.fill(silver) #user sprite is white
        self.original_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.position = Vector2(pos) #size part of vector
        self.direction = Vector2(0, -1) #distance part of vector
        self.speed = 0
        self.angle_speed = 0
        self.angle = 0
    def update(self):
        if self.angle_speed != 0:
            self.direction.rotate_ip(self.angle_speed) #updates the speed and direction the player is going in
            self.angle += self.angle_speed #updates the direction of the player to where it is currently facing
            self.image = pygame.transform.rotate(self.original_image, -self.angle) #only uses update angle to move the entire player sprite
            self.rect = self.image.get_rect(midtop=self.rect.midtop) #re-centers
        # updates the direction and position of the player
        self.position += self.direction * self.speed
        self.rect.center = self.position #re-centers

class Enemy(pygame.sprite.Sprite):
    def __init__(self,color,width,height):
        super().__init__()
        self.image= pygame.Surface([width,height])
        self.image.fill(lime)
        self.rect = self.image.get_rect()
    def draw(self):
        self.rect.y = random.randrange(-200,600)
        self.rect.x = random.randrange(0,800)
    def collision(self,orb_group,user):
        for i in orb_group:
            if self.rect.colliderect(i.rect):
                    self.kill
                    i.kill
                    print("BOOM")
    def update(self):
        self.rect.y += random.randrange(0,3)
        self.rect.x += random.randrange(0,5)
        
        if self.rect.x > 800 or self.rect.y > 600:
            self.kill()

class Orb(pygame.sprite.Sprite): #makes orbs
    def __init__(self, pos, direction, angle): #uses position and direction of the Player sprite
        
        super(Orb, self).__init__()
        self.image = pygame.Surface([4, 10], pygame.SRCALPHA)
        self.image.fill(yellow) #ors are maroon
        self.image = pygame.transform.rotozoom(self.image, -angle, 1) #follows angle of the player (y coords are flipped cuz its inverted)
        self.rect = self.image.get_rect(center=pos) #center of the bullet Sprite is center of the Player
        self.position = Vector2(pos)  # size of vector
        self.velocity = direction * 10
    def update(self): #moves bullet
        self.position += self.velocity  #speed
        self.rect.center = self.position  #hitbox
        #deltes the orbs if they go off the screen
        if self.rect.x < 0 or self.rect.x > windowW or self.rect.y < 0 or self.rect.y > windowH:
            self.kill()
def shootingorb(all_sprites_list,orb_group,user): #condense shooting animation
    pygame.key.set_repeat(2,1)                 
    orb = Orb(user.rect.center, user.direction, user.angle)
    all_sprites_list.add(orb)
    orb_group.add(orb)
    
    
    soundeffect = pygame.mixer.Sound("laser2.wav") #this is a downloaded wave file
    soundeffect.play() #adds sound to the shooting animation   
def enemyspawn(all_sprites_list, orb_group, user):
    alien= Enemy( lime , 20 , 20 )
    alien.rect.x= random.randrange(800)
    alien.rect.y= random.randrange(600)
    all_sprites_list.add(alien)
   
def changingAngle(user):
    for event in pygame.event.get():
        if event.key == pygame.K_a or event.key == pygame.K_LEFT:
            pygame.key.set_repeat(2,1)
            user.angle_speed = 0
            
        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
            pygame.key.set_repeat(2,1)
            user.angle_speed = 0
def main(): #sets up screen
    pygame.init()
    pygame.key.set_repeat(500,30)

    screen = pygame.display.set_mode([windowW, windowH])
    screen_rect = screen.get_rect()

    all_sprites_list = pygame.sprite.Group()
    orb_group = pygame.sprite.Group()  # "group" not "list".

    user = User() #adding pygame.sprite.Sprite breaks it, THE WHOLE PALYER CLASS IS STR8 BOONED
    all_sprites_list.add(user)
    speedCap = 8
    speedMin = -5

    clock = pygame.time.Clock()

    x = True
    while x == True:
        clock.tick(60)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                x = False
            elif event.type == pygame.KEYDOWN:
                enemyspawn(all_sprites_list, orb_group,user)
                if event.key == pygame.K_w or event.key == pygame.K_UP and user.speed > speedMin:
                    pygame.key.set_repeat(2,1) #prevents superspeed
                    user.speed += 1
                if event.key == pygame.K_s  or event.key == pygame.K_DOWN and user.speed < speedCap:
                    pygame.key.set_repeat(2,1) #prevents superspeed(if it is low enuf it resets to the max integer value)
                    user.speed -= 1
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    user.angle_speed = -3
                    
                if event.key == pygame.K_d or event.key == pygame.K_RIGHT: 
                    user.angle_speed = 3
                    
                if event.key == pygame.K_SPACE: #shoots orb when user pushes space
                    shootingorb(all_sprites_list, orb_group,user)
            elif event.type == pygame.KEYUP:
                changingAngle(user)
        all_sprites_list.update()
        user.rect.clamp_ip(screen_rect)

        screen.fill(white)
        all_sprites_list.draw(screen)
        pygame.display.flip()

if __name__ == '__main__':
    main()
    pygame.quit()