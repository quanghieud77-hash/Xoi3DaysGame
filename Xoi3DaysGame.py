import random
import tkinter as tk
from tkinter import messagebox
import json
import os

class Xoi3NightsGame:
    BG = "#1e1e2f"
    PANEL = "#2a2a40"
    PANEL2 = "#383854"
    BORDER = "#4a4a6a"
    TEXT = "#f8f8f2"
    MUTED = "#b5b5c3"
    GOLD = "#f1fa8c"
    GREEN = "#50fa7b"
    RED = "#ff5555"
    CYAN = "#8be9fd"
    DREAM_BG = "#0a0a12"

    BTN_PRIMARY = "#bd93f9"
    BTN_SUCCESS = "#50fa7b"
    BTN_DANGER = "#ff5555"
    BTN_INFO = "#8be9fd"
    BTN_WARNING = "#ffb86c"
    BTN_DARK = "#44475a"

    def __init__(self, root):
        self.root = root
        self.root.title("Xoi3NightsGame - Extended Edition")
        self.root.configure(bg=self.BG)
        self.root.minsize(980, 780)
        self.center_window(1100, 820)

        self.default_font = ("Segoe UI", 10)
        self.bold_font = ("Segoe UI", 10, "bold")
        self.title_font = ("Segoe UI", 28, "bold")
        self.big_font = ("Segoe UI", 15, "bold")

        self.achievement_database = {
            "Ach_1": ("Sống Sót Qua Ngày", "Vượt qua ngày đầu tiên bán xôi an toàn."),
            "Ach_2": ("Sa Ngã", "Chọn đi theo kẻ trùm ẩn danh vào Đêm 2."),
            "Ach_3": ("Hợp Lực Cơm Tấm", "Phối hợp cùng Lâm truy đuổi thành công (True Ending)."),
            "Ach_Secret": ("Vua Xã Hội Đen", "Tự lập tổ chức ngầm và trở thành Vị vua xã hội đen (Secret Ending)."),
            "Ach_4": ("Vua Xôi", "Phục vụ đúng món liên tiếp 8 lần."),
            "Ach_5": ("Thám Tử Đường Phố", "Thu thập ít nhất 3 manh mối quan trọng trong sổ tay.")
        }
        
        self.save_file = "xoi_3nights_qhouse_save.json"
        self.unlocked_endings = set()
        self.unlocked_achievements = set()
        self.load_endings()
        
        self.reset_game_data()
        self.build_main_menu()

    def load_endings(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.unlocked_endings = set(data.get("endings", []))
                    self.unlocked_achievements = set(data.get("achievements", []))
            except:
                self.unlocked_endings = set()
                self.unlocked_achievements = set()

    def save_endings(self):
        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump({
                "endings": list(self.unlocked_endings),
                "achievements": list(self.unlocked_achievements)
            }, f, ensure_ascii=False, indent=4)

    def check_achievements(self):
        new_unlocked = []

        if self.day > 1 and "Ach_1" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_1")
            new_unlocked.append(self.achievement_database["Ach_1"][0])

        if "Ending 2" in self.unlocked_endings and "Ach_2" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_2")
            new_unlocked.append(self.achievement_database["Ach_2"][0])

        if "Ending 3" in self.unlocked_endings and "Ach_3" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_3")
            new_unlocked.append(self.achievement_database["Ach_3"][0])
            
        if "Secret Ending" in self.unlocked_endings and "Ach_Secret" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_Secret")
            new_unlocked.append(self.achievement_database["Ach_Secret"][0])
            
        if getattr(self, "correct_serve_streak", 0) >= 8 and "Ach_4" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_4")
            new_unlocked.append(self.achievement_database["Ach_4"][0])

        if len(self.clues_found) >= 3 and "Ach_5" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_5")
            new_unlocked.append(self.achievement_database["Ach_5"][0])

        if new_unlocked:
            self.save_endings()
            for name in new_unlocked:
                messagebox.showinfo("🏆 THÀNH TỰU MỚI!", f"Chúc mừng! Bạn đã đạt thành tựu:\n\n🏆 [{name}]", parent=self.root)

    def show_achievements(self):
        self.check_achievements()
        text = f"TỔNG SỐ THÀNH TỰU ĐÃ ĐẠT: {len(self.unlocked_achievements)}/6\n\n"
        for idx, (code, (title, desc)) in enumerate(self.achievement_database.items(), 1):
            if code in self.unlocked_achievements:
                text += f"• {title} -> [✅ ĐÃ ĐẠT]\n  {desc}\n\n"
            else:
                text += f"• Thành tựu {idx}: ??? -> [🔒 ???]\n  ???\n\n"
        messagebox.showinfo("Thành Tựu Q-HOUSETEAM", text)

    def center_window(self, width, height):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = max((sw - width) // 2, 0)
        y = max((sh - height) // 2, 0)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def make_button(self, parent, text, command, width=20, bg=None, fg="white", height=1, state="normal"):
        return tk.Button(
            parent, text=text, command=command, width=width, height=height, state=state,
            font=self.bold_font, bg=bg or self.PANEL2, fg=fg,
            activebackground="#505070", activeforeground="white",
            relief="flat", bd=0, cursor="hand2"
        )

    def get_weather_description(self):
        weathers = {
            1: "Trời Nắng Gắt: Khách hàng vội vã, dễ cáu gắt nếu làm sai món.",
            2: "Trời Mưa Lất Phất: Không gian u ám, độ cảnh giác của giang hồ tăng cao.",
            3: "Trời Mát Mẻ: Ngày quyết định mọi cục diện."
        }
        return weathers.get(self.day, "")

    def reset_game_data(self):
        self.game_running = False
        self.money = 50
        self.suspicion = random.randint(5, 10)
        self.sanity = 100
        self.day = 1
        self.orders_completed_today = 0
        self.serve_reward = 25 
        self.correct_serve_streak = 0
        self.clues_found = []
        
        self.talked_current_customer = False
        self.current_customer = None
        self.current_plate = []
        self.customer_visual = None
        
        self.hour = 8
        self.minute = 35
        self.event_night_2_triggered = False

    def build_main_menu(self):
        self.clear_root()
        self.game_running = False

        outer = tk.Frame(self.root, bg=self.BG)
        outer.pack(fill="both", expand=True, padx=40, pady=25)

        top = tk.Frame(outer, bg=self.BG)
        top.pack(fill="both", expand=True)

        tk.Label(top, text="Xoi3NightsGame", font=("Segoe UI", 36, "bold"), fg=self.GOLD, bg=self.BG).pack(pady=(10, 0))
        tk.Label(top, text="CREATOR BY: Q-HOUSETEAM", font=("Segoe UI", 12, "bold"), fg=self.CYAN, bg=self.BG).pack(pady=(5, 0))
        # Dòng tri ân Q-HOUSETEAM được giữ chuẩn xác theo yêu cầu
        tk.Label(top, text="Tri ân Q-HOUSETEAM vì đã ra sê-ri tuyệt vời này!", font=("Segoe UI", 10, "italic"), fg=self.GREEN, bg=self.BG).pack(pady=(0, 15))

        card = tk.Frame(top, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(ipadx=30, ipady=12)

        tk.Label(card, text="LUẬT CHƠI MỚI", font=("Segoe UI", 11, "bold"), fg=self.GOLD, bg=self.PANEL).pack(pady=(0, 4))
        tk.Label(
            card,
            text="• Mỗi ngày bạn chỉ cần phục vụ **8 suất xôi** để có thời gian hóng chuyện.\n"
                 "• Theo dõi **Thanh Tỉnh Táo (🧠)**: Hỏi thăm nhiều sẽ làm bạn mệt mỏi.\n"
                 "• Sử dụng **Sổ Tay Manh Mối (📖)** để xem lại các bí mật đã thu thập.\n"
                 "• Đạt tối đa các Ending và Thành tựu để khám phá toàn bộ sự thật.",
            font=("Segoe UI", 10), fg=self.TEXT, bg=self.PANEL, justify="left"
        ).pack()

        buttons = tk.Frame(outer, bg=self.BG)
        buttons.pack(pady=10)

        self.make_button(buttons, "BẮT ĐẦU BÁN XÔI", self.start_game, width=28, height=2, bg=self.BTN_PRIMARY, fg="black").pack(pady=4)
        self.make_button(buttons, f"THƯ VIỆN ENDING ({len(self.unlocked_endings)}/4)", self.show_endings, width=28, height=2, bg=self.BTN_INFO, fg="black").pack(pady=4)
        self.make_button(buttons, f"THÀNH TỰU ({len(self.unlocked_achievements)}/6)", self.show_achievements, width=28, height=2, bg=self.BTN_WARNING, fg="black").pack(pady=4)
        self.make_button(buttons, "THOÁT GAME", self.root.destroy, width=28, height=2, bg=self.BTN_DANGER, fg="black").pack(pady=4)

    def show_endings(self):
        end_data = [
            ("Ending 1", "Ending 1: Kẻ tò mò bị thủ tiêu (GameOver)"),
            ("Ending 2", "Ending 2: Chấp nhận làm tay sai hắc bang (Bad End)"),
            ("Ending 3", "Ending 3: Hợp lực cùng Cơm Tấm (True End)"),
            ("Secret Ending", "Secret Ending: Vị vua của xã hội đen (Secret End)")
        ]
        
        text = f"TỔNG SỐ ENDING ĐÃ KHÁM PHÁ: {len(self.unlocked_endings)}/4\n\n"
        for i, (key, full_name) in enumerate(end_data, 1):
            if key in self.unlocked_endings:
                text += f"• {full_name} -> [✅ ĐÃ MỞ KHÓA]\n\n"
            else:
                text += f"• Ending {i}: ??? -> [🔒 ???]\n\n"

        messagebox.showinfo("Thư Viện Endings", text)

    def start_game(self):
        self.reset_game_data()
        self.game_running = True
        self.build_game_ui()
        messagebox.showinfo("Khởi Đầu", "Sáng sớm tinh mơ. Bạn đẩy xe xôi ra góc đường quen thuộc. Mục tiêu hôm nay là 8 suất xôi và tìm kiếm manh mối ngầm.")
        self.next_customer()

    def build_game_ui(self):
        self.clear_root()

        if self.day == 3:
            self.build_night_3_ui()
            return

        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=18, pady=10)

        header = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        header.pack(fill="x", pady=(0, 6))

        top_row = tk.Frame(header, bg=self.PANEL)
        top_row.pack(fill="x", padx=15, pady=(6, 2))

        self.lbl_title = tk.Label(top_row, text="Xe Xôi Chuyện Bao Đồng", font=("Segoe UI", 13, "bold"), fg=self.GOLD, bg=self.PANEL)
        self.lbl_title.pack(side="left")

        self.lbl_stats = tk.Label(top_row, text="", font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL)
        self.lbl_stats.pack(side="right")

        self.lbl_weather_info = tk.Label(header, text=self.get_weather_description(), font=("Segoe UI", 9, "italic"), fg=self.GOLD, bg=self.PANEL)
        self.lbl_weather_info.pack(anchor="w", padx=15, pady=(0, 6))

        scene_box = tk.Frame(main, bg="#111318", highlightbackground=self.BORDER, highlightthickness=1)
        scene_box.pack(fill="x", pady=(0, 4))

        self.canvas_view = tk.Canvas(scene_box, height=150, bg="#111318", highlightthickness=0, bd=0)
        self.canvas_view.pack(fill="x", padx=8, pady=4)

        self.lbl_canvas_status = tk.Label(scene_box, text="Đang chờ khách...", font=("Segoe UI", 11, "bold"), fg=self.GOLD, bg="#111318")
        self.lbl_canvas_status.pack(pady=(0, 6))

        dialog_box = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        dialog_box.pack(fill="x", pady=4)

        tk.Label(dialog_box, text="DIỄN BIẾN TRONG NGÀY", font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL).pack(anchor="w", padx=12, pady=(4, 2))
        self.lbl_dialog = tk.Label(dialog_box, text="", font=("Segoe UI", 10), fg=self.TEXT, bg=self.PANEL, wraplength=1000, justify="left", anchor="w")
        self.lbl_dialog.pack(fill="x", padx=12, pady=(0, 6))

        self.kitchen_frame = tk.LabelFrame(
            main, text=" CHUẨN BỊ XÔI ", font=("Segoe UI", 10, "bold"),
            fg=self.GOLD, bg=self.PANEL2, padx=10, pady=6,
            highlightbackground=self.BORDER, highlightthickness=1, bd=0
        )
        self.kitchen_frame.pack(fill="x", pady=4)

        plate_row = tk.Frame(self.kitchen_frame, bg=self.PANEL2)
        plate_row.pack(fill="x", pady=(0, 4))

        self.lbl_plate = tk.Label(plate_row, text="Gói xôi: [Trống]", font=("Segoe UI", 10, "bold"), fg=self.BTN_WARNING, bg=self.PANEL2)
        self.lbl_plate.pack(side="left")

        self.ing_frame = tk.Frame(self.kitchen_frame, bg=self.PANEL2)
        self.ing_frame.pack(fill="x", pady=(2, 0))

        for text, value in [("Xôi", "Xôi"), ("Thịt Kho", "Thịt Kho"), ("Trứng", "Trứng"), ("Chả", "Chả"), ("Lạp Xưởng", "Lạp Xưởng")]:
            btn = self.make_button(self.ing_frame, text, lambda item=value: self.add_ing(item), width=9, bg=self.BTN_DARK)
            btn.pack(side="left", padx=2)

        self.btn_reset_plate = self.make_button(self.ing_frame, "LÀM LẠI", self.reset_plate, width=8, bg=self.BTN_DANGER, fg="black")
        self.btn_reset_plate.pack(side="left", padx=(8, 2))

        self.btn_serve = self.make_button(self.ing_frame, "GIAO XÔI", self.serve_plate, width=12, bg=self.BTN_SUCCESS, fg="black")
        self.btn_serve.pack(side="right", padx=2)

        actions = tk.Frame(main, bg=self.BG)
        actions.pack(fill="x", pady=(8, 0))

        self.btn_talk = self.make_button(actions, "💬 HỎI THĂM TIN ĐỒN", self.action_talk_customer, width=24, bg=self.BTN_INFO, fg="black", height=2)
        self.btn_talk.pack(side="left", expand=True, fill="x", padx=3)

        self.btn_clues = self.make_button(actions, "📖 SỔ TAY MANH MỐI", self.show_clues_notebook, width=24, bg=self.BTN_WARNING, fg="black", height=2)
        self.btn_clues.pack(side="left", expand=True, fill="x", padx=3)

        bottom = tk.Frame(main, bg=self.BG)
        bottom.pack(fill="x", pady=(10, 0))
        self.make_button(bottom, "VỀ MENU", self.confirm_back_menu, width=14, bg=self.BTN_DARK).pack(side="left")

        self.update_stats()
        self.root.after(50, self.draw_counter_scene)

    def show_clues_notebook(self):
        if not self.clues_found:
            messagebox.showinfo("Sổ Tay Manh Mối", "Sổ tay còn trống! Hãy lân la hỏi chuyện khách hàng để thu thập thông tin về vụ án.")
        else:
            text = f"ĐÃ THU THẬP ĐƯỢC {len(self.clues_found)} MANH MỐI:\n\n"
            for idx, clue in enumerate(self.clues_found, 1):
                text += f"{idx}. {clue}\n\n"
            messagebox.showinfo("📖 Sổ Tay Manh Mối Trinh Thám", text)

    def show_dream_sequence(self):
        self.clear_root()
        self.root.configure(bg=self.DREAM_BG)
        
        main = tk.Frame(self.root, bg=self.DREAM_BG)
        main.pack(fill="both", expand=True, padx=40, pady=60)
        
        tk.Label(main, text="ĐÊM XUỐNG - TRONG GIẤC MƠ...", font=("Segoe UI", 20, "bold", "italic"), fg=self.CYAN, bg=self.DREAM_BG).pack(pady=(20, 30))
        
        dream_text = ""
        if self.day == 1:
            dream_text = (
                "\"Xin anh... trả lại tiền cọc cho em đi… em không còn tiền đóng học phí nữa…\"\n"
                "(Tiếng khóc nức nở của một sinh viên vang vọng trong bóng tối...)\n\n"
                "\"Mày nghĩ cái cầu Nhật Tân này vắng người qua lại hả? Nhảy đi! Không có tiền trả thì nhảy!\"\n"
                "(Âm thanh nước chảy xiết lạnh lẽo, xen lẫn tiếng cười gằn ác độc...)"
            )
        elif self.day == 2:
            dream_text = (
                "\"Thằng bán xôi… mày tò mò quá rồi đấy…\"\n"
                "(Một bóng đen cao lớn che khuất mọi ánh sáng xung quanh bạn...)\n\n"
                "\"Làm việc cho tao, hoặc kết cục của mày cũng giống mấy đứa sinh viên kia thôi…\"\n"
                "(Tiếng súng lên nòng vang lên chát chúa trong vô thức...)"
            )

        tk.Label(main, text=dream_text, font=("Segoe UI", 13, "italic"), fg=self.MUTED, bg=self.DREAM_BG, wraplength=800, justify="center").pack(pady=20)
        
        self.make_button(main, "TỈNH GIẤC", self.start_next_day, width=20, height=2, bg=self.BTN_PRIMARY, fg="black").pack(pady=40)

    def build_night_3_ui(self):
        self.root.configure(bg=self.BG)
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=40, pady=40)

        tk.Label(main, text="ĐÊM QUYẾT CHIẾN (ĐÊM THỨ 3)", font=("Segoe UI", 26, "bold"), fg=self.RED, bg=self.BG).pack(pady=(20, 10))
        
        card = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=2)
        card.pack(fill="both", expand=True, ipadx=20, ipady=20)
        
        story = (
            "Đêm thứ 3 định mệnh đã đến. Tại phòng khách tối om, cánh cửa bật mở.\n"
            "Mọi uẩn khúc về các vụ lừa đảo và ép nợ đã sáng tỏ, giờ là lúc bạn đưa ra quyết định thay đổi cục diện thế giới ngầm.\n\n"
            "Bạn sẽ chọn hành động như thế nào?"
        )

        tk.Label(card, text=story, font=("Segoe UI", 12), fg=self.TEXT, bg=self.PANEL, wraplength=800, justify="center").pack(pady=30)

        def do_final_action_lam():
            self.trigger_ending(
                "Ending 3", 
                "HỢP LỰC CÙNG CƠM TẤM (TRUE ENDING)", 
                "Ngọn lửa bùng lên! Bạn lập tức rút điện thoại gọi Lâm (chủ quán Cơm Tấm) đang mai phục sẵn.\n\n"
                "Ngôi nhà rực cháy, Kiều Đăng Tuân hoảng loạn tháo chạy nhưng Lâm đã lái xe chặn mọi ngả đường. Cả hai cùng nhau truy đuổi và tóm gọn tên trùm khét tiếng!\n"
                "Sự thật về các vụ án cuối cùng đã được phơi bày!"
            )

        def do_final_action_secret():
            self.trigger_ending(
                "Secret Ending", 
                "VỊ VUA CỦA XÃ HỘI ĐEN (SECRET ENDING)", 
                "Bạn từ chối đi theo Kiều Đăng Tuân lẫn gọi Lâm. Bằng bản lĩnh và thế lực ngầm tiềm ẩn trong quá khứ, bạn tự quyết định lãnh đạo riêng một tổ chức khác hoàn toàn.\n\n"
                "Chỉ trong một đêm, bạn thống lĩnh lực lượng riêng, đánh sập và tiếp quản toàn bộ đế chế của Kiều Đăng Tuân. Bạn chính thức trở thành 'Vị vua của xã hội đen'!"
            )

        btn_frame = tk.Frame(card, bg=self.PANEL)
        btn_frame.pack(pady=20)

        self.make_button(btn_frame, "GỌI LÂM & ĐỐT NHÀ", do_final_action_lam, width=32, height=3, bg=self.BTN_WARNING, fg="black").pack(side="left", padx=20)
        self.make_button(btn_frame, "TỰ LÃNH ĐẠO TỔ CHỨC RIÊNG", do_final_action_secret, width=32, height=3, bg=self.BTN_PRIMARY, fg="black").pack(side="right", padx=20)

    def update_stats(self):
        if hasattr(self, "lbl_stats") and self.game_running:
            time_str = f"{self.hour:02d}:{self.minute:02d}"
            self.lbl_stats.config(
                text=f"Ngày: {self.day}/3 | Tiền: ${self.money} | Nghi ngờ: {self.suspicion}% | Tỉnh táo: {self.sanity}🧠 | Suất: {self.orders_completed_today}/8"
            )
            
    def draw_counter_scene(self):
        if not hasattr(self, "canvas_view") or not self.game_running or self.day == 3:
            return
        self.canvas_view.delete("all")
        cw = self.canvas_view.winfo_width()
        ch = self.canvas_view.winfo_height()
        if cw <= 1:
            cw, ch = 1000, 150

        self.canvas_view.create_rectangle(0, 0, cw, ch, fill="#111318", outline="")
        self.canvas_view.create_rectangle(0, ch - 40, cw, ch, fill="#1b1e24", outline="")
        self.canvas_view.create_line(0, ch - 40, cw, ch - 40, fill="#2a2e37", width=2)

        if self.customer_visual:
            self.draw_face(self.canvas_view, cw // 2, ch - 50, self.customer_visual, scale=1.0)

    def start_next_day(self):
        self.root.configure(bg=self.BG)
        self.day += 1
        self.orders_completed_today = 0
        self.hour, self.minute = 8, 35
        self.sanity = 100 
        self.suspicion = max(self.suspicion, random.randint(15, 25))
        self.build_game_ui()
        if self.day < 3:
            self.next_customer()

    def next_customer(self):
        if not self.game_running:
            return

        self.talked_current_customer = False

        names_pool = [
            "Ông Chú Xe Ôm", "Sinh Viên Đại học FPT", "Khách Mặc Vest", "Người Đàn Ông Đội Mũ"
        ]
        dialogues_pool = [
            "Cho hộp xôi nhiều thịt nhé, sáng nay đói bụng quá.",
            "Bán em suất xôi mang vào trường ĐH FPT học cho kịp giờ.",
            "Làm nhanh lên, tôi đang vội ra phía Cầu Nhật Tân có việc.",
            "Dạo này khu này trộm cắp nhiều, bán xôi cũng cẩn thận đấy."
        ]

        toppings_pool = ["Thịt Kho", "Trứng", "Chả", "Lạp Xưởng"]
        required_dishes = ["Xôi"] + random.sample(toppings_pool, k=random.randint(1, 3))

        raw_name = random.choice(names_pool)
        self.current_customer = {
            "name": raw_name,
            "dialog": random.choice(dialogues_pool),
            "required": required_dishes
        }
        self.customer_visual = self.customer_visual_from_name(raw_name)
        self.current_plate = []

        self.lbl_canvas_status.config(text=f"Khách: {raw_name}")
        req = ", ".join(self.current_customer["required"])

        self.lbl_dialog.config(
            text=f"[{raw_name}]\n\"{self.current_customer['dialog']}\"\n\n"
                 f"YÊU CẦU: [ {req} ]   |   Suất thứ {self.orders_completed_today + 1}/8"
        )
        self.update_plate_display()
        self.update_stats()
        self.draw_counter_scene()

    def trigger_ending(self, ending_code, title, description):
        self.unlocked_endings.add(ending_code)
        self.save_endings()
        self.check_achievements()
        
        if ending_code in ["Ending 3", "Secret Ending"]:
            messagebox.showinfo(f"KẾT CỤC: {title}", description)
        else:
            messagebox.showerror(f"KẾT CỤC: {title}", description)
            
        self.game_running = False
        self.build_main_menu()

    def trigger_end_of_day_logic(self):
        self.check_achievements()
        if self.day == 1:
            messagebox.showinfo("Hoàn thành ngày bán", "Đã đến chiều tối. Bạn dọn hàng về nhà và chìm vào giấc ngủ...")
            self.show_dream_sequence()

    def check_game_over(self):
        if self.suspicion >= 100:
            self.trigger_ending("Ending 1", "KẺ TÒ MÒ BỊ THỦ TIÊU (GAME OVER)", "Độ nghi ngờ chạm 100%. Băng đảng đã phát hiện ra một kẻ bán xôi hay lân la hỏi chuyện. Bạn đã bị thủ tiêu trong đêm tối.")
            return True
        if self.sanity <= 0:
            messagebox.showwarning("Kiệt Sức", "Bạn đã quá kiệt sức và mất phương hướng vì lo nghĩ quá nhiều. Tạm nghỉ ngơi một chút nhé!")
            self.sanity = 20
        return False

    def action_talk_customer(self):
        if not self.game_running or not self.current_customer:
            return
        if self.talked_current_customer:
            messagebox.showinfo("Đối thoại", "Bạn đã trò chuyện với khách này rồi, họ đang giục gói xôi kìa!")
            return

        self.talked_current_customer = True
        self.sanity -= 15 
        
        topics = [
            ("Anh có nghe tin gì về mấy vụ nhảy Cầu Nhật Tân gần đây không?", 
             "Khách đảo mắt: 'Nghe đồn toàn bị giang hồ ép nợ đến đường cùng đấy, chứ tự tử gì đâu!'",
             "Manh mối: Các vụ nhảy cầu Nhật Tân thực chất là do bị ép nợ nặng lãi."),
            ("Nghe nói quanh đây có bọn chủ trọ chuyên đi lừa tiền cọc sinh viên phải không?", 
             "Khách chép miệng: 'Bọn nó làm theo băng đảng cả đấy, sinh viên thấp cổ bé họng kêu ai được.'",
             "Manh mối: Bọn chủ trọ lừa tiền cọc sinh viên có dính líu tới băng đảng."),
            ("Dạo này sinh viên Đại học FPT ra mua xôi kể nhiều chuyện lạ lắm...", 
             "Khách ngập ngừng: 'Đừng có xía mũi vào. Khu này có tay trùm thâu tóm hết đường dây cho vay nặng lãi đấy.'",
             "Manh mối: Có một tay trùm bí ẩn đang thâu tóm toàn bộ đường dây cho vay.")
        ]
        
        question, answer, clue_text = random.choice(topics)
        
        # Logic: Hỏi khéo thành công mới nhận manh mối, hỏi hớ sẽ mất cơ hội và bị tăng nghi ngờ
        if random.random() < 0.65:
            if clue_text not in self.clues_found:
                self.clues_found.append(clue_text)
            msg = f"Bạn: \"{question}\"\n{answer}\n✨ (Đã khéo léo moi được manh mối mới vào Sổ tay!)"
        else:
            self.suspicion += random.randint(8, 15)
            msg = f"Bạn: \"{question}\"\nKhách hàng nhìn bạn với ánh mắt dò xét: 'Mày chỉ là thằng bán xôi, hỏi chuyện đó làm gì?'.\n⚠️ (Hỏi hớ! Không thu thập được gì và độ nghi ngờ tăng lên!)"

        self.lbl_dialog.config(text=f"[BẠN LÂN LA HỎI CHUYỆN]\n\n{msg}")
        self.check_game_over()
        self.update_stats()

    def add_ing(self, item):
        if not self.game_running:
            return
        self.current_plate.append(item)
        self.update_plate_display()

    def reset_plate(self):
        self.current_plate = []
        self.update_plate_display()

    def update_plate_display(self):
        if hasattr(self, "lbl_plate"):
            self.lbl_plate.config(text=f"Gói xôi: [ Trống ]" if not self.current_plate else f"Gói xôi: [ {', '.join(self.current_plate)} ]")

    def serve_plate(self):
        if not self.game_running or not self.current_customer:
            return

        required = self.current_customer["required"]
        if sorted(self.current_plate) == sorted(required):
            self.money += self.serve_reward
            self.suspicion = max(0, self.suspicion - 2)
            self.correct_serve_streak += 1
            
            self.orders_completed_today += 1
            self.advance_time()
            messagebox.showinfo("Thành công", f"Giao xôi chuẩn! Khách trả ${self.serve_reward}.")
        else:
            self.correct_serve_streak = 0
            self.suspicion += 6
            self.advance_time()
            messagebox.showwarning("Sai món", "Khách khó chịu vì gói xôi không đúng yêu cầu! Nghi ngờ tăng.")

        if self.check_game_over():
            return

        self.check_achievements()

        if self.orders_completed_today >= 8:
            if self.day == 2 and not self.event_night_2_triggered:
                self.trigger_kdt_event_night_2()
                return
            else:
                self.trigger_end_of_day_logic()
            return

        self.update_stats()
        self.next_customer()

    def advance_time(self):
        self.minute += 45 
        if self.minute >= 60:
            self.hour += 1
            self.minute -= 60

    def trigger_kdt_event_night_2(self):
        self.event_night_2_triggered = True
        self.game_running = False
        self.clear_root()

        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=40, pady=40)

        tk.Label(main, text="SỰ KIỆN TỐI NGÀY 2 (20:00)", font=("Segoe UI", 22, "bold"), fg=self.RED, bg=self.BG).pack(pady=(15, 10))
        
        card = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=2)
        card.pack(fill="both", expand=True, ipadx=20, ipady=20)
        
        story = (
            "Đến 8:00 tối, vừa mở cửa bước vào phòng khách, bạn đứng sững lại. Một người đàn ông mang theo sát khí đang ngồi chễm chệ trên ghế.\n\n"
            "Hắn chính là KIỀU ĐĂNG TUÂN!\n"
            "Tuân nhìn bạn và nói:\n\n"
            "\"tao là Kiều Đăng Tuân con trai Kiều Lương Tâm chắc mày cx biết gã nhỉ đó là bố tao tao đc cử đến đây để thông báo với mày QHiếu mày phải đi theo tao , mày là con của Chị đại mà campuchia hay myanmar cx đc miễn là mày theo bọn tao để về nhà cả nhà đag chờ mày , mày từng là một tên tàn bạo mà sao lại thành ra như thế này\""
        )
        tk.Label(card, text=story, font=("Segoe UI", 11), fg=self.TEXT, bg=self.PANEL, wraplength=750, justify="left").pack(pady=25)

        def choose_follow():
            self.trigger_ending("Ending 2", "CHẤP NHẬN LÀM TAY SAI (BAD END)", "Bạn gật đầu đồng ý nhận lấy xấp tiền. Ánh mắt Kiều Đăng Tuân lộ rõ vẻ đắc ý. Bạn chấp nhận nhắm mắt làm ngơ trước tội ác, đánh mất bản thân và trở thành thuộc hạ của hắc bang.")
        
        def choose_think():
            messagebox.showinfo("Lựa chọn", "Bạn cố giữ bình tĩnh: 'Tôi cần thời gian suy nghĩ.'\n\nKiều Đăng Tuân bật cười lớn: 'Được! Tao cho mày đúng 1 ngày. Tối mai tao sẽ quay lại lấy câu trả lời.' Hắn đứng dậy và rời đi. Bạn mệt mỏi thiếp đi...")
            self.show_dream_sequence()

        btn_frame = tk.Frame(card, bg=self.PANEL)
        btn_frame.pack(pady=10)

        self.make_button(btn_frame, "ĐI THEO HẮN", choose_follow, width=24, height=2, bg=self.BTN_DANGER, fg="black").pack(side="left", padx=20)
        self.make_button(btn_frame, "SUY NGHĨ THÊM", choose_think, width=24, height=2, bg=self.BTN_INFO, fg="black").pack(side="right", padx=20)

    def confirm_back_menu(self):
        if messagebox.askyesno("Về menu", "Nghỉ bán sớm và quay lại menu chính?"):
            self.build_main_menu()

    def customer_visual_from_name(self, name):
        visuals = {
            "Ông Chú Xe Ôm": {"skin": "#d7a47d", "hair": "#181a1f", "shirt": "#39424e", "style": "buzz", "scar": False, "glasses": False},
            "Sinh Viên Đại học FPT": {"skin": "#edbc92", "hair": "#25262a", "shirt": "#f28e2b", "style": "fringe", "scar": False, "glasses": True},
            "Người Đàn Ông Đội Mũ": {"skin": "#c78d6e", "hair": "#111318", "shirt": "#2d3139", "style": "cap", "scar": True, "glasses": False},
            "Khách Mặc Vest": {"skin": "#b08569", "hair": "#0d0f12", "shirt": "#1f2229", "style": "short", "scar": False, "glasses": True},
        }
        return visuals.get(name, {"skin": "#d7a47d", "hair": "#181a1f", "shirt": "#2b6cb0", "style": "buzz", "scar": False, "glasses": False})

    def draw_face(self, canvas, cx, cy, visual, scale=1.0):
        skin = visual["skin"]
        hair = visual["hair"]
        shirt = visual["shirt"]
        r = int(35 * scale)

        canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill=skin, outline="#0c0f13", width=2)
        canvas.create_rectangle(cx - int(r * 1.55), cy + int(r * 0.8), cx + int(r * 1.55), cy + int(r * 2.2), fill=shirt, outline="#0c0f13", width=2)

        style = visual["style"]
        if style == "short":
            canvas.create_arc(cx - r, cy - r, cx + r, cy + int(r * 0.5), start=0, extent=180, fill=hair, outline=hair)
        elif style == "buzz":
            canvas.create_oval(cx - r, cy - r, cx + r, cy - int(r * 0.35), fill=hair, outline=hair)
        elif style == "fringe":
            canvas.create_polygon(cx - r, cy - int(r * 0.15), cx - int(r * 0.75), cy - r, cx + int(r * 0.9), cy - int(r * 0.85), cx + int(r * 0.1), cy - int(r * 0.15), fill=hair, outline=hair)
        elif style == "cap":
            canvas.create_arc(cx - int(r*1.1), cy - r, cx + int(r*1.1), cy - int(r * 0.1), start=0, extent=180, fill=hair, outline=hair)
            canvas.create_rectangle(cx - int(r*1.2), cy - int(r*0.2), cx + r, cy, fill=hair, outline=hair)

        eye_y = cy - int(r * 0.08)
        eye_dx = int(r * 0.34)
        eye_r = max(2, int(r * 0.08))
        canvas.create_oval(cx - eye_dx - eye_r, eye_y - eye_r, cx - eye_dx + eye_r, eye_y + eye_r, fill="white")
        canvas.create_oval(cx + eye_dx - eye_r, eye_y - eye_r, cx + eye_dx + eye_r, eye_y + eye_r, fill="white")
        canvas.create_oval(cx - eye_dx - int(eye_r/2), eye_y - int(eye_r/2), cx - eye_dx + int(eye_r/2), eye_y + int(eye_r/2), fill="black")
        canvas.create_oval(cx + eye_dx - int(eye_r/2), eye_y - int(eye_r/2), cx + eye_dx + int(eye_r/2), eye_y + int(eye_r/2), fill="black")

        if visual.get("scar"):
            canvas.create_line(cx - int(r * 0.3), cy + int(r * 0.3), cx + int(r * 0.1), cy + int(r * 0.6), fill="#8a3b3b", width=2)
            
        if visual.get("glasses"):
            canvas.create_rectangle(cx - eye_dx - int(eye_r * 1.5), eye_y - eye_r - 2, cx - eye_dx + int(eye_r * 1.5), eye_y + eye_r + 2, outline="#1a202c", width=2)
            canvas.create_rectangle(cx + eye_dx - int(eye_r * 1.5), eye_y - eye_r - 2, cx + eye_dx + int(eye_r * 1.5), eye_y + eye_r + 2, outline="#1a202c", width=2)
            canvas.create_line(cx - eye_dx + int(eye_r * 1.5), eye_y, cx + eye_dx - int(eye_r * 1.5), eye_y, fill="#1a202c", width=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = Xoi3NightsGame(root)
    root.mainloop()