from gui import MusicDownloaderApp
import lib

if __name__ == "__main__":
    lib.create_database()
    app = MusicDownloaderApp()
    app.mainloop()
