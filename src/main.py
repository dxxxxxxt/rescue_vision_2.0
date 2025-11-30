"""
状态机说明:
状态0:寻找球体
状态1:接近小球
状态2:抓取小球
状态3:寻找安全区,即目标区域
状态4:放置小球和进行后续操作
"""

import cv2
import time
import json
import UART
import vision

# 加载配置
with open('config/config.json', 'r') as f:
    config = json.load(f)

team_color = config["team_color"]
camera_id = config["camera"]["device_id"]

# 初始化变量
current_state = 0  # 开始状态：找球
current_target = None
ball_type = 0
first_grab = True     # 是否是第一次抓取
has_yellow = False    # 是否已经抓了黄球

# 初始化摄像头和串口
cap = cv2.VideoCapture(camera_id)
print(f"队伍: {team_color}, 开始!!!!!!!!!!!!")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    
    # 读取电控数据
    UART.read_ecu_command()
    
    # 检测所有小球
    red_balls = vision.find_balls(frame, "red")
    blue_balls = vision.find_balls(frame, "blue") 
    yellow_balls = vision.find_balls(frame, "yellow")
    black_balls = vision.find_balls(frame, "black")
    
    # 状态机
    if current_state == 0:  # 找球
        valid_balls = []
        
        if first_grab:
            
            # 第一次必须抓己方颜色小球
            if team_color == "red" and red_balls:
                valid_balls = red_balls
                ball_type = 1
                print("第一次抓取: 红色球")
            elif team_color == "blue" and blue_balls:
                valid_balls = blue_balls  
                ball_type = 2
                print("第一次抓取: 蓝色球")
        else:
            # 后续抓取：看到哪个抓哪个，但不能抓对方球
            if yellow_balls and not has_yellow:
                # 看到黄球且还没抓过黄球
                valid_balls = yellow_balls
                ball_type = 3
                print("发现黄色球")
            elif black_balls:
                # 看到黑球
                valid_balls = black_balls
                ball_type = 4
                print("发现黑色球")
            elif team_color == "red" and red_balls:
                # 看到己方红球
                valid_balls = red_balls
                ball_type = 1
                print("发现红色球")
            elif team_color == "blue" and blue_balls:
                # 看到己方蓝球
                valid_balls = blue_balls
                ball_type = 2
                print("发现蓝色球")
        
        if valid_balls:
            current_target = valid_balls[0]
            current_state = 1  # 切换到接近状态
            print("发现目标，切换到状态1: 接近")
    
    elif current_state == 1:  # 接近小球
        if current_target:
            x, y, r = current_target
            x_offset, y_offset = vision.calculate_offset(x, y, frame_width, frame_height)
            
            # 计算距离
            distance = vision.calculate_distance(r)
                
            UART.send_data(x_offset, y_offset, ball_type, distance)
            
            if r > 25:  # 接近目标（可能需要调整）
                current_state = 2  # 切换到抓取状态
                print("距离足够近，切换到状态2: 抓取")
    
    elif current_state == 2:  # 抓取小球
        # 发送抓取命令，距离设为0
        UART.send_data(0, 0, ball_type, 0)
        time.sleep(1)  # 等待抓取完成
        
        if ball_type == 3:  # 黄色小球
            has_yellow = True
            print("已抓取黄色球! 不再抓取其他球")
        
        current_state = 3  # 切换到找安全区状态
        print("切换到状态3: 寻找安全区")
    
    elif current_state == 3:  # 找安全区
        zone_info = vision.find_safe_zone(frame, team_color)
        if zone_info:
            x, y, zone_type = zone_info
            # 计算安全区相对于图像中心的偏移量
            x_offset, y_offset = vision.calculate_offset(x, y, frame_width, frame_height)
            # 发送安全区具体位置坐标
            UART.send_data(x_offset, y_offset, zone_type, 0)
            current_state = 4  # 切换到放置状态
            print(f"找到安全区，位置({x}, {y})，切换到状态4: 放置")
        else:
            # 没找到安全区，发送特定信号让机器人继续寻找
            zone_type = 5 if team_color == "red" else 6
            UART.send_data(0, 0, zone_type, 100)  # 距离100表示继续寻找
            print("正在寻找安全区...")
    
    elif current_state == 4:  # 放置小球
        # 发送放置命令，距离设为0
        UART.send_data(0, 0, ball_type, 0)
        time.sleep(1)  # 等待放置完成
        
        # 更新第一次抓取标志
        if first_grab:
            first_grab = False
            print("第一次抓取完成")
        
        current_state = 0  # 回到找球状态
        current_target = None
        print("放置完成，切换到状态0: 寻找下一个球")
    
    # 显示检测结果
    all_balls = red_balls + blue_balls + yellow_balls + black_balls
    vision.show_frame(frame, all_balls, current_target)
    
    # 退出条件
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 清理资源
cap.release()
cv2.destroyAllWindows()
UART.close()
print("程序结束")