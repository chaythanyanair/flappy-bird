#   Modules

import pygame,sys
from pygame.locals import *
pygame.init()
import random


#global variables
width,height=1000,600
clock=pygame.time.Clock()
point=pygame.mixer.Sound('sfx_point.ogg')
wing=pygame.mixer.Sound('sfx_wing.ogg')
whoosh=pygame.mixer.Sound('sfx_swhooshing.ogg')
hit=pygame.mixer.Sound('sfx_hit.ogg')
die=pygame.mixer.Sound('sfx_die.ogg')

#Sprite class
class _pipe(pygame.sprite.Sprite):


    def __init__(self,x,y,transform,bird):
        super(_pipe, self).__init__()
        self.x = x
        self.y = y
        if bird==False:
        	self.object=pygame.image.load('pipe.jpeg')
        	self.object=pygame.transform.scale(self.object,(50,y))
        	self.gap=random.randint(130,150)
        	self.transform=transform
        	self.bird=bird
        else:
        	self.bird=bird
        	self.object=pygame.image.load('flappy2.png')
        	self.object=pygame.transform.scale(self.object,(100,100))
        	self.transform=transform
        	self.gap=random.randint(100,150)
        self.rect = self.object.get_rect(center=(self.x,self.y))
        
        	
    def blit_pipe(self,screen):
    	if self.bird==True:
    	    screen.blit(self.object,(self.x,self.y))
        elif self.transform:
            self.object=pygame.image.load('pipe.jpeg')
            self.object=pygame.transform.scale(self.object,(50,self.y))
   	    self.object=pygame.transform.rotate(self.object,90)
    	    self.object=pygame.transform.rotate(self.object,90)
    	    screen.blit(self.object,(self.x,0))
    	    self.rect.move_ip(self.x,0)
    	elif self.bird==False and self.transform==False:
    	    self.object=pygame.image.load('pipe.jpeg')
    	    c=600-(self.y-self.gap)
    	    self.object=pygame.transform.scale(self.object,(50,c))
    	    screen.blit(self.object,(self.x,(self.y+self.gap)))
    	if self.transform:
            self.rect = self.object.get_rect(center=(self.x+23,0))
            self.rect=self.rect.inflate(4,self.y-10)
        elif self.bird==False:
            self.rect = self.object.get_rect(center=(self.x+23,(600-(self.y-self.gap))))
            p = pygame.Rect(self.x,(self.y+self.gap),70,self.y*10)
            self.rect=p.clip(self.rect)
        else:
            self.rect=self.object.get_rect(center=((self.x+90),(self.y+70)))
            p = pygame.Rect(self.x-3,self.y+13,70,53)
            self.rect=p.clip(self.rect)
      	    


def initialise():
    score=0    
    pygame.display.set_caption('My flappy bird')
    y_scale=0
    x_pos=500
    rect_speed=1
    y_pos=0
    level=0
    
    screen=pygame.display.set_mode((width,height))
    s = pygame.display.get_surface()
    
    bird=_pipe(200,300,False,True)
    bg=pygame.image.load('bg.jpeg')
    bg=pygame.transform.scale(bg,(width,height))
    
    size=random.randint(200,350)
    pipe1_up=_pipe(500,size,True,False)
    pipe1_down=_pipe(500,size,False,False)
    
    size=random.randint(200,350)
    temp=random.randint(400,500)
    pipe2_up=_pipe(500+temp,size,True,False)
    pipe2_down=_pipe(500+temp,size,False,False)
    
    size=random.randint(200,350)
    temp=random.randint(800,950)    
    pipe3_up=_pipe(500+temp,size,True,False)
    pipe3_down=_pipe(500+temp,size,False,False)
    
    pipe_gang=pygame.sprite.Group()
    pipe_gang.add(pipe1_up,pipe1_down,pipe2_up,pipe2_down,pipe3_up,pipe3_down)
    
    game_loop(y_pos,pipe1_up,pipe1_down,pipe2_up,pipe2_down,pipe3_up,pipe3_down,y_scale,rect_speed,bird,bg,s,screen,score,pipe_gang)
    

def game_over(screen,bird):
 
    font=pygame.font.Font(None,100)
    text=font.render('GAMEOVER',1,[0,0,0])
    screen.blit(text,[300,250]) 
    font=pygame.font.Font(None,50)
    text=font.render('Press Enter To Replay...',1,[0,0,0])
    screen.blit(text,[350,400]) 
    pygame.display.flip()
    done=False  
    bird.y=580
    i=1
    while done==False:
        clock.tick(20)
        for event in pygame.event.get():    
        
            if event.type==pygame.QUIT:    
                done=True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    initialise()
            bird.blit_pipe(screen)
            pygame.display.flip()
                    
    sys.exit()                 
                             
    
def game_loop(y_pos,pipe1_up,pipe1_down,pipe2_up,pipe2_down,pipe3_up,pipe3_down,y_scale,rect_speed,bird,bg,s,screen,score,pipe_gang):
    
    global point
    global wing
    global whoosh
    global hit
    global die
    
    i=1    
    flag=1
    
    while True:
        seconds=clock.tick()/1000.0
        if flag==1:
            y_scale=3*i
            i+=0.1
            flag=0
        if flag==0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
	        if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        wing.play(loops=0,maxtime=0)
	                y_scale=-2
		    
	        if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:	
	                y_scale=3*i
                        i+=0.1
                        
                    
        screen.blit(bg,(0,0))
        bird.blit_pipe(screen)
        pipe1_up.blit_pipe(screen)
        s.fill(Color("red"),pipe1_up.rect)
        pipe1_down.blit_pipe(screen)
        pipe2_up.blit_pipe(screen)
        s.fill(Color("red"),pipe2_up.rect)
        pipe2_down.blit_pipe(screen)
        pipe3_up.blit_pipe(screen)
        s.fill(Color("red"),pipe3_up.rect)
        pipe3_down.blit_pipe(screen)
        p=pygame.draw.rect(screen,(0,0,0),[0,height-30,width,30],2)
        s.fill(Color('brown'), p)
      	
      	if bird.y>=(height-100):
      	    die.play(loops=0,maxtime=0)
	    flag=1
	    break
	    
	if not bird.y>height:
            bird.y+=y_scale
        if not (pipe1_up.x<-50 or pipe1_down.x<-50):
            pipe1_up.x-=rect_speed
            pipe1_down.x-=rect_speed
        else:
	    pipe1_up.x=1000
	    pipe1_down.x=1000
	    i=1
        if not (pipe2_up.x<-50 or pipe2_down.x<-50):
            pipe2_up.x-=rect_speed
            pipe2_down.x-=rect_speed
        else:
	    pipe2_up.x=1000
	    pipe2_down.x=1000
	    i=1
        if not (pipe3_up.x<-50 or pipe3_down.x<-50):
            pipe3_up.x-=rect_speed
            pipe3_down.x-=rect_speed
        else:
	    pipe3_up.x=1000
	    pipe3_down.x=1000
	    i=1
	if bird.x>pipe1_up.x and bird.x < pipe1_down.x+2:
            score = (score + 1)
            point.play(loops=0,maxtime=0)
        elif bird.x>pipe2_up.x and bird.x < pipe2_down.x+2:
            score = (score + 1)
            point.play(loops=0,maxtime=0)
        elif bird.x>pipe3_up.x and bird.x < pipe3_down.x+2:
            score = (score + 1)
            point.play(loops=0,maxtime=0)
        if score>=15:
            rect_speed=1.5
       
	
	
	font=pygame.font.Font(None,50)
        text=font.render('Score:'+str(score),1,[0,0,0])
        screen.blit(text,[600,100]) 
        if pygame.sprite.spritecollideany(bird,pipe_gang):
            hit.play(loops=0,maxtime=0)
            game_over(screen,bird)
        pygame.display.update()
    game_over(screen,bird)


if __name__=="__main__":        
    initialise()
    sys.exit()









































