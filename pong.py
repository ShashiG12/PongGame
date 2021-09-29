#based on https://learn.wecode24.com/pong-with-turtle-graphics-part-1/
from turtle import Turtle, Screen, Shape   
from random import randint

#sets up main screen
win = Screen()
win.title("Game")
win.setup(width = 800, height =600)

#turns off tracer
win.tracer(0)

#sets border variables for play area
play_top = win.window_height() / 2 -100
play_bottom = -win.window_height() / 2 +100
play_left = -win.window_width() / 2 +50
play_right = win.window_width() / 2 -50

#creates turtle for area
area = Turtle()
area.hideturtle()
area.penup()
area.goto(play_right, play_top)
area.pendown()
area.goto(play_left, play_top)
area.goto(play_left, play_bottom)
area.goto(play_right, play_bottom)
area.goto(play_right, play_top)

#creates turtle for ball
ball = Turtle()
ball.penup()
ball.shape("circle")
ball.color("red")
ball.shapesize(0.5,0.5)
ball_radius = 5

#creates paddle turtles
L = Turtle()
R = Turtle()
L.penup()
R.penup()

#dimensions of paddle
paddle_w_half = 10/2
paddle_h_half = 40/2
paddle_shape = Shape("compound")
paddle_points =((-paddle_h_half, -paddle_w_half),
                 (-paddle_h_half, paddle_w_half),
                 (paddle_h_half, paddle_w_half),
                 (paddle_h_half, -paddle_w_half))
paddle_shape.addcomponent(paddle_points, "black")
win.register_shape("paddle", paddle_shape)
L.shape("paddle")
R.shape("paddle")

#sets paddle starting positions
L.setx(play_left + 10)
R.setx(play_right - 10)

score_turtle = Turtle()
score_turtle.penup()
score_turtle.hideturtle()

score_L = 0
score_R = 0

#method for writing scores
def write_scores():
    score_turtle.clear()
    score_turtle.goto(-win.window_width()/4, win.window_height()/2 - 80)
    score_turtle.write(score_L, align="center", font=("Arial", 32, "bold"))
    score_turtle.goto(win.window_width()/4, win.window_height()/2 - 80)
    score_turtle.write(score_R, align="center", font=("Arial", 32, "bold"))

write_scores()

#updates screen
win.update()


#GAME LOGIC
#
#
#
#
#

ball_move_horiz = 3
ball_move_vert = 2

def ball_collides_with_paddle(paddle):
    x_distance = abs(paddle.xcor()-ball.xcor())
    y_distance = abs(paddle.ycor()-ball.ycor())
    overlap_horizontally = (ball_radius + paddle_w_half >= x_distance)
    overlap_vertically = (ball_radius + paddle_h_half >= y_distance)
    return overlap_horizontally and overlap_vertically

def update_ball_position():
    global ball_move_horiz, ball_move_vert
    ball.setx(ball.xcor() + ball_move_horiz)
    ball.sety(ball.ycor() + ball_move_vert)

    if ball.ycor() + ball_radius >= play_top:
        ball_move_vert *= -1
    elif play_bottom >= ball.ycor() - ball_radius:
        ball_move_vert *= -1
    ball.setx(ball.xcor() + ball_move_horiz)
    ball.sety(ball.ycor() + ball_move_vert)

    if ball.xcor() + ball_radius >= play_right:
        ball_move_horiz *= -1
    elif play_left >= ball.xcor() - ball_radius:
        ball_move_horiz *= -1
    ball.setx(ball.xcor() + ball_move_horiz)
    ball.sety(ball.ycor() + ball_move_vert)

    if ball_collides_with_paddle(R) or ball_collides_with_paddle(L) :
        ball_move_horiz *= -1

def reset_ball():
    global ball_move_horiz, ball_move_vert
    ball.setpos(0,0)
    speed_horiz = randint(2,4)
    speed_vert = randint(2,4)
    direction_vert = 1
    direction_horiz = 1
    if randint(0,100) >50:
        direction_horiz = -1
    if randint(0,100) >50:
        direction_vert = -1
    ball_move_horiz = direction_horiz * speed_horiz
    ball_move_vert = direction_vert * speed_vert

def check_if_score():
    global score_L, score_R
    if (ball.xcor() + ball_radius) >= play_right:
        score_L += 1
        write_scores()
        reset_ball()
    elif play_left >= (ball.xcor()-ball_radius):
        score_R += 1
        write_scores()
        reset_ball()

paddle_L_direction = 0
paddle_R_direction = 0

#on key press
def L_up():
    global paddle_L_direction
    paddle_L_direction = 1

def L_down():
    global paddle_L_direction
    paddle_L_direction = -1

def R_up():
    global paddle_R_direction
    paddle_R_direction = 1

def R_down():
    global paddle_R_direction
    paddle_R_direction = -1

win.onkeypress(L_up, "w")
win.onkeypress(L_down, "s")
win.onkeypress(R_up, "Up")
win.onkeypress(R_down, "Down")

#on key releases
def L_off():
    global paddle_L_direction
    paddle_L_direction = 0

def R_off():
    global paddle_R_direction
    paddle_R_direction = 0

win.onkeyrelease(L_off, "w")
win.onkeyrelease(L_off, "s")
win.onkeyrelease(R_off, "Up")
win.onkeyrelease(R_off, "Down")
win.listen()

paddle_move_vert = 20

def paddle_is_allowed_to_move(new_y_pos):
    if (play_bottom > new_y_pos - paddle_h_half):
        return False
    if (new_y_pos + paddle_h_half >play_top):
        return False
    return True

def update_paddle_positions():
    L_new_y_pos = L.ycor() + (paddle_L_direction * paddle_move_vert)
    R_new_y_pos = R.ycor() + (paddle_R_direction * paddle_move_vert)
    if paddle_is_allowed_to_move(L_new_y_pos):
        L.sety(L_new_y_pos)
    if paddle_is_allowed_to_move (R_new_y_pos):
        R.sety(R_new_y_pos)

def frame():
    check_if_score()
    update_paddle_positions()
    update_ball_position()
    win.update()
    win.ontimer(frame, framerate_ms)

framerate_ms = 40
frame()

win.mainloop()