import serial
import time

# 初始化串口，添加简单异常处理
try:
    ser = serial.Serial('/dev/ttyS3', 115200)
    time.sleep(2)
    print("串口准备好了111111111111111111111111111111111111111")
except Exception as e:
    print(f"串口初始化失败: {e}")
    # 将ser设置为None，表示初始化失败
    ser = None

# 红色小球=1
# 蓝色小球=2
# 黄色小球=3
# 黑色小球=4
# 红色安全区=5
# 蓝色安全区=6

def read_ecu_command():
    """读取电控发送的数组信号"""
    try:
        # 检查串口是否初始化成功且处于打开状态
        if ser is None or not ser.is_open:
            print("警告: 串口未初始化或已关闭，无法接收数据")
            return None
        
        if ser.in_waiting > 0:
            data = ser.read(ser.in_waiting)
            print(f"收到电控信号: {list(data)}")
            return list(data)  # 返回数组格式
        return None
    except Exception as e:
        print(f"接收数据出错: {e}")
        return None
def send_data(x_offset, y_offset, target_type, distance):
    """
    发送数据给电控
    x_offset: x坐标偏移(-128~127)
    y_offset: y坐标偏移(-128~127) 
    target_type: 目标类型(1-6)
    distance: 目标距离(0-255厘米)
    """
    try:
        # 检查串口是否初始化成功且处于打开状态
        if ser is None or not ser.is_open:
            print("警告: 串口未初始化或已关闭，无法发送数据")
            return
        
        data = bytes([0xAA, x_offset, y_offset, target_type, distance, 0xBB])
        ser.write(data)
        print(f"Send: x{x_offset} y{y_offset} type{target_type} dist{distance}cm")
    except Exception as e:
        print(f"发送数据出错: {e}")

def send_no_target():
    """没有看到目标时发送0"""
    try:
        # 检查串口是否初始化成功且处于打开状态
        if ser is None or not ser.is_open:
            print("警告: 串口未初始化或已关闭，无法发送数据")
            return
        
        data = bytes([0xAA, 0, 0, 0, 0, 0xBB])
        ser.write(data)
        print("发送: 未发现目标")
    except Exception as e:
        print(f"发送数据出错: {e}")

def close():
    """关闭串口连接"""
    try:
        if ser and ser.is_open:
            ser.close()
            print("关闭串口333333333333333")
        else:
            print("串口未初始化或已经关闭")
    except Exception as e:
        print(f"关闭串口时出错: {e}")