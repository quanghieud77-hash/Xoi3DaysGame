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

        self.lang = "vi" # Mặc định tiếng Việt ("vi" hoặc "en")

        self.achievement_database = {
            "Ach_1": {
                "vi": ("Sống Sót Qua Ngày", "Vượt qua ngày đầu tiên bán xôi an toàn."),
                "en": ("Surviving the Day", "Get safely through the first day of selling xoi.")
            },
            "Ach_2": {
                "vi": ("Sa Ngã", "Chọn đi theo kẻ trùm ẩn danh vào Đêm 2."),
                "en": ("Fallen", "Choose to follow the mysterious boss on Night 2.")
            },
            "Ach_3": {
                "vi": ("Hợp Lực Cơm Tấm", "Phối hợp cùng Lâm truy đuổi thành công (True Ending)."),
                "en": ("Broken Rice Alliance", "Team up with Lam for a successful pursuit (True Ending).")
            },
            "Ach_Secret": {
                "vi": ("Vua Xã Hội Đen", "Tự lập tổ chức ngầm và trở thành Vị vua xã hội đen (Secret Ending)."),
                "en": ("Underworld King", "Establish your own underground organization and become the Underworld King (Secret Ending).")
            },
            "Ach_4": {
                "vi": ("Vua Xôi", "Phục vụ đúng món liên tiếp 8 lần."),
                "en": ("Xoi Master", "Serve the correct dishes 8 times in a row.")
            },
            "Ach_5": {
                "vi": ("Thám Tử Đường Phố", "Thu thập ít nhất 3 manh mối quan trọng trong sổ tay."),
                "en": ("Street Detective", "Collect at least 3 important clues in your notebook.")
            }
        }
        
        self.save_file = "xoi_3nights_qhouse_save.json"
        self.unlocked_endings = set()
        self.unlocked_achievements = set()
        self.load_endings()
        
        self.reset_game_data()
        self.build_main_menu()

    def toggle_language(self):
        self.lang = "en" if self.lang == "vi" else "vi"
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
            new_unlocked.append(self.achievement_database["Ach_1"][self.lang][0])

        if "Ending 2" in self.unlocked_endings and "Ach_2" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_2")
            new_unlocked.append(self.achievement_database["Ach_2"][self.lang][0])

        if "Ending 3" in self.unlocked_endings and "Ach_3" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_3")
            new_unlocked.append(self.achievement_database["Ach_3"][self.lang][0])
            
        if "Secret Ending" in self.unlocked_endings and "Ach_Secret" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_Secret")
            new_unlocked.append(self.achievement_database["Ach_Secret"][self.lang][0])
            
        if getattr(self, "correct_serve_streak", 0) >= 8 and "Ach_4" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_4")
            new_unlocked.append(self.achievement_database["Ach_4"][self.lang][0])

        if len(self.clues_found) >= 3 and "Ach_5" not in self.unlocked_achievements:
            self.unlocked_achievements.add("Ach_5")
            new_unlocked.append(self.achievement_database["Ach_5"][self.lang][0])

        if new_unlocked:
            self.save_endings()
            for name in new_unlocked:
                title_msg = "🏆 NEW ACHIEVEMENT!" if self.lang == "en" else "🏆 THÀNH TỰU MỚI!"
                content_msg = f"Congratulations! You unlocked achievement:\n\n🏆 [{name}]" if self.lang == "en" else f"Chúc mừng! Bạn đã đạt thành tựu:\n\n🏆 [{name}]"
                messagebox.showinfo(title_msg, content_msg, parent=self.root)

    def show_achievements(self):
        self.check_achievements()
        total_text = f"TOTAL ACHIEVEMENTS UNLOCKED: {len(self.unlocked_achievements)}/6" if self.lang == "en" else f"TỔNG SỐ THÀNH TỰU ĐÃ ĐẠT: {len(self.unlocked_achievements)}/6"
        text = total_text + "\n\n"
        for idx, (code, data) in enumerate(self.achievement_database.items(), 1):
            title, desc = data[self.lang]
            if code in self.unlocked_achievements:
                status = "[✅ UNLOCKED]" if self.lang == "en" else "[✅ ĐÃ ĐẠT]"
                text += f"• {title} -> {status}\n  {desc}\n\n"
            else:
                text += f"• Achievement {idx}: ??? -> [🔒 ???]\n  ???" if self.lang == "en" else f"• Thành tựu {idx}: ??? -> [🔒 ???]\n  ???"
                text += "\n\n"
        messagebox.showinfo("Q-HOUSETEAM Achievements", text)

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
        weathers_vi = {
            1: "Trời Nắng Gắt: Khách hàng vội vã, dễ cáu gắt nếu làm sai món.",
            2: "Trời Mưa Lất Phất: Không gian u ám, độ cảnh giác của giang hồ tăng cao.",
            3: "Trời Mát Mẻ: Ngày quyết định mọi cục diện."
        }
        weathers_en = {
            1: "Scorching Sun: Customers are rushed and easily annoyed if orders are wrong.",
            2: "Drizzling Rain: Gloomy atmosphere, underworld vigilance is heightened.",
            3: "Cool Weather: The decisive day for all outcomes."
        }
        return weathers_en.get(self.day, "") if self.lang == "en" else weathers_vi.get(self.day, "")

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
        
        # Dòng tri ân Q-HOUSETEAM được giữ chuẩn xác theo yêu cầu (Hỗ trợ cả song ngữ)
        tribute_text = (
            "Tribute to Q-HOUSETEAM for creating this amazing series!" 
            if self.lang == "en" 
            else "Tri ân Q-HOUSETEAM vì đã ra sê-ri tuyệt vời này!"
        )
        tk.Label(top, text=tribute_text, font=("Segoe UI", 10, "italic"), fg=self.GREEN, bg=self.BG).pack(pady=(0, 15))

        card = tk.Frame(top, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        card.pack(ipadx=30, ipady=12)

        rules_title = "NEW GAME RULES" if self.lang == "en" else "LUẬT CHƠI MỚI"
        rules_content = (
            "• Serve **8 portions of xoi** each day to have time for gossip.\n"
            "• Monitor **Sanity Bar (🧠)**: Asking too much will exhaust you.\n"
            "• Use the **Clue Notebook (📖)** to review gathered secrets.\n"
            "• Unlock all Endings and Achievements to uncover the full truth."
        ) if self.lang == "en" else (
            "• Mỗi ngày bạn chỉ cần phục vụ **8 suất xôi** để có thời gian hóng chuyện.\n"
            "• Theo dõi **Thanh Tỉnh Táo (🧠)**: Hỏi thăm nhiều sẽ làm bạn mệt mỏi.\n"
            "• Sử dụng **Sổ Tay Manh Mối (📖)** để xem lại các bí mật đã thu thập.\n"
            "• Đạt tối đa các Ending và Thành tựu để khám phá toàn bộ sự thật."
        )

        tk.Label(card, text=rules_title, font=("Segoe UI", 11, "bold"), fg=self.GOLD, bg=self.PANEL).pack(pady=(0, 4))
        tk.Label(card, text=rules_content, font=("Segoe UI", 10), fg=self.TEXT, bg=self.PANEL, justify="left").pack()

        buttons = tk.Frame(outer, bg=self.BG)
        buttons.pack(pady=10)

        btn_start_text = "START SELLING XOI" if self.lang == "en" else "BẮT ĐẦU BÁN XÔI"
        btn_end_text = f"ENDINGS LIBRARY ({len(self.unlocked_endings)}/4)" if self.lang == "en" else f"THƯ VIỆN ENDING ({len(self.unlocked_endings)}/4)"
        btn_ach_text = f"ACHIEVEMENTS ({len(self.unlocked_achievements)}/6)" if self.lang == "en" else f"THÀNH TỰU ({len(self.unlocked_achievements)}/6)"
        btn_lang_text = "🌐 LANGUAGE: ENGLISH" if self.lang == "en" else "🌐 NGÔN NGỮ: TIẾNG VIỆT"
        btn_exit_text = "EXIT GAME" if self.lang == "en" else "THOÁT GAME"

        self.make_button(buttons, btn_start_text, self.start_game, width=32, height=2, bg=self.BTN_PRIMARY, fg="black").pack(pady=4)
        self.make_button(buttons, btn_end_text, self.show_endings, width=32, height=2, bg=self.BTN_INFO, fg="black").pack(pady=4)
        self.make_button(buttons, btn_ach_text, self.show_achievements, width=32, height=2, bg=self.BTN_WARNING, fg="black").pack(pady=4)
        self.make_button(buttons, btn_lang_text, self.toggle_language, width=32, height=2, bg=self.BTN_DARK, fg="white").pack(pady=4)
        self.make_button(buttons, btn_exit_text, self.root.destroy, width=32, height=2, bg=self.BTN_DANGER, fg="black").pack(pady=4)

    def show_endings(self):
        end_data = [
            ("Ending 1", "Ending 1: Curious soul eliminated (GameOver)" if self.lang == "en" else "Ending 1: Kẻ tò mò bị thủ tiêu (GameOver)"),
            ("Ending 2", "Ending 2: Accepting to be a mob minion (Bad End)" if self.lang == "en" else "Ending 2: Chấp nhận làm tay sai hắc bang (Bad End)"),
            ("Ending 3", "Ending 3: Alliance with Broken Rice (True End)" if self.lang == "en" else "Ending 3: Hợp lực cùng Cơm Tấm (True End)"),
            ("Secret Ending", "Secret Ending: King of the Underworld (Secret End)" if self.lang == "en" else "Secret Ending: Vị vua của xã hội đen (Secret End)")
        ]
        
        header_text = f"TOTAL ENDINGS DISCOVERED: {len(self.unlocked_endings)}/4\n\n" if self.lang == "en" else f"TỔNG SỐ ENDING ĐÃ KHÁM PHÁ: {len(self.unlocked_endings)}/4\n\n"
        text = header_text
        for i, (key, full_name) in enumerate(end_data, 1):
            if key in self.unlocked_endings:
                status = "[✅ UNLOCKED]" if self.lang == "en" else "[✅ ĐÃ MỞ KHÓA]"
                text += f"• {full_name} -> {status}\n\n"
            else:
                text += f"• Ending {i}: ??? -> [🔒 ???]\n\n"

        title_win = "Endings Library" if self.lang == "en" else "Thư Viện Endings"
        messagebox.showinfo(title_win, text)

    def start_game(self):
        self.reset_game_data()
        self.game_running = True
        self.build_game_ui()
        start_msg = (
            "Early morning. You push your xoi cart to the familiar street corner. Today's goal is 8 portions of xoi and gathering underground clues."
            if self.lang == "en"
            else "Sáng sớm tinh mơ. Bạn đẩy xe xôi ra góc đường quen thuộc. Mục tiêu hôm nay là 8 suất xôi và tìm kiếm manh mối ngầm."
        )
        title_msg = "Initialization" if self.lang == "en" else "Khởi Đầu"
        messagebox.showinfo(title_msg, start_msg)
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

        title_cart = "Gossip Xoi Cart" if self.lang == "en" else "Xe Xôi Chuyện Bao Đồng"
        self.lbl_title = tk.Label(top_row, text=title_cart, font=("Segoe UI", 13, "bold"), fg=self.GOLD, bg=self.PANEL)
        self.lbl_title.pack(side="left")

        self.lbl_stats = tk.Label(top_row, text="", font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL)
        self.lbl_stats.pack(side="right")

        self.lbl_weather_info = tk.Label(header, text=self.get_weather_description(), font=("Segoe UI", 9, "italic"), fg=self.GOLD, bg=self.PANEL)
        self.lbl_weather_info.pack(anchor="w", padx=15, pady=(0, 6))

        scene_box = tk.Frame(main, bg="#111318", highlightbackground=self.BORDER, highlightthickness=1)
        scene_box.pack(fill="x", pady=(0, 4))

        self.canvas_view = tk.Canvas(scene_box, height=150, bg="#111318", highlightthickness=0, bd=0)
        self.canvas_view.pack(fill="x", padx=8, pady=4)

        wait_text = "Waiting for customer..." if self.lang == "en" else "Đang chờ khách..."
        self.lbl_canvas_status = tk.Label(scene_box, text=wait_text, font=("Segoe UI", 11, "bold"), fg=self.GOLD, bg="#111318")
        self.lbl_canvas_status.pack(pady=(0, 6))

        dialog_box = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=1)
        dialog_box.pack(fill="x", pady=4)

        dev_text = "DAILY PROGRESSION" if self.lang == "en" else "DIỄN BIẾN TRONG NGÀY"
        tk.Label(dialog_box, text=dev_text, font=("Segoe UI", 10, "bold"), fg=self.CYAN, bg=self.PANEL).pack(anchor="w", padx=12, pady=(4, 2))
        self.lbl_dialog = tk.Label(dialog_box, text="", font=("Segoe UI", 10), fg=self.TEXT, bg=self.PANEL, wraplength=1000, justify="left", anchor="w")
        self.lbl_dialog.pack(fill="x", padx=12, pady=(0, 6))

        kitchen_title = " PREPARE XOI " if self.lang == "en" else " CHUẨN BỊ XÔI "
        self.kitchen_frame = tk.LabelFrame(
            main, text=kitchen_title, font=("Segoe UI", 10, "bold"),
            fg=self.GOLD, bg=self.PANEL2, padx=10, pady=6,
            highlightbackground=self.BORDER, highlightthickness=1, bd=0
        )
        self.kitchen_frame.pack(fill="x", pady=4)

        plate_row = tk.Frame(self.kitchen_frame, bg=self.PANEL2)
        plate_row.pack(fill="x", pady=(0, 4))

        self.lbl_plate = tk.Label(plate_row, text="", font=("Segoe UI", 10, "bold"), fg=self.BTN_WARNING, bg=self.PANEL2)
        self.lbl_plate.pack(side="left")

        self.ing_frame = tk.Frame(self.kitchen_frame, bg=self.PANEL2)
        self.ing_frame.pack(fill="x", pady=(2, 0))

        ingredients = [
            ("Xôi", "Xôi" if self.lang == "vi" else "Xoi"), 
            ("Thịt Kho", "Thịt Kho" if self.lang == "vi" else "Braised Pork"), 
            ("Trứng", "Trứng" if self.lang == "vi" else "Egg"), 
            ("Chả", "Chả" if self.lang == "vi" else "Pork Paste"), 
            ("Lạp Xưởng", "Lạp Xưởng" if self.lang == "vi" else "Chinese Sausage")
        ]

        for text, value in ingredients:
            btn = self.make_button(self.ing_frame, text, lambda item=value: self.add_ing(item), width=11, bg=self.BTN_DARK)
            btn.pack(side="left", padx=2)

        reset_btn_text = "RESET" if self.lang == "en" else "LÀM LẠI"
        serve_btn_text = "SERVE XOI" if self.lang == "en" else "GIAO XÔI"

        self.btn_reset_plate = self.make_button(self.ing_frame, reset_btn_text, self.reset_plate, width=9, bg=self.BTN_DANGER, fg="black")
        self.btn_reset_plate.pack(side="left", padx=(8, 2))

        self.btn_serve = self.make_button(self.ing_frame, serve_btn_text, self.serve_plate, width=13, bg=self.BTN_SUCCESS, fg="black")
        self.btn_serve.pack(side="right", padx=2)

        actions = tk.Frame(main, bg=self.BG)
        actions.pack(fill="x", pady=(8, 0))

        talk_btn_text = "💬 GOSSIP & RUMORS" if self.lang == "en" else "💬 HỎI THĂM TIN ĐỒN"
        clue_btn_text = "📖 CLUE NOTEBOOK" if self.lang == "en" else "📖 SỔ TAY MANH MỐI"

        self.btn_talk = self.make_button(actions, talk_btn_text, self.action_talk_customer, width=24, bg=self.BTN_INFO, fg="black", height=2)
        self.btn_talk.pack(side="left", expand=True, fill="x", padx=3)

        self.btn_clues = self.make_button(actions, clue_btn_text, self.show_clues_notebook, width=24, bg=self.BTN_WARNING, fg="black", height=2)
        self.btn_clues.pack(side="left", expand=True, fill="x", padx=3)

        bottom = tk.Frame(main, bg=self.BG)
        bottom.pack(fill="x", pady=(10, 0))
        menu_btn_text = "BACK TO MENU" if self.lang == "en" else "VỀ MENU"
        self.make_button(bottom, menu_btn_text, self.confirm_back_menu, width=16, bg=self.BTN_DARK).pack(side="left")

        self.update_stats()
        self.update_plate_display()
        self.root.after(50, self.draw_counter_scene)

    def show_clues_notebook(self):
        if not self.clues_found:
            msg = "Notebook is empty! Chat with customers to gather information about the case." if self.lang == "en" else "Sổ tay còn trống! Hãy lân la hỏi chuyện khách hàng để thu thập thông tin về vụ án."
            title = "Clue Notebook" if self.lang == "en" else "Sổ Tay Manh Mối"
            messagebox.showinfo(title, msg)
        else:
            header = f"COLLECTED {len(self.clues_found)} CLUES:\n\n" if self.lang == "en" else f"ĐÃ THU THẬP ĐƯỢC {len(self.clues_found)} MANH MỐI:\n\n"
            text = header
            for idx, clue in enumerate(self.clues_found, 1):
                text += f"{idx}. {clue}\n\n"
            title = "📖 Detective Clue Notebook" if self.lang == "en" else "📖 Sổ Tay Manh Mối Trinh Thám"
            messagebox.showinfo(title, text)

    def show_dream_sequence(self):
        self.clear_root()
        self.root.configure(bg=self.DREAM_BG)
        
        main = tk.Frame(self.root, bg=self.DREAM_BG)
        main.pack(fill="both", expand=True, padx=40, pady=60)
        
        dream_title = "NIGHTFALL - IN A DREAM..." if self.lang == "en" else "ĐÊM XUỐNG - TRONG GIẤC MƠ..."
        tk.Label(main, text=dream_title, font=("Segoe UI", 20, "bold", "italic"), fg=self.CYAN, bg=self.DREAM_BG).pack(pady=(20, 30))
        
        if self.lang == "en":
            if self.day == 1:
                dream_text = (
                    "\"Please... give my deposit back... I have no money left for tuition fee...\"\n"
                    "(The sobbing of a student echoes in the dark...)\n\n"
                    "\"You think this Nhat Tan bridge has no passersby? Jump! If you can't pay, just jump!\"\n"
                    "(The sound of cold rushing water mixed with cruel laughter...)"
                )
            else:
                dream_text = (
                    "\"Xoi seller... you're getting way too nosy...\"\n"
                    "(A tall dark shadow blocks all light around you...)\n\n"
                    "\"Work for me, or your fate will be just like those students...\"\n"
                    "(The sound of a gun cocking echoes unconsciously...)"
                )
        else:
            if self.day == 1:
                dream_text = (
                    "\"Xin anh... trả lại tiền cọc cho em đi… em không còn tiền đóng học phí nữa…\"\n"
                    "(Tiếng khóc nức nở của một sinh viên vang vọng trong bóng tối...)\n\n"
                    "\"Mày nghĩ cái cầu Nhật Tân này vắng người qua lại hả? Nhảy đi! Không có tiền trả thì nhảy!\"\n"
                    "(Âm thanh nước chảy xiết lạnh lẽo, xen lẫn tiếng cười gằn ác độc...)"
                )
            else:
                dream_text = (
                    "\"Thằng bán xôi… mày tò mò quá rồi đấy…\"\n"
                    "(Một bóng đen cao lớn che khuất mọi ánh sáng xung quanh bạn...)\n\n"
                    "\"Làm việc cho tao, hoặc kết cục của mày cũng giống mấy đứa sinh viên kia thôi…\"\n"
                    "(Tiếng súng lên nòng vang lên chát chúa trong vô thức...)"
                )

        tk.Label(main, text=dream_text, font=("Segoe UI", 13, "italic"), fg=self.MUTED, bg=self.DREAM_BG, wraplength=800, justify="center").pack(pady=20)
        
        btn_wake = "WAKE UP" if self.lang == "en" else "TỈNH GIẤC"
        self.make_button(main, btn_wake, self.start_next_day, width=20, height=2, bg=self.BTN_PRIMARY, fg="black").pack(pady=40)

    def build_night_3_ui(self):
        self.root.configure(bg=self.BG)
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=40, pady=40)

        night3_title = "DECISIVE NIGHT (NIGHT 3)" if self.lang == "en" else "ĐÊM QUYẾT CHIẾN (ĐÊM THỨ 3)"
        tk.Label(main, text=night3_title, font=("Segoe UI", 26, "bold"), fg=self.RED, bg=self.BG).pack(pady=(20, 10))
        
        card = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=2)
        card.pack(fill="both", expand=True, ipadx=20, ipady=20)
        
        story = (
            "The fated 3rd night has arrived. In the dark living room, the door swings open.\n"
            "All mysteries regarding scams and debt coercion have been unraveled. Now is the time to make a choice that changes the underworld.\n\n"
            "What will be your action?"
        ) if self.lang == "en" else (
            "Đêm thứ 3 định mệnh đã đến. Tại phòng khách tối om, cánh cửa bật mở.\n"
            "Mọi uẩn khúc về các vụ lừa đảo và ép nợ đã sáng tỏ, giờ là lúc bạn đưa ra quyết định thay đổi cục diện thế giới ngầm.\n\n"
            "Bạn sẽ chọn hành động như thế nào?"
        )

        tk.Label(card, text=story, font=("Segoe UI", 12), fg=self.TEXT, bg=self.PANEL, wraplength=800, justify="center").pack(pady=30)

        def do_final_action_lam():
            title_desc = "TRUE ENDING" if self.lang == "en" else "TRUE ENDING"
            desc = (
                "Flames erupt! You immediately grab your phone and call Lam (the Broken Rice shop owner) who is waiting in ambush.\n\n"
                "The house burns down. Kieu Dang Tuan panics and tries to escape, but Lam blocks every road with his car. Together, you pursue and capture the notorious boss!\n"
                "The truth behind the cases is finally brought to light!"
            ) if self.lang == "en" else (
                "Ngọn lửa bùng lên! Bạn lập tức rút điện thoại gọi Lâm (chủ quán Cơm Tấm) đang mai phục sẵn.\n\n"
                "Ngôi nhà rực cháy, Kiều Đăng Tuân hoảng loạn tháo chạy nhưng Lâm đã lái xe chặn mọi ngả đường. Cả hai cùng nhau truy đuổi và tóm gọn tên trùm khét tiếng!\n"
                "Sự thật về các vụ án cuối cùng đã được phơi bày!"
            )
            self.trigger_ending("Ending 3", title_desc, desc)

        def do_final_action_secret():
            title_desc = "SECRET ENDING" if self.lang == "en" else "SECRET ENDING"
            desc = (
                "You refuse both Kieu Dang Tuan and Lam. With your hidden underworld background and courage, you decide to lead a completely different organization yourself.\n\n"
                "In just one night, you command your own force, collapse and take over Kieu Dang Tuan's entire empire. You officially become the 'Underworld King'!"
            ) if self.lang == "en" else (
                "Bạn từ chối đi theo Kiều Đăng Tuân lẫn gọi Lâm. Bằng bản lĩnh và thế lực ngầm tiềm ẩn trong quá khứ, bạn tự quyết định lãnh đạo riêng một tổ chức khác hoàn toàn.\n\n"
                "Chỉ trong một đêm, bạn thống lĩnh lực lượng riêng, đánh sập và tiếp quản toàn bộ đế chế của Kiều Đăng Tuân. Bạn chính thức trở thành 'Vị vua của xã hội đen'!"
            )
            self.trigger_ending("Secret Ending", title_desc, desc)

        btn_frame = tk.Frame(card, bg=self.PANEL)
        btn_frame.pack(pady=20)

        btn1_text = "CALL LAM & BURN HOUSE" if self.lang == "en" else "GỌI LÂM & ĐỐT NHÀ"
        btn2_text = "LEAD OWN ORGANIZATION" if self.lang == "en" else "TỰ LÃNH ĐẠO TỔ CHỨC"

        self.make_button(btn_frame, btn1_text, do_final_action_lam, width=30, height=3, bg=self.BTN_WARNING, fg="black").pack(side="left", padx=20)
        self.make_button(btn_frame, btn2_text, do_final_action_secret, width=30, height=3, bg=self.BTN_PRIMARY, fg="black").pack(side="right", padx=20)

    def update_stats(self):
        if hasattr(self, "lbl_stats") and self.game_running:
            time_str = f"{self.hour:02d}:{self.minute:02d}"
            if self.lang == "en":
                stats_str = f"Day: {self.day}/3 | Money: ${self.money} | Suspicion: {self.suspicion}% | Sanity: {self.sanity}🧠 | Served: {self.orders_completed_today}/8"
            else:
                stats_str = f"Ngày: {self.day}/3 | Tiền: ${self.money} | Nghi ngờ: {self.suspicion}% | Tỉnh táo: {self.sanity}🧠 | Suất: {self.orders_completed_today}/8"
            self.lbl_stats.config(text=stats_str)
            
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

        if self.lang == "en":
            names_pool = ["Motorbike Taxi Uncle", "FPT University Student", "Suit Man", "Cap-wearing Man"]
            dialogues_pool = [
                "Give me a box of xoi with extra meat, feeling hungry this morning.",
                "Sell me a portion of xoi to take to FPT University in time for class.",
                "Hurry up, I'm in a rush heading toward Nhat Tan Bridge.",
                "Lots of thefts around here lately, be careful selling xoi."
            ]
            toppings_pool = ["Braised Pork", "Egg", "Pork Paste", "Chinese Sausage"]
        else:
            names_pool = ["Ông Chú Xe Ôm", "Sinh Viên Đại học FPT", "Khách Mặc Vest", "Người Đàn Ông Đội Mũ"]
            dialogues_pool = [
                "Cho hộp xôi nhiều thịt nhé, sáng nay đói bụng quá.",
                "Bán em suất xôi mang vào trường ĐH FPT học cho kịp giờ.",
                "Làm nhanh lên, tôi đang vội ra phía Cầu Nhật Tân có việc.",
                "Dạo này khu này trộm cắp nhiều, bán xôi cũng cẩn thận đấy."
            ]
            toppings_pool = ["Thịt Kho", "Trứng", "Chả", "Lạp Xưởng"]

        required_dishes = ["Xôi" if self.lang == "vi" else "Xoi"] + random.sample(toppings_pool, k=random.randint(1, 3))

        raw_name = random.choice(names_pool)
        self.current_customer = {
            "name": raw_name,
            "dialog": random.choice(dialogues_pool),
            "required": required_dishes
        }
        self.customer_visual = self.customer_visual_from_name(raw_name)
        self.current_plate = []

        c_status = f"Customer: {raw_name}" if self.lang == "en" else f"Khách: {raw_name}"
        self.lbl_canvas_status.config(text=c_status)
        req = ", ".join(self.current_customer["required"])

        dialog_label_text = (
            f"[{raw_name}]\n\"{self.current_customer['dialog']}\"\n\n"
            f"REQUIRED: [ {req} ]   |   Portion {self.orders_completed_today + 1}/8"
            if self.lang == "en"
            else f"[{raw_name}]\n\"{self.current_customer['dialog']}\"\n\n"
                 f"YÊU CẦU: [ {req} ]   |   Suất thứ {self.orders_completed_today + 1}/8"
        )
        self.lbl_dialog.config(text=dialog_label_text)
        self.update_plate_display()
        self.update_stats()
        self.draw_counter_scene()

    def trigger_ending(self, ending_code, title, description):
        self.unlocked_endings.add(ending_code)
        self.save_endings()
        self.check_achievements()
        
        if ending_code in ["Ending 3", "Secret Ending"]:
            messagebox.showinfo(f"ENDING: {title}", description)
        else:
            messagebox.showerror(f"ENDING: {title}", description)
            
        self.game_running = False
        self.build_main_menu()

    def trigger_end_of_day_logic(self):
        self.check_achievements()
        if self.day == 1:
            msg = "Evening has come. You pack up your cart, head home and fall asleep..." if self.lang == "en" else "Đã đến chiều tối. Bạn dọn hàng về nhà và chìm vào giấc ngủ..."
            title = "End of Day" if self.lang == "en" else "Hoàn thành ngày bán"
            messagebox.showinfo(title, msg)
            self.show_dream_sequence()

    def check_game_over(self):
        if self.suspicion >= 100:
            title = "CURIOUS SOUL ELIMINATED (GAME OVER)" if self.lang == "en" else "KẺ TÒ MÒ BỊ THỦ TIÊU (GAME OVER)"
            desc = (
                "Suspicion reached 100%. The gang discovered a xoi seller nosing around. You were eliminated in the dark."
                if self.lang == "en"
                else "Độ nghi ngờ chạm 100%. Băng đảng đã phát hiện ra một kẻ bán xôi hay lân la hỏi chuyện. Bạn đã bị thủ tiêu trong đêm tối."
            )
            self.trigger_ending("Ending 1", title, desc)
            return True
        if self.sanity <= 0:
            title_warn = "Exhausted" if self.lang == "en" else "Kiệt Sức"
            msg = "You are completely exhausted and disoriented from overthinking. Rest a bit!" if self.lang == "en" else "Bạn đã quá kiệt sức và mất phương hướng vì lo nghĩ quá nhiều. Tạm nghỉ ngơi một chút nhé!"
            messagebox.showwarning(title_warn, msg)
            self.sanity = 20
        return False

    def action_talk_customer(self):
        if not self.game_running or not self.current_customer:
            return
        if self.talked_current_customer:
            msg = "You've already chatted with this customer, they are rushing for their xoi!" if self.lang == "en" else "Bạn đã trò chuyện với khách này rồi, họ đang giục gói xôi kìa!"
            title = "Dialogue" if self.lang == "en" else "Đối thoại"
            messagebox.showinfo(title, msg)
            return

        self.talked_current_customer = True
        self.sanity -= 15 
        
        if self.lang == "en":
            topics = [
                ("Have you heard anything about the Nhat Tan Bridge jumping cases lately?", 
                 "Customer rolls eyes: 'Rumor says they were all forced into a corner by loan sharks, not suicide at all!'",
                 "Clue: The Nhat Tan Bridge jumping cases are actually caused by heavy debt coercion."),
                ("I heard around here there are landlords specializing in student deposit scams?", 
                 "Customer clicks tongue: 'They work for the underworld syndicate, students have nowhere to turn.'",
                 "Clue: Landlords scamming student deposits are linked to the underworld syndicate."),
                ("Lately, FPT University students coming to buy xoi tell strange stories...", 
                 "Customer hesitates: 'Don't stick your nose into it. There's a big boss controlling all loan shark networks here.'",
                 "Clue: A mysterious big boss controls the entire loan shark network.")
            ]
        else:
            topics = [
                ("Anh có nghe tin gì về mấy vụ nhảy Cầu Nhật Tân gần đây không?", 
                 "Khách đảo mắt: 'Nghe đồn toàn bị giang hồ ép nợ đến đường cùng đấy, chứ tự tử gì đâu!'",
                 "Manh mối: Các vụ nhảy cầu Nhật Tân thực chất là do bị ép nợ nặng lãi."),
                ("Nghe nói quanh đây có bọn chủ trọ chuyên đi lân la lừa tiền cọc sinh viên phải không?", 
                 "Khách chép miệng: 'Bọn nó làm theo băng đảng cả đấy, sinh viên thấp cổ bé họng kêu ai được.'",
                 "Manh mối: Bọn chủ trọ lừa tiền cọc sinh viên có dính líu tới băng đảng."),
                ("Dạo này sinh viên Đại học FPT ra mua xôi kể nhiều chuyện lạ lắm...", 
                 "Khách ngập ngừng: 'Đừng có xía mũi vào. Khu này có tay trùm thâu tóm hết đường dây cho vay nặng lãi đấy.'",
                 "Manh mối: Có một tay trùm bí ẩn đang thâu tóm toàn bộ đường dây cho vay.")
            ]
        
        question, answer, clue_text = random.choice(topics)
        
        if random.random() < 0.65:
            if clue_text not in self.clues_found:
                self.clues_found.append(clue_text)
            msg = (
                f"You: \"{question}\"\n{answer}\n✨ (Successfully extracted a new clue into your notebook!)"
                if self.lang == "en"
                else f"Bạn: \"{question}\"\n{answer}\n✨ (Đã khéo léo moi được manh mối mới vào Sổ tay!)"
            )
            header_box = "[CHAT & GOSSIP]" if self.lang == "en" else "[BẠN LÂN LA HỎI CHUYỆN]"
        else:
            self.suspicion += random.randint(8, 15)
            msg = (
                f"You: \"{question}\"\nCustomer looks at you suspiciously: 'You're just a xoi seller, why ask about that?'.\n⚠️ (Clumsy question! Nothing gathered and suspicion increased!)"
                if self.lang == "en"
                else f"Bạn: \"{question}\"\nKhách hàng nhìn bạn với ánh mắt dò xét: 'Mày chỉ là thằng bán xôi, hỏi chuyện đó làm gì?'.\n⚠️ (Hỏi hớ! Không thu thập được gì và độ nghi ngờ tăng lên!)"
            )
            header_box = "[CHAT & GOSSIP]" if self.lang == "en" else "[BẠN LÂN LA HỎI CHUYỆN]"

        self.lbl_dialog.config(text=f"{header_box}\n\n{msg}")
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
            if not self.current_plate:
                txt = "Xoi pack: [ Empty ]" if self.lang == "en" else "Gói xôi: [ Trống ]"
            else:
                txt = f"Xoi pack: [ {', '.join(self.current_plate)} ]" if self.lang == "en" else f"Gói xôi: [ {', '.join(self.current_plate)} ]"
            self.lbl_plate.config(text=txt)

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
            msg = f"Served correctly! Customer pays ${self.serve_reward}." if self.lang == "en" else f"Giao xôi chuẩn! Khách trả ${self.serve_reward}."
            title = "Success" if self.lang == "en" else "Thành công"
            messagebox.showinfo(title, msg)
        else:
            self.correct_serve_streak = 0
            self.suspicion += 6
            self.advance_time()
            msg = "Customer is upset because the xoi pack doesn't match their request! Suspicion increases." if self.lang == "en" else "Khách khó chịu vì gói xôi không đúng yêu cầu! Nghi ngờ tăng."
            title = "Wrong Dish" if self.lang == "en" else "Sai món"
            messagebox.showwarning(title, msg)

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

        title_e = "NIGHT 2 EVENT (20:00)" if self.lang == "en" else "SỰ KIỆN TỐI NGÀY 2 (20:00)"
        tk.Label(main, text=title_e, font=("Segoe UI", 22, "bold"), fg=self.RED, bg=self.BG).pack(pady=(15, 10))
        
        card = tk.Frame(main, bg=self.PANEL, highlightbackground=self.BORDER, highlightthickness=2)
        card.pack(fill="both", expand=True, ipadx=20, ipady=20)
        
        if self.lang == "en":
            story = (
                "At 8:00 PM, stepping into your living room, you freeze. A murderous man is sitting leisurely on the chair.\n\n"
                "He is KIEU DANG TUAN!\n"
                "Tuan looks at you and says:\n\n"
                "\"I am Kieu Dang Tuan, son of Kieu Luong Tam, I bet you know him, he is my father. I've been sent here to inform you, QHieu, you must come with me. You are the Big Boss's child whether from Cambodia or Myanmar doesn't matter, just follow us home everyone is waiting. You used to be such a brutal guy, how did you turn into this?\""
            )
        else:
            story = (
                "Đến 8:00 tối, vừa mở cửa bước vào phòng khách, bạn đứng sững lại. Một người đàn ông mang theo sát khí đang ngồi chễm chệ trên ghế.\n\n"
                "Hắn chính là KIỀU ĐĂNG TUÂN!\n"
                "Tuân nhìn bạn và nói:\n\n"
                "\"tao là Kiều Đăng Tuân con trai Kiều Lương Tâm chắc mày cx biết gã nhỉ đó là bố tao tao đc cử đến đây để thông báo với mày QHiếu mày phải đi theo tao , mày là con của Chị đại mà campuchia hay myanmar cx đc miễn là mày theo bọn tao để về nhà cả nhà đag chờ mày , mày từng là một tên tàn bạo mà sao lại thành ra như thế này\""
            )

        tk.Label(card, text=story, font=("Segoe UI", 11), fg=self.TEXT, bg=self.PANEL, wraplength=750, justify="left").pack(pady=25)

        def choose_follow():
            title_desc = "BAD END" if self.lang == "en" else "BAD END"
            desc = (
                "You nod in agreement to take the stack of cash. Kieu Dang Tuan's eyes reveal a smug look. You accept turning a blind eye to crimes, losing yourself and becoming the mafia's minion."
                if self.lang == "en"
                else "Bạn gật đầu đồng ý nhận lấy xấp tiền. Ánh mắt Kiều Đăng Tuân lộ rõ vẻ đắc ý. Bạn chấp nhận nhắm mắt làm ngơ trước tội ác, đánh mất bản thân và trở thành thuộc hạ của hắc bang."
            )
            self.trigger_ending("Ending 2", title_desc, desc)
        
        def choose_think():
            if self.lang == "en":
                messagebox.showinfo("Choice", "You try to stay calm: 'I need time to think.'\n\nKieu Dang Tuan laughs loudly: 'Fine! I give you exactly 1 day. Tomorrow night I'll be back for your answer.' He stands up and leaves. You fall asleep exhausted...")
            else:
                messagebox.showinfo("Lựa chọn", "Bạn cố giữ bình tĩnh: 'Tôi cần thời gian suy nghĩ.'\n\nKiều Đăng Tuân bật cười lớn: 'Được! Tao cho mày đúng 1 ngày. Tối mai tao sẽ quay lại lấy câu trả lời.' Hắn đứng dậy và rời đi. Bạn mệt mỏi thiếp đi...")
            self.show_dream_sequence()

        btn_frame = tk.Frame(card, bg=self.PANEL)
        btn_frame.pack(pady=10)

        b1 = "FOLLOW HIM" if self.lang == "en" else "ĐI THEO HẮN"
        b2 = "THINK MORE" if self.lang == "en" else "SUY NGHĨ THÊM"

        self.make_button(btn_frame, b1, choose_follow, width=24, height=2, bg=self.BTN_DANGER, fg="black").pack(side="left", padx=20)
        self.make_button(btn_frame, b2, choose_think, width=24, height=2, bg=self.BTN_INFO, fg="black").pack(side="right", padx=20)

    def confirm_back_menu(self):
        msg = "Stop selling early and return to main menu?" if self.lang == "en" else "Nghỉ bán sớm và quay lại menu chính?"
        title = "Back to Menu" if self.lang == "en" else "Về menu"
        if messagebox.askyesno(title, msg):
            self.build_main_menu()

    def customer_visual_from_name(self, name):
        visuals = {
            "Ông Chú Xe Ôm": {"skin": "#d7a47d", "hair": "#181a1f", "shirt": "#39424e", "style": "buzz", "scar": False, "glasses": False},
            "Sinh Viên Đại học FPT": {"skin": "#edbc92", "hair": "#25262a", "shirt": "#f28e2b", "style": "fringe", "scar": False, "glasses": True},
            "Người Đàn Ông Đội Mũ": {"skin": "#c78d6e", "hair": "#111318", "shirt": "#2d3139", "style": "cap", "scar": True, "glasses": False},
            "Khách Mặc Vest": {"skin": "#b08569", "hair": "#0d0f12", "shirt": "#1f2229", "style": "short", "scar": False, "glasses": True},
            # English keys mapping
            "Motorbike Taxi Uncle": {"skin": "#d7a47d", "hair": "#181a1f", "shirt": "#39424e", "style": "buzz", "scar": False, "glasses": False},
            "FPT University Student": {"skin": "#edbc92", "hair": "#25262a", "shirt": "#f28e2b", "style": "fringe", "scar": False, "glasses": True},
            "Cap-wearing Man": {"skin": "#c78d6e", "hair": "#111318", "shirt": "#2d3139", "style": "cap", "scar": True, "glasses": False},
            "Suit Man": {"skin": "#b08569", "hair": "#0d0f12", "shirt": "#1f2229", "style": "short", "scar": False, "glasses": True},
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