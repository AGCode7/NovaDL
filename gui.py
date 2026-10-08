import utils
import os
import lib
from datetime import datetime
import threading
import customtkinter as ctk
from tkinter import filedialog, messagebox
import config
import downloader
from pathlib import Path

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MusicDownloaderApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(config.WINDOW_TITLE)
        self.geometry(config.WINDOW_SIZE)
        self.resizable(*config.WINDOW_RESIZABLE)
        self.str_font = ctk.CTkFont(size=config.FONT_SIZE, weight=config.FONT_WEIGHT)

        self.iconbitmap(str(config.ICON_PATH))

        self.is_running = False
        self.is_paused = False
        self.shutdown_requested = False

        if Path("setting.json").is_file():
            self.json_path = utils.load_path(config.JSON_PATH)["download_path"]
        else:
            self.json_path = config.DEFAULT_DOWNLOAD_PATH

        self.download = downloader.Downloader()

        self._build_widgets()

    def _build_widgets(self):
        # عنوان اصلی
        ctk.CTkLabel(
            self, text=config.TEXT_APP_TITLE, font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(config.PADY_MAIN, 10))

        # پوشه ذخیره
        frame_folder = ctk.CTkFrame(self, fg_color="transparent")
        frame_folder.pack(pady=config.PADY_SMALL, padx=config.PADX_MAIN, fill="x")

        self.entry_folder = ctk.CTkEntry(
            frame_folder,
            fg_color=config.FG_ENTRY_COLOR,
            border_color=config.BORDER_ENTRY_COLOR,
            font=self.str_font,
            border_width=1,
            corner_radius=10,
            placeholder_text=config.TEXT_FOLDER_PLACEHOLDER,
        )
        self.entry_folder.pack(
            side="left", padx=config.PADX_SMALL, fill="x", expand=True
        )
        self.entry_folder.insert(0, self.json_path)

        ctk.CTkButton(
            frame_folder,
            fg_color=config.BTN_FOLDER_COLOR,
            hover_color=config.BTN_FOLDER_HOVER,
            font=self.str_font,
            text=config.TEXT_BTN_FOLDER,
            width=config.BTN_WIDTH,
            corner_radius=10,
            command=self.choose_folder,
        ).pack(side="left", padx=config.PADX_SMALL)

        # تعداد صفحات
        frame_pages = ctk.CTkFrame(self, fg_color="transparent")
        frame_pages.pack(pady=config.PADY_SMALL, padx=config.PADX_MAIN, fill="x")

        ctk.CTkLabel(
            frame_pages, font=self.str_font, text=config.TEXT_LABEL_PAGES
        ).pack(side="left", padx=config.PADX_SMALL)

        self.entry_pages = ctk.CTkEntry(
            frame_pages,
            font=self.str_font,
            fg_color=config.FG_ENTRY_COLOR,
            border_color=config.BORDER_ENTRY_COLOR,
            border_width=1,
            placeholder_text=config.TEXT_PAGES_PLACEHOLDER,
            corner_radius=10,
            width=config.ENTRY_WIDTH,
        )
        self.entry_pages.pack(side="left", padx=config.PADX_SMALL)
        self.entry_pages.insert(0, str(config.DEFAULT_PAGE_COUNT))

        # دکمه‌های کنترل
        self.btn_start = ctk.CTkButton(
            frame_pages,
            text=config.TEXT_BTN_DOWNLOAD,
            text_color=config.COLOR_TEXT_WHITE,
            fg_color=config.BTN_DOWNLOAD_COLOR,
            hover_color=config.BTN_DOWNLOAD_HOVER,
            font=self.str_font,
            width=config.BTN_WIDTH,
            corner_radius=10,
            command=self.start_download,
        )
        self.btn_start.pack(side="left", padx=config.PADX_SMALL)

        self.btn_pause = ctk.CTkButton(
            frame_pages,
            text=config.TEXT_BTN_PAUSE,
            fg_color=config.BTN_PAUSE_COLOR,
            hover_color=config.BTN_PAUSE_HOVER,
            font=self.str_font,
            width=config.BTN_WIDTH,
            corner_radius=10,
            command=self.toggle_pause,
            state="disabled",
        )
        self.btn_pause.pack(side="left", padx=config.PADX_SMALL)

        self.btn_shutdown = ctk.CTkButton(
            frame_pages,
            text=config.TEXT_BTN_SHUTDOWN_OFF,
            text_color=config.BTN_SHUTDOWN_TEXT,
            fg_color=config.BTN_SHUTDOWN_COLOR,
            hover_color=config.BTN_SHUTDOWN_HOVER,
            border_color=config.BORDER_ENTRY_COLOR,
            border_width=1,
            font=self.str_font,
            width=config.BTN_WIDTH,
            corner_radius=10,
            command=self.shutdown_download,
        )
        self.btn_shutdown.pack(side="left", padx=config.PADX_SMALL)

        # نوار پیشرفت
        self.progress_bar = ctk.CTkProgressBar(
            self,
            height=15,
            width=config.PROGRESS_WIDTH,
            progress_color=config.PROGRESS_COLOR,
        )
        self.progress_bar.set(0)
        self.progress_bar.pack(pady=(5, 15))

        # باکس لاگ
        self.log_box = ctk.CTkTextbox(
            self,
            corner_radius=15,
            width=config.PROGRESS_WIDTH,
            font=self.str_font,
            height=config.LOG_BOX_HEIGHT,
            fg_color=config.LOG_BOX_COLOR,
        )
        self.log_box.pack(pady=config.PADY_SMALL, padx=config.PADX_MAIN)
        self.log_box.configure(state="disabled")

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.entry_folder.delete(0, "end")
            self.entry_folder.insert(0, folder)

    def log(self, text):
        def append():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", text + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")

        self.after(0, append)

    def set_progress(self, value):
        self.after(0, lambda: self.progress_bar.set(value))

    def start_download(self):
        if self.is_running:
            return

        try:
            page_count = int(self.entry_pages.get())
            if page_count < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "error", "The number of pages must be a positive integer."
            )
            return

        folder = self.entry_folder.get().strip()
        if not folder:
            messagebox.showerror("error", "Please select a folder to save to.")
            return
        self.json_path = folder
        self.is_running = True
        self.is_paused = False
        self.btn_start.configure(state="disabled")
        self.btn_pause.configure(state="normal")
        self.progress_bar.set(0)

        thread = threading.Thread(
            target=self.run_download, args=(page_count, folder), daemon=True
        )
        thread.start()

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.btn_pause.configure(
                text=config.TEXT_BTN_RESUME,
                text_color=config.BTN_SHUTDOWN_ACTIVE_TEXT,
                fg_color=config.BTN_START_COLOR,
                hover_color=config.BTN_START_HOVER,
            )
        else:
            self.btn_pause.configure(
                text=config.TEXT_BTN_PAUSE,
                text_color=config.BTN_SHUTDOWN_TEXT,
                fg_color=config.BTN_PAUSE_COLOR,
                hover_color=config.BTN_PAUSE_HOVER,
            )

    def shutdown_download(self):
        self.shutdown_requested = not self.shutdown_requested

        if self.shutdown_requested:
            self.btn_shutdown.configure(
                text=config.TEXT_BTN_SHUTDOWN_ON,
                text_color=config.BTN_SHUTDOWN_ACTIVE_TEXT,
                fg_color=config.BTN_SHUTDOWN_ACTIVE_COLOR,
                hover_color=config.BTN_SHUTDOWN_ACTIVE_HOVER,
            )
        else:
            self.download.cancel_shutdown()
            self.btn_shutdown.configure(
                text=config.TEXT_BTN_SHUTDOWN_OFF,
                text_color=config.BTN_SHUTDOWN_TEXT,
                fg_color=config.BTN_SHUTDOWN_COLOR,
                hover_color=config.BTN_SHUTDOWN_HOVER,
                border_color=config.BORDER_ENTRY_COLOR,
                border_width=1,
            )

    def finish(self, folder):
        self.after(0, self._finish_ui, folder)

    def _finish_ui(self, folder):
        self.is_running = False

        template_data = {
            "version": "1.2.0",
            "report_date": datetime.now().strftime("%Y/%m/%d"),
            "report_time": datetime.now().strftime("%H:%M"),
            "musics": lib.get_records("musics"),
        }

        output_path = os.path.join(folder, "report", "report.html")

        if utils.render_html(
            template_name="report.html",
            data=template_data,
            output_path=output_path,
            template_dir=config.TEMPLATE_PATH,
        ):
            self.log(config.LOG_SAVE_PDF)
        else:
            self.log(config.LOG_SAVE_PDF_ERROR)

        self.btn_start.configure(state="normal")
        self.btn_pause.configure(state="disabled")

        if self.shutdown_requested and not self.is_paused:
            self.log(config.LOG_SHUTDOWN_SYSTEM.format(config.SHUTDOWN_DELAY_MINUTES))
            self.download.shutdown_system(delay_minutes=config.SHUTDOWN_DELAY_MINUTES)
        else:
            messagebox.showinfo("Download", config.MESSAGEBOX_SUCCESSFULY)

    def run_download(self, page_count, folder):
        try:
            self.download.download_all(
                page_count=page_count,
                adr_folder=folder,
                log=self.log,
                progress=self.set_progress,
                is_paused=lambda: self.is_paused,
            )

        except Exception as e:
            self.log(f"Unexpected error: {e}")

        finally:
            self.finish(folder)
