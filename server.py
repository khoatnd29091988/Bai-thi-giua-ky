#Code game Oan tu ti
# Nhóm 3
# 1/ Thái Nguyễn Đăng Khoa
# 2/ Trượng Lệ Hào
# 3/ Vũ Mạnh Cường
import socket
import threading
import time

HOST = '127.0.0.1'
PORT = 65432

def check_result(move1, move2):
    """
    1=Búa, 2=Kéo, 3=Bao
    Trả về: 0 (Hòa), 1 (P1 thắng), 2 (P2 thắng)
    """
    if move1 == move2:
        return 0
    if (move1 == "1" and move2 == "2") or \
       (move1 == "2" and move2 == "3") or \
       (move1 == "3" and move2 == "1"):
        return 1
    return 2

def handle_game(conn1, conn2):
    """Xử lý ván chơi giữa 2 người"""
    map_name = {"1": "BÚA", "2": "KÉO", "3": "BAO"}
    
    try:
        while True:
            # Gửi tín hiệu để cả 2 client bắt đầu nhập
            conn1.send("START".encode('utf-8'))
            conn2.send("START".encode('utf-8'))

            # Nhận lựa chọn của P1
            move1 = conn1.recv(1024).decode('utf-8')
            if not move1: break
            
            # Nhận lựa chọn của P2
            move2 = conn2.recv(1024).decode('utf-8')
            if not move2: break

            # Tính toán kết quả
            winner = check_result(move1, move2)
            p1_choice = map_name.get(move1, "Lỗi")
            p2_choice = map_name.get(move2, "Lỗi")

            # Tạo thông báo kết quả riêng cho từng người
            res_p1 = f"Bạn: {p1_choice} | Đối thủ: {p2_choice} -> "
            res_p2 = f"Bạn: {p2_choice} | Đối thủ: {p1_choice} -> "

            if winner == 0:
                conn1.send((res_p1 + "HÒA!").encode('utf-8'))
                conn2.send((res_p2 + "HÒA!").encode('utf-8'))
            elif winner == 1:
                conn1.send((res_p1 + "BẠN THẮNG!").encode('utf-8'))
                conn2.send((res_p2 + "BẠN THUA!").encode('utf-8'))
            else: # winner == 2
                conn1.send((res_p1 + "BẠN THUA!").encode('utf-8'))
                conn2.send((res_p2 + "BẠN THẮNG!").encode('utf-8'))
            time.sleep(4)

    except Exception as e:
        print("Lỗi kết nối:", e)
    finally:
        conn1.close()
        conn2.close()
        print("Kết thúc ván đấu.")
# kết nối server 
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[ĐANG CHẠY] Server đang chờ người chơi tại {HOST}:{PORT}")
    
    clients = []
    
    while True:
        conn, addr = server.accept()
        print(f"[KẾT NỐI] {addr} đã tham gia.")
        clients.append(conn)

        # Nếu đủ 2 người thì bắt đầu game
        if len(clients) >= 2:
            print(">>> Đủ 2 người chơi! Bắt đầu ván đấu...")
            # Lấy 2 người đầu tiên ra khỏi hàng chờ để cho đấu với nhau
            p1 = clients.pop(0)
            p2 = clients.pop(0)
            
            # Tạo luồng riêng cho cặp đôi này
            thread = threading.Thread(target=handle_game, args=(p1, p2))
            thread.start()
        else:
            conn.send("WAIT".encode('utf-8')) # Báo người 1 đợi

if __name__ == "__main__":
    start_server()






