
import random

import pygame

pygame.init()

WIDTH = 600
HEIGHT = 650
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Yatzhee!!!!")

timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font("freesansbold.ttf", 18)
background = (128, 128, 128)
black = (0, 0, 0)
white = (255, 255, 255)
numbers = [0, 0, 0, 0, 0] #dice numbers
roll = False
rolls_left = 3

dice_selected = [False] * 5
selected_choice = [False] * 13 # because we have 13 choices
possible = [False] * 13
done = [False] * 13
score = [0] * 13
totals = [0] * 5
current_score = 0
clicked = -1  

something_selected = False

def check_scores(selected_choice_list, numbers_list, possible_list, current_score):
    active = 0
    for index in range(len(selected_choice_list)):
        if selected_choice_list[index]:
            active = index
    if active == 0:
        current_score = numbers_list.count(1)
    elif active == 1:
        current_score = numbers_list.count(2) * 2
    elif active == 2:
        current_score = numbers_list.count(3) * 3
    elif active == 3:
        current_score = numbers_list.count(4) * 4
    elif active == 4:
        current_score = numbers_list.count(5) * 5
    elif active == 5:
        current_score = numbers_list.count(6) * 6
    elif active == 6 or active == 7:
        if possible_list[active]:
            current_score = sum(numbers_list)
        else:
            current_score = 0
    elif active == 8:
        if possible_list[active]:
            current_score = 25
        else:
            current_score = 0
    elif active == 9:
        if possible_list[active]:
            current_score = 30
        else:
            current_score = 0
    elif active == 10:
        if possible_list[active]:
            current_score = 40
        else:
            current_score = 0
    elif active == 11:
        if possible_list[active]:
            current_score = 50
        else:
            current_score = 0
    elif active == 12:
        current_score = sum(numbers_list)
    return current_score
    


def draw_stuff():
    global rolls_left
    roll_text = font.render('Click to Roll', True, white)
    screen.blit(roll_text, (85, 75))
    accept_text = font.render('Accept Turn', True, white)
    screen.blit(accept_text, (400, 75))
    rolls_text = font.render("Rolls left in this turn: "+str(rolls_left), True, white)
    screen.blit(rolls_text, (15, 15))

    pygame.draw.rect(screen, white, [0, 105, 225, HEIGHT-100])
    # pygame.draw.line(screen, black, (0, 40), (WIDTH, 40), 3)  #HORIZONTAL LINE THAT SEPARATES DICE FORM ROLLS_TEXT

    pygame.draw.line(screen, black, (0,105), (WIDTH, 105), 3)
    pygame.draw.line(screen, black, (145, 105), (145, HEIGHT), 3)
    pygame.draw.line(screen, black, (225, 105), (225, HEIGHT), 3)

class Dice:
    def __init__(self, x_pos, y_pos, num, key):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.number = num
        self.key = key
        self.die = ''
        self.selected = dice_selected[key]

    def draw(self):
        self.die = pygame.draw.rect(screen, (255, 255, 255), [self.x_pos, self.y_pos, 50, 50], 0, 5)
        if self.number == 1:
            pygame.draw.circle(screen, black, (self.x_pos + 25, self.y_pos + 25), 5)
        if self.number == 2:
            pygame.draw.circle(screen, black, (self.x_pos + 10, self.y_pos+10), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 40, self.y_pos + 40), 5)
        if self.number == 3:
            pygame.draw.circle(screen, black, (self.x_pos+10, self.y_pos+10), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 25, self.y_pos + 25), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 40, self.y_pos + 40), 5)
        if self.number == 4:
            pygame.draw.circle(screen, black, (self.x_pos + 10, self.y_pos+10), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 10, self.y_pos+40), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 40, self.y_pos + 10), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 40, self.y_pos + 40), 5)
        if self.number == 5:
            pygame.draw.circle(screen, black, (self.x_pos + 10, self.y_pos+10), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 10, self.y_pos+40), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 25, self.y_pos+25), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 40, self.y_pos + 10), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 40, self.y_pos + 40), 5)
        if self.number == 6:
            pygame.draw.circle(screen, black, (self.x_pos + 10, self.y_pos+10), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 10, self.y_pos+25), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 10, self.y_pos+40), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 40, self.y_pos + 10), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 40, self.y_pos + 25), 5)
            pygame.draw.circle(screen, black, (self.x_pos + 40, self.y_pos+40), 5)

        if self.selected:
            self.die = pygame.draw.rect(screen, (255, 0, 0), [self.x_pos, self.y_pos, 50, 50], 4, 5)

    def check_click(self, coordinates):
        if self.die.collidepoint(coordinates):
            if dice_selected[self.key]:
                dice_selected[self.key] = False
            else:
                dice_selected[self.key] = True



class Choice:
    def __init__(self, x_pos, y_pos, text, select, possible, done, score):
        self.x_pos= x_pos
        self.y_pos = y_pos
        self.text = text
        self.select = select
        self.possible = possible
        self.done = done
        self.score = score

    def draw(self):
        pygame.draw.line (screen, black, (self.x_pos, self.y_pos), (self.x_pos+225, self.y_pos), 2)
        pygame.draw.line (screen, black, (self.x_pos, self.y_pos + 30), (self.x_pos+ 225, self.y_pos + 30), 2)
        if not self.done:
            if self.possible:
                my_text = font.render(self.text, True, (34, 140, 34))
            elif not self.possible:
                my_text = font.render(self.text, True, (255, 0, 0))
        else:
            my_text = font.render (self.text, True, black)
        if self.select:
            pygame.draw.rect(screen, (20, 35, 30), [self.x_pos, self.y_pos, 145, 30])
        screen.blit (my_text, (self.x_pos + 5, self.y_pos + 10))

        score_text = font.render (str(self.score), True, (0, 0, 255))
        screen.blit (score_text, (self.x_pos + 165, self.y_pos + 10))


def check_possibilities(possible_list, numbers_list):
    if 1 in numbers_list:
        possible_list[0] = True
    else:
        possible_list[0] = False

    if 2 in numbers_list:
        possible_list[1] = True
    else:
        possible_list[1] = False

    if 3 in numbers_list:
        possible_list[2] = True
    else:
        possible_list[2] = False

    if 4 in numbers_list:
        possible_list[3] = True
    else:
        possible_list[3] = False

    if 5 in numbers_list:
        possible_list[4] = True
    else:
        possible_list[4] = False

    if 6 in numbers_list:
        possible_list[5] = True
    else:
        possible_list[5] = False
    
    possible_list[12] = True   #chance
    max_count = 0
    for index in range(1, 7):
        if numbers_list.count(index) > max_count:
            max_count = numbers_list.count(index)

    if max_count >= 3:
        possible_list[6] = True
        if max_count >= 4:
            possible_list[7] = True
            if max_count >= 5:
                possible_list [11] = True

    if max_count < 3:
        possible_list[6] = False 
        possible_list[7] = False
        possible_list[8] = False
        possible_list[11] = False

    elif max_count == 3:
        possible_list[7] = False
        possible_list[11] = False
        checker = False
        for index in range(len(numbers_list)):
            if numbers_list.count(numbers_list[index]) == 2:
                possible_list[8] = True
                checker = True
        if not checker:
            possible_list[8] = False

    elif max_count == 4:
        possible_list[11] = False

    lowest = 10
    highest = 0
    for index in range(len (numbers_list)):
        if numbers_list[index] < lowest:
            lowest = numbers_list[index]
        if numbers_list[index]> highest:
            highest = numbers_list[index]

    #large straight
    if (lowest+1 in numbers_list) and (lowest+2 in numbers_list) and (lowest+3 in numbers_list) and (lowest+4 in numbers_list):
        possible_list [10] = True
    else:
        possible_list [10] = False
    
    # small straight
    if ((lowest+1 in numbers_list) and (lowest+2 in numbers_list) and (lowest+3 in numbers_list)) or ((highest-1 in numbers_list) and (highest-2 in numbers_list) and (highest-3 in numbers_list)):
        possible_list [9] = True
    else:
        possible_list [9] = False

    return possible_list

def check_totals(totals_list, scores_list):

    totals_list[0] = scores_list[0] + scores_list[1] + scores_list[2] + scores_list[3] + scores_list[4] + scores_list[5]

    if totals_list[0] > 63:
        totals_list[1] = 35
    else:
        scores_list[1] = 0

    totals_list[2] = totals_list[0] + totals_list[1]

    totals_list[3] = scores_list[6] + scores_list[7] + scores_list[8] + scores_list[9] + scores_list[10] + scores_list[11] + scores_list[12]
    
    totals_list[4] = totals_list[2] + totals_list[3]


    return totals_list

def make_choice(clicked_num, selected_list, done_list):
    for index in range(len(selected_list)):
        selected_list[index] = False
    if not done_list[clicked_num]:
        selected_list[clicked_num] = True
    return selected_list


running = True

while running:
    timer.tick(fps)
    screen.fill(background)
    roll_button = pygame.draw.rect (screen, black, [10, 70, 280, 30])
    accept_button = pygame.draw.rect (screen, black, [310, 70, 280, 30])
    draw_stuff()
    
    die1 = Dice(10, 10, numbers[0], 0)
    die2 = Dice(130, 10, numbers[1], 1)
    die3 = Dice(250, 10, numbers[2], 2)
    die4 = Dice(370, 10, numbers[3], 3)
    die5 = Dice(490, 10, numbers[4], 4)


    die1.draw()
    die2.draw()
    die3.draw()
    die4.draw()
    die5.draw()

    ones = Choice (0, 105, '1s', selected_choice[0], possible[0], done[0], score[0])
    twos = Choice (0, 135, '2s', selected_choice[1], possible[1], done[1], score[1])
    threes = Choice (0, 165, '3s', selected_choice[2], possible[2], done[2], score[2])
    fours = Choice (0, 195, '4s', selected_choice[3], possible[3], done[3], score[3])
    fives = Choice (0, 225, '5s', selected_choice[4], possible[4], done[4], score[4])
    sixes = Choice (0, 255, '6s', selected_choice[5], possible[5], done[5], score[5])
    upper_total1 = Choice (0, 285, 'Upper Score', False, False, True, totals[0])
    upper_bonus = Choice (0, 315, 'Bonus if >= 63', False, False, True, totals[1])
    upper_total2 = Choice (0, 345, 'Upper Total', False, False, True, totals[2])
    three_kind = Choice (0, 375, '3 of Kind', selected_choice[6], possible[6], done[6], score[6])
    four_kind = Choice (0, 405, '4 of Kind', selected_choice[7], possible[7], done[7], score[7])
    full_house = Choice (0, 435, 'Full House', selected_choice[8], possible[8], done[8], score[8])
    small_straight = Choice (0, 465, 'Sm. Straight', selected_choice[9], possible[9], done[9], score[9])
    large_straight = Choice (0, 495, 'Lg. Straight', selected_choice[10], possible[10], done[10], score[10])
    yahtzee = Choice (0, 525, 'YAHTZEE!', selected_choice[11], possible[11], done[11], score[11])
    chance = Choice (0, 555, 'Chance', selected_choice[12], possible[12], done[12], score[12])
    # bonus = Choice (0, 640, 'Yahtzee Bonus', True, False, False)
    lower_total1 = Choice (0, 585, 'Lower Total', False, False, True, totals[3])
    # lower_total2 = Choice (0, 615, 'Upper Total', False, False, True)
    grand_total = Choice (0, 615, 'Grand Total', False, False, True, totals[4])

    possible = check_possibilities(possible, numbers)
    current_score = check_scores(selected_choice, numbers, possible, score)
    totals = check_totals(totals, score)
    if True in selected_choice:
        something_selected = True


    ones.draw()
    twos.draw()
    threes.draw()
    fours.draw()
    fives.draw()
    sixes.draw()
    upper_total1.draw()
    upper_bonus.draw()
    upper_total2.draw()
    three_kind.draw()
    four_kind.draw()
    full_house.draw()
    small_straight.draw()
    large_straight.draw()
    yahtzee.draw()
    chance.draw()
    # # bonus.draw()
    lower_total1.draw()
    # lower_total2.draw()
    grand_total.draw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            die1.check_click(event.pos)
            die2.check_click(event.pos)
            die3.check_click(event.pos)
            die4.check_click(event.pos)
            die5.check_click(event.pos)

            if 0 <= event.pos[0] <= 155:
                if 105 < event.pos[1] < 285 or 345 < event.pos[1] < 575:
                    if 105 < event.pos[1] < 135:
                        clicked = 0
                    elif 135 < event.pos[1] < 165:                          
                        clicked = 1
                    elif 165 < event.pos[1] < 195:
                        clicked = 2
                    elif 195 < event.pos[1] < 225:
                        clicked = 3
                    elif 225 < event.pos[1] < 255:
                        clicked = 4
                    elif 255 < event.pos[1] < 285:
                        clicked = 5
                    elif 375 < event.pos[1] < 405:
                        clicked = 6
                    elif 405 < event.pos[1] < 435:
                        clicked = 7
                    elif 435 < event.pos[1] < 465:
                        clicked = 8
                    elif 465 < event.pos[1] < 495:
                        clicked = 9
                    elif 495 < event.pos[1] < 525:
                        clicked = 10
                    elif 525 < event.pos[1] < 555:
                        clicked = 11
                    elif 555 < event.pos[1] < 575:
                        clicked = 12
                    choice = make_choice(clicked, selected_choice, done)


            if roll_button.collidepoint(event.pos) and rolls_left > 0:
                roll = True
                rolls_left -= 1

            if accept_button.collidepoint(event.pos) and something_selected and rolls_left < 3:
                for i in range(len(selected_choice)):
                    if selected_choice[i]:
                        done[i] = True
                        score[i] = current_score
                        selected_choice[i] = False
                    for index in range(len(dice_selected)):
                        dice_selected[index] = False
                    numbers = [7, 18, 30, 41, 53]
                    something_selected = False
                    rolls_left = 3

    if roll:
        for number in range(len(numbers)):
            if not dice_selected[number]:
                numbers[number] = random.randint(1,6)
        roll = False
    pygame.display.flip()
pygame.quit()
