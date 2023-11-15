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

DEFAULT_PLAYER_SPEED = 1.5    # 플레이어 기본 속도
MAX_BONUS_SPEED = 1.5         # 플레이어 최고 추가 속도
MIN_BONUS_SPEED = -0.5        # 플레이어 최소 추가 속도
INCREASE_SPEED = 0.15         # 플레이어 추가 속도 증가량
DECREASE_SPEED = -0.1         # 플레이어 추가 속도 감소량
BOT_STOP_TIME = 1.5     # AI가 멈추는 시간
REVERSE_TIME = 5      # 방향키 반전 시간

ITEM_TYPE = {
  'SPEED_UP': f'속도 +{INCREASE_SPEED}',
  'AI_STOP': 'AI 일시정지',
  'SPEED_DOWN': f'속도 {DECREASE_SPEED}',
  'REVERSE': '방향키 반전'
}

# 플레이 시간 계산
def get_play_time():
  return round(time.time() - start_game_time - acc_minigame_time, 1)

# 난이도 값 반환
def get_level():
  playtime = get_play_time()

  if playtime < 10:
    return 1
  elif playtime < 25:
    return 2
  elif playtime < 50:
    return 3
  elif playtime < 90:
    return 4
  else:
    return 5
  
# 다음 레벨까지 남은 시간 계산
def get_remain_time_next_level():
  level = get_level()
  playtime = get_play_time()

  if level == 1:
    return round(10 - playtime, 1)
  elif level == 2:
    return round(25 - playtime, 1)
  elif level == 3:
    return round(50 - playtime, 1)
  elif level == 4:
    return round(90 - playtime, 1)

# 총합 점수 계산
def get_total_score():
  return round(score * 60 + get_play_time(), 1)

# 플레이어 속도 계산
def get_player_speed():
  return round(max(DEFAULT_PLAYER_SPEED + MIN_BONUS_SPEED, min(DEFAULT_PLAYER_SPEED + bonus_speed, DEFAULT_PLAYER_SPEED + MAX_BONUS_SPEED)), 2) # 최소 1, 최대 3

# AI 속도 계산
def get_bot_speed():
  level = get_level()

  if level == 1:
    return 1.3
  elif level == 2:
    return 1.55
  elif level == 3:
    return 1.8
  elif level == 4:
    return 2.35
  else:
    return 2.7

# AI 활성화 개수
def get_bot_count():
  level = get_level()

  if level == 1:
    return 1
  if level == 2:
    return 3
  elif level == 3:
    return 6
  elif level == 4:
    return 10
  else:
    return 15

# 미니게임 제한 시간
def get_minigame_limit_time():
  level = get_level()

  if level <= 3:
    return 3.5
  elif level == 3:
    return 3
  else:
    return 2.5

# 게임 메시지 출력
def show_game_message(title = None, content = None):
  game_message.clear()
  if title is not None:
    game_message.goto(0, 30)
    game_message.write(title, align='center', font=('', 36, 'bold'))
  if content is not None:
    game_message.goto(0, -30)
    game_message.write(content, align='center', font=('', 16, 'bold'))

# 게임 상태 정보 업데이트
def update_status():
  status_message.clear()
  status_message.color('#4a4a4a')
  status_message.goto(0, SCREEN_SIZE / 2 - 30)
  status_message.write(f'Level {get_level()} | 점수: {get_total_score()}', align='center', font=('', 14))
  status_message.goto(0, SCREEN_SIZE / 2 - 50)
  status_message.write(f'플레이어 속도: {get_player_speed()} | AI 속도: {get_bot_speed()} | AI 개수: {get_bot_count()}개', align='center', font=('', 14))

  # AI 멈추는 시간 표시
  remain_bot_timestop = round(BOT_STOP_TIME - (time.time() - start_bot_timestop), 1)
  if remain_bot_timestop > 0 and remain_bot_timestop < BOT_STOP_TIME:
    for i in range(get_bot_count()):
      [x, y] = BOT_LIST[i].pos()
      status_message.color('#ff5c5c')
      status_message.goto(x + 2, y + 15)
      status_message.write(f'{remain_bot_timestop}s', align='center', font=('', 12))

  # 방향키 반전 시간 표시
  remain_reverse_time = round(REVERSE_TIME - (time.time() - start_reverse_time), 1)
  if remain_reverse_time > 0 and remain_reverse_time < REVERSE_TIME:
    [x ,y] = player.pos()
    status_message.color('#274fff')
    status_message.goto(x + 2, y + 15)
    status_message.write(f'{remain_reverse_time}s', align='center', font=('', 12, 'bold'))

  # 레벨 증가 알림
  remain_time_to_next_level = get_remain_time_next_level()
  alert_message.clear()
  if remain_time_to_next_level < 5:
    alert_message.write(f'다음 레벨까지 {remain_time_to_next_level}s', align='center', font=('', 16, 'bold'))

# 화면 상태 변경
def change_screen_style(minigame = False):
  game_message.clear()
  status_message.clear()

  for turtle in MINIGAME_TURTLE_LIST:
    turtle.clear()

  for i in range(get_bot_count()):
    BOT_LIST[i].hideturtle() if minigame else BOT_LIST[i].showturtle()

  if minigame:
    player.hideturtle()
    point.hideturtle()
    item.hideturtle()
    minigame_message.clear()
    MAIN_SCREEN.bgcolor('white')
  else:
    player.showturtle()
    point.showturtle()
    item.showturtle()
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

# 랜덤 아이템 반환
def get_random_item(buff: bool):
  global bonus_speed
  global start_bot_timestop
  global start_reverse_time

  list = (['SPEED_UP'] * 7 + ['AI_STOP'] * 3) if buff else (['SPEED_DOWN'] * 7 + ['REVERSE'] * 3)
  random.shuffle(list)
  item = random.choice(list)

  if item == 'SPEED_UP':
    bonus_speed = min(bonus_speed + INCREASE_SPEED, MAX_BONUS_SPEED)
  elif item == 'AI_STOP':
    start_bot_timestop = time.time() + 2
  elif item == 'SPEED_DOWN':
    bonus_speed = max(bonus_speed + DECREASE_SPEED, MIN_BONUS_SPEED)
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

  remain_time = max(0, round(get_minigame_limit_time() - (time.time() - start_minigame_time), 1))
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
  turtle.color('#274fff' if is_success else '#ff5c5c')
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
  global acc_minigame_time
  global minigame_pattern_list
  global minigame_success_count

  acc_minigame_time += round(time.time() - start_minigame_time, 1) + 2
  
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
  global bonus_speed
  global start_game_time
  global acc_minigame_time

  score = 0
  bonus_speed = 0
  start_game_time = time.time()
  acc_minigame_time = 0

  for turtle in BOT_LIST: turtle.goto(get_random_position())

  player.goto(0, 200)   # 게임 시작시 플레이어 상단으로 이동
  player.setheading(-90)
  point.goto(get_random_position())   # 게임 시작시 점수 랜덤 좌표로 이동
  item.goto(get_random_position())    # 게임 시작시 아이템 랜덤 좌표로 이동

  change_screen_style()

# 게임 진행 스케줄러
def game_scheduler():
  global score

  player.forward(get_player_speed())
  check_leave_screen(player)

  # AI 추격 및 화면 밖으로 가는 경우 반대편으로 이동
  if (time.time() - start_bot_timestop < BOT_STOP_TIME) is False:
    for i in range(get_bot_count()):
      bot = BOT_LIST[i]
      bot.showturtle()
      bot.forward(get_bot_speed())
      check_leave_screen(bot)

      # 일정 확률로 AI 각도 돌리기
      if random.randint(1, 20) == 2:
        change_turtle_angle(bot, bot.towards(player.pos()))

  # 게임 종료 조건
  is_collision = len(list(filter(lambda i: player.distance(BOT_LIST[i]) < 18, range(get_bot_count())))) > 0
  if is_collision:
    game_over()

  # 점수 먹은 조건
  if player.distance(point) < 16:
    score += 1
    point.goto(get_random_position())

  # 아이템 먹은 조건
  if player.distance(item) < 14:
    minigame_start()
    item.goto(get_random_position())

  if start_minigame_time is None and start_game_time is not None:
    update_status()
    MAIN_SCREEN.update()
    MAIN_SCREEN.ontimer(game_scheduler, 10)

# 게임 시작
def game_start():
  if start_game_time is None:
    reset_setting()
    game_scheduler()

# 게임 종료
def game_over():
  global start_game_time

  total_score = get_total_score()
  start_game_time = None

  for turtle in BOT_LIST: turtle.hideturtle()
  
  status_message.clear()
  player.hideturtle()
  point.hideturtle()
  item.hideturtle()
  show_game_message(f'점수: {total_score}', '재시작 - [space]')
  MAIN_SCREEN.update()

# 방향키(오른쪽) 이벤트 처리
def on_keypress_right():
  if (time.time() - start_reverse_time < REVERSE_TIME):
    change_turtle_angle(player, 180)
  else:
    change_turtle_angle(player, 0)

# 방향키(위쪽) 이벤트 처리
def on_keypress_up():
  if (time.time() - start_reverse_time < REVERSE_TIME):
    change_turtle_angle(player, -90)
  else:
    change_turtle_angle(player, 90)

# 방향키(왼쪽) 이벤트 처리
def on_keypress_left():
  if (time.time() - start_reverse_time < REVERSE_TIME):
    change_turtle_angle(player, 0)
  else:
    change_turtle_angle(player, 180)

# 방향키(아래쪽) 이벤트 처리
def on_keypress_down():
  if (time.time() - start_reverse_time < REVERSE_TIME):
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

# 그 외 모든 키 입력 처리
def on_keypress_other():
  minigame_process_key(None)

MINIGAME_TURTLE_LIST = list(map(lambda _: create_turtle(), range(8)))
BOT_LIST = list(map(lambda _: create_turtle(color='#ff5c5c'), range(15)))

player = create_turtle()                                  # 플레이어
point = create_turtle(shape='circle', color='#ffa748')    # 점수
item = create_turtle(shape='square', color='#274fff')     # 아이템

game_message = create_turtle()                  # 게임 메시지
minigame_message = create_turtle(color='black') # 미니게임 메시지
minigame_message.goto(0, -50)                   # 미니게임 메시지 기본 위치 설정
status_message = create_turtle()                # 상태 메시지
alert_message = create_turtle()
alert_message.goto(0, -50)

start_game_time = None        # 터틀런 게임 시작 시간
start_minigame_time = None    # 미니게임 게임 시작 시간
acc_minigame_time = 0         # 총합 미니게임 플레이 시간

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
MAIN_SCREEN.onkeypress(on_keypress_other, '')

show_game_message('Turtle Run', '시작 - [space]')

MAIN_SCREEN.listen()
MAIN_SCREEN.mainloop()