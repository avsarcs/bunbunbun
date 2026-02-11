# Grammar Drill 文法ドリル

A spaced-repetition grammar practice app for Japanese learners (or any language). Grammar points appear as cards weighted by difficulty — the more you struggle with something, the more it shows up. Rate each card after writing a sentence, and watch your weak points gradually disappear.

![Theme preview: Wabi-sabi Dark, Moonlight, Sakura Light, Forest, Solarized Dark, High Contrast]

---

## Features

- **Weighted spaced repetition** — Hard-rated points increase in frequency; Easy-rated points fade into the background
- **Session customisation** — Choose how many grammar points appear per round (1–5)
- **Sentence input** — Write a sentence using each grammar point to reinforce active recall
- **Statistics dashboard** — Activity heatmap, streak tracking, difficulty breakdown, weekday patterns, mastery overview and more
- **Searchable history** — Filter past sessions by grammar point, difficulty, or keyword
- **6 built-in themes** — Wabi-sabi Dark, Moonlight, Sakura Light, Forest, Solarized Dark, High Contrast
- **BunPro integration** — Each card links directly to its BunPro reference page
- **Portable data** — Progress and history stored as plain JSON in `user_data/`

---
## Disclaimer & Acknowledgements

This project is an unofficial application and is not affiliated with, endorsed by, or connected to Bunpro.

The grammar point names and JLPT level classifications used in this application are sourced from (Bunpro.jp)[https://bunpro.jp/]. All grammar explanations and detailed content are externally linked directly to Bunpro to support their platform. All intellectual property rights regarding the original content and curriculum structure belong to Bunpro.

---

## Screenshots

<img width="664" height="765" alt="image" src="https://github.com/user-attachments/assets/d43f0740-ece5-422c-bcb2-3c48eb90c92f" />

<img width="665" height="768" alt="image" src="https://github.com/user-attachments/assets/7dc0e65f-fd36-4b14-8473-e1fa5164c11f" />

<img width="616" height="767" alt="image" src="https://github.com/user-attachments/assets/383ba8ed-05b7-42c7-908f-7f6f5f32ce7a" />

<img width="566" height="642" alt="image" src="https://github.com/user-attachments/assets/19b2d0b0-7849-43ac-83ec-421a4c73eb35" />


---

## Quick Start

### Windows

1. Go to the [Releases](../../releases) page
2. Download `GrammarDrill.exe` from the latest release
3. Place it in a folder of your choice (e.g. `C:\GrammarDrill\`)
4. Double-click to run

---

### Linux

#### Option A — Download the binary (quickest)

1. Go to the [Releases](../../releases) page
2. Download `GrammarDrill-linux` from the latest release
3. Open a terminal in your download folder and make it executable:

```bash
chmod +x GrammarDrill-linux
./GrammarDrill-linux
```

> **Compatibility note:** The binary is built on Ubuntu. It will work on most Debian/Ubuntu-based distros. If it fails on your system, use Option B below.
Also, you might need to install
sudo apt install python3-tk
if tkinter is not bundled with Python on your system.

#### Option B — Run from source (most reliable, works on any distro)

**1. Install Python 3 and tkinter**

Tkinter is not always included with Python on Linux. Install it for your distro:

```bash
# Debian / Ubuntu / Mint
sudo apt install python3 python3-tk

# Fedora / RHEL
sudo dnf install python3 python3-tkinter

# Arch / Manjaro
sudo pacman -S python tk

# openSUSE
sudo zypper install python3 python3-tk
```

**2. Clone the repository**

```bash
git clone https://github.com/YOUR_USERNAME/grammar-drill.git
cd grammar-drill
```

**3. Run the app**

```bash
python3 main.py
```

**Optional: Create a desktop shortcut**

```bash
chmod +x install.sh
./install.sh
```

This creates a `.desktop` entry so you can launch Grammar Drill from your application menu.

---

## Adding Grammar Data

Grammar Drill reads `.txt` files from the `data/` folder. Each file represents a level (e.g. `N5.txt`, `N4.txt`).

**File format — one grammar point per line:**

```
grammar_name ;; https://bunpro.jp/grammar_points/your-point
```

**Example `data/N5.txt`:**

```
〜は〜です ;; https://bunpro.jp/grammar_points/は-だ-1
〜が好き ;; https://bunpro.jp/grammar_points/が好き
〜てください ;; https://bunpro.jp/grammar_points/てください
〜ている ;; https://bunpro.jp/grammar_points/ている-1
〜たことがある ;; https://bunpro.jp/grammar_points/たことがある
```

Drop as many `.txt` files into `data/` as you like. They all appear in the level selector dropdown.

---

## How It Works

### Weighted selection

Each grammar point starts with a weight of **100**. When you rate a card:

| Rating | Effect |
|--------|--------|
| HARD   | weight × 1.5 (max 500) |
| OK     | no change |
| EASY   | weight × 0.6 (min 10) |

Cards are drawn using weighted random selection, so a point with weight 300 is 30× more likely to appear than one at weight 10.

### Mastery tiers

| Weight | Tier |
|--------|------|
| ≤ 30 | Mastered |
| 31–80 | Comfortable |
| 81–150 | Learning |
| > 150 | Struggling |

### Session flow

1. Select a level file and how many points to show per round
2. Press **START** — cards are drawn weighted by difficulty
3. Write one sentence in the input box that uses the grammar points shown
4. Rate each card (HARD / OK / EASY)
5. Press **NEXT** — weights update, data saves, new cards are drawn

---

## Data & Privacy

All data is stored locally on your machine in the `user_data/` folder:

| File | Contents |
|------|----------|
| `user_data/progress.json` | Grammar weights |
| `user_data/study_log.json` | Full session history |
| `user_data/settings.json` | Theme preference |

Nothing is sent anywhere. The only outbound connection is when you click a **bunpro >>** link, which opens your browser.

---

## Building from Source

### Prerequisites

- Python 3.8+
- tkinter (included with Python on Windows/macOS; see Linux install above)
- PyInstaller (for building binaries only)

### Run directly

```bash
python main.py        # Windows
python3 main.py       # Linux / macOS
```

### Build a binary

**Windows (run in PowerShell or cmd):**

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name GrammarDrill main.py
# Output: dist/GrammarDrill.exe
```

**Linux:**

```bash
pip3 install pyinstaller
pyinstaller --onefile --name GrammarDrill main.py
chmod +x dist/GrammarDrill
# Output: dist/GrammarDrill
```

---

## Project Structure

```
grammar-drill/
├── main.py                  # Entire application (single file)
├── data/                    # Grammar level files (you create these)
│   └── N5.txt               # Example level
├── user_data/               # Auto-created on first run (gitignored)
│   ├── progress.json
│   ├── study_log.json
│   └── settings.json
├── .github/
│   └── workflows/
│       └── build.yml        # Auto-build EXE + Linux binary on release
├── install.sh               # Linux desktop shortcut installer
├── .gitignore
└── README.md
```

---

## Contributing

Issues and pull requests are welcome. A few areas that would be good to improve:

- macOS binary build in CI
- Import/export of progress data
- Support for multiple sentence inputs (one per card)
- Anki deck export

---

## License

MIT — do whatever you like with it.
