import serial
import time

def read_ecu_command():
    """读取电控发送的数组信号"""
    try:
        # 检查串口是否初始化成功且处于打开状态
        if  ser and ser.is_open:
            print("警告: 串口未初始化或已关闭，无法接收数据")
            return None
        
        if ser.in_waiting > 0:
            cmd = ser.read(ser.in_waiting).decode('utf-8').strip()
            print(f"收到电控信号: {list(cmd)}")
            return list(cmd)  # 返回数组格式
        return None
    except Exception as e:
        print(f"接收数据出错: {e}")
        return None

    
# 红色小球=1
# 蓝色小球=2
# 黄色小球=3
# 黑色小球=4
# 红色安全区=5
# 蓝色安全区=6

# # 1. 发送测试数据
# send_data(50, -30, 1, 100)


# # 2. 尝试接收数据
# print("等待电控回应...")
# for i in range(5):
#     data = read_ecu_command()
#     if data:
#         
#         break
#     else:
#         print(f"尝试 {i+1}: 暂无数据")
#     time.sleep(1)

# # 3. 发送无目标信号
# send_no_target()
# time.sleep(1)

def send_data(dx, dy, distance, ball_id):
    """
    发送 ASCII 字符串给 STM32
    格式: "dx:100 dy:200 dis:200 id:1"
    """
    # 构造严格匹配 sscanf 的字符串
    msg = f"dx:{dx} dy:{dy} dis:{distance} id:{ball_id}\n"
    
    # 发送 ASCII 字节
    ser.write(msg.encode('ascii'))
    print(f"发送: '{msg}'")

def send_no_target():
    """没有看到目标时发送0"""
    try:
        # 检查串口是否初始化成功且处于打开状态
        if not ser or not ser.is_open:
            print("警告: 串口未初始化或已关闭，无法发送数据")
            return
        
        data = bytes([0xAA, 0, 0, 0, 0, 0xBB])
        ser.write(data)
        print("发送: 未发现目标")
    except Exception as e:
        print(f"发送数据出错: {e}")

ser = serial.Serial('/dev/ttyS3', 115200)

if ser and ser.is_open:
    print("串口已初始化并打开")
    while True:
        cmd=ser.read().decode('utf-8')
        print(f"收到电控数据: {cmd}")
        send_data(100, 200, 200, 2) 

ser.close()