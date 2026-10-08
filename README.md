# 🎵 NovaDL

**NovaDL** is a desktop music downloader built with Python and CustomTkinter.

It provides a simple graphical interface for downloading music, managing download records, and generating an HTML report of downloaded tracks.

## ✨ Features

* 🎵 Download music through a simple desktop GUI
* 📥 Multiple-page downloading
* ⏯️ Pause / Resume downloads
* 🛑 Stop download process
* 📴 Optional automatic system shutdown after downloading
* 🗃️ SQLite database for downloaded music records
* 📊 HTML download report
* 📁 Custom download folder
* ⚙️ Persistent download-path configuration
* 🧹 Filename sanitization for downloaded files
* 🖥️ Windows executable and installer

## 🛠️ Built With

* **Python**
* **CustomTkinter**
* **Requests**
* **SQLite**
* **BeautifulSoup**
* **PyInstaller**
* **Inno Setup**

## 📸 Interface

Screenshots of the application can be added here.

## 🚀 Installation

### Option 1 — Windows Installer

Download the latest `NovaDL_Setup.exe` from the **Releases** section of this repository and run the installer.

### Option 2 — Run From Source

Clone the repository:

```bash
git clone https://github.com/AGCode7/NovaDL.git
cd NovaDL
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

## 📂 Project Structure

```text
NovaDL/
│
├── icon/
│   └── icon.ico
│
├── templates/
│   └── report.html
│
├── config.py
├── downloader.py
├── gui.py
├── lib.py
├── main.py
├── utils.py
│
├── requirements.txt
├── LICENSE
├── README.md
└── .gitignore
```

## 💾 Data & Configuration

NovaDL uses:

* **SQLite** for storing downloaded music records
* **JSON** for storing the configured download path
* **HTML** for generating download reports

The application automatically handles the required application data directories.

## 📊 Download Report

After a download session, NovaDL can generate an HTML report containing information about the downloaded music.

The report is stored inside the selected download directory:

```text
report/
└── report.html
```

## 🧑‍💻 Developer

**AGCode7**

NovaDL was developed as a Python desktop application with a focus on simplicity, usability, and practical download management.

## 📄 License

This project is distributed under the license included in the `LICENSE` file.
