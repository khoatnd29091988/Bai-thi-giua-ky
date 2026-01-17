#Code game Oan tu ti
# Nhóm 3:
# 1/ Thái Nguyễn Đăng Khoa
import tkinter as tk
from tkinter import messagebox
import socket
import threading

HOST = '127.0.0.1'
PORT = 65432

class RPSGameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Oẳn Tù Tì PvP")
        self.root.geometry("400x450")
        self.root.resizable(False, False)

        # --- Kết nối Socket ---
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        try:
            self.client.connect((HOST, PORT))
            self.connected = True
        except:
            messagebox.showerror("Lỗi", "Không thể kết nối đến Server!")
            root.destroy()
            return

        # --- Giao diện (GUI) ---
        # 1. Tiêu đề trạng thái
        self.lbl_status = tk.Label(root, text="Đang kết nối...", font=("Arial", 14, "bold"), pady=20, fg="blue")
        self.lbl_status.pack()

        # 2. Khu vực nút bấm (Frame chứa 3 nút)
        self.btn_frame = tk.Frame(root)
        self.btn_frame.pack(pady=10)

        # Tạo 3 nút: Búa (1), Kéo (2), Bao (3)
        # Ban đầu khóa nút lại (state=tk.DISABLED) chưa cho bấm
        self.btn_bua = tk.Button(self.btn_frame, text="✊ BÚA", font=("Arial", 16), width=8, height=2, command=lambda: self.send_move("1"), state=tk.DISABLED, bg="#f0f0f0")
        self.btn_bua.grid(row=0, column=0, padx=5)
        
        self.btn_keo = tk.Button(self.btn_frame, text="✌ KÉO", font=("Arial", 16), width=8, height=2, command=lambda: self.send_move("2"), state=tk.DISABLED, bg="#f0f0f0")
        self.btn_keo.grid(row=0, column=1, padx=5)
        
        self.btn_bao = tk.Button(self.btn_frame, text="✋ BAO", font=("Arial", 16), width=8, height=2, command=lambda: self.send_move("3"), state=tk.DISABLED, bg="#f0f0f0")
        self.btn_bao.grid(row=0, column=2, padx=5)

        # 3. Khu vực hiển thị kết quả
        self.lbl_result = tk.Label(root, text="...", font=("Arial", 12), pady=20, height=5, wraplength=380, bg="#e6e6e6", relief="sunken")
        self.lbl_result.pack(fill=tk.X, padx=20, pady=20)

        # --- Bắt đầu luồng nhận tin nhắn ---
        # daemon=True để luồng này tự tắt khi cửa sổ chính đóng
        threading.Thread(target=self.receive_data, daemon=True).start()

    def set_buttons_state(self, state):
        """Hàm tiện ích để Bật/Tắt 3 nút cùng lúc"""
        self.btn_bua.config(state=state)
        self.btn_keo.config(state=state)
        self.btn_bao.config(state=state)
        # Đổi màu nút để người dùng dễ nhận biết
        color = "lightgreen" if state == tk.NORMAL else "#f0f0f0"
        self.btn_bua.config(bg=color)
        self.btn_keo.config(bg=color)
        self.btn_bao.config(bg=color)

    def send_move(self, choice):
        """Gửi lựa chọn (1, 2 hoặc 3) lên server"""
        if self.connected:
            self.client.send(choice.encode('utf-8'))
            # Sau khi bấm thì khóa nút lại ngay
            self.set_buttons_state(tk.DISABLED)
            self.lbl_status.config(text="Đã chọn! Đang chờ đối thủ...", fg="orange")

    def receive_data(self):
        """Luồng chạy ngầm: Liên tục nghe tin từ Server"""
        while self.connected:
            try:
                msg = self.client.recv(1024).decode('utf-8')
                if not msg: break

                # Xử lý các loại tin nhắn
                if msg == "WAIT":
                    self.lbl_status.config(text="Đang tìm đối thủ...", fg="grey")
                    self.lbl_result.config(text="Vui lòng đợi người chơi thứ 2...")
                
                elif msg == "START":
                    self.lbl_status.config(text="ĐẾN LƯỢT BẠN! Hãy chọn đi!", fg="green")
                    self.lbl_result.config(text="Trận đấu bắt đầu.")
                    # Mở khóa nút để người dùng bấm
                    self.set_buttons_state(tk.NORMAL)
                
                else:
                    # Đây là tin nhắn kết quả thắng thua
                    self.lbl_status.config(text="KẾT QUẢ VÁN ĐẤU", fg="purple")
                    # Hiển thị kết quả chi tiết lên Label ở dưới
                    self.lbl_result.config(text=msg)
                    # Sau vài giây, server sẽ gửi lại lệnh START cho ván mới

            except:
                break
        
        self.connected = False
        self.lbl_status.config(text="Mất kết nối với Server!", fg="red")
        self.set_buttons_state(tk.DISABLED)
        self.client.close()

# --- Chạy chương trình ---
if __name__ == "__main__":
    root = tk.Tk()
    game = RPSGameGUI(root)
    root.mainloop()

