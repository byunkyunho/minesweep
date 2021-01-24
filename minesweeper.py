import pygame as pg
import random as rd
import time

pg.init()

screen = pg.display.set_mode((350, 430))
pg.display.set_caption("minesweep")

num_font = pg.font.SysFont("Viga",35 ,bold=100)

white = (255,255,255)

pg.key.set_repeat(1, 1)

win_font = pg.font.SysFont("Viga", 150)

bomb = 10
down_button = 0

running = True
replay_button = True

win_game = win_font.render("WIN!", True, (255,255,255,128))

color_list = [(0,0,255), (0,128,0), (255,0,0),(1, 0, 124),(1, 0, 124),(1, 0, 124),(1, 0, 124),(1, 0, 124)]

index_list = [(0, - 1), (0,  1), (1, 0), ( -1, 0), (-1, 1), (- 1, - 1), (1,1), (1, -1)]

num_light_list =[
    (True, True, True, True, True, True, False),
    (False, False, False, True, True, False, False),
    (True, False, True, True, False, True, True),
    (True, False, False, True, True, True ,True),
    (False, True, False, True, True,False, True),
    (True, True, False, False, True, True, True),
    (True, True, True, False, True, True, True),
    (True, False, False, True, True, False, False),
    (True, True, True, True, True, True, True),
    (True, True, False, True, True, True, True)
]
text_list = []

for a in range(8):
    text_list.append(num_font.render(str(a+1), True, color_list[a]))

def d_block(x1,y1, width, height, center_color, side_gap,ud_gap, flip):
    block_color = [ (128,128,128), white]
    if flip:
        block_color.reverse()
    pg.draw.polygon(screen, block_color[0], [(x1, y1), (x1 + width, y1), (x1, y1 + height)])
    pg.draw.polygon(screen, block_color[1], [(x1 + width, y1), (x1, y1 + height),(x1 + width, y1 + height )])
    pg.draw.rect(screen,  center_color, [ x1 + side_gap,y1 + ud_gap,  width - side_gap*2, height - ud_gap*2])

def set_array():
    global main_array, state_array
    state_array = [[1 for a in range(10)] for b in range(10)]
    main_array =  [[0 for a in range(10)] for b in range(10)] 
    random = 0
    while not random == 10:
        random_raw = rd.randint(0,9)
        random_column = rd.randint(0,9)
        if not main_array[random_raw][random_column] == 10:
            main_array[random_raw][random_column] = 10
            random += 1

    for loop in range(100):
        x,y = loop % 10, loop // 10
        around_bomb = 0
        if not main_array[y][x] == 10:
            check_list = [ x != 0, x !=9, y != 9, y != 0, y != 0 and x != 9, y != 0 and x != 0, y != 9 and x != 9, y != 9 and x != 0]
            for check, index in zip(check_list, index_list):
                if check:
                    if main_array[y + index[0]][x + index[1]] == 10:
                        around_bomb += 1

            main_array[y][x] = around_bomb

def change_color(index):
    global light_color
    light_color = (96,0,0)
    if light[index]:
        light_color = (255,0,0)

def draw_num(x,y,num):
    global light_color, light
    
    light = num_light_list[num]

    num_xy_list =[
        (0,0,10,6,0,0,  -5, 0, 0, 5, 10, 0, 15,0, 10, 5),
        ( -6,8,6,9,-6,8,-1,8,-6,3,-6,17,-1,17,-6,22), 
        (-6,31,6,9,-6,30,-1,30,-6,24,-6,40,-1,40,-6,45),
        (12,8,6,9,17,8,12,8,17,3,17,17,12,17,17,22),
        (12,31,6,9,17,30,12,30,17,24,17,40,12,40,17,45),
        (1,42,9,6,1,42,-4,47,0,47,10,42,15,47,10,47),
        (0,20,11,7,0,20,-5,23,0,26,10,20,15,23,10,26),
    ]
    for num in range(7):
        change_color(num)
        xy_list = num_xy_list[num]
        pg.draw.rect(screen, light_color, [x + xy_list[0] , y + xy_list[1], xy_list[2],xy_list[3]])
        pg.draw.polygon(screen, light_color, [(x + xy_list[4], y + xy_list[5]), (x + xy_list[6], y + xy_list[7] ), (x + xy_list[8], y + xy_list[9])])
        pg.draw.polygon(screen, light_color, [(x + xy_list[10],y + xy_list[11]), (x  + xy_list[12], y+ xy_list[13] ), (x + xy_list[14], y + xy_list[15])])

def game_set():
    global main_array, state_array, gameover, bomb, start_time, start, win, red_block
    bomb = 10
    set_array()
    gameover = False
    start_time = True
    start = 0
    win = False
    red_block = [None, None]

def d_time():
    global now
    if gameover or win:
        for a,num in enumerate(now):
            draw_num(224+a*34,28, int(num))
    else:
        if start == 0:
            for a in range(3):
                draw_num(224+a*34,28, 0)
        else:
            now = round(time.time() - start)
            if int(now) > 999:
                now = "999"
            else:
                if int(now) < 10:
                    now = f"00{now}"
                elif int(now) < 100:
                    now = f"0{now}"
                else:
                    now = str(now)
            for a,num in enumerate(now):
                draw_num(224+a*34,28, int(num))

def d_background():
    d_block(0,0,350,430,(192,192,192),4,4,True)
    d_block(20 , 13 , 311 , 80,(198,198,198),5,2, False)

    d_block(20, 100, 310,310,(0,0,0),5,5 ,False)

    d_block(30 , 23 , 110 , 60, (0,0,0),3,3, False)
    d_block(209 , 23 , 110 , 60, (0,0,0),3,3, False)
    d_block(145, 23 , 60,60 ,  (198,198,198),5,5, replay_button)

    pg.draw.circle(screen, (248,253,34), (175,53), 20)
    
    if not gameover and not win:
        pg.draw.circle(screen, (0,0,0), (168 , 48), 3)
        pg.draw.circle(screen, (0,0,0), (183 , 48), 3)
        pg.draw.ellipse(screen, (0,0,0), [165,57, 21, 10])
        pg.draw.ellipse(screen, (255,255,0), [165,53, 21, 10]) 
    elif gameover and not win:
        pg.draw.line(screen, (0,0,0),(165, 45), (170, 50) ,3)
        pg.draw.line(screen, (0,0,0),(170, 45), (165, 50) ,3)
        pg.draw.line(screen, (0,0,0),(180, 45), (185, 50) ,3)
        pg.draw.line(screen, (0,0,0),(185, 45), (180, 50) ,3)
        pg.draw.ellipse(screen, (0,0,0), [165,59, 21, 10])
        pg.draw.ellipse(screen, (255,255,0), [165,63, 21, 10])
    else:
        pg.draw.rect(screen, (0,0,0), [163, 44, 9, 7])
        pg.draw.rect(screen, (0,0,0), [178, 44, 9, 7])
        pg.draw.line(screen, (0,0,0),(163, 46), (185, 46) ,2)
        pg.draw.line(screen, (0,0,0),(163, 46), (157, 43) ,2)
        pg.draw.line(screen, (0,0,0),(187, 46), (192, 43) ,2)
        pg.draw.ellipse(screen, (0,0,0), [165,57, 21, 10])
        pg.draw.ellipse(screen, (255,255,0), [165,53, 21, 10]) 
    
def d_line():
    for a in range(11):
        pg.draw.line(screen, (128,128,128),(55+30*a, 105),(55+30*a, 404),  1)
        pg.draw.line(screen, (128,128,128),(25, 104+30*a),(325, 104+30*a),  1)

def check_win():
    find = 0
    for a in range(100):
        if state_array[a//10][a%10] == 0:
            find += 1
    if 90 == find:
        return True

def d_board(i,j):
    if state_array[i][j] == 0:
        pg.draw.rect(screen, (196,196,196), [25+j*30, 105+i*30, 30,30])
        if not  main_array[i][j] == 0:
            if not main_array[i][j] == 10:
                screen.blit(text_list[main_array[i][j] - 1], (34+j*30, 109+i*30))

    if state_array[i][j] > 0:
        d_block(25+j*30,105+i*30,30,30,(198,198,198), 5,5,True)

    if state_array[i][j] == 2:
        pg.draw.polygon(screen, (255,0,0), [(35+j*30, 122+i*30), (35+j*30, 108 +i*30),(48+j*30, 115+i*30)])
        pg.draw.line(screen, (0,0,0), (34+j*30, 108 +i*30), (34+j*30, 128 +i*30), 3)

def d_all_bomb(i,j):
    if main_array[i][j] == 10:
        if [i,j] == red_block:
            pg.draw.rect(screen, (255,0,0), [25+j*30, 105+i*30, 30,30])
        else:
            pg.draw.rect(screen, (196,196,196), [25+j*30, 105+i*30, 30,30])
        pg.draw.line(screen, (255,0,0),(35+j*30, 120+i*30),(45+j*30, 108+i*30),  2)
        pg.draw.circle(screen, (0,0,0), (40+j*30, 120+i*30), 10)

def update_main_array():
    global gameover, main_array, open_list, state_array, red_block, start, now, bomb
    if main_array[mouse_y][mouse_x] == 10:
        gameover = True
        now = round((time.time() - start))
        if int(now) > 999:
            now = "999"
        else:
            if int(now) < 10:
                now = f"00{now}"
            elif int(now) <  100:
                now = f"0{now}"
            else:
                now = str(now)
        red_block = [mouse_y, mouse_x]

    elif state == 1 or state == 2:
        if state == 2:
            bomb += 1
        if main_array[mouse_y][mouse_x] == 0:
            open_list = [(mouse_y, mouse_x)]         
            for a in range(20):
                copy_list = open_list[:]
                for y,x in copy_list: 
                    check_list = [ x != 0, x !=9, y != 9, y != 0, y != 0 and x != 9, y != 0 and x != 0, y != 9 and x != 9, y != 9 and x != 0]
                    for check,index in zip(check_list, index_list):
                        if check:
                            if main_array[y + index[0]][x + index[1]] == 0:
                                open_list.append((y + index[0], x + index[1])) 

                    open_list = list(set(open_list))

                for y,x in open_list:
                    if state_array[y][x] == 2:

                        bomb += 1 
                    state_array[y][x] = 0

                    check_list = [ x != 0, x !=9, y != 9, y != 0, y != 0 and x != 9, y != 0 and x != 0, y != 9 and x != 9, y != 9 and x != 0]

                    for check, index in zip(check_list, index_list):
                        if check:
                            if not main_array[y + index[0]][x + index[1]] == 0:
                                if state_array[y + index[0]][x + index[1]] == 2:
                                    bomb += 1
                                state_array[y + index[0]][x + index[1]] = 0
                                                  
        else:
            state_array[mouse_y][mouse_x] = 0           

def left_bomb():
    global bomb
    bomb = int(bomb)
    if bomb < 10:
        string_bomb = f"00{bomb}"
    elif bomb < 100:
        string_bomb = f"0{bomb}"
    for a,num in enumerate(str(string_bomb)):
        draw_num(45 + a*34,28, int(num))
    
game_set()

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos() 
            if mouse_x > 145 and mouse_x < 205 and mouse_y > 23 and mouse_y < 83:
                game_set()
                replay_button = False
                win = False
                down_button = 10
            
            if not win and not gameover:
                if mouse_x > 32 and mouse_x < 323 and mouse_y > 107 and mouse_y < 398:
                    if start_time:
                        start = time.time()
                      
                        start_time = False

                    mouse_x, mouse_y = (mouse_x - 25) // 30 ,(mouse_y - 105) // 30

                    state = state_array[mouse_y][mouse_x]

                    if event.button == 1:
                        update_main_array()

                    elif event.button == 3:
                        if  not gameover and not win:
                            if state == 2:
                                state_array[mouse_y][mouse_x] = 1
                                bomb += 1
                            else:
                                if bomb > 0:
                                    if state == 1:
                                        state_array[mouse_y][mouse_x] = 2
                                        bomb -= 1

                if check_win():
                    win = True
                    gameover = True
                    now = round((time.time() - start))
                    if int(now) > 999:
                        now = "999"
                    else:
                        if int(now) < 10:
                            now = f"00{now}"
                        elif int(now) <  100:
                            now = f"0{now}"
                        else:
                            now = str(now)
                       
    d_background()

    for i in range(10):
        for j in range(10):

            d_board(i,j)

            if gameover:

                d_all_bomb(i,j)

    d_line()
    d_time()
    left_bomb()
                   
    if win:
        screen.blit(win_game, (58 , 195))
     
    if down_button > 0:
        down_button -= 1
    else:
        replay_button = True

    pg.display.update()

    time.sleep(0.01)
