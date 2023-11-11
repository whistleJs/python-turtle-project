import turtle as t
import random

PATTERN_TYPE = ['Q', 'W', 'E', 'R', 'A', 'S', 'D', 'F']

pattern_turtle = t.Turtle()
pattern_turtle.color('black')
pattern_turtle.hideturtle()
pattern_turtle.penup()
pattern_turtle.speed(0)

success_pattern_turtle = t.Turtle()
success_pattern_turtle.hideturtle()
success_pattern_turtle.penup()
success_pattern_turtle.speed(0)

message = t.Turtle()
message.color('black')
message.hideturtle()
message.speed(0)
message.goto(0, -50)

pattern_list = []
success_count = 0
limit_time = 0
is_playing = False
is_success_pattern = False

def start():
  global success_count
  global limit_time
  global is_playing
  global is_success_pattern

  if is_playing == False:
    success_count = 0
    limit_time = random.randint(6, 9)
    is_playing = True
    is_success_pattern = False

    create_pattern()
    timer()

def get_pattern_pos(i):
  return (400 / len(pattern_list) * i - 170, 50)

def create_pattern():
  global pattern_list

  pattern_list = []
  pattern_turtle.clear()
  success_pattern_turtle.clear()

  for _ in range(random.randint(6, 8)):
    pattern_list.append(random.choice(PATTERN_TYPE))
  
  pattern_size = len(pattern_list)
  for i in range(pattern_size):
    pattern_turtle.goto(get_pattern_pos(i))
    pattern_turtle.write(pattern_list[i], align='center', font=('', 14))

def timer():
  global is_playing
  global is_success_pattern
  global limit_time

  message.clear()

  if is_success_pattern:
    message.write('Success!', align='center', font=('', 16))
    is_playing = False
    return

  if limit_time <= 0:
    message.write('Time over', align='center', font=('', 12))
    is_playing = False
    return

  limit_time = round(limit_time - 0.1, 2)

  message.write(f'{limit_time}s', align='center', font=('', 12))
  t.ontimer(timer, 50)

def on_key_pattern(key):
  global is_success_pattern
  global success_count

  if is_playing == False:
    return

  success_pattern_turtle.goto(get_pattern_pos(success_count))

  if pattern_list[success_count] == key:
    success_pattern_turtle.color('blue')
    success_pattern_turtle.write(key, align='center', font=('', 14))
    success_count += 1
  else:
    success_pattern_turtle.color('red')
    success_pattern_turtle.write(pattern_list[success_count], align='center', font=('', 14))

  is_success_pattern = success_count == len(pattern_list)

def on_key_q():
  on_key_pattern('Q')

def on_key_w():
  on_key_pattern('W')

def on_key_e():
  on_key_pattern('E')

def on_key_r():
  on_key_pattern('R')

def on_key_a():
  on_key_pattern('A')

def on_key_s():
  on_key_pattern('S')

def on_key_d():
  on_key_pattern('D')

def on_key_f():
  on_key_pattern('F')

t.setup(500, 500)
t.onkeypress(on_key_q, 'q')
t.onkeypress(on_key_w, 'w')
t.onkeypress(on_key_e, 'e')
t.onkeypress(on_key_r, 'r')
t.onkeypress(on_key_a, 'a')
t.onkeypress(on_key_s, 's')
t.onkeypress(on_key_d, 'd')
t.onkeypress(on_key_f, 'f')
t.onkeypress(start, 'space')

t.listen()
t.mainloop()
