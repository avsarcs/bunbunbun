import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import random
import os
import glob
import webbrowser
from datetime import datetime, timedelta
from collections import Counter, defaultdict
import math

# ─────────────────────────────────────────────────────────────
# Themes
# ─────────────────────────────────────────────────────────────

THEMES = {
    "Wabi-sabi Dark": {
        "bg":         "#0F0F0F",
        "surface":    "#1A1A1A",
        "surface2":   "#222222",
        "input_bg":   "#161616",
        "text":       "#E8E4DF",
        "text_dim":   "#7A756F",
        "text_faint": "#4A4642",
        "border":     "#2A2826",
        "accent":     "#C4956A",
        "accent_dim": "#8B6A4A",
        "red":        "#BF616A",
        "red_bg":     "#2A1A1C",
        "green":      "#A3BE8C",
        "green_bg":   "#1A2A1C",
        "amber":      "#D4A959",
        "amber_bg":   "#2A2418",
        "blue":       "#81A1C1",
    },
    "Moonlight": {
        "bg":         "#1B1E2B",
        "surface":    "#222636",
        "surface2":   "#2A2E3F",
        "input_bg":   "#1E2130",
        "text":       "#C8D3F5",
        "text_dim":   "#7A88A8",
        "text_faint": "#444B6A",
        "border":     "#2F3451",
        "accent":     "#82AAFF",
        "accent_dim": "#5A7FCC",
        "red":        "#FF757F",
        "red_bg":     "#2D1F2A",
        "green":      "#C3E88D",
        "green_bg":   "#1F2D1A",
        "amber":      "#FFC777",
        "amber_bg":   "#2D2818",
        "blue":       "#82AAFF",
    },
    "Sakura Light": {
        "bg":         "#FAF6F2",
        "surface":    "#FFFFFF",
        "surface2":   "#F0EBE5",
        "input_bg":   "#FFFFFF",
        "text":       "#2C2420",
        "text_dim":   "#8C7E74",
        "text_faint": "#C4BAB0",
        "border":     "#E0D8D0",
        "accent":     "#D4728C",
        "accent_dim": "#B85A74",
        "red":        "#C44D58",
        "red_bg":     "#FCEAEC",
        "green":      "#5A9E6F",
        "green_bg":   "#E8F5EC",
        "amber":      "#C49A3C",
        "amber_bg":   "#FDF5E6",
        "blue":       "#5B8DB8",
    },
    "Forest": {
        "bg":         "#1A1F1A",
        "surface":    "#222822",
        "surface2":   "#2A322A",
        "input_bg":   "#1C221C",
        "text":       "#D4DED0",
        "text_dim":   "#7A8A74",
        "text_faint": "#4A5644",
        "border":     "#2E3A2C",
        "accent":     "#8CB878",
        "accent_dim": "#6A9458",
        "red":        "#C47070",
        "red_bg":     "#2A1C1C",
        "green":      "#8CB878",
        "green_bg":   "#1C2A1A",
        "amber":      "#C4AA58",
        "amber_bg":   "#2A2618",
        "blue":       "#78A8B8",
    },
    "Solarized Dark": {
        "bg":         "#002B36",
        "surface":    "#073642",
        "surface2":   "#0A3F4C",
        "input_bg":   "#003340",
        "text":       "#FDF6E3",
        "text_dim":   "#839496",
        "text_faint": "#586E75",
        "border":     "#0D4450",
        "accent":     "#B58900",
        "accent_dim": "#8C6A00",
        "red":        "#DC322F",
        "red_bg":     "#1A1012",
        "green":      "#859900",
        "green_bg":   "#0A1A00",
        "amber":      "#CB4B16",
        "amber_bg":   "#1A1208",
        "blue":       "#268BD2",
    },
    "High Contrast": {
        "bg":         "#000000",
        "surface":    "#111111",
        "surface2":   "#1A1A1A",
        "input_bg":   "#0A0A0A",
        "text":       "#FFFFFF",
        "text_dim":   "#AAAAAA",
        "text_faint": "#666666",
        "border":     "#333333",
        "accent":     "#FFD700",
        "accent_dim": "#CCA800",
        "red":        "#FF4444",
        "red_bg":     "#220000",
        "green":      "#44FF44",
        "green_bg":   "#002200",
        "amber":      "#FFAA00",
        "amber_bg":   "#221800",
        "blue":       "#44AAFF",
    },
}

C = dict(THEMES["Wabi-sabi Dark"])

JP_DISPLAY = ("Yu Gothic UI", "Hiragino Sans", "Noto Sans JP", "MS Gothic", "TkDefaultFont")
UI_FONT    = ("Segoe UI", "Helvetica Neue", "Helvetica", "TkDefaultFont")

def pick_font(families, size, weight="normal"):
    return (families[0], size, weight)

F = {
    "jp_large":   pick_font(JP_DISPLAY, 26, "bold"),
    "jp_medium":  pick_font(JP_DISPLAY, 18, "bold"),
    "jp_input":   pick_font(JP_DISPLAY, 13),
    "ui":         pick_font(UI_FONT, 10),
    "ui_bold":    pick_font(UI_FONT, 10, "bold"),
    "ui_small":   pick_font(UI_FONT, 9),
    "ui_tiny":    pick_font(UI_FONT, 8),
    "header":     pick_font(UI_FONT, 13, "bold"),
    "mono":       ("Consolas", 9),
}

DATA_FOLDER      = "data"
USER_DATA_FOLDER = "user_data"
PROGRESS_FILE    = os.path.join(USER_DATA_FOLDER, "progress.json")
LOG_FILE         = os.path.join(USER_DATA_FOLDER, "study_log.json")
SETTINGS_FILE    = os.path.join(USER_DATA_FOLDER, "settings.json")
DEFAULT_WEIGHT   = 100

def _lighten(hex_color, amount):
    try:
        r, g, b = int(hex_color[1:3], 16), int(hex_color[3:5], 16), int(hex_color[5:7], 16)
        r, g, b = min(r+amount, 255), min(g+amount, 255), min(b+amount, 255)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex_color

def _blend(hex1, hex2, ratio=0.5):
    try:
        r1, g1, b1 = int(hex1[1:3], 16), int(hex1[3:5], 16), int(hex1[5:7], 16)
        r2, g2, b2 = int(hex2[1:3], 16), int(hex2[3:5], 16), int(hex2[5:7], 16)
        r = int(r1 + (r2 - r1) * ratio)
        g = int(g1 + (g2 - g1) * ratio)
        b = int(b1 + (b2 - b1) * ratio)
        return f"#{r:02x}{g:02x}{b:02x}"
    except Exception:
        return hex1


# ─────────────────────────────────────────────────────────────
# Custom Widgets
# ─────────────────────────────────────────────────────────────

class FlatButton(tk.Canvas):
    def __init__(self, master, text, command, fg=None, bg=None,
                 hover_bg=None, btn_width=140, btn_height=36, font=None, **kw):
        fg = fg or C["text"]
        bg = bg or C["surface2"]
        font = font or F["ui_bold"]
        super().__init__(master, width=btn_width, height=btn_height,
                         bg=master["bg"], highlightthickness=0, **kw)
        self.command = command
        self.fg = fg
        self.bg_color = bg
        self.hover_bg = hover_bg or _lighten(bg, 15)
        self._text = text
        self._font = font
        self.btn_w = btn_width
        self.btn_h = btn_height
        self._disabled = False
        self._draw(bg)
        self.bind("<Enter>", lambda e: self._on_hover(True))
        self.bind("<Leave>", lambda e: self._on_hover(False))
        self.bind("<Button-1>", lambda e: self._click())

    def _draw(self, fill):
        self.delete("all")
        r = self.btn_h // 2
        self.create_oval(0, 0, r*2, r*2, fill=fill, outline="")
        self.create_oval(self.btn_w - r*2, 0, self.btn_w, r*2, fill=fill, outline="")
        self.create_rectangle(r, 0, self.btn_w - r, self.btn_h, fill=fill, outline="")
        self.create_text(self.btn_w // 2, self.btn_h // 2, text=self._text,
                         fill=self.fg if not self._disabled else C["text_faint"],
                         font=self._font)

    def _on_hover(self, entering):
        if self._disabled:
            return
        self._draw(self.hover_bg if entering else self.bg_color)
        self.config(cursor="hand2" if entering else "")

    def _click(self):
        if not self._disabled:
            self.command()

    def set_disabled(self, val):
        self._disabled = val
        self._draw(C["bg"] if val else self.bg_color)

    def update_text(self, text):
        self._text = text
        self._draw(self.bg_color)


class BarChart(tk.Canvas):
    def __init__(self, master, data, width=300, bar_height=18, spacing=4,
                 label_width=100, **kw):
        if not data:
            data = [("No data", 0, C["text_faint"])]
        max_val = max((d[1] for d in data), default=1)
        max_val = max(max_val, 1)
        total_h = len(data) * (bar_height + spacing) + 10
        super().__init__(master, width=width, height=total_h,
                         bg=master["bg"], highlightthickness=0, **kw)
        chart_w = width - label_width - 50
        for i, (label, val, color) in enumerate(data):
            y = i * (bar_height + spacing) + 5
            display_label = label if len(label) <= 18 else label[:16] + "..."
            self.create_text(label_width - 4, y + bar_height // 2, text=display_label,
                             anchor="e", fill=C["text_dim"], font=F["ui_tiny"])
            self.create_rectangle(label_width, y, label_width + chart_w,
                                  y + bar_height, fill=C["border"], outline="")
            if val > 0:
                bw = max(2, int(chart_w * val / max_val))
                self.create_rectangle(label_width, y, label_width + bw,
                                      y + bar_height, fill=color, outline="")
            self.create_text(label_width + chart_w + 6, y + bar_height // 2,
                             text=str(val), anchor="w", fill=C["text_dim"], font=F["ui_tiny"])


class HeatmapStrip(tk.Canvas):
    def __init__(self, master, day_counts, num_days=90, cell=10, gap=2, **kw):
        cols = math.ceil(num_days / 7)
        w = cols * (cell + gap) + 60
        h = 7 * (cell + gap) + 30
        super().__init__(master, width=w, height=h,
                         bg=master["bg"], highlightthickness=0, **kw)
        max_count = max(day_counts.values()) if day_counts else 1
        max_count = max(max_count, 1)
        today = datetime.now().date()
        day_names = ["M", "", "W", "", "F", "", "S"]
        for r, name in enumerate(day_names):
            y = r * (cell + gap) + 20
            self.create_text(8, y + cell // 2, text=name, anchor="w",
                             fill=C["text_faint"], font=F["ui_tiny"])
        last_month = None
        for d in range(num_days - 1, -1, -1):
            date = today - timedelta(days=d)
            col = (num_days - 1 - d) // 7
            row = date.weekday()
            x = col * (cell + gap) + 24
            y = row * (cell + gap) + 20
            count = day_counts.get(date.strftime("%Y-%m-%d"), 0)
            if count == 0:
                color = C["border"]
            else:
                intensity = min(count / max_count, 1.0)
                if intensity < 0.25:
                    color = _blend(C["border"], C["accent"], 0.3)
                elif intensity < 0.5:
                    color = _blend(C["border"], C["accent"], 0.55)
                elif intensity < 0.75:
                    color = _blend(C["border"], C["accent"], 0.8)
                else:
                    color = C["accent"]
            self.create_rectangle(x, y, x + cell, y + cell, fill=color, outline="")
            month_str = date.strftime("%b")
            if month_str != last_month and row == 0:
                self.create_text(x, 8, text=month_str, anchor="w",
                                 fill=C["text_faint"], font=F["ui_tiny"])
                last_month = month_str


class GrammarCard(tk.Frame):
    def __init__(self, master, grammar, index, total, on_rated, app):
        super().__init__(master, bg=C["surface"], highlightthickness=1,
                         highlightbackground=C["border"])
        self.grammar = grammar
        self.on_rated = on_rated
        self.app = app
        self.rated = False

        header = tk.Frame(self, bg=C["surface"])
        header.pack(fill=tk.X, padx=16, pady=(14, 6))
        badge = tk.Label(header, text=f"{index}/{total}", bg=C["accent_dim"],
                         fg=C["bg"], font=F["ui_tiny"], padx=6, pady=1)
        badge.pack(side=tk.LEFT, padx=(0, 10))
        name_lbl = tk.Label(header, text=grammar["name"], bg=C["surface"],
                            fg=C["text"], font=F["jp_medium"], anchor="w")
        name_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)
        link = tk.Label(header, text="bunpro >>", bg=C["surface"],
                        fg=C["accent"], font=F["ui_small"], cursor="hand2")
        link.pack(side=tk.RIGHT)
        link.bind("<Button-1>", lambda e: self._open_ref())
        link.bind("<Enter>", lambda e: link.config(fg=C["text"]))
        link.bind("<Leave>", lambda e: link.config(fg=C["accent"]))

        w = app.weights.get(grammar["name"], DEFAULT_WEIGHT)
        mastery = max(0, min(100, int((1 - (w - 10) / 490) * 100)))
        bar_frame = tk.Frame(self, bg=C["surface"])
        bar_frame.pack(fill=tk.X, padx=16, pady=(0, 8))
        bar_bg = tk.Frame(bar_frame, bg=C["border"], height=3)
        bar_bg.pack(fill=tk.X)
        bar_fill = tk.Frame(bar_bg, bg=C["accent"] if mastery < 80 else C["green"],
                            height=3, width=max(1, int(mastery * 3)))
        bar_fill.place(x=0, y=0, relheight=1)

        rate_frame = tk.Frame(self, bg=C["surface"])
        rate_frame.pack(fill=tk.X, padx=16, pady=(0, 12))
        self.status_lbl = tk.Label(rate_frame, text="Rate this point:",
                                    bg=C["surface"], fg=C["text_dim"], font=F["ui_small"])
        self.status_lbl.pack(side=tk.LEFT)
        btn_w, btn_h = 80, 28
        self.btn_easy = FlatButton(rate_frame, "EASY", lambda: self._rate("Easy"),
                                    fg=C["green"], bg=C["green_bg"], btn_width=btn_w, btn_height=btn_h, font=F["ui_small"])
        self.btn_easy.pack(side=tk.RIGHT, padx=(4, 0))
        self.btn_norm = FlatButton(rate_frame, "OK", lambda: self._rate("Normal"),
                                    fg=C["text_dim"], bg=C["surface2"], btn_width=btn_w, btn_height=btn_h, font=F["ui_small"])
        self.btn_norm.pack(side=tk.RIGHT, padx=(4, 0))
        self.btn_hard = FlatButton(rate_frame, "HARD", lambda: self._rate("Hard"),
                                    fg=C["red"], bg=C["red_bg"], btn_width=btn_w, btn_height=btn_h, font=F["ui_small"])
        self.btn_hard.pack(side=tk.RIGHT, padx=(4, 0))

    def _open_ref(self):
        url = self.grammar.get("url", "")
        if url.startswith("http"):
            webbrowser.open(url)

    def _rate(self, difficulty):
        if self.rated:
            return
        self.rated = True
        for b in (self.btn_hard, self.btn_norm, self.btn_easy):
            b.set_disabled(True)
        labels = {"Hard": ("HARD x", C["red"]), "Normal": ("OK -", C["text_dim"]), "Easy": ("EASY +", C["green"])}
        txt, color = labels[difficulty]
        self.status_lbl.config(text=f"Rated: {txt}", fg=color)
        self.configure(highlightbackground=C["text_faint"])
        self.on_rated(self.grammar, difficulty)

    def is_rated(self):
        return self.rated


# ─────────────────────────────────────────────────────────────
# Stats Window
# ─────────────────────────────────────────────────────────────

class StatsWindow:
    def __init__(self, parent_root, history, weights):
        self.history = history
        self.weights = weights
        self.top = tk.Toplevel(parent_root)
        self.top.title("Stats")
        self.top.geometry("640x780")
        self.top.configure(bg=C["bg"])
        self.top.minsize(540, 600)
        self._build()

    def _parse_date(self, date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M")
        except Exception:
            return None

    def _section(self, parent, text):
        tk.Label(parent, text=text, bg=C["bg"], fg=C["text_faint"],
                 font=F["ui_tiny"]).pack(anchor="w", padx=20, pady=(14, 4))

    def _stat_row(self, parent, label, value, color=None):
        row = tk.Frame(parent, bg=C["surface"])
        row.pack(fill=tk.X, pady=1)
        tk.Label(row, text=label, bg=C["surface"], fg=C["text_dim"],
                 font=F["ui_small"]).pack(side=tk.LEFT)
        tk.Label(row, text=str(value), bg=C["surface"], fg=color or C["text"],
                 font=F["ui_bold"]).pack(side=tk.RIGHT)

    def _calc_streaks(self, parsed):
        if not parsed:
            return 0, 0
        dates = sorted(set(dt.strftime("%Y-%m-%d") for dt, _ in parsed))
        today = datetime.now().strftime("%Y-%m-%d")
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        date_set = set(dates)
        streak = 0
        check = today
        if check in date_set or yesterday in date_set:
            if check not in date_set:
                check = yesterday
            while check in date_set:
                streak += 1
                check = (datetime.strptime(check, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        max_streak = 1 if dates else 0
        current_run = 1
        for i in range(1, len(dates)):
            d1 = datetime.strptime(dates[i-1], "%Y-%m-%d")
            d2 = datetime.strptime(dates[i], "%Y-%m-%d")
            if (d2 - d1).days == 1:
                current_run += 1
                max_streak = max(max_streak, current_run)
            else:
                current_run = 1
        return streak, max_streak

    def _diff_bar(self, parent, easy_n, ok_n, hard_n):
        """Stacked proportional difficulty bar."""
        total = easy_n + ok_n + hard_n
        if total == 0:
            return
        container = tk.Frame(parent, bg=C["border"], height=8)
        container.pack(fill=tk.X, pady=(6, 4))
        container.update_idletasks()
        # Use a canvas for precise proportional drawing
        bar = tk.Canvas(container, height=8, bg=C["border"], highlightthickness=0)
        bar.pack(fill=tk.X)
        bar.update_idletasks()
        w = max(bar.winfo_width(), 200)
        x = 0
        for count, color in [(easy_n, C["green"]), (ok_n, C["amber"]), (hard_n, C["red"])]:
            if count > 0:
                seg_w = max(2, int(w * count / total))
                bar.create_rectangle(x, 0, x + seg_w, 8, fill=color, outline="")
                x += seg_w

    def _build(self):
        canvas = tk.Canvas(self.top, bg=C["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.top, orient="vertical", command=canvas.yview,
                                  bg=C["surface"], troughcolor=C["bg"])
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        frame = tk.Frame(canvas, bg=C["bg"])
        cw = canvas.create_window((0, 0), window=frame, anchor="nw")
        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        # Title
        tk.Label(frame, text="統計", bg=C["bg"], fg=C["accent"],
                 font=pick_font(JP_DISPLAY, 22, "bold")).pack(pady=(20, 2))
        tk.Label(frame, text="Statistics Dashboard", bg=C["bg"], fg=C["text_dim"],
                 font=F["ui"]).pack(pady=(0, 10))

        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")

        parsed = []
        for item in self.history:
            dt = self._parse_date(item.get("date", ""))
            if dt:
                parsed.append((dt, item))

        # ── OVERVIEW CARDS ────────────────────────────────
        self._section(frame, "OVERVIEW")
        overview = tk.Frame(frame, bg=C["bg"])
        overview.pack(fill=tk.X, padx=20, pady=(0, 12))

        total_reviews = len(parsed)
        total_days_active = len(set(dt.strftime("%Y-%m-%d") for dt, _ in parsed))
        unique_grammar = len(set(it["grammar"] for _, it in parsed))
        total_sentences = len(set(it.get("sentence", "") for _, it in parsed))
        streak, max_streak = self._calc_streaks(parsed)

        cards_data = [
            ("Total Reviews", str(total_reviews), C["accent"]),
            ("Days Active", str(total_days_active), C["blue"]),
            ("Grammar Studied", str(unique_grammar), C["green"]),
            ("Unique Sentences", str(total_sentences), C["amber"]),
            ("Current Streak", f"{streak}d", C["accent"]),
            ("Best Streak", f"{max_streak}d", C["green"]),
        ]
        row_frame = None
        for i, (label, value, color) in enumerate(cards_data):
            if i % 3 == 0:
                row_frame = tk.Frame(overview, bg=C["bg"])
                row_frame.pack(fill=tk.X, pady=(0, 6))
            card = tk.Frame(row_frame, bg=C["surface"], padx=14, pady=10)
            card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0 if i % 3 == 0 else 4, 0))
            tk.Label(card, text=value, bg=C["surface"], fg=color,
                     font=pick_font(UI_FONT, 20, "bold")).pack(anchor="w")
            tk.Label(card, text=label, bg=C["surface"], fg=C["text_dim"],
                     font=F["ui_tiny"]).pack(anchor="w")

        # ── ACTIVITY HEATMAP ──────────────────────────────
        self._section(frame, "ACTIVITY  (last 90 days)")
        day_counts = Counter(dt.strftime("%Y-%m-%d") for dt, _ in parsed)
        heatmap = HeatmapStrip(frame, day_counts, num_days=90)
        heatmap.pack(padx=20, anchor="w", pady=(0, 4))
        # Legend
        leg = tk.Frame(frame, bg=C["bg"])
        leg.pack(padx=24, anchor="w", pady=(0, 12))
        tk.Label(leg, text="Less", bg=C["bg"], fg=C["text_faint"], font=F["ui_tiny"]).pack(side=tk.LEFT, padx=(0, 4))
        for ratio in [0, 0.3, 0.55, 0.8, 1.0]:
            clr = C["border"] if ratio == 0 else _blend(C["border"], C["accent"], ratio)
            tk.Canvas(leg, width=10, height=10, bg=clr, highlightthickness=0).pack(side=tk.LEFT, padx=1)
        tk.Label(leg, text="More", bg=C["bg"], fg=C["text_faint"], font=F["ui_tiny"]).pack(side=tk.LEFT, padx=(4, 0))

        # ── PERIOD BREAKDOWN ──────────────────────────────
        self._section(frame, "PERIOD BREAKDOWN")
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        year_ago = now - timedelta(days=365)

        periods = [
            ("Today",      [(dt, it) for dt, it in parsed if dt.strftime("%Y-%m-%d") == today_str]),
            ("This Week",  [(dt, it) for dt, it in parsed if dt >= week_ago]),
            ("This Month", [(dt, it) for dt, it in parsed if dt >= month_ago]),
            ("This Year",  [(dt, it) for dt, it in parsed if dt >= year_ago]),
        ]
        for pname, pitems in periods:
            pcard = tk.Frame(frame, bg=C["surface"], padx=14, pady=10)
            pcard.pack(fill=tk.X, padx=20, pady=(0, 4))
            hdr = tk.Frame(pcard, bg=C["surface"])
            hdr.pack(fill=tk.X)
            tk.Label(hdr, text=pname, bg=C["surface"], fg=C["text"], font=F["ui_bold"]).pack(side=tk.LEFT)
            tk.Label(hdr, text=f"{len(pitems)} reviews", bg=C["surface"], fg=C["text_dim"], font=F["ui_small"]).pack(side=tk.RIGHT)
            if pitems:
                diffs = Counter(it["difficulty"] for _, it in pitems)
                easy_n, ok_n, hard_n = diffs.get("Easy", 0), diffs.get("Normal", 0), diffs.get("Hard", 0)
                self._diff_bar(pcard, easy_n, ok_n, hard_n)
                detail = tk.Frame(pcard, bg=C["surface"])
                detail.pack(fill=tk.X)
                for cnt, clr, lbl in [(easy_n, C["green"], "Easy"), (ok_n, C["text_dim"], "OK"), (hard_n, C["red"], "Hard")]:
                    tk.Label(detail, text=f"{lbl}: {cnt}", bg=C["surface"], fg=clr, font=F["ui_tiny"]).pack(side=tk.LEFT, padx=(0, 12))
                unique_g = len(set(it["grammar"] for _, it in pitems))
                tk.Label(detail, text=f"Points: {unique_g}", bg=C["surface"], fg=C["text_faint"], font=F["ui_tiny"]).pack(side=tk.RIGHT)

        # ── DIFFICULTY DISTRIBUTION ───────────────────────
        self._section(frame, "DIFFICULTY DISTRIBUTION  (all time)")
        all_diffs = Counter(it["difficulty"] for _, it in parsed)
        diff_data = [
            ("Easy", all_diffs.get("Easy", 0), C["green"]),
            ("OK", all_diffs.get("Normal", 0), C["amber"]),
            ("Hard", all_diffs.get("Hard", 0), C["red"]),
        ]
        BarChart(frame, diff_data, width=400, bar_height=20).pack(padx=20, anchor="w", pady=(0, 12))

        # ── MOST STRUGGLED ────────────────────────────────
        self._section(frame, "MOST STRUGGLED  (highest weight)")
        struggled = sorted(self.weights.items(), key=lambda x: x[1], reverse=True)[:10]
        if struggled:
            sd = [(n, int(w), C["red"] if w > 200 else C["amber"] if w > 100 else C["text_dim"]) for n, w in struggled]
            BarChart(frame, sd, width=480, bar_height=18, label_width=120).pack(padx=20, anchor="w", pady=(0, 12))

        # ── MOST MASTERED ─────────────────────────────────
        self._section(frame, "MOST MASTERED  (lowest weight)")
        mastered = sorted(self.weights.items(), key=lambda x: x[1])[:10]
        if mastered:
            md = [(n, int(w), C["green"] if w < 50 else C["blue"] if w < 100 else C["text_dim"]) for n, w in mastered]
            BarChart(frame, md, width=480, bar_height=18, label_width=120).pack(padx=20, anchor="w", pady=(0, 12))

        # ── MOST REVIEWED ─────────────────────────────────
        self._section(frame, "MOST REVIEWED")
        review_counts = Counter(it["grammar"] for _, it in parsed)
        top_rev = review_counts.most_common(10)
        if top_rev:
            rd = [(n, c, C["accent"]) for n, c in top_rev]
            BarChart(frame, rd, width=480, bar_height=18, label_width=120).pack(padx=20, anchor="w", pady=(0, 12))

        # ── LEAST REVIEWED ────────────────────────────────
        self._section(frame, "LEAST REVIEWED  (blind spots)")
        if review_counts:
            bottom_rev = review_counts.most_common()[-10:]
            bottom_rev.reverse()
            if bottom_rev:
                brd = [(n, c, C["red"] if c <= 2 else C["amber"]) for n, c in bottom_rev]
                BarChart(frame, brd, width=480, bar_height=18, label_width=120).pack(padx=20, anchor="w", pady=(0, 12))

        # ── DAILY VOLUME (last 30 days) ───────────────────
        self._section(frame, "DAILY VOLUME  (last 30 days)")
        last_30 = []
        for d in range(29, -1, -1):
            date = (now - timedelta(days=d)).strftime("%Y-%m-%d")
            count = day_counts.get(date, 0)
            last_30.append((date[-5:], count, C["accent"] if count > 0 else C["border"]))
        BarChart(frame, last_30, width=520, bar_height=10, spacing=2, label_width=50).pack(padx=20, anchor="w", pady=(0, 12))

        # ── WEEKDAY PATTERN ───────────────────────────────
        self._section(frame, "WEEKDAY PATTERN")
        weekday_counts = Counter()
        for dt, _ in parsed:
            weekday_counts[dt.strftime("%A")] += 1
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        wd_data = [(d[:3], weekday_counts.get(d, 0), C["accent"]) for d in day_order]
        BarChart(frame, wd_data, width=400, bar_height=16, spacing=3, label_width=50).pack(padx=20, anchor="w", pady=(0, 12))

        # ── HOUR OF DAY PATTERN ───────────────────────────
        self._section(frame, "TIME OF DAY PATTERN")
        hour_counts = Counter()
        for dt, _ in parsed:
            hour_counts[dt.hour] += 1
        hour_data = []
        for h in range(24):
            label = f"{h:02d}:00"
            hour_data.append((label, hour_counts.get(h, 0), C["blue"] if hour_counts.get(h, 0) > 0 else C["border"]))
        BarChart(frame, hour_data, width=460, bar_height=8, spacing=1, label_width=50).pack(padx=20, anchor="w", pady=(0, 12))

        # ── WRITING STATS ─────────────────────────────────
        self._section(frame, "WRITING STATS")
        wcard = tk.Frame(frame, bg=C["surface"], padx=14, pady=12)
        wcard.pack(fill=tk.X, padx=20, pady=(0, 12))
        sentences = [it.get("sentence", "") for _, it in parsed]
        if sentences:
            lengths = [len(s) for s in sentences if s]
            avg_len = sum(lengths) / len(lengths) if lengths else 0
            total_chars = sum(lengths)
            self._stat_row(wcard, "Total characters written", f"{total_chars:,}")
            self._stat_row(wcard, "Average sentence length", f"{avg_len:.1f} chars")
            self._stat_row(wcard, "Longest sentence", f"{max(lengths) if lengths else 0} chars")
            self._stat_row(wcard, "Shortest sentence", f"{min(lengths) if lengths else 0} chars")
            self._stat_row(wcard, "Unique sentences", str(len(set(s for s in sentences if s))))
        else:
            tk.Label(wcard, text="No sentences yet", bg=C["surface"], fg=C["text_faint"], font=F["ui_small"]).pack()

        # ── MASTERY OVERVIEW ──────────────────────────────
        if self.weights:
            self._section(frame, "MASTERY OVERVIEW")
            mcard = tk.Frame(frame, bg=C["surface"], padx=14, pady=12)
            mcard.pack(fill=tk.X, padx=20, pady=(0, 12))
            wvals = list(self.weights.values())
            mastered_n = sum(1 for w in wvals if w <= 30)
            comfortable_n = sum(1 for w in wvals if 30 < w <= 80)
            learning_n = sum(1 for w in wvals if 80 < w <= 150)
            struggling_n = sum(1 for w in wvals if w > 150)
            total_g = len(wvals)
            for label, cnt, clr in [("Mastered (w <= 30)", mastered_n, C["green"]),
                                     ("Comfortable (w <= 80)", comfortable_n, C["blue"]),
                                     ("Learning (w <= 150)", learning_n, C["amber"]),
                                     ("Struggling (w > 150)", struggling_n, C["red"])]:
                pct = f"{cnt}/{total_g}  ({100*cnt/total_g:.0f}%)" if total_g else "0"
                self._stat_row(mcard, label, pct, clr)
            # Stacked bar
            bar_outer = tk.Frame(mcard, bg=C["border"], height=10)
            bar_outer.pack(fill=tk.X, pady=(8, 0))
            inner = tk.Frame(bar_outer, bg=C["border"])
            inner.pack(fill=tk.BOTH, expand=True)
            if total_g > 0:
                for cnt, clr in [(mastered_n, C["green"]), (comfortable_n, C["blue"]),
                                  (learning_n, C["amber"]), (struggling_n, C["red"])]:
                    if cnt > 0:
                        tk.Frame(inner, bg=clr, height=10,
                                 width=max(2, int(400 * cnt / total_g))).pack(side=tk.LEFT, fill=tk.Y)

        # ── RECENT HARD POINTS ────────────────────────────
        self._section(frame, "RECENT HARD-RATED POINTS  (last 50 reviews)")
        recent_hard = [it["grammar"] for _, it in parsed[:50] if it.get("difficulty") == "Hard"]
        if recent_hard:
            hc = Counter(recent_hard).most_common(8)
            hd = [(n, c, C["red"]) for n, c in hc]
            BarChart(frame, hd, width=400, bar_height=16, label_width=120).pack(padx=20, anchor="w", pady=(0, 12))
        else:
            tk.Label(frame, text="No hard ratings recently!", bg=C["bg"], fg=C["green"], font=F["ui_small"]).pack(padx=20, anchor="w", pady=(0, 12))

        # Bottom pad
        tk.Frame(frame, bg=C["bg"], height=24).pack()


# ─────────────────────────────────────────────────────────────
# History Window (searchable)
# ─────────────────────────────────────────────────────────────

class HistoryWindow:
    def __init__(self, parent_root, history):
        self.history = history
        self.filtered = list(history)
        self.top = tk.Toplevel(parent_root)
        self.top.title("History")
        self.top.geometry("580x660")
        self.top.configure(bg=C["bg"])
        self.top.minsize(420, 400)
        self._build()

    def _build(self):
        tk.Label(self.top, text="履歴", bg=C["bg"], fg=C["accent"],
                 font=pick_font(JP_DISPLAY, 18, "bold")).pack(pady=(16, 2))
        tk.Label(self.top, text="Study History", bg=C["bg"], fg=C["text_dim"],
                 font=F["ui"]).pack(pady=(0, 8))

        # Search bar
        search_frame = tk.Frame(self.top, bg=C["bg"])
        search_frame.pack(fill=tk.X, padx=16, pady=(0, 4))
        tk.Label(search_frame, text="SEARCH", bg=C["bg"], fg=C["text_faint"],
                 font=F["ui_tiny"]).pack(side=tk.LEFT, padx=(0, 8))
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *a: self._apply_filter())
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var,
                                      bg=C["input_bg"], fg=C["text"], font=F["ui"],
                                      insertbackground=C["accent"], relief=tk.FLAT,
                                      highlightthickness=1, highlightbackground=C["border"],
                                      highlightcolor=C["accent"])
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4)

        # Difficulty filter
        filter_frame = tk.Frame(self.top, bg=C["bg"])
        filter_frame.pack(fill=tk.X, padx=16, pady=(4, 8))
        tk.Label(filter_frame, text="FILTER", bg=C["bg"], fg=C["text_faint"],
                 font=F["ui_tiny"]).pack(side=tk.LEFT, padx=(0, 8))
        self.filter_var = tk.StringVar(value="All")
        for val, label, color in [("All", "All", C["text_dim"]), ("Hard", "Hard", C["red"]),
                                   ("Normal", "OK", C["text_dim"]), ("Easy", "Easy", C["green"])]:
            rb = tk.Radiobutton(filter_frame, text=label, variable=self.filter_var,
                                value=val, bg=C["bg"], fg=color, selectcolor=C["surface"],
                                activebackground=C["bg"], activeforeground=color,
                                font=F["ui_small"], command=self._apply_filter,
                                indicatoron=0, padx=10, pady=3, bd=0,
                                highlightthickness=0, relief=tk.FLAT)
            rb.pack(side=tk.LEFT, padx=(0, 4))

        # Results count
        self.results_lbl = tk.Label(self.top, text="", bg=C["bg"], fg=C["text_faint"],
                                     font=F["ui_tiny"])
        self.results_lbl.pack(anchor="w", padx=16, pady=(0, 4))

        # Results text area
        self.txt = scrolledtext.ScrolledText(self.top, bg=C["surface"], fg=C["text"],
                                              font=F["mono"], relief=tk.FLAT,
                                              padx=14, pady=14, wrap=tk.WORD)
        self.txt.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 16))
        self.txt.tag_config("meta", foreground=C["text_faint"])
        self.txt.tag_config("grammar", foreground=C["accent"], font=pick_font(UI_FONT, 10, "bold"))
        self.txt.tag_config("sentence", foreground=C["text"])
        self.txt.tag_config("hard", foreground=C["red"])
        self.txt.tag_config("easy", foreground=C["green"])
        self.txt.tag_config("normal", foreground=C["text_dim"])

        self._apply_filter()
        self.search_entry.focus_set()

    def _apply_filter(self):
        query = self.search_var.get().strip().lower()
        diff_filter = self.filter_var.get()
        self.filtered = []
        for item in self.history:
            if diff_filter != "All" and item.get("difficulty", "Normal") != diff_filter:
                continue
            if query:
                searchable = f"{item.get('date', '')} {item.get('grammar', '')} {item.get('sentence', '')} {item.get('difficulty', '')}".lower()
                if query not in searchable:
                    continue
            self.filtered.append(item)
        self._render()

    def _render(self):
        self.txt.config(state=tk.NORMAL)
        self.txt.delete("1.0", tk.END)
        self.results_lbl.config(text=f"{len(self.filtered)} of {len(self.history)} entries")
        if not self.filtered:
            self.txt.insert(tk.END, "No matching entries found.", "meta")
        else:
            for item in self.filtered[:500]:
                diff = item.get("difficulty", "Normal")
                diff_tag = diff.lower()
                self.txt.insert(tk.END, f"{item.get('date', '?')}  ", "meta")
                self.txt.insert(tk.END, f"[{diff}]\n", diff_tag)
                self.txt.insert(tk.END, f"  {item.get('grammar', '?')}\n", "grammar")
                self.txt.insert(tk.END, f"  {item.get('sentence', '')}\n\n", "sentence")
        self.txt.config(state=tk.DISABLED)


# ─────────────────────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────────────────────

class GrammarDrillApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Grammar Drill")
        self.root.geometry("680x780")
        self.root.configure(bg=C["bg"])
        self.root.minsize(500, 600)
        self.grammar_list = []
        self.current_cards = []
        self.card_widgets = []
        self.weights = {}
        self.history = []
        self.card_count = 1
        self.current_theme = "Wabi-sabi Dark"
        self._ensure_dirs()
        self._load_settings()
        self._load_data()
        self.is_first_time = not os.path.exists(PROGRESS_FILE)
        if self.is_first_time:
            self._show_onboarding()
        else:
            self._build_main_ui()

    # ── Onboarding ────────────────────────────────────────

    def _show_onboarding(self):
        self.onboard_frame = tk.Frame(self.root, bg=C["bg"])
        self.onboard_frame.pack(fill=tk.BOTH, expand=True)
        center = tk.Frame(self.onboard_frame, bg=C["bg"])
        center.place(relx=0.5, rely=0.5, anchor="center")
        tk.Label(center, text="Grammar Drill", bg=C["bg"], fg=C["accent"],
                 font=pick_font(JP_DISPLAY, 36, "bold")).pack(pady=(0, 4))
        tk.Label(center, text="Spaced-repetition grammar practice", bg=C["bg"], fg=C["text_dim"],
                 font=pick_font(UI_FONT, 12)).pack(pady=(0, 30))
        card = tk.Frame(center, bg=C["surface"], padx=32, pady=24)
        card.pack(padx=40)
        instructions = [
            ("1. Load a level", "Place .txt files in the 'data/' folder.\nEach line: grammar_name ;; reference_url"),
            ("2. Drill", "Grammar points appear as cards, weighted\nby difficulty. Harder ones show up more."),
            ("3. Write & Rate", "Write a sentence using the grammar, then\nrate each point as HARD, OK, or EASY."),
            ("4. Track progress", "Your ratings adjust future card weights.\nReview history and stats anytime."),
        ]
        for i, (title, desc) in enumerate(instructions):
            row = tk.Frame(card, bg=C["surface"])
            row.pack(fill=tk.X, pady=(0 if i == 0 else 12, 0), anchor="w")
            tk.Label(row, text=title, bg=C["surface"], fg=C["accent"],
                     font=F["ui_bold"], anchor="w").pack(anchor="w")
            tk.Label(row, text=desc, bg=C["surface"], fg=C["text_dim"],
                     font=F["ui_small"], anchor="w", justify=tk.LEFT).pack(anchor="w", padx=(16, 0))
        tk.Label(center, text="Pick a theme to start:", bg=C["bg"],
                 fg=C["text_dim"], font=F["ui_small"]).pack(pady=(24, 8))
        theme_row = tk.Frame(center, bg=C["bg"])
        theme_row.pack()
        for tname, tcolors in THEMES.items():
            swatch = tk.Frame(theme_row, bg=C["bg"], padx=4, pady=4)
            swatch.pack(side=tk.LEFT, padx=4)
            dot_frame = tk.Frame(swatch, bg=C["bg"])
            dot_frame.pack()
            for clr in [tcolors["bg"], tcolors["accent"], tcolors["surface"]]:
                tk.Canvas(dot_frame, width=12, height=12, bg=clr,
                          highlightthickness=1, highlightbackground=C["border"]).pack(side=tk.LEFT, padx=1)
            lbl = tk.Label(swatch, text=tname.split()[0], bg=C["bg"],
                           fg=C["text_dim"], font=F["ui_tiny"], cursor="hand2")
            lbl.pack(pady=(2, 0))
            lbl.bind("<Button-1>", lambda e, t=tname: self._preview_theme_onboard(t))
            lbl.bind("<Enter>", lambda e, l=lbl: l.config(fg=C["accent"]))
            lbl.bind("<Leave>", lambda e, l=lbl: l.config(fg=C["text_dim"]))
        self.btn_begin = FlatButton(center, "Let's Begin", self._finish_onboarding,
                                     fg=C["bg"], bg=C["accent"], hover_bg=C["accent_dim"],
                                     btn_width=220, btn_height=44, font=F["ui_bold"])
        self.btn_begin.pack(pady=(24, 0))

    def _preview_theme_onboard(self, theme_name):
        self._apply_theme(theme_name)
        self.onboard_frame.destroy()
        self._show_onboarding()

    def _finish_onboarding(self):
        self._save_data()
        self._save_settings()
        self.onboard_frame.destroy()
        self._build_main_ui()

    # ── Theme Management ──────────────────────────────────

    def _apply_theme(self, theme_name):
        if theme_name not in THEMES:
            return
        self.current_theme = theme_name
        C.update(THEMES[theme_name])

    def _load_settings(self):
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self._apply_theme(settings.get("theme", "Wabi-sabi Dark"))
        except Exception:
            pass

    def _save_settings(self):
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump({"theme": self.current_theme}, f, indent=2)

    def _show_theme_picker(self):
        top = tk.Toplevel(self.root)
        top.title("Theme")
        top.geometry("320x420")
        top.configure(bg=C["bg"])
        top.resizable(False, False)
        tk.Label(top, text="Themes", bg=C["bg"], fg=C["accent"],
                 font=pick_font(JP_DISPLAY, 14, "bold")).pack(pady=(16, 12))
        for tname, tcolors in THEMES.items():
            row = tk.Frame(top, bg=C["surface"] if tname == self.current_theme else C["bg"],
                           padx=12, pady=8, cursor="hand2")
            row.pack(fill=tk.X, padx=16, pady=2)
            sf = tk.Frame(row, bg=row["bg"])
            sf.pack(side=tk.LEFT, padx=(0, 12))
            for clr in [tcolors["bg"], tcolors["surface"], tcolors["accent"], tcolors["text"]]:
                tk.Canvas(sf, width=16, height=16, bg=clr, highlightthickness=1,
                          highlightbackground=tcolors["border"]).pack(side=tk.LEFT, padx=1)
            fg = C["accent"] if tname == self.current_theme else C["text"]
            lbl = tk.Label(row, text=tname, bg=row["bg"], fg=fg, font=F["ui_bold"])
            lbl.pack(side=tk.LEFT)
            if tname == self.current_theme:
                tk.Label(row, text="*", bg=row["bg"], fg=C["accent"], font=F["ui_bold"]).pack(side=tk.RIGHT)
            for widget in [row, lbl, sf]:
                widget.bind("<Button-1>", lambda e, t=tname, w=top: self._select_theme(t, w))

    def _select_theme(self, theme_name, dialog):
        self._apply_theme(theme_name)
        self._save_settings()
        dialog.destroy()
        self._rebuild_ui()

    def _rebuild_ui(self):
        for w in self.root.winfo_children():
            w.destroy()
        self.root.configure(bg=C["bg"])
        self._build_main_ui()

    # ── Data ──────────────────────────────────────────────

    def _ensure_dirs(self):
        os.makedirs(USER_DATA_FOLDER, exist_ok=True)
        os.makedirs(DATA_FOLDER, exist_ok=True)

    def _load_data(self):
        try:
            if os.path.exists(PROGRESS_FILE):
                with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                    self.weights = json.load(f)
        except Exception:
            self.weights = {}
        try:
            if os.path.exists(LOG_FILE):
                with open(LOG_FILE, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception:
            self.history = []

    def _save_data(self):
        with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.weights, f, indent=2)
        with open(LOG_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    # ── UI ────────────────────────────────────────────────

    def _build_main_ui(self):
        # Top bar
        topbar = tk.Frame(self.root, bg=C["surface"], height=52)
        topbar.pack(fill=tk.X)
        topbar.pack_propagate(False)
        tk.Label(topbar, text="Grammar Drill", bg=C["surface"], fg=C["accent"],
                 font=pick_font(JP_DISPLAY, 14, "bold")).pack(side=tk.LEFT, padx=16)
        self.btn_history = FlatButton(topbar, "History", self._show_history,
                                       fg=C["text_dim"], bg=C["surface"], btn_width=80, btn_height=30)
        self.btn_history.pack(side=tk.RIGHT, padx=(4, 12), pady=11)
        self.btn_stats = FlatButton(topbar, "Stats", self._show_stats,
                                     fg=C["text_dim"], bg=C["surface"], btn_width=70, btn_height=30)
        self.btn_stats.pack(side=tk.RIGHT, padx=(4, 0), pady=11)
        self.btn_theme = FlatButton(topbar, "Theme", self._show_theme_picker,
                                     fg=C["text_dim"], bg=C["surface"], btn_width=70, btn_height=30)
        self.btn_theme.pack(side=tk.RIGHT, padx=(4, 0), pady=11)

        # Bottom bar (pack BEFORE middle so always visible)
        bottom = tk.Frame(self.root, bg=C["surface"])
        bottom.pack(fill=tk.X, side=tk.BOTTOM)
        tk.Frame(bottom, bg=C["border"], height=1).pack(fill=tk.X)
        input_area = tk.Frame(bottom, bg=C["surface"])
        input_area.pack(fill=tk.X, padx=16, pady=12)
        tk.Label(input_area, text="YOUR SENTENCE", bg=C["surface"], fg=C["text_dim"],
                 font=F["ui_tiny"]).pack(anchor="w", pady=(0, 4))
        input_row = tk.Frame(input_area, bg=C["surface"])
        input_row.pack(fill=tk.X)
        self.btn_next = FlatButton(input_row, "NEXT >>", self._next_round,
                                    fg=C["bg"], bg=C["accent"], hover_bg=C["accent_dim"],
                                    btn_width=90, btn_height=40)
        self.btn_next.pack(side=tk.RIGHT, padx=(10, 0))
        self.btn_next.set_disabled(True)
        self.txt_input = tk.Text(input_row, height=3, bg=C["input_bg"], fg=C["text"],
                                  insertbackground=C["accent"], relief=tk.FLAT,
                                  font=F["jp_input"], padx=12, pady=10,
                                  wrap=tk.WORD, state=tk.DISABLED)
        self.txt_input.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Control strip
        ctrl = tk.Frame(self.root, bg=C["bg"])
        ctrl.pack(fill=tk.X, padx=20, pady=(16, 0))
        tk.Label(ctrl, text="LEVEL", bg=C["bg"], fg=C["text_dim"], font=F["ui_tiny"]).pack(side=tk.LEFT, padx=(0, 6))
        self.level_var = tk.StringVar(value="--")
        self.level_menu = tk.OptionMenu(ctrl, self.level_var, "--")
        self.level_menu.config(bg=C["surface2"], fg=C["text"], font=F["ui"],
                                highlightthickness=0, bd=0, activebackground=C["surface2"],
                                activeforeground=C["text"], relief=tk.FLAT, padx=8)
        self.level_menu["menu"].config(bg=C["surface"], fg=C["text"],
                                        activebackground=C["accent_dim"],
                                        activeforeground=C["text"], font=F["ui"])
        self.level_menu.pack(side=tk.LEFT, padx=(0, 16))
        tk.Label(ctrl, text="POINTS", bg=C["bg"], fg=C["text_dim"],
                 font=F["ui_tiny"]).pack(side=tk.LEFT, padx=(0, 6))
        self.count_var = tk.StringVar(value="1")
        count_frame = tk.Frame(ctrl, bg=C["surface2"])
        count_frame.pack(side=tk.LEFT, padx=(0, 16))
        minus_btn = tk.Label(count_frame, text="-", bg=C["surface2"], fg=C["text_dim"],
                             font=F["ui_bold"], padx=8, pady=2, cursor="hand2")
        minus_btn.pack(side=tk.LEFT)
        minus_btn.bind("<Button-1>", lambda e: self._adjust_count(-1))
        self.count_label = tk.Label(count_frame, textvariable=self.count_var,
                                     bg=C["surface2"], fg=C["accent"], font=F["ui_bold"],
                                     width=2, anchor="center")
        self.count_label.pack(side=tk.LEFT, padx=2)
        plus_btn = tk.Label(count_frame, text="+", bg=C["surface2"], fg=C["text_dim"],
                            font=F["ui_bold"], padx=8, pady=2, cursor="hand2")
        plus_btn.pack(side=tk.LEFT)
        plus_btn.bind("<Button-1>", lambda e: self._adjust_count(1))
        self.btn_start = FlatButton(ctrl, ">> START", self._start_session,
                                     fg=C["bg"], bg=C["accent"], hover_bg=C["accent_dim"],
                                     btn_width=120, btn_height=32)
        self.btn_start.pack(side=tk.LEFT, padx=(0, 6))
        self.lbl_stats = tk.Label(ctrl, text="", bg=C["bg"], fg=C["text_faint"], font=F["ui_tiny"])
        self.lbl_stats.pack(side=tk.RIGHT)

        # Separator
        tk.Frame(self.root, bg=C["border"], height=1).pack(fill=tk.X, padx=20, pady=(14, 0))

        # Scrollable card area
        self.canvas = tk.Canvas(self.root, bg=C["bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview,
                                       bg=C["surface"], troughcolor=C["bg"])
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(14, 0))
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0), pady=(14, 0))
        self.scroll_frame = tk.Frame(self.canvas, bg=C["bg"])
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(-1 * (e.delta // 120), "units"))
        self._show_empty_state()
        self._scan_levels()

    def _show_empty_state(self):
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        empty = tk.Frame(self.scroll_frame, bg=C["bg"])
        empty.pack(fill=tk.BOTH, expand=True, pady=80)
        tk.Label(empty, text="文", bg=C["bg"], fg=C["text_faint"],
                 font=pick_font(JP_DISPLAY, 48, "bold")).pack()
        tk.Label(empty, text="Select a level and press START", bg=C["bg"],
                 fg=C["text_faint"], font=F["ui"]).pack(pady=(10, 0))

    def _adjust_count(self, delta):
        curr = int(self.count_var.get())
        self.count_var.set(str(max(1, min(5, curr + delta))))

    def _scan_levels(self):
        files = glob.glob(os.path.join(DATA_FOLDER, "*.txt"))
        levels = sorted([os.path.basename(f).replace(".txt", "") for f in files])
        menu = self.level_menu["menu"]
        menu.delete(0, "end")
        if levels:
            for lvl in levels:
                menu.add_command(label=lvl, command=lambda v=lvl: self.level_var.set(v))
            self.level_var.set(levels[0])
        else:
            self.level_var.set("No data files")
            self.lbl_stats.config(text=f"Add .txt files to '{DATA_FOLDER}/' folder")

    # ── Session Logic ─────────────────────────────────────

    def _start_session(self):
        level = self.level_var.get()
        path = os.path.join(DATA_FOLDER, f"{level}.txt")
        if not os.path.exists(path) or level == "--":
            messagebox.showwarning("Setup", "Select a valid level first.")
            return
        self.grammar_list = []
        try:
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if ";;" in line:
                        parts = [p.strip() for p in line.split(";;")]
                        if len(parts) >= 2 and parts[0] and parts[1]:
                            self.grammar_list.append({"name": parts[0], "url": parts[1]})
        except Exception as e:
            messagebox.showerror("Error", f"Could not load: {e}")
            return
        if not self.grammar_list:
            messagebox.showerror("Error", "No grammar points found in file.\nFormat: name ;; url")
            return
        for g in self.grammar_list:
            if g["name"] not in self.weights:
                self.weights[g["name"]] = DEFAULT_WEIGHT
        self.lbl_stats.config(text=f"{len(self.grammar_list)} grammar points loaded")
        self.txt_input.config(state=tk.NORMAL)
        self._deal_cards()

    def _deal_cards(self):
        if not self.grammar_list:
            return
        n = min(int(self.count_var.get()), len(self.grammar_list))
        pool = list(self.grammar_list)
        weights = [self.weights.get(g["name"], DEFAULT_WEIGHT) for g in pool]
        chosen = []
        for _ in range(n):
            if not pool:
                break
            pick = random.choices(range(len(pool)), weights=weights, k=1)[0]
            chosen.append(pool[pick])
            pool.pop(pick)
            weights.pop(pick)
        self.current_cards = chosen
        self.pending_ratings = {}
        for w in self.scroll_frame.winfo_children():
            w.destroy()
        self.card_widgets = []
        for i, g in enumerate(chosen, 1):
            card = GrammarCard(self.scroll_frame, g, i, n, self._on_card_rated, self)
            card.pack(fill=tk.X, padx=4, pady=(0, 8))
            self.card_widgets.append(card)
        self.txt_input.delete("1.0", tk.END)
        self.txt_input.focus_set()
        self.btn_next.set_disabled(True)
        self.canvas.yview_moveto(0)

    def _on_card_rated(self, grammar, difficulty):
        self.pending_ratings[grammar["name"]] = difficulty
        if len(self.pending_ratings) == len(self.current_cards):
            self.btn_next.set_disabled(False)

    def _next_round(self):
        sentence = self.txt_input.get("1.0", tk.END).strip()
        if not sentence:
            self.root.bell()
            self.txt_input.config(highlightbackground=C["red"], highlightthickness=1)
            self.root.after(600, lambda: self.txt_input.config(highlightthickness=0))
            return
        if len(self.pending_ratings) < len(self.current_cards):
            messagebox.showinfo("Rate All", "Please rate every grammar point before continuing.")
            return
        for g in self.current_cards:
            name = g["name"]
            diff = self.pending_ratings.get(name, "Normal")
            w = self.weights.get(name, DEFAULT_WEIGHT)
            if diff == "Hard":
                w = min(w * 1.5, 500)
            elif diff == "Easy":
                w = max(w * 0.6, 10)
            self.weights[name] = w
            self.history.insert(0, {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "grammar": name,
                "sentence": sentence,
                "difficulty": diff,
            })
        self._save_data()
        self._deal_cards()

    # ── History & Stats ───────────────────────────────────

    def _show_history(self):
        HistoryWindow(self.root, self.history)

    def _show_stats(self):
        StatsWindow(self.root, self.history, self.weights)


# ─────────────────────────────────────────────────────────────
# Entry
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass
    app = GrammarDrillApp(root)
    root.mainloop()