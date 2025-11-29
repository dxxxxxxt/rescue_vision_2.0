import serial
import time

ser = serial.Serial('/dev/ttyS3', 115200)
time.sleep(2)
print("串口准备好了111111111111111111111111111111111111111")

# 红色小球=1
# 蓝色小球=2
# 黄色小球=3
# 黑色小球=4
# 红色安全区=5
# 蓝色安全区=6

def read_ecu_command():
    """读取电控发送的数组信号"""
    if ser.in_waiting > 0:
        data = ser.read(ser.in_waiting)
        print(f"收到电控信号: {list(data)}")
        return list(data)  # 返回数组格式
    return None
def send_data(x_offset, y_offset, target_type, distance):
    """
    发送数据给电控
    x_offset: x坐标偏移(-128~127)
    y_offset: y坐标偏移(-128~127) 
    target_type: 目标类型(1-6)
    distance: 目标距离(0-255厘米)
    """
    data = bytes([0xAA, x_offset, y_offset, target_type, distance, 0xBB])
    ser.write(data)
    print(f"Send: x{x_offset} y{y_offset} type{target_type} dist{distance}cm")

def send_no_target():
    """没有看到目标时发送0"""
    data = bytes([0xAA, 0, 0, 0, 0, 0xBB])
    ser.write(data)
    print("发送: 未发现目标")