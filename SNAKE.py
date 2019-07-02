
import pygame
import random

#initializing pygame(compulsary line whenever pygame module is imported)
pygame.init()

yellow = (225, 225, 0)

#creates a pygame window of size 800x600 pixels
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('SNAKE GAME BY ASUTOSH')
displayWidth = 800
displayHeight = 600
blockSize = 24
appleSize = 30
FPS = 15

#loading bite sound and background music
bite = pygame.mixer.Sound("bite.wav")
pygame.mixer.music.load("backmusic.mp3")

#loading required images
introimg = pygame.image.load('intro.png')

offplayimg = pygame.image.load('offplay5.png')
offcontrolsimg = pygame.image.load('offcontrols5.png')
offquitimg = pygame.image.load('offquit5.png')
onplayimg = pygame.image.load('onplay5.png')
oncontrolsimg = pygame.image.load('oncontrols5.png')
onquitimg = pygame.image.load('onquit5.png')

backgndimg = pygame.image.load('backgnd1.png')
gameoverimg = pygame.image.load('gameover.png')
onpaimg = pygame.image.load('onpa5.png')
offpaimg = pygame.image.load('offpa5.png')
oncontimg = pygame.image.load('oncont5.png')
offcontimg = pygame.image.load('offcont5.png')
onpauseimg = pygame.image.load('onpause50.png')
offpauseimg = pygame.image.load('offpause50.png')
pauseimg = pygame.image.load('pause.png')
controlsimg =  pygame.image.load('controls.png')
offbackimg = pygame.image.load('offback5.png')
onbackimg = pygame.image.load('onback5.png')

sheadimg = pygame.image.load('snakehead24.png')
ssegimg = pygame.image.load('snakeseg24.png')
stailimg = pygame.image.load('snaketail24.png')

appleimg = pygame.image.load('apple1.png')
mangoimg = pygame.image.load('mango1.png')
grapesimg =  pygame.image.load('grapes1.png')
watermelonimg = pygame.image.load('watermelon1.png')
mouseimg = pygame.image.load('mouse1.png')

iconimg = pygame.image.load('icon.png')


foodList = [appleimg, mangoimg, watermelonimg, grapesimg, mouseimg]
pygame.display.set_icon(iconimg)

#defining Clock obj
clock = pygame.time.Clock()

'''displays the score on the game screen'''
def score(score):
    #converting the integer score to string and appending it to the total message
    msg = 'Score : '+ str(score)
    message_to_screen(msg, yellow, 10, 5, 50)
    
'''informs user about the controls and consists of a back button which takes us back to the into screen'''
def controls():

    gcont = True
    while gcont:

        #for the top right red cross to be able to quit the game when clicked
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        gameDisplay.blit(controlsimg, (0, 0))
        button(700, 500, 75, 75, offbackimg, onbackimg, 'back')
        pygame.display.update()
        clock.tick(5)

'''here a semi transparent screen/image is displayed, and the music pauses this screen consists of 2 buttons
continue which actually breaks out of the pause func so that the game can continue and another quit to quit the game'''
def pause():
    p = 0
    pygame.mixer.music.pause()

    gpause = True
    while gpause:
        
        #for the top right red cross to be able to quit the game when clicked
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

        gameDisplay.blit(pauseimg, (0, 0))
        p = button(134, 493, 183, 72, offcontimg, oncontimg, 'continue')
        button(483, 493, 183, 72, offquitimg, onquitimg, 'quit')
        pygame.display.update()
        pcur = pygame.mouse.get_pos()
        pclick = pygame.mouse.get_pressed()

        if p == 1:
            pygame.mixer.music.unpause()
            gpause = False
  
        clock.tick(FPS)


'''this func displays a button at a particular pos and checks for the cursor pos if the cursor pos
happens to be within the area of the button then it makes the button lighter(displays another image
at the same x-y pos), it also checks for mouse clicks within the area of the button and if found
performs a particular action as given in the parameter'''

def button(bx, by, bwidth, bheight, offimg, onimg, action = None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if bx + 10 < cur[0] < bx + bwidth - 10 and by + 10 < cur[1] < by + bheight - 10:
        gameDisplay.blit(onimg, (bx, by))
    else:
        gameDisplay.blit(offimg, (bx, by))


    if bx + 10 < cur[0] < bx + bwidth - 10 and by + 10 < cur[1] < by + bheight - 10:    
        if click[0] == 1 and action != None:    
            if action == 'play' or action == 'playagain':
                gameLoop()
            elif action == 'controls':
                controls()
                
            elif action == 'quit':
                pygame.quit()
                quit()
            elif action == 'pause':
                pause()
            elif action == 'continue':
                return 1
            elif action == 'back':
                gameIntro()
'''this screen appers as soon as the code is execuated and it consists of 3 buttons one to start
the game one to quit another to check the controls'''            
def gameIntro():

    gintro = True
    

    while gintro:

        #for the top right red cross to be able to quit the game when clicked
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()


        gameDisplay.blit(introimg, (0, 0))

        button(68, 468, 183, 72, offplayimg, onplayimg, 'play')
        button(309, 468, 183, 72, offcontrolsimg, oncontrolsimg, 'controls')
        button(550, 468, 183, 72, offquitimg, onquitimg, 'quit')
        
        pygame.display.update()
        clock.tick(FPS)


def snake(snakeList, blockSize, snakeLen):

    #to rotate the snakehead as per the direction
    if direction == 'left':
        shead = pygame.transform.rotate(sheadimg, 90)
    elif direction == 'right':
        shead = pygame.transform.rotate(sheadimg, 270)
    elif direction == 'down':
        shead = pygame.transform.rotate(sheadimg, 180)
    elif direction == 'up':
        shead = sheadimg
    else:    
        shead = sheadimg
    #now we need to blit the rotated image
    gameDisplay.blit(shead, (snakeList[-1][0], snakeList[-1][1]))
    
    if snakeLen > 2:
        '''not including 0 i.e. this loop runs in reverse manner not including the head(0) and tail(last)'''
        for r in range(-snakeLen+2,0):
            if snakeList[-r][0] == snakeList[-r+1][0] and snakeList[-r][1] != snakeList[-r+1][1]:
                sseg = ssegimg
            else:
                sseg = pygame.transform.rotate(ssegimg, 90)
            gameDisplay.blit(sseg, (snakeList[-r][0], snakeList[-r][1]))

        if snakeList[1][0] == snakeList[0][0] and snakeList[1][1] != snakeList[0][1]:
            if snakeList[1][1] < snakeList[0][1]:
                stail = stailimg
            else:
                stail = pygame.transform.rotate(stailimg, 180)
        else:
            if snakeList[1][0] < snakeList[0][0]:
                stail = pygame.transform.rotate(stailimg, 90)
            else:
                stail = pygame.transform.rotate(stailimg, 270)

        gameDisplay.blit(stail, (snakeList[0][0], snakeList[0][1]))

        '''initially the snake body consists only of the head but after it grabs the 1st food(i.e. snakelen = 2)
        then the tail must appear not the seg after the 2nd food snkelen = 3then the snake tail must go back making
        space for the new seg and this process goes on'''

        '''now the problem is to rotate the other body parts as the head but at any time we cannot copy the direction
        of the head as it might happen that at any time head is moving down and another part is moving left'''

        '''we can solve this by using a simple logic i.e. the snakeseg image symmetrical rectangle i.e. left pos = right
        and top = bottom if the x coord of any seg and its prev seg are same and y not(which is obvious) then the
        seg mustbe in vertical pos and if y coords are same then seg in horizontal pos'''

        '''but the above logic won't work for tail as in case of tail, left pos != right and top != bottom therefore
        after checking for similarity in x and y coordinates we need to apply another logic i.e. if the y pos of the
        tail and its prev seg are same then the tail can be in left or right pos, now lets compare the x pos is x pos of
        tail greater than it's prev seg then then tail in right pos and vice versa and similar logic for the other case'''
    
    elif snakeLen == 2:
        if snakeList[snakeLen-1][0] == snakeList[snakeLen-2][0] and snakeList[snakeLen-1][1] != snakeList[snakeLen-2][1]:
            if direction == 'up':
                stail = stailimg
            else:
                stail = pygame.transform.rotate(stailimg, 180)
        else:
            if direction == 'right':
                stail = pygame.transform.rotate(stailimg, 270)
            else:
                stail = pygame.transform.rotate(stailimg, 90)

        gameDisplay.blit(stail, (snakeList[snakeLen-2][0], snakeList[snakeLen-2][1]))

'''used to display text on the screen'''
def message_to_screen(msg, color, textX, textY, textSize):
    font = pygame.font.Font("LOOPY_IT.TTF", textSize)
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [textX, textY])

'''this is the actual game, as soon as the ctrl enters this func background music starts
playing and the snakehead an be moved using arrow keys, the screen also consists of the
score board and the pause button'''    
def gameLoop():
    #plays the music(-1 means music is played in infinite loops) 
    pygame.mixer.music.play(-1)
    
    global direction
    #no proper direction is given so that the snake doesn't start moving as soon as the ctrl enters the gameLoop()
    direction = 'abcd'

    gameExit = False

    #x and y coords of the snakehead
    lead_x = displayWidth/2
    lead_y = displayHeight/2


    '''lead_y_change and lead_x_change are 0 initially but are given a  value
    as soon as any correct key is pressed(we don't directly change change
    the y coordinate instead we change ychange and add it to y to change y)'''
    lead_x_change = 0
    lead_y_change = 0
    
    snakeList = []
    snakeLen = 1
    speed = 15
    
    appleX = random.randrange(0, displayWidth-appleSize)
    appleY = random.randrange(0, displayHeight-appleSize)
    index = random.randrange(0,5)
    

    gameOver = False
    
    while not gameExit:

        while gameOver:
            pygame.mixer.music.pause()
            
            gameDisplay.blit(gameoverimg, (0, 0))
            button(134, 493, 183, 72, offpaimg, onpaimg, 'playagain')
            button(483, 493, 183, 72, offquitimg, onquitimg, 'quit')
            pygame.display.update()

            #for the top right red cross to be able to quit the game when clicked
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
     
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
                
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:
                    direction = 'left'
                    lead_x_change = -speed
                    '''here if we don't make ychange zero then only xchange and hence
                    lead_x will be updated and if ychange carries any prev non-zero
                    value it would remain as it is and the snake will move diagonally'''
                    lead_y_change = 0 
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                    lead_x_change = speed
                    lead_y_change = 0 
                elif event.key == pygame.K_UP:
                    direction = 'up'
                    lead_y_change = -speed
                    lead_x_change = 0 
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                    lead_y_change = speed
                    lead_x_change = 0

        lead_x += lead_x_change
        lead_y += lead_y_change

        
        #if the pos of snakehead == pos of any other body segments then the snake crashes into itself 
        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        '''snakehead stores the x and y coordinates of the snake head, converts it into a single element
        (a list of 2 elements) and passes it to the snakelist''' 
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        '''so the snakelist stores all the positions of the snakehead with the latest one at the end and
        accordingly displays bodysegments at those positions(as the segs follow the head)''' 
        snakeList.append(snakeHead)

        
        #if the head collides with any of the 4 boundary walls then gameover
        if lead_x > displayWidth-blockSize or lead_x < 0 or lead_y > displayHeight-blockSize or lead_y < 0:
            gameOver = True

        #if the head collides with food then bite sound is played snakelen is increased and the food appears in a different location  
        if lead_x > appleX and lead_x < appleX+appleSize or lead_x+blockSize > appleX and lead_x+blockSize < appleX+appleSize:
            if lead_y > appleY and lead_y < appleY+appleSize or lead_y+blockSize > appleY and lead_y+blockSize < appleY+appleSize:
                appleX = random.randrange(0, displayWidth-appleSize)
                appleY = random.randrange(0, displayHeight-appleSize)
                #so that a random food is generated from the foodlist
                index = random.randrange(0,5)
                snakeLen += 1
                pygame.mixer.Sound.play(bite)
        
            
        gameDisplay.blit(backgndimg, (0, 0))
        
        #the snakelist stores all the pos of the head so it nedds to be cut repeatedly otherwise at all positions segs would be drawn 
        if len(snakeList) > snakeLen:
            del snakeList[0]
 
        snake(snakeList, blockSize, snakeLen)

        gameDisplay.blit(foodList[index], (appleX, appleY))
        
        score(snakeLen-1) 
        
        button(737, 15, 50, 50, offpauseimg, onpauseimg, 'pause')

        pygame.display.update()
        
        #as the snake grows longer the its speed increases
        if snakeLen > 15 and 30 > snakeLen:
            speed = 20
        elif snakeLen >= 30 and 50 > snakeLen:
            spped = 25
        elif snakeLen >= 50:
            speed = 30
        clock.tick(FPS)
    
    
    pygame.quit()
    quit()


gameIntro()                
gameLoop()            
       
        
        
        

