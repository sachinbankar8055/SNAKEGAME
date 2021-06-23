
import pygame
import random
import os

pygame.init()



# color difining
black=0,0,0
white=255,255,255
red=255,0,0


# setting size of window
screen_width=900
screen_height=500

# for the size of window
gameWindow=pygame.display.set_mode((screen_width,screen_height))

# background image
bgimg = pygame.image.load("snkbg.jpg")
bgimg = pygame.transform.scale(bgimg,(screen_width,screen_height)).convert_alpha()

# home snake image
homeimg = pygame.image.load("snk.jpg")
homeimg = pygame.transform.scale(homeimg,(screen_width,screen_height)).convert_alpha()

# game over image
gameoverimg = pygame.image.load("gameoversnk.jpg")
gameoverimg = pygame.transform.scale(gameoverimg,(screen_width,screen_height)).convert_alpha()

# name to game
pygame.display.set_caption("Snake")
pygame.display.update()

clock = pygame.time.Clock() # defining the clock

# using system font
font = pygame.font.SysFont(None,55)

# function for printing score on screen
def scoreonscreen(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,[x,y]) # for updating score


# creating function for plotting snake on screen
def plot_snake(gameWindow,color,snake_list,snake_size):
    for x,y in snake_list: # x,y used to access coordinats fron snake list
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():

    fps=60
    exit_game = False

    while not exit_game:
        gameWindow.fill((200,250,100))
        # filling the background color in window
        gameWindow.fill(white)
        gameWindow.blit(homeimg,(0,0))
        scoreonscreen("welcome to snake ",	(255,255,0),280,10)
        scoreonscreen("press ENTER to play game",	(255,255,0), 250, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # to quit the game
                exit_game = True

            if event.type == pygame.KEYDOWN:
                # when we press enter it restart the game by calling the game loop
                if event.key == pygame.K_RETURN:
                    gameloop()



        # updating the changes
        pygame.display.update()
        clock.tick(fps)




# creating a game loop
# it update user activity like pressing up,down,moving mouse,right ,left
# game loop
def gameloop():

    # game specific variables
    exit_game = False
    game_over = False

    snake_x = 45
    snake_y = 45
    snake_size = 10

    velocity_x = 0
    velocity_y = 0
    initvelocity = 5

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    score = 0

    fps = 30  # fps is frame per second

    snake_list = []
    snake_length = 1

    # reading the high score from the text file
    # openig file in read mode

    # if highscore text file is not exist
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt","r") as f:
        highscore=f.read()

    while not exit_game:

        if game_over:
            # for game over

            # updating the high score in the text file when game gets over
            # opening the file in the write mode
            with open("highscore.txt", "w") as f:
                f.write(str(highscore))

            gameWindow.fill(white)
            gameWindow.blit(gameoverimg, (0, 0))

            # showing game over on the screen
            scoreonscreen("score " + str(score), white, 200, 75)
            scoreonscreen("high score " + str(highscore), white, 500, 75)
            scoreonscreen("press ENTER to continue ",red,200,350)

            for event in pygame.event.get():
                # to quit the game the when we click on the x
                if event.type == pygame.QUIT:  # to quit the game
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    # when we press enter it restart the game by calling the game loop
                    if event.key == pygame.K_RETURN:
                        welcome() # gameloop()


        else:


            for event in pygame.event.get():
                if event.type == pygame.QUIT: # to quit the game
                    exit_game=True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT: # moving snake right
                        velocity_x = initvelocity # snake_x=snake_x+10 # position change
                        velocity_y = 0

                    if event.key == pygame.K_LEFT: # moving snake left
                        velocity_x = -initvelocity # snake_x = snake_x - 10 # position change
                        velocity_y = 0

                    if event.key == pygame.K_UP: # moving snake up
                        velocity_y = -initvelocity # snake_y = snake_y - 10 # position change
                        velocity_x = 0

                    if event.key == pygame.K_DOWN: # moving snake down
                        velocity_y = initvelocity # snake_y = snake_y + 10 # position change
                        velocity_x = 0

                    if event.key == pygame.K_q: # adding cheat code in score of game
                        score = score +10

            # speed of snake
            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # snake is eating the food
            if abs(snake_x - food_x)<6 and abs(snake_y - food_y)<6: # it is distance from center
                score=score+10 # updating score
                #print('score ',score*10)

                # updating position of  food after eating it
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                # increase length of snake
                snake_length = snake_length +5

                # print(highscore)
                # updating new high score
                if score > int(highscore):
                    highscore = score



            # filling the background color in window
            gameWindow.fill(white)
            gameWindow.blit(bgimg,(0,0))

            # calling function for printing score on screen
            scoreonscreen("score " + str(score), white, 5, 5)
            scoreonscreen("high score " + str(highscore), white, 600, 5)

            # food for the snake
            pygame.draw.rect(gameWindow,(255,255,0), [food_x, food_y, snake_size, snake_size])

            # making the head of snake
            head=[]
            # appending coordinates
            head.append(snake_x)
            head.append(snake_y)
            # appending head in snake list
            snake_list.append(head)

            # cuts the head when snake eat food, not deleting head lead to continous increase in snake length
            if len(snake_list) > snake_length:
                del snake_list[0]

            if head in snake_list[:-1]:
                # when snake collide with itself game gets over
                game_over=True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                # when snake collide with wall game gets over
                game_over=True

            #pygame.draw.rect(gameWindow,black,[snake_x,snake_y,snake_size,snake_size])

            # calling function for plotting snake on screen
            plot_snake(gameWindow,(165,42,42),snake_list,snake_size)



        # updating the changes
        pygame.display.update()
        clock.tick(fps)



    pygame.quit()
    quit()


#gameloop()
welcome()
