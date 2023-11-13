import turtle as t
import random

ITEM_LIST = (
  # 투명효과 (봇 충돌 무시)
  (['TRANSPARENT'] * 3) + 
  # 시간 정지 (봇 일시 정지)
  (['STOP'] * 4) + 
  # 속도 증가 (유저 속도 증가)
  (['SPEED_UP'] * 7) + 
  # [디버프] 속도 감소 (유저 속도 감소)
  (['SPEED_DOWN'] * 7) +
  # [디버프] 방향키 전환
  (['REVERSE'] * 4)
)
random.shuffle(ITEM_LIST)
print(ITEM_LIST)

playing = False
score = 0

item = -1
bonus_speed = 0
stop_check = 0

def get_random_pos():
  return random.randint(-230, 230)

def get_level():
  if score < 3:
    return 1
  elif score < 10:
    return 2
  elif score < 25:
    return 3
  elif score < 50:
    return 4
  else:
    return 5
    
def get_bot_chase_range():
  level = get_level()

  if level <= 2:
    return 10
  elif level == 3:
    return 7
  elif level == 4:
    return 4
  else:
    return 2
  
def get_bot_speed():
  level = get_level()

  if level == 1:
    return 2.5
  elif level == 2:
    return 3.6
  elif level == 3:
    return 4.3
  else:
    return 4.8
  
def get_user_speed():
  level = get_level()

  if level == 1:
    return 4
  elif level == 2:
    return 4.3
  elif level == 3:
    return 4.8
  else:
    return 5

message = t.Turtle()
item_message = t.Turtle()
bot = t.Turtle()
point = t.Turtle()
user = t.Turtle()
item = t.Turtle()

def turn_right():
  if playing:
    user.setheading(0)

def turn_up():
  if playing:
    user.setheading(90)

def turn_left():
  if playing:
    user.setheading(180)

def turn_down():
  if playing:
    user.setheading(270)

def show_item_message(item):
  color = '#3623ff'

  if item == 'SPEED_UP':
    content = 'Bonus Speed!'
  elif item == 'STOP':
    content = 'Time Stop!'
  elif item == 'TRANSPARENT':
    content = 'Invisible!'
  elif item == 'SPEED_DOWN':
    content = 'Speed Down :('
    color = '#ff5c5c'
  elif item == 'REVERSE':
    content = 'Reverse direction X('
    color = '#ff5c5c'

  item_message.color(color)
  item_message.write(content, align='center', font=('', 12))

def show_message(title, content):
  message.clear()

  if title != '':
    message.goto(0, 100)
    message.write(title, False, 'center', ('', 25))

  if content != '':
    message.goto(0, -100)
    message.write(content, False, 'center', ('', 15))

  message.home()

# Init Setting
def init_setting():
  bot.shape('turtle')
  bot.color('#ff5c5c')
  bot.speed(0)
  bot.penup()

  point.shape('circle')
  point.color('#ffa748')
  point.speed(0)
  point.penup()

  user.shape('turtle')
  user.color('#592ed9')
  user.speed(0)
  user.penup()

  message.color('white')
  message.speed(0)
  message.penup()
  message.hideturtle()

  item_message.speed(0)
  item_message.penup()
  item_message.hideturtle()

  item.shape('square')
  item.color('#3623ff')
  item.speed(0)
  item.penup()

  t.setup(500, 500)
  t.bgcolor('#44a4ff')

  show_message('Turtle Run', '[Space]')

  reset_setting()

# Reset Setting
def reset_setting():
  global playing
  global score
  global bonus_speed
  
  point.goto(get_random_pos(), get_random_pos())
  item.goto(get_random_pos(), get_random_pos())
  user.goto(0, 200)
  user.setheading(270)
  bot.goto(0, 0)
  bot.setheading(90)

  playing = False
  score = 0
  bonus_speed = 0

# Start Game
def start_game():
  global playing

  if playing == False:
    playing = True
    message.clear()
    play()

# Play
def play():
  global playing
  global score
  # [Item Effect]
  global bonus_speed
  global stop_check

  # [Level] Angle
  if random.randint(1, get_bot_chase_range()) == 2:
    bot.setheading(bot.towards(user.pos()))

  # [Level] Speed
  if stop_check == 0:
    user.forward(get_user_speed() + bonus_speed)
    bot.forward(get_bot_speed())
  else:
    user.forward((get_user_speed() + bonus_speed) / 2)
    stop_check += 1
    if stop_check > 100:
      stop_check = 0

  # [Check] Game Over
  if user.distance(bot) < 12:
    show_message(f'Game Over (Score: {score})', 'Again? [Space]')
    reset_setting()

  # [Check] Point
  if user.distance(point) < 12:
    score += 1
    point.goto(get_random_pos(), get_random_pos())
    show_message('', f'[Level {get_level()}] score: {score}')

  # [Check] Item
  if user.distance(item) < 12:
    item.goto(get_random_pos(), get_random_pos())
    item_message.clear()
    item_message.goto(user.pos())
    choice_item = random.choice(ITEM_LIST)

    if choice_item == 'SPEED_UP':
      if bonus_speed < 0.5:
       bonus_speed += 0.05
    elif choice_item == 'STOP':
      stop_check += 1
    elif choice_item == 'SPEED_DOWN':
      if bonus_speed > -0.3:
       bonus_speed -= 0.025

    show_item_message(choice_item)

  if playing:
    t.ontimer(play, 10)

t.onkeypress(turn_right, 'Right')
t.onkeypress(turn_up, 'Up')
t.onkeypress(turn_left, 'Left')
t.onkeypress(turn_down, 'Down')
t.onkeypress(start_game, 'space')

init_setting()

t.listen()
t.mainloop()