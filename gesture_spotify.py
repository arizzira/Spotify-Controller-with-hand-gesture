import cv2
import mediapipe as mp
import pyautogui
import time
import platform
import os
import threading
from datetime import datetime
from collections import deque
import random

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich import box

# Setup console
console = Console(width=120, height=40, legacy_windows=False)

class GestureStats:
    def __init__(self):
        self.total_gestures = 0
        self.gesture_count = {"next": 0, "prev": 0, "play_pause": 0, "vol_up": 0, "vol_down": 0}
        self.session_start = datetime.now()
        self.last_activity = datetime.now()
        
    def add_gesture(self, gesture_type):
        self.total_gestures += 1
        if gesture_type in self.gesture_count:
            self.gesture_count[gesture_type] += 1
        self.last_activity = datetime.now()
        
    def get_most_used(self):
        if self.total_gestures == 0:
            return "None"
        return max(self.gesture_count, key=self.gesture_count.get)
        
    def get_session_duration(self):
        return datetime.now() - self.session_start

class AnimatedDisplay:
    def __init__(self):
        self.wave_offset = 0
        self.rainbow_colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        
    def get_wave_text(self, text, style="bold"):
        """Efek animasi gelombang pada teks"""
        self.wave_offset += 0.5
        result = ""
        for i, char in enumerate(text):
            if char == " ":
                result += char
                continue
            wave_pos = (i + self.wave_offset) % 10
            distance = abs(wave_pos - 5)
            normalized = distance / 5
            intensity_factor = 1 + 0.5 * (1 + normalized)
            intensity = int(3 * intensity_factor)
            
            if intensity > 2:
                color = self.rainbow_colors[i % len(self.rainbow_colors)]
                result += f"[bold {color}]{char}[/bold {color}]"
            else:
                result += f"[{style}]{char}[/{style}]"
        return result

# Global variables
OS = platform.system()
stats = GestureStats()
display = AnimatedDisplay()
gesture_history = deque(maxlen=15)
current_song = "Unknown Track"
artist_name = "Unknown Artist"
volume_level = 50
is_playing = False
hands_detected = False
current_gesture = "None"
fps_counter = 0
last_fps_time = time.time()
current_fps = 0

# === GUNAKAN MEDIA KEYS GLOBAL (LEBIH ANDAL) ===
NEXT_CMD = lambda: pyautogui.press('nexttrack')
PREV_CMD = lambda: pyautogui.press('prevtrack')
PLAY_PAUSE_CMD = lambda: pyautogui.press('playpause')
VOL_UP_CMD = lambda: pyautogui.press('volumeup')
VOL_DOWN_CMD = lambda: pyautogui.press('volumedown')

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
    max_num_hands=1
)

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 60)

# Gesture control
gesture_cooldown = 0.7
last_gesture_time = time.time()
last_gesture_pattern = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_epic_header():
    title = display.get_wave_text("GESTURE SPOTIFY CONTROL")
    subtitle = Text("Hand gesture media control - Simple and powerful", style="italic bright_cyan")
    header_content = Align.center(title) + "\n" + Align.center(subtitle)
    return Panel(header_content, box=box.DOUBLE_EDGE, border_style="bright_magenta", padding=(1, 2), title="ACTIVE", title_align="left")

def create_music_player_mockup():
    global is_playing, current_song, artist_name
    songs = [
        ("Blinding Lights", "The Weeknd"),
        ("Shape of You", "Ed Sheeran"),
        ("Someone Like You", "Adele"),
        ("Bohemian Rhapsody", "Queen"),
        ("Hotel California", "Eagles"),
        ("Imagine", "John Lennon"),
        ("Stairway to Heaven", "Led Zeppelin")
    ]
    if random.random() < 0.1:
        current_song, artist_name = random.choice(songs)
    play_status = "Paused" if not is_playing else "Playing"
    progress = "Progress: [========================================]"
    player_content = f"""
Now Playing
Title:  {current_song}
Artist: {artist_name}

Status: {play_status}
Time:   2:34 / 3:45

Volume: {volume_level}%
"""
    return Panel(player_content, title="Spotify Player", border_style="green", box=box.ROUNDED, padding=(1, 1))

def create_advanced_stats():
    duration = stats.get_session_duration()
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    max_val = max(stats.gesture_count.values()) if stats.total_gestures > 0 else 1
    chart = ""
    gestures = {
        "Next": stats.gesture_count["next"],
        "Prev": stats.gesture_count["prev"],
        "Play": stats.gesture_count["play_pause"],
        "Vol+": stats.gesture_count["vol_up"],
        "Vol-": stats.gesture_count["vol_down"]
    }
    for name, count in gestures.items():
        bar_length = int((count / max_val) * 15)
        bar = "█" * bar_length + "░" * (15 - bar_length)
        chart += f"{name:4} [{count:3}] [cyan]{bar}[/cyan]\n"
    stats_content = f"""
Session Statistics

Duration: {hours:02d}:{minutes:02d}:{seconds:02d}
Total Gestures: {stats.total_gestures}
Most Used: {stats.get_most_used().title()}
FPS: {current_fps}

{chart.rstrip()}
"""
    return Panel(stats_content, title="Analytics", border_style="yellow", box=box.ROUNDED)

def create_gesture_commands():
    table = Table(show_header=True, box=box.HEAVY_EDGE)
    table.add_column(" Gesture", style="cyan", width=20)
    table.add_column(" Action", style="green", width=20)
    
    gestures = [
        (" 5 Fingers", "Next Song"),
        (" 0 Fingers", "Previous Song"),
        (" Thumb Only", "Play Pause"),
        (" 4 Fingers", "Volume Up"),
        (" 3 Fingers", "Volume Down"),
    ]
    for gesture, action in gestures:
        table.add_row(gesture, action)
    return Panel(table, title="Gesture Guide", border_style="cyan", box=box.ROUNDED)

def create_activity_timeline():
    if not gesture_history:
        content = "No gestures detected yet. Start using your hand."
    else:
        content = ""
        for activity in reversed(list(gesture_history)[-10:]):
            time_str = activity['time']
            action = activity['action']
            content += f"{time_str}  {action}\n"
    return Panel(content, title="Recent Actions", border_style="blue", box=box.ROUNDED, height=10)

def create_system_monitor():
    try:
        import psutil
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
    except ImportError:
        cpu, ram = random.randint(10, 50), random.randint(30, 70)
    
    def bar(p):
        filled = int(p / 5)
        return f"[{'green' if p < 70 else 'yellow' if p < 90 else 'red'}]{'█' * filled}{'░' * (20-filled)}[/] {p:.0f}%"
    
    content = f"""
System Status

Camera FPS: {current_fps}
Hand Detected: {"Yes" if hands_detected else "No"}

CPU Usage: {bar(cpu)}
RAM Usage: {bar(ram)}
"""
    return Panel(content, title="System Monitor", border_style="blue", box=box.ROUNDED)

def log_gesture(action, gesture_type):
    global is_playing, volume_level
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    stats.add_gesture(gesture_type)
    if gesture_type == "play_pause":
        is_playing = not is_playing
    elif gesture_type == "vol_up":
        volume_level = min(100, volume_level + 8)
    elif gesture_type == "vol_down":
        volume_level = max(0, volume_level - 8)
    gesture_history.append({
        'time': timestamp,
        'action': action,
        'type': gesture_type
    })

def hitung_jari_terangkat(landmarks):
    jari = []
    # Jempol
    jari.append(1 if landmarks[4].x < landmarks[3].x else 0)
    # Telunjuk - Kelingking
    jari.append(1 if landmarks[8].y < landmarks[6].y else 0)
    jari.append(1 if landmarks[12].y < landmarks[10].y else 0)
    jari.append(1 if landmarks[16].y < landmarks[14].y else 0)
    jari.append(1 if landmarks[20].y < landmarks[18].y else 0)
    return jari

def create_main_layout():
    layout = Layout()
    layout.split_column(
        Layout(create_epic_header(), size=6),
        Layout(name="main_body", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["main_body"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="center", ratio=2),
        Layout(name="right", ratio=2)
    )
    layout["left"].split_column(
        Layout(create_music_player_mockup()),
        Layout(create_system_monitor())
    )
    layout["center"] = create_gesture_commands()
    layout["right"].split_column(
        Layout(create_advanced_stats()),
        Layout(create_activity_timeline())
    )
    footer = Text.assemble(
        ("ESC: Quit | SPACE: Screenshot", "bold yellow"),
        (" | Made with Python", "dim")
    )
    layout["footer"] = Panel(Align.center(footer), box=box.SIMPLE, border_style="dim")
    return layout

def show_splash():
    clear_screen()
    console.print("\n" + " " * 30 + "Gesture Spotify Control\n", justify="center", style="bold green")
    console.print("• Detecting hand...", justify="center")
    time.sleep(0.5)
    console.print("• Loading gestures...", justify="center")
    time.sleep(0.5)
    console.print("• Ready!\n", justify="center")
    time.sleep(1)

def update_fps():
    global fps_counter, last_fps_time, current_fps
    fps_counter += 1
    if time.time() - last_fps_time >= 1.0:
        current_fps = fps_counter
        fps_counter = 0
        last_fps_time = time.time()

def main_display_loop():
    with Live(create_main_layout(), console=console, refresh_per_second=4) as live:
        while cap.isOpened():
            try:
                live.update(create_main_layout())
                time.sleep(0.25)
            except Exception:
                break

# === START PROGRAM ===
show_splash()

# Jalankan UI di thread terpisah
display_thread = threading.Thread(target=main_display_loop, daemon=True)
display_thread.start()

# Loop utama deteksi
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        hands_detected = False
        continue

    update_fps()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    if results.multi_hand_landmarks:
        hands_detected = True
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=3)
            )
            landmarks = hand_landmarks.landmark
            jari = hitung_jari_terangkat(landmarks)
            jumlah = sum(jari)
            current_time = time.time()

            # Reset gesture
            current_gesture = "Standby"

            # 0 jari = Previous
            if jumlah == 0:
                current_gesture = "Previous (Keput)"
                if jumlah != last_gesture_pattern and current_time - last_gesture_time > gesture_cooldown:
                    PREV_CMD()
                    log_gesture("Previous Song", "prev")
                    last_gesture_time = current_time
                    last_gesture_pattern = jumlah

            # 5 jari = Next
            elif jumlah == 5:
                current_gesture = "Next (Terbuka)"
                if jumlah != last_gesture_pattern and current_time - last_gesture_time > gesture_cooldown:
                    NEXT_CMD()
                    log_gesture("Next Song", "next")
                    last_gesture_time = current_time
                    last_gesture_pattern = jumlah

            # Volume Up (4 jari, jempol turun)
            elif jumlah == 4 and jari[0] == 0:
                current_gesture = "Volume Up"
                if current_time - last_gesture_time > 0.15:
                    VOL_UP_CMD()
                    log_gesture("Volume Up", "vol_up")
                    last_gesture_time = current_time

            # Volume Down (3 jari tengah: telunjuk, tengah, manis)
            elif jumlah == 3 and jari[1] == 1 and jari[2] == 1 and jari[3] == 1 and jari[0] == 0 and jari[4] == 0:
                current_gesture = "Volume Down"
                if current_time - last_gesture_time > 0.15:
                    VOL_DOWN_CMD()
                    log_gesture("Volume Down", "vol_down")
                    last_gesture_time = current_time

            # Play/Pause dengan jempol saja
            elif jari == [1, 0, 0, 0, 0]:
                current_gesture = "Play Pause"
                if jari != last_gesture_pattern and current_time - last_gesture_time > gesture_cooldown:
                    PLAY_PAUSE_CMD()
                    log_gesture("Play Pause", "play_pause")
                    last_gesture_time = current_time
                    last_gesture_pattern = jari

    else:
        hands_detected = False
        current_gesture = "No hand detected"

    # Tampilkan status di frame kamera
    color = (0, 255, 0) if hands_detected else (0, 0, 255)
    cv2.rectangle(frame, (10, 10), (350, 100), (0, 0, 0), -1)
    cv2.putText(frame, f"Gesture: {current_gesture}", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    cv2.putText(frame, f"FPS: {current_fps} | Total: {stats.total_gestures}", (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    cv2.putText(frame, f"Volume: {volume_level}%", (15, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.imshow("Gesture Spotify Control", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord(' '):  # Screenshot
        timestamp = datetime.now().strftime("%H%M%S")
        cv2.imwrite(f"screenshot_{timestamp}.jpg", frame)
        log_gesture("Screenshot taken", "screenshot")

# Cleanupimport cv2
import mediapipe as mp
import pyautogui
import time
import platform
import os
import threading
from datetime import datetime
from collections import deque
import random

from rich.console import Console
from rich.text import Text
from rich.panel import Panel
from rich.align import Align
from rich.layout import Layout
from rich.live import Live
from rich.table import Table
from rich import box

# Setup console
console = Console(width=120, height=40, legacy_windows=False)

class GestureStats:
    def __init__(self):
        self.total_gestures = 0
        self.gesture_count = {"next": 0, "prev": 0, "play_pause": 0, "vol_up": 0, "vol_down": 0}
        self.session_start = datetime.now()
        self.last_activity = datetime.now()
        
    def add_gesture(self, gesture_type):
        self.total_gestures += 1
        if gesture_type in self.gesture_count:
            self.gesture_count[gesture_type] += 1
        self.last_activity = datetime.now()
        
    def get_most_used(self):
        if self.total_gestures == 0:
            return "None"
        return max(self.gesture_count, key=self.gesture_count.get)
        
    def get_session_duration(self):
        return datetime.now() - self.session_start

class AnimatedDisplay:
    def __init__(self):
        self.wave_offset = 0
        self.rainbow_colors = ["red", "yellow", "green", "cyan", "blue", "magenta"]
        
    def get_wave_text(self, text, style="bold"):
        """Efek animasi gelombang pada teks"""
        self.wave_offset += 0.5
        result = ""
        for i, char in enumerate(text):
            if char == " ":
                result += char
                continue
            wave_pos = (i + self.wave_offset) % 10
            distance = abs(wave_pos - 5)
            normalized = distance / 5
            intensity_factor = 1 + 0.5 * (1 + normalized)
            intensity = int(3 * intensity_factor)
            
            if intensity > 2:
                color = self.rainbow_colors[i % len(self.rainbow_colors)]
                result += f"[bold {color}]{char}[/bold {color}]"
            else:
                result += f"[{style}]{char}[/{style}]"
        return result

# Global variables
OS = platform.system()
stats = GestureStats()
display = AnimatedDisplay()
gesture_history = deque(maxlen=15)
current_song = "Unknown Track"
artist_name = "Unknown Artist"
volume_level = 50
is_playing = False
hands_detected = False
current_gesture = "None"
fps_counter = 0
last_fps_time = time.time()
current_fps = 0

# === GUNAKAN MEDIA KEYS GLOBAL (LEBIH ANDAL) ===
NEXT_CMD = lambda: pyautogui.press('nexttrack')
PREV_CMD = lambda: pyautogui.press('prevtrack')
PLAY_PAUSE_CMD = lambda: pyautogui.press('playpause')
VOL_UP_CMD = lambda: pyautogui.press('volumeup')
VOL_DOWN_CMD = lambda: pyautogui.press('volumedown')

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    min_detection_confidence=0.8,
    min_tracking_confidence=0.8,
    max_num_hands=1
)

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
cap.set(cv2.CAP_PROP_FPS, 60)

# Gesture control
gesture_cooldown = 0.7
last_gesture_time = time.time()
last_gesture_pattern = None

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def create_epic_header():
    title = display.get_wave_text("GESTURE SPOTIFY CONTROL")
    subtitle = Text("Hand gesture media control - Simple and powerful", style="italic bright_cyan")
    header_content = Align.center(title) + "\n" + Align.center(subtitle)
    return Panel(header_content, box=box.DOUBLE_EDGE, border_style="bright_magenta", padding=(1, 2), title="ACTIVE", title_align="left")

def create_music_player_mockup():
    global is_playing, current_song, artist_name
    songs = [
        ("Blinding Lights", "The Weeknd"),
        ("Shape of You", "Ed Sheeran"),
        ("Someone Like You", "Adele"),
        ("Bohemian Rhapsody", "Queen"),
        ("Hotel California", "Eagles"),
        ("Imagine", "John Lennon"),
        ("Stairway to Heaven", "Led Zeppelin")
    ]
    if random.random() < 0.1:
        current_song, artist_name = random.choice(songs)
    play_status = "Paused" if not is_playing else "Playing"
    progress = "Progress: [========================================]"
    player_content = f"""
Now Playing
Title:  {current_song}
Artist: {artist_name}

Status: {play_status}
Time:   2:34 / 3:45

Volume: {volume_level}%
"""
    return Panel(player_content, title="Spotify Player", border_style="green", box=box.ROUNDED, padding=(1, 1))

def create_advanced_stats():
    duration = stats.get_session_duration()
    hours = duration.seconds // 3600
    minutes = (duration.seconds % 3600) // 60
    seconds = duration.seconds % 60
    max_val = max(stats.gesture_count.values()) if stats.total_gestures > 0 else 1
    chart = ""
    gestures = {
        "Next": stats.gesture_count["next"],
        "Prev": stats.gesture_count["prev"],
        "Play": stats.gesture_count["play_pause"],
        "Vol+": stats.gesture_count["vol_up"],
        "Vol-": stats.gesture_count["vol_down"]
    }
    for name, count in gestures.items():
        bar_length = int((count / max_val) * 15)
        bar = "█" * bar_length + "░" * (15 - bar_length)
        chart += f"{name:4} [{count:3}] [cyan]{bar}[/cyan]\n"
    stats_content = f"""
Session Statistics

Duration: {hours:02d}:{minutes:02d}:{seconds:02d}
Total Gestures: {stats.total_gestures}
Most Used: {stats.get_most_used().title()}
FPS: {current_fps}

{chart.rstrip()}
"""
    return Panel(stats_content, title="Analytics", border_style="yellow", box=box.ROUNDED)

def create_gesture_commands():
    table = Table(show_header=True, box=box.HEAVY_EDGE)
    table.add_column(" Gesture", style="cyan", width=20)
    table.add_column(" Action", style="green", width=20)
    
    gestures = [
        (" 5 Fingers", "Next Song"),
        (" 0 Fingers", "Previous Song"),
        (" Thumb Only", "Play Pause"),
        (" 4 Fingers", "Volume Up"),
        (" 3 Fingers", "Volume Down"),
    ]
    for gesture, action in gestures:
        table.add_row(gesture, action)
    return Panel(table, title="Gesture Guide", border_style="cyan", box=box.ROUNDED)

def create_activity_timeline():
    if not gesture_history:
        content = "No gestures detected yet. Start using your hand."
    else:
        content = ""
        for activity in reversed(list(gesture_history)[-10:]):
            time_str = activity['time']
            action = activity['action']
            content += f"{time_str}  {action}\n"
    return Panel(content, title="Recent Actions", border_style="blue", box=box.ROUNDED, height=10)

def create_system_monitor():
    try:
        import psutil
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
    except ImportError:
        cpu, ram = random.randint(10, 50), random.randint(30, 70)
    
    def bar(p):
        filled = int(p / 5)
        return f"[{'green' if p < 70 else 'yellow' if p < 90 else 'red'}]{'█' * filled}{'░' * (20-filled)}[/] {p:.0f}%"
    
    content = f"""
System Status

Camera FPS: {current_fps}
Hand Detected: {"Yes" if hands_detected else "No"}

CPU Usage: {bar(cpu)}
RAM Usage: {bar(ram)}
"""
    return Panel(content, title="System Monitor", border_style="blue", box=box.ROUNDED)

def log_gesture(action, gesture_type):
    global is_playing, volume_level
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    stats.add_gesture(gesture_type)
    if gesture_type == "play_pause":
        is_playing = not is_playing
    elif gesture_type == "vol_up":
        volume_level = min(100, volume_level + 8)
    elif gesture_type == "vol_down":
        volume_level = max(0, volume_level - 8)
    gesture_history.append({
        'time': timestamp,
        'action': action,
        'type': gesture_type
    })

def hitung_jari_terangkat(landmarks):
    jari = []
    # Jempol
    jari.append(1 if landmarks[4].x < landmarks[3].x else 0)
    # Telunjuk - Kelingking
    jari.append(1 if landmarks[8].y < landmarks[6].y else 0)
    jari.append(1 if landmarks[12].y < landmarks[10].y else 0)
    jari.append(1 if landmarks[16].y < landmarks[14].y else 0)
    jari.append(1 if landmarks[20].y < landmarks[18].y else 0)
    return jari

def create_main_layout():
    layout = Layout()
    layout.split_column(
        Layout(create_epic_header(), size=6),
        Layout(name="main_body", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["main_body"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="center", ratio=2),
        Layout(name="right", ratio=2)
    )
    layout["left"].split_column(
        Layout(create_music_player_mockup()),
        Layout(create_system_monitor())
    )
    layout["center"] = create_gesture_commands()
    layout["right"].split_column(
        Layout(create_advanced_stats()),
        Layout(create_activity_timeline())
    )
    footer = Text.assemble(
        ("ESC: Quit | SPACE: Screenshot", "bold yellow"),
        (" | Made with Python", "dim")
    )
    layout["footer"] = Panel(Align.center(footer), box=box.SIMPLE, border_style="dim")
    return layout

def show_splash():
    clear_screen()
    console.print("\n" + " " * 30 + "Gesture Spotify Control\n", justify="center", style="bold green")
    console.print("• Detecting hand...", justify="center")
    time.sleep(0.5)
    console.print("• Loading gestures...", justify="center")
    time.sleep(0.5)
    console.print("• Ready!\n", justify="center")
    time.sleep(1)

def update_fps():
    global fps_counter, last_fps_time, current_fps
    fps_counter += 1
    if time.time() - last_fps_time >= 1.0:
        current_fps = fps_counter
        fps_counter = 0
        last_fps_time = time.time()

def main_display_loop():
    with Live(create_main_layout(), console=console, refresh_per_second=4) as live:
        while cap.isOpened():
            try:
                live.update(create_main_layout())
                time.sleep(0.25)
            except Exception:
                break

# === START PROGRAM ===
show_splash()

# Jalankan UI di thread terpisah
display_thread = threading.Thread(target=main_display_loop, daemon=True)
display_thread.start()

# Loop utama deteksi
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        hands_detected = False
        continue

    update_fps()
    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    
    if results.multi_hand_landmarks:
        hands_detected = True
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                mp_drawing.DrawingSpec(color=(255, 0, 255), thickness=3)
            )
            landmarks = hand_landmarks.landmark
            jari = hitung_jari_terangkat(landmarks)
            jumlah = sum(jari)
            current_time = time.time()

            # Reset gesture
            current_gesture = "Standby"

            # 0 jari = Previous
            if jumlah == 0:
                current_gesture = "Previous (Keput)"
                if jumlah != last_gesture_pattern and current_time - last_gesture_time > gesture_cooldown:
                    PREV_CMD()
                    log_gesture("Previous Song", "prev")
                    last_gesture_time = current_time
                    last_gesture_pattern = jumlah

            # 5 jari = Next
            elif jumlah == 5:
                current_gesture = "Next (Terbuka)"
                if jumlah != last_gesture_pattern and current_time - last_gesture_time > gesture_cooldown:
                    NEXT_CMD()
                    log_gesture("Next Song", "next")
                    last_gesture_time = current_time
                    last_gesture_pattern = jumlah

            # Volume Up (4 jari, jempol turun)
            elif jumlah == 4 and jari[0] == 0:
                current_gesture = "Volume Up"
                if current_time - last_gesture_time > 0.15:
                    VOL_UP_CMD()
                    log_gesture("Volume Up", "vol_up")
                    last_gesture_time = current_time

            # Volume Down (3 jari tengah: telunjuk, tengah, manis)
            elif jumlah == 3 and jari[1] == 1 and jari[2] == 1 and jari[3] == 1 and jari[0] == 0 and jari[4] == 0:
                current_gesture = "Volume Down"
                if current_time - last_gesture_time > 0.15:
                    VOL_DOWN_CMD()
                    log_gesture("Volume Down", "vol_down")
                    last_gesture_time = current_time

            # Play/Pause dengan jempol saja
            elif jari == [1, 0, 0, 0, 0]:
                current_gesture = "Play Pause"
                if jari != last_gesture_pattern and current_time - last_gesture_time > gesture_cooldown:
                    PLAY_PAUSE_CMD()
                    log_gesture("Play Pause", "play_pause")
                    last_gesture_time = current_time
                    last_gesture_pattern = jari

    else:
        hands_detected = False
        current_gesture = "No hand detected"

    # Tampilkan status di frame kamera
    color = (0, 255, 0) if hands_detected else (0, 0, 255)
    cv2.rectangle(frame, (10, 10), (350, 100), (0, 0, 0), -1)
    cv2.putText(frame, f"Gesture: {current_gesture}", (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    cv2.putText(frame, f"FPS: {current_fps} | Total: {stats.total_gestures}", (15, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
    cv2.putText(frame, f"Volume: {volume_level}%", (15, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    cv2.imshow("Gesture Spotify Control", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord(' '):  # Screenshot
        timestamp = datetime.now().strftime("%H%M%S")
        cv2.imwrite(f"screenshot_{timestamp}.jpg", frame)
        log_gesture("Screenshot taken", "screenshot")

# Cleanup
cap.release()
cv2.destroyAllWindows()
clear_screen()
console.print(Panel("Session ended. Thank you.", title="Goodbye", style="bold green"))
cap.release()
cv2.destroyAllWindows()
clear_screen()
console.print(Panel("Session ended. Thank you.", title="Goodbye", style="bold green"))