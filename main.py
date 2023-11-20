import turtle as t
import random
import time

SCREEN_SIZE = 500           # 화면 크기
MAIN_SCREEN = t.Screen()    # 게임 화면
MAIN_SCREEN.setup(SCREEN_SIZE, SCREEN_SIZE)
MAIN_SCREEN._root.resizable(False, False)   # 전체 화면 막기
MAIN_SCREEN.register_shape('potion.gif')
MAIN_SCREEN.register_shape('bot.gif')
MAIN_SCREEN.register_shape('turtle.gif')
MAIN_SCREEN.register_shape('point.gif')
MAIN_SCREEN.bgcolor('black')
MAIN_SCREEN.tracer(0)

MINIGAME_PATTERN_TYPE = ['Q', 'W', 'E', 'A', 'S', 'D']    # 미니게임 패턴 타입

DEFAULT_PLAYER_SPEED = 2      # 플레이어 기본 속도
MAX_BONUS_SPEED = 1.5         # 플레이어 최고 추가 속도
MIN_BONUS_SPEED = -0.5        # 플레이어 최소 추가 속도
INCREASE_SPEED = 0.15         # 플레이어 추가 속도 증가량
DECREASE_SPEED = -0.1         # 플레이어 추가 속도 감소량
BOT_STOP_TIME = 1.5     # AI가 멈추는 시간
REVERSE_TIME = 5        # 방향키 반전 시간

# 아이템 타입 정리
ITEM_TYPE = {
  'SPEED_UP': f'속도 +{INCREASE_SPEED}',
  'AI_STOP': 'AI 일시정지',
  'SPEED_DOWN': f'속도 {DECREASE_SPEED}',
  'REVERSE': '방향키 반전'
}

# 화면 메시지 정보
MESSAGE_INFO = {
  'GAME_START': [
    { 'x': 0, 'y': 60, 'size': 32, 'message': 'Turtle Run' },
    { 'x': 0, 'y': -20, 'size': 14, 'message': '게임 시작' },
    { 'x': 0, 'y': -60, 'size': 14, 'message': '도움말' },
    { 'x': 0, 'y': -100, 'size': 14, 'message': '종료' },
  ],
  'GAME_OVER': [
    { 'x': 0, 'y': 60, 'size': 32, 'message': '점수: $total_score' },
    { 'x': 0, 'y': -20, 'size': 14, 'message': '게임 재시작' },
    { 'x': 0, 'y': -60, 'size': 14, 'message': '도움말' },
    { 'x': 0, 'y': -100, 'size': 14, 'message': '종료' },
  ],
  'HELP': [
    { 'x': 0, 'y': 180, 'size': 24, 'message': '도움말' },
    { 'x': 0, 'y': -200, 'size': 16, 'message': '게임 시작' },
    { 'x': -180, 'y': 140, 'size': 14, 'align': 'left', 'message': '[플레이어]: 방향키(상하좌우)를 통해 방향을 전환할 수 있습니다.' },
    { 'x': -180, 'y': 90, 'size': 14, 'align': 'left', 'message': '[점수]: 점수가 추가로 증가합니다.' },
    { 'x': -180, 'y': 40, 'size': 14, 'align': 'left', 'message': '[아이템]: 패턴이 발동되면 성공하면 버프, 실패하면 디버프가 발생합니다.' },
    { 'x': -180, 'y': -10, 'size': 14, 'align': 'left', 'message': '[패턴]: 제한 시간 안에 제시하는 키워드를 입력해야합니다.' },
    { 'x': -180, 'y': -60, 'size': 14, 'align': 'left', 'message': '[AI]: 레벨에 따라 속도가 상승하며 개수가 증가합니다.' },
    { 'x': -180, 'y': -100, 'size': 14, 'align': 'left', 'message': '[레벨]: 1부터 시작하여 최대 5단계까지 있으며' },
    { 'x': -140, 'y': -120, 'size': 14, 'align': 'left', 'message': '최대 단계 도달 시 점수를 먹었을 때도 패턴이 발동됩니다.' },
  ]
}

# 플레이 시간 계산
def get_play_time():
  if start_game_time is None: return 0
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
  return round(
    max(DEFAULT_PLAYER_SPEED + MIN_BONUS_SPEED,
      min(DEFAULT_PLAYER_SPEED + bonus_speed,
          DEFAULT_PLAYER_SPEED + MAX_BONUS_SPEED)), 2) # 최소 1, 최대 3

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
def show_game_message():
  game_message.clear()

  if view_type == 'HELP':
    player_sample.showturtle()
    point_sample.showturtle()
    item_sample.showturtle()
    bot_sample.showturtle()
  else:
    player_sample.hideturtle()
    point_sample.hideturtle()
    item_sample.hideturtle()
    bot_sample.hideturtle()

  for i in range(len(MESSAGE_INFO[view_type])):
    row = MESSAGE_INFO[view_type][i]
    align = row.get('align')
    message: str = row['message']
    message = message.replace('$total_score', str(prev_total_score))

    if align is None:
      align = 'center'
    
    if i == menu + 1:
      font = ('맑은 고딕', row['size'], 'underline')
    else:
      font = ('맑은 고딕', row['size'])
    
    game_message.goto(row['x'], row['y'])
    game_message.write(message, align=align, font=font)

  MAIN_SCREEN.update()

# 게임 상태 정보 업데이트
def update_status():
  status_message.clear()
  status_message.color('#4a4a4a')
  # 상단 1번째 줄
  first_line_message = f'Level {get_level()} | 점수: {get_total_score()}'
  status_message.goto(0, SCREEN_SIZE / 2 - 30)
  status_message.write(first_line_message, align='center', font=('맑은 고딕', 14))
  # 상단 2번째 줄
  second_line_message = f'플레이어 속도: {get_player_speed()}'
  if bonus_speed == MAX_BONUS_SPEED:
    second_line_message += '(최대 속도)'
  second_line_message += f' | AI 속도: {get_bot_speed()} | AI 개수: {get_bot_count()}개'
  status_message.goto(0, SCREEN_SIZE / 2 - 50)
  status_message.write(second_line_message, align='center', font=('맑은 고딕', 14))

  # AI 멈추는 시간 표시
  remain_bot_timestop = round(BOT_STOP_TIME - (time.time() - start_bot_timestop), 1)
  if remain_bot_timestop > 0 and remain_bot_timestop < BOT_STOP_TIME:
    for i in range(get_bot_count()):
      [x, y] = BOT_LIST[i].pos()
      status_message.color('#ff5c5c')
      status_message.goto(x + 2, y + 15)
      status_message.write(f'{remain_bot_timestop}s', align='center', font=('맑은 고딕', 12))

  # 방향키 반전 시간 표시
  remain_reverse_time = round(REVERSE_TIME - (time.time() - start_reverse_time), 1)
  if remain_reverse_time > 0 and remain_reverse_time < REVERSE_TIME:
    [x ,y] = player.pos()
    status_message.color('#274fff')
    status_message.goto(x + 2, y + 15)
    status_message.write(f'{remain_reverse_time}s', align='center', font=('맑은 고딕', 12, 'bold'))

  # 레벨 증가 알림
  level = get_level()
  remain_time_to_next_level = get_remain_time_next_level()
  time_message.clear()
  if level < 5 and remain_time_to_next_level < 5:
    time_message.write(f'다음 레벨까지 {remain_time_to_next_level}s', align='center', font=('맑은 고딕', 16, 'bold'))

# 화면 상태 변경
def change_screen_style(minigame = False):
  game_message.clear()
  minigame_message.clear()
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
def create_turtle(shape='turtle', color='white', size=1):
  turtle = t.Turtle(shape=shape, visible=False)
  turtle.color(color)
  turtle.shapesize(1.0 * size, 1.0 * size, 1)
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
  global bonus_speed, start_bot_timestop, start_reverse_time

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
    turtle.write(pattern, align='center', font=('맑은 고딕', 20, 'bold'))

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
  if start_minigame_time is None: return
  minigame_message.clear()

  remain_time = max(0, round(get_minigame_limit_time() - (time.time() - start_minigame_time), 1))
  minigame_message.write(f'{remain_time}s', align='center', font=('맑은 고딕', 16))

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
  turtle.write(pattern, align='center', font=('맑은 고딕', 20, 'bold'))

  if is_success:
    minigame_success_count += 1
  else:
    minigame_over(False)
    return

  if minigame_success_count is len(minigame_pattern_list):
    minigame_over(True)

# 미니게임 종료
def minigame_over(success: bool):
  global start_minigame_time, acc_minigame_time, minigame_pattern_list, minigame_success_count

  acc_minigame_time += round(time.time() - start_minigame_time, 1) + 2
  
  start_minigame_time = None
  minigame_pattern_list= []
  minigame_success_count = 0

  item = get_random_item(success)

  minigame_message.clear()
  minigame_message.write(f'패턴 공략에 성공했습니다! ({ITEM_TYPE[item]})' if success else f'패턴 공략에 실패했습니다. ({ITEM_TYPE[item]})', align='center', font=('맑은 고딕', 18, 'bold'))
  MAIN_SCREEN.update()

  time.sleep(1.5) # 메세지 보여주기 위해서 일시적으로 멈추기

  change_screen_style()  # 터틀런 게임 화면 전환
  MAIN_SCREEN.ontimer(game_scheduler, 500)

# 게임 설정 초기화
def reset_setting():
  global score, bonus_speed, start_game_time, acc_minigame_time, start_bot_timestop, start_reverse_time

  score = 0
  bonus_speed = 0
  start_game_time = time.time()
  acc_minigame_time = 0
  start_bot_timestop = 0
  start_reverse_time = 0

  for turtle in BOT_LIST: turtle.goto(get_random_position())

  player.goto(0, 200)   # 게임 시작시 플레이어 상단으로 이동
  player.setheading(-90)
  point.goto(get_random_position())   # 게임 시작시 점수 랜덤 좌표로 이동
  item.goto(get_random_position())    # 게임 시작시 아이템 랜덤 좌표로 이동

  player_sample.hideturtle()
  point_sample.hideturtle()
  item_sample.hideturtle()
  bot_sample.hideturtle()
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
    # 난이도 조절
    if get_level() == 5:
      minigame_start()

  # 아이템 먹은 조건
  if player.distance(item) < 20:
    minigame_start()
    item.goto(get_random_position())

  if start_minigame_time is None and start_game_time is not None:
    update_status()
    MAIN_SCREEN.update()
    MAIN_SCREEN.ontimer(game_scheduler, 10)

# 게임 시작
def game_start():
  global view_type

  if start_game_time is None:
    view_type = 'GAME_OVER'
    reset_setting()
    game_scheduler()

# 게임 종료
def game_over():
  global prev_total_score, start_game_time

  prev_total_score = get_total_score()
  start_game_time = None

  for turtle in BOT_LIST: turtle.hideturtle()
  
  status_message.clear()
  time_message.clear()
  player.hideturtle()
  point.hideturtle()
  item.hideturtle()
  show_game_message()
  MAIN_SCREEN.update()

# 방향키(오른쪽) 이벤트 처리
def on_keypress_right():
  if (time.time() - start_reverse_time < REVERSE_TIME):
    change_turtle_angle(player, 180)
  else:
    change_turtle_angle(player, 0)

# 방향키(위쪽) 이벤트 처리
def on_keypress_up():
  global menu

  if start_game_time is None and (view_type == 'GAME_START' or view_type == 'GAME_OVER'):
    menu = max(menu - 1, 0)
    show_game_message()

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
  global menu

  if start_game_time is None and (view_type == 'GAME_START' or view_type == 'GAME_OVER'):
    menu = min(menu + 1, 2)
    show_game_message()

  if (time.time() - start_reverse_time < REVERSE_TIME):
    change_turtle_angle(player, 90)
  else:
    change_turtle_angle(player, -90)

# 키(space) 이벤트 처리
def on_keypress_space():
  global view_type, menu

  if menu == 0:
    game_start()
  elif menu == 1:
    view_type = 'HELP'
    menu = 0
    show_game_message()
  elif menu == 2:
    t.bye()

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

# 미니게임 터틀 모음
MINIGAME_TURTLE_LIST = list(map(lambda _: create_turtle(), range(8)))
# AI 터틀 모음
BOT_LIST = list(map(lambda _: create_turtle(shape='bot.gif'), range(15)))

player = create_turtle(shape='turtle.gif')    # 플레이어
point = create_turtle(shape='point.gif')      # 점수
item = create_turtle(shape='potion.gif')      # 아이템

player_sample = create_turtle(shape='turtle.gif')    # 도움말용 플레이어
point_sample = create_turtle(shape='point.gif')      # 도움말용 점수
item_sample = create_turtle(shape='potion.gif')      # 도움말용 아이템
bot_sample = create_turtle(shape='bot.gif')          # 도움말용 AI

game_message = create_turtle()                    # 게임 메시지
minigame_message = create_turtle(color='black')   # 미니게임 메시지
status_message = create_turtle()                  # 상태 메시지
time_message = create_turtle()                    # 시간 알림 메시지

# 최초 생성 시 이동 (이동 필요 없음)
player_sample.goto(-210, 150)
point_sample.goto(-210, 100)
item_sample.goto(-210, 50)
bot_sample.goto(-210, -50)
minigame_message.goto(0, -50)
time_message.goto(0, -50)

start_game_time = None        # 터틀런 게임 시작 시간
start_minigame_time = None    # 미니게임 게임 시작 시간
acc_minigame_time = 0         # 누적 미니게임 플레이 시간

minigame_pattern_list = []    # 미니게임 패턴 리스트 (게임 진행시 생성)
minigame_success_count = 0    # 미니게임 패턴 성공 횟수

menu = 0                  # 선택 메뉴
score = 0                 # 점수
bonus_speed = 0           # 아이템 효과 - 플레이어 추가 속도
start_bot_timestop = 0    # 아이템 효과 - AI 시간 정지
start_reverse_time = 0    # 아이템 효과 - 방향키 반전

view_type = 'GAME_START'    # 화면 메시지 타입
prev_total_score = 0        # 이전 최종 점수

# 터틀런 키 이벤트
MAIN_SCREEN.onkeypress(on_keypress_right, 'Right')
MAIN_SCREEN.onkeypress(on_keypress_up, 'Up')
MAIN_SCREEN.onkeypress(on_keypress_left, 'Left')
MAIN_SCREEN.onkeypress(on_keypress_down, 'Down')
MAIN_SCREEN.onkeypress(on_keypress_space, 'space')

# 미니게임 키 이벤트
MAIN_SCREEN.onkeypress(on_keypress_q, 'q')
MAIN_SCREEN.onkeypress(on_keypress_w, 'w')
MAIN_SCREEN.onkeypress(on_keypress_e, 'e')
MAIN_SCREEN.onkeypress(on_keypress_a, 'a')
MAIN_SCREEN.onkeypress(on_keypress_s, 's')
MAIN_SCREEN.onkeypress(on_keypress_d, 'd')
MAIN_SCREEN.onkeypress(on_keypress_other, '')

show_game_message()

MAIN_SCREEN.listen()
MAIN_SCREEN.mainloop()
