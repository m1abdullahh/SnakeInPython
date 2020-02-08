import turtle
import time
import random2
import os
from os import path

# Speed of the game, Lower is faster
delay = 0.1

# Setup the screen
wn = turtle.Screen()
wn.screensize(600, 600)
wn.bgcolor("White")
wn.title("Snake Xiaoyu")
wn.tracer()  # Tracer turns off screen updates.. (!!!!)


# Loading turtle
loading = turtle.Turtle()
loading.speed(0)
loading.penup()
loading.goto(0, -80)
loading.shape('square')
loading.color('Blue')
loading.write("Game Loading, Please wait..", align='Center', font=('Arial', 28, 'italic'))
loading.hideturtle()


# Border Lines
class BorderLines_TB:  # Top and Bottom Borders

    def line(self):
        line = turtle.Turtle()
        line.speed(0)
        line.penup()
        line.color('red')
        line.shape('square')
        line.goto(self.x, 320)

    def line_2(self):
        line_2 = turtle.Turtle()
        line_2.speed(0)
        line_2.penup()
        line_2.color('red')
        line_2.shape('square')
        line_2.goto(self.x, -320)


# Drawing Top and Bottom Border Lines Here..
main = BorderLines_TB()
main.x = -310
main.line()
for x in range(31):
    main.x += 20
    main.line()
main.x = -310
main.line_2()
for x in range(31):
    main.x += 20
    main.line_2()


class BorderLines_LR:  # Left and Right Borders

    y = None

    def line_3(self):
        line_3 = turtle.Turtle()
        line_3.speed(0)
        line_3.penup()
        line_3.color('red')
        line_3.shape('square')
        line_3.goto(-280, self.y)

    def line_4(self):
        line_4 = turtle.Turtle()
        line_4.speed(0)
        line_4.penup()
        line_4.color('red')
        line_4.shape('square')
        line_4.goto(280, self.y)


main = BorderLines_LR()
main.y = -300
main.line_3()
for x in range(30):
    main.y += 20
    main.line_3()
main.y = -300
main.line_4()
for x in range(30):
    main.y += 20
    main.line_4()

loading.clear()

# Body
segments = []

# Score
score_m = 0
high_score = 0

# Display last gameplay scores (If exist)
last_scores = turtle.Turtle()
last_scores.penup()
last_scores.speed(0)
last_scores.hideturtle()
last_scores.shape('square')
last_scores.color('grey')
last_scores.goto(0, -370)
if path.exists('scores.txt'):
    file = open('scores.txt', "r+")
    scores_last = file.readline()
    file.close()
    last_scores.write("High score from last game: {0}".format(scores_last), align='center', font=('Arial', 18, 'italic'))
else:
    first_time = 'It\'s the first game play'
    last_scores.write(first_time, align='center', font=('Arial', 18, 'italic'))


# Score Monitor
score = turtle.Turtle()
score.speed(0)
score.shape('square')
score.color('grey')
score.penup()
score.hideturtle()
score.goto(0, 350)
score.write("Score: 0  High Score: 0", align='center', font=('Courier', 18, 'normal'))

# Head(shot) [HAHA, IKWYDT]
head = turtle.Turtle()
head.speed(0)
head.shape('square')
head.color('black')
head.penup()
head.goto(0, 0)
head.direction = 'stop'

# Food
food = turtle.Turtle()
food.speed(0)
food.shape('circle')
food.color('red')
food.penup()
food.goto(0, 100)


# Functions
def go_up():
    if head.direction != 'down':
        head.direction = 'up'


def go_down():
    if head.direction != 'up':
        head.direction = 'down'


def go_left():
    if head.direction != 'right':
        head.direction = 'left'


def go_right():
    if head.direction != 'left':
        head.direction = 'right'


def move():
    if head.direction == 'up':
        y_1 = head.ycor()
        head.sety(y_1 + 20)
    if head.direction == 'down':
        y_2 = head.ycor()
        head.sety(y_2 - 20)
    if head.direction == 'left':
        x_1 = head.xcor()
        head.setx(x_1 - 20)
    if head.direction == 'right':
        x_2 = head.xcor()
        head.setx(x_2 + 20)


# Keyboard Presses
wn.listen()
wn.onkeypress(go_up, 'Up')
wn.onkeypress(go_down, 'Down')
wn.onkeypress(go_left, 'Left')
wn.onkeypress(go_right, 'Right')

# Main game loop
while True:
    wn.update()
    # Checking the collision with the food..
    if head.distance(food) < 20:
        # Moving the food..
        x_food = random2.randint(-250, 250)
        y_food = random2.randint(-250, 250)
        food.goto(x_food, y_food)
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape('square')
        new_segment.color('green')
        new_segment.penup()
        segments.append(new_segment)

        # Decreasing the delay
        delay -= 0.001

        # Increasing the scores..
        score_m += 10
        if score_m > high_score:
            high_score = score_m
            # Adding scores to the scores.txt
            file = open('scores.txt', 'w+')
            file.write(str(high_score))
            file.close()
        score.clear()
        score.write("Score: {0}  High Score: {1}".format(score_m, high_score), align='center',
                    font=('Courier', 18, 'normal'))

    # Move the end segments first in reverse order
    for index in range(len(segments) - 1, 0, -1):
        x = segments[index - 1].xcor()
        y = segments[index - 1].ycor()
        segments[index].goto(x, y)
    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x, y)
    # Check for collision with the border
    if head.xcor() > 240 or head.xcor() < -240 or head.ycor() > 280 or head.ycor() < -280:
        time.sleep(1)
        head.goto(0, 0)
        # Hiding segments
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()
        head.direction = 'stop'
        score_m = 0
        score.clear()
        score.write("Score: {0}  High Score: {1}".format(score_m, high_score), align='center',
                    font=('Courier', 18, 'normal'))
    move()
    # Checking collisions with the segments of the body
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(1)
            head.direction = 'stop'
            head.goto(0, 0)
            # hiding the segments
            for segment_2 in segments:
                segment_2.goto(1000, 1000)
            # Clearing the segments list for next play
            segments.clear()
            score_m = 0
            score.clear()
            score.write("Score: {0}  High Score: {1}".format(score_m, high_score), align='center',
                        font=('Courier', 18, 'normal'))

    time.sleep(delay)

wn.mainloop()
