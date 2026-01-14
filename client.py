import socket

HOST = '127.0.0.1'
PORT = 65432

def show_menu():
    print("\n--- ĐẤU TRƯỜNG OẲN TÙ TÌ ---")
    print("1. Chọn Búa")
    print("2. Chọn Kéo")
    print("3. Chọn Bao")
    print("--------------------------")

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print("Đã kết nối! Đang tìm đối thủ...")
        
        # Nhận tín hiệu đầu tiên từ server
        msg = client.recv(1024).decode('utf-8')
        if msg == "WAIT":
            print(">>> Vui lòng đợi người chơi thứ 2...")
            # Đợi tiếp tín hiệu START
            msg = client.recv(1024).decode('utf-8')
            
    except ConnectionRefusedError:
        print("Không tìm thấy Server.")
        return

    while True:
        # Nếu server gửi lệnh START thì mới cho nhập
        if "START" in msg:
            show_menu()
            choice = input("Lựa chọn của bạn (1-3): ")
            while choice not in ['1', '2', '3']:
                choice = input("Sai rồi, nhập lại (1-3): ")
            
            print("Đã gửi! Đang chờ đối thủ ra đòn...")
            client.send(choice.encode('utf-8'))

            # Nhận kết quả
            result = client.recv(1024).decode('utf-8')
            print(f"\n>>> KẾT QUẢ: {result}")
            
            # Chuẩn bị cho vòng sau (Server sẽ gửi START tiếp hoặc đóng)
            try:
                msg = client.recv(1024).decode('utf-8')
                if not msg: break
            except:
                break
        else:
            break

    client.close()
    print("Kết thúc game.")

if __name__ == "__main__":
    start_client()
