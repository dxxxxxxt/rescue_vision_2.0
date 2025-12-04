import serial
import time


ser = serial.Serial('/dev/ttyS3', 115200, timeout=1)
print("串口已初始化并打开")

def send_data(dx, dy, distance, ball_id):
    """
    发送 ASCII 字符串给 STM32
    格式: "dx:100 dy:200 dis:200 id:1"
    注意: 无换行符！无多余空格！字段名必须是 dx/dy/dis/id
    """
    # 构造严格匹配 sscanf 的字符串
    msg = f"dx:{dx} dy:{dy} dis:{distance} id:{ball_id}\n"
    
    # 发送 ASCII 字节
    ser.write(msg.encode('ascii'))
    print(f"📤 发送: '{msg}'")

def send_no_target():
    """没有目标时，发送全0（id=0 表示无目标）"""
    msg = "dx:0 dy:0 dis:0 id:0"
    ser.write(msg.encode('ascii'))
    print(f"📤 发送: '{msg}' (无目标)")

# ============ 主循环 ============
try:
    while True:
        # 示例：每2秒发送一次测试数据
         # dx:100 dy:200 dis:200 id:1
        time.sleep(2)
        
        # send_no_target()
        # time.sleep(2)

except KeyboardInterrupt:
    print("\n🛑 程序被中断")
finally:
    if ser.is_open:
        ser.close()
        print("🔌 串口已关闭")