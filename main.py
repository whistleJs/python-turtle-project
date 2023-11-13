import turtle as t
import random
import time

SCREEN_SIZE = 500           # 화면 크기
MAIN_SCREEN = t.Screen()    # 게임 화면
MAIN_SCREEN.setup(SCREEN_SIZE, SCREEN_SIZE)
MAIN_SCREEN._root.resizable(False, False)   # 전체 화면 막기
MAIN_SCREEN.bgcolor('black')
MAIN_SCREEN.tracer(0)

MINIGAME_PATTERN_TYPE = ['Q', 'W', 'E', 'A', 'S', 'D']    # 미니게임 패턴 타입
MINIGAME_LIMIT_TIME = 4                                   # 미니게임 제한 시간

ITEM_TYPE = {
  'SPEED_UP': '속도 증가',
  'AI_STOP': '추격 일시정지',
  'SPEED_DOWN': '속도 감소',
  'REVERSE': '방향키 반전'
}

# 게임 메시지 출력
def show_game_message(title = None, content = None):
  game_message.clear()
  if title is not None:
    game_message.goto(0, 30)
    game_message.write(title, align='center', font=('', 36, 'bold'))
  if content is not None:
    game_message.goto(0, -30)
    game_message.write(content, align='center', font=('', 16, 'bold'))

# 화면 상태 변경
def change_screen_style(minigame = False):
  show_game_message()

  for turtle in MINIGAME_TURTLE_LIST:
    turtle.clear()

  if minigame:
    player.hideturtle()
    bot.hideturtle()
    point.hideturtle()
    item.hideturtle()
    score_message.clear()
    minigame_message.clear()
    MAIN_SCREEN.bgcolor('white')
  else:
    player.showturtle()
    bot.showturtle()
    point.showturtle()
    item.showturtle()
    update_score(score)
    MAIN_SCREEN.bgcolor('black')

  MAIN_SCREEN.update()

# Turtle 생성
def create_turtle(shape='turtle', color = 'white'):
  turtle = t.Turtle()
  turtle.hideturtle()
  turtle.shape(shape)
  turtle.color(color)
  turtle.penup()
  turtle.speed(0)

  return turtle

# Turtle 각도 조절
def change_turtle_angle(turtle: t.Turtle, angle = 0):
  if start_game_time is None: return
  turtle.setheading(angle)

# 랜덤 좌표 값 반환
def get_random_position():
  GAP = 20
  return (
    random.randint(-SCREEN_SIZE / 2 + GAP, SCREEN_SIZE / 2 - GAP),
    random.randint(-SCREEN_SIZE / 2 + GAP, SCREEN_SIZE / 2 - GAP)
  )

# 화면 밖으로 나가는 경우 반대편으로 이동
def check_leave_screen(turtle: t.Turtle):
  [x, y] = turtle.pos()
  if x < -SCREEN_SIZE / 2 + 15:
    turtle.goto(SCREEN_SIZE / 2 - 15, y)
  elif x > SCREEN_SIZE / 2 - 15:
    turtle.goto(-SCREEN_SIZE / 2 + 15, y)
  elif y < -SCREEN_SIZE / 2 + 15:
    turtle.goto(x, SCREEN_SIZE / 2 - 15)
  elif y > SCREEN_SIZE / 2 - 15:
    turtle.goto(x, -SCREEN_SIZE / 2 + 15)

# 난이도 값 반환
def get_level():
  return 1

# 점수 업데이트 처리
def update_score(after_score):
  global score

  score = after_score
  score_message.clear()
  score_message.write(f'[Level {get_level()}] Score: {score}', align='center', font=('', 16))

# 랜덤 아이템 반환
def get_random_item(buff: bool):
  global bonus_speed
  global start_bot_timestop
  global start_reverse_time

  list = (['SPEED_UP'] * 7 + ['AI_STOP'] * 3) if buff else (['SPEED_DOWN'] * 7 + ['REVERSE'] * 3)
  random.shuffle(list)
  item = random.choice(list)

  if item == 'SPEED_UP':
    bonus_speed = min(bonus_speed + 0.15, 1.5)
  elif item == 'AI_STOP':
    start_bot_timestop = time.time() + 2
  elif item == 'SPEED_DOWN':
    bonus_speed = max(bonus_speed - 0.1, -0.5)
  elif item == 'REVERSE':
    start_reverse_time = time.time() + 2

  return item

# 미니게임 패턴 생성
def create_minigame_pattern():
  pattern_count = random.randint(6, 8)
  gap = SCREEN_SIZE / pattern_count

  for i in range(pattern_count):
    turtle = MINIGAME_TURTLE_LIST[i]
    pattern = random.choice(MINIGAME_PATTERN_TYPE)

    turtle.color('black')
    turtle.goto((gap * i + gap / 2) - SCREEN_SIZE / 2, 50)
    turtle.write(pattern, align='center', font=('', 20, 'bold'))

    MINIGAME_TURTLE_LIST.append(turtle)
    minigame_pattern_list.append(pattern)

# 미니게임 시작
def minigame_start():
  global start_minigame_time

  change_screen_style(True)   # 미니게임 화면 전환
  create_minigame_pattern()

  start_minigame_time = time.time()

  minigame_scheduler()

# 미니게임 진행 스케줄러
def minigame_scheduler():
  minigame_message.clear()

  if start_minigame_time is None: return

  remain_time = max(0, round(MINIGAME_LIMIT_TIME - (time.time() - start_minigame_time), 1))
  minigame_message.write(f'{remain_time}s', align='center', font=('', 16))

  if remain_time <= 0:
    minigame_over(False)
  else:
    MAIN_SCREEN.ontimer(minigame_scheduler, 50)

# 미니게임 키 이벤트 처리
def minigame_process_key(key):
  global minigame_success_count

  if start_minigame_time is None: return
  
  pattern = minigame_pattern_list[minigame_success_count]
  is_success = key is pattern

  turtle = MINIGAME_TURTLE_LIST[minigame_success_count]
  turtle.clear()
  turtle.color('blue' if is_success else 'red')
  turtle.write(pattern, align='center', font=('', 20, 'bold'))

  if is_success:
    minigame_success_count += 1
  else:
    minigame_over(False)
    return

  if minigame_success_count is len(minigame_pattern_list):
    minigame_over(True)

# 미니게임 종료
def minigame_over(success: bool):
  global start_minigame_time
  global minigame_pattern_list
  global minigame_success_count
  
  start_minigame_time = None
  minigame_pattern_list= []
  minigame_success_count = 0

  item = get_random_item(success)

  minigame_message.clear()
  minigame_message.write(f'패턴 공략에 성공했습니다! ({ITEM_TYPE[item]})' if success else f'패턴 공략에 실패했습니다. ({ITEM_TYPE[item]})', align='center', font=('', 18, 'bold'))
  MAIN_SCREEN.update()

  time.sleep(1.5) # 메세지 보여주기 위해서 일시적으로 멈추기

  change_screen_style()  # 터틀런 게임 화면 전환
  MAIN_SCREEN.ontimer(game_scheduler, 500)

# 게임 설정 초기화
def reset_setting():
  global score
  global start_game_time

  score = 0
  start_game_time = time.time()

  player.goto(0, 200)   # 게임 시작시 플레이어 상단으로 이동
  player.setheading(-90)
  bot.home()            # 게임 시작시 AI 가운데로 이동
  bot.setheading(90)
  point.goto(get_random_position())   # 게임 시작시 점수 랜덤 좌표로 이동
  item.goto(get_random_position())    # 게임 시작시 아이템 랜덤 좌표로 이동

  change_screen_style()

# 게임 진행 스케줄러
def game_scheduler():
  player.forward(1.5 + bonus_speed)
  check_leave_screen(player)

  # AI 추격 및 화면 밖으로 가는 경우 반대편으로 이동
  if (time.time() - start_bot_timestop < 1) is False:
    bot.forward(1.3)
    check_leave_screen(bot)

    # 일정 확률로 AI 각도 돌리기
    if random.randint(1, 20) == 2:
      change_turtle_angle(bot, bot.towards(player.pos()))

  # 게임 종료 조건
  if player.distance(bot) < 18:
    game_over()

  # 점수 먹은 조건
  if player.distance(point) < 16:
    update_score(score + 1)
    point.goto(get_random_position())

  # 아이템 먹은 조건
  if player.distance(item) < 14:
    minigame_start()
    item.goto(get_random_position())

  MAIN_SCREEN.update()

  if start_minigame_time is None and start_game_time is not None:
    MAIN_SCREEN.ontimer(game_scheduler, 10)

# 게임 시작
def game_start():
  if start_game_time is None:
    reset_setting()
    game_scheduler()

# 게임 종료
def game_over():
  global start_game_time

  total_score = score * 60 + round(time.time() - start_game_time)
  start_game_time = None
  
  score_message.clear()
  show_game_message(f'점수: {total_score}', '재시작 - [space]')

# 방향키(오른쪽) 이벤트 처리
def on_keypress_right():
  if (time.time() - start_reverse_time < 3):
    change_turtle_angle(player, 180)
  else:
    change_turtle_angle(player, 0)

# 방향키(위쪽) 이벤트 처리
def on_keypress_up():
  if (time.time() - start_reverse_time < 3):
    change_turtle_angle(player, -90)
  else:
    change_turtle_angle(player, 90)

# 방향키(왼쪽) 이벤트 처리
def on_keypress_left():
  if (time.time() - start_reverse_time < 3):
    change_turtle_angle(player, 0)
  else:
    change_turtle_angle(player, 180)

# 방향키(아래쪽) 이벤트 처리
def on_keypress_down():
  if (time.time() - start_reverse_time < 3):
    change_turtle_angle(player, 90)
  else:
    change_turtle_angle(player, -90)

# 키(Q) 이벤트 처리
def on_keypress_q():
  minigame_process_key('Q')

# 키(W) 이벤트 처리
def on_keypress_w():
  minigame_process_key('W')

# 키(E) 이벤트 처리
def on_keypress_e():
  minigame_process_key('E')

# 키(A) 이벤트 처리
def on_keypress_a():
  minigame_process_key('A')

# 키(s) 이벤트 처리
def on_keypress_s():
  minigame_process_key('S')

# 키(d) 이벤트 처리
def on_keypress_d():
  minigame_process_key('D')

MINIGAME_TURTLE_LIST = list(map(lambda _: create_turtle(), range(8)))

player = create_turtle()                                  # 플레이어
bot = create_turtle(color='#ff5c5c')                      # AI
point = create_turtle(shape='circle', color='#ffa748')    # 점수
item = create_turtle(shape='square', color='#3623ff')     # 아이템

game_message = create_turtle()                  # 게임 메시지
minigame_message = create_turtle(color='black') # 미니게임 메시지
minigame_message.goto(0, -50)                   # 미니게임 메시지 기본 위치 설정
score_message = create_turtle()                 # 점수 메시지
score_message.goto(0, -100)                     # 점수 메시지 기본 위치 설정
status_message = create_turtle()                # 상태 메시지

start_game_time = None        # 터틀런 게임 시작 시간
start_minigame_time = None    # 미니게임 게임 시작 시간

minigame_pattern_list = []    # 미니게임 패턴 리스트 (게임 진행시 생성)
minigame_success_count = 0    # 미니게임 패턴 성공 횟수

score = 0                     # 점수
bonus_speed = 0               # 아이템 효과 - 플레이어 추가 속도
start_bot_timestop = 0        # 아이템 효과 - AI 시간 정지
start_reverse_time = 0        # 아이템 효과 - 방향키 반전

# 터틀런 키 이벤트
MAIN_SCREEN.onkeypress(on_keypress_right, 'Right')
MAIN_SCREEN.onkeypress(on_keypress_up, 'Up')
MAIN_SCREEN.onkeypress(on_keypress_left, 'Left')
MAIN_SCREEN.onkeypress(on_keypress_down, 'Down')
MAIN_SCREEN.onkeypress(game_start, 'space')

# 미니게임 키 이벤트
MAIN_SCREEN.onkeypress(on_keypress_q, 'q')
MAIN_SCREEN.onkeypress(on_keypress_w, 'w')
MAIN_SCREEN.onkeypress(on_keypress_e, 'e')
MAIN_SCREEN.onkeypress(on_keypress_a, 'a')
MAIN_SCREEN.onkeypress(on_keypress_s, 's')
MAIN_SCREEN.onkeypress(on_keypress_d, 'd')

show_game_message('Turtle Run', '시작 - [space]')

MAIN_SCREEN.listen()
MAIN_SCREEN.mainloop()