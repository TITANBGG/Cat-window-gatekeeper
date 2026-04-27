import json
import time
import tkinter as tk
from pathlib import Path
from typing import Any, Dict, List

import pygetwindow as gw


APP_NAME = "Ali Focus Gatekeeper"
OWNER = "Ali Nebi ER"
DEFAULT_CONFIG: Dict[str, Any] = {
    "owner": OWNER,
    "global_rest_time_minutes": 5,
    "smart_video_detection": True,
    "check_interval_seconds": 1,
    "apps": [],
}


class FocusOverlay:
    """Full-screen rest overlay shown when an app reaches its limit."""

    def __init__(self, app_label: str, rest_time_minutes: float):
        self.remaining_seconds = max(1, int(rest_time_minutes * 60))
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.96)
        self.root.overrideredirect(True)
        self.root.configure(bg="#121826")

        self.root.bind("<Control-Shift-Q>", lambda _event: self.root.destroy())

        container = tk.Frame(self.root, bg="#121826")
        container.pack(expand=True, fill="both")

        tk.Label(
            container,
            text="ALI FOCUS GATEKEEPER",
            font=("Segoe UI", 18, "bold"),
            fg="#7dd3fc",
            bg="#121826",
        ).pack(pady=(90, 20))

        tk.Label(
            container,
            text="Mola zamani.",
            font=("Segoe UI", 54, "bold"),
            fg="#f8fafc",
            bg="#121826",
        ).pack(pady=10)

        tk.Label(
            container,
            text=f"{app_label} icin belirlenen sure doldu.",
            font=("Segoe UI", 22),
            fg="#cbd5e1",
            bg="#121826",
        ).pack(pady=8)

        self.timer_label = tk.Label(
            container,
            text="",
            font=("Segoe UI", 44, "bold"),
            fg="#facc15",
            bg="#121826",
        )
        self.timer_label.pack(pady=28)

        tk.Label(
            container,
            text="Acil cikis: Ctrl + Shift + Q",
            font=("Segoe UI", 13),
            fg="#94a3b8",
            bg="#121826",
        ).pack(side="bottom", pady=32)

    def start(self) -> None:
        self._tick()
        self.root.mainloop()

    def _tick(self) -> None:
        minutes, seconds = divmod(self.remaining_seconds, 60)
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")

        if self.remaining_seconds <= 0:
            self.root.destroy()
            return

        self.remaining_seconds -= 1
        self.root.after(1000, self._tick)


class FocusGatekeeper:
    """Tracks configured window titles and enforces rest breaks."""

    def __init__(self, config_path: str = "config.json"):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.app_usage: Dict[str, int] = {}
        self.is_resting = False
        self.last_seen_key = ""

    def _load_config(self) -> Dict[str, Any]:
        if not self.config_path.exists():
            print("config.json bulunamadi. Varsayilan ayarlar kullaniliyor.")
            return DEFAULT_CONFIG.copy()

        with self.config_path.open("r", encoding="utf-8") as file:
            loaded = json.load(file)

        config = DEFAULT_CONFIG.copy()
        config.update(loaded)
        config["apps"] = loaded.get("apps", [])
        return config

    def _configured_apps(self) -> List[Dict[str, Any]]:
        apps = []
        for item in self.config.get("apps", []):
            if not item.get("enabled", True):
                continue
            if not item.get("process_name") or not item.get("time_limit_minutes"):
                continue
            apps.append(item)
        return apps

    def _active_window_title(self) -> str:
        try:
            active_window = gw.getActiveWindow()
        except Exception:
            return ""

        if active_window is None or not active_window.title:
            return ""
        return active_window.title.strip()

    def _match_active_app(self, title: str) -> Dict[str, Any] | None:
        normalized_title = title.lower()
        for app in self._configured_apps():
            process_name = app["process_name"]
            process_stem = process_name.lower().removesuffix(".exe")
            keywords = [process_stem, *app.get("window_keywords", [])]

            if any(keyword.lower() in normalized_title for keyword in keywords):
                return app
        return None

    def is_fullscreen_video_playing(self) -> bool:
        if not self.config.get("smart_video_detection", True):
            return False

        title = self._active_window_title().lower()
        video_keywords = ("youtube", "netflix", "prime video", "disney+", "fullscreen")
        return any(keyword in title for keyword in video_keywords)

    def trigger_rest(self, app: Dict[str, Any]) -> None:
        app_key = app["process_name"]
        app_label = app.get("description") or app_key

        print(f"{app_label}: limit doldu. {OWNER} icin mola baslatiliyor.")
        self.is_resting = True

        overlay = FocusOverlay(
            app_label=app_label,
            rest_time_minutes=float(self.config.get("global_rest_time_minutes", 5)),
        )
        overlay.start()

        self.app_usage[app_key] = 0
        self.is_resting = False
        print("Mola bitti. Takip yeniden basladi.")

    def start_tracking(self) -> None:
        interval = max(1, int(self.config.get("check_interval_seconds", 1)))
        owner = self.config.get("owner", OWNER)

        print(f"{APP_NAME} baslatildi.")
        print(f"Sahip: {owner}")
        print("Takip edilen uygulamalar:")
        for app in self._configured_apps():
            print(f"- {app['process_name']}: {app['time_limit_minutes']} dk")

        while True:
            time.sleep(interval)

            if self.is_resting or self.is_fullscreen_video_playing():
                continue

            title = self._active_window_title()
            active_app = self._match_active_app(title)

            if active_app is None:
                continue

            app_key = active_app["process_name"]
            limit_seconds = int(float(active_app["time_limit_minutes"]) * 60)
            self.app_usage[app_key] = self.app_usage.get(app_key, 0) + interval

            if app_key != self.last_seen_key:
                self.last_seen_key = app_key
                label = active_app.get("description") or app_key
                print(f"Aktif takip: {label}")

            if self.app_usage[app_key] >= limit_seconds:
                self.trigger_rest(active_app)


if __name__ == "__main__":
    gatekeeper = FocusGatekeeper()
    gatekeeper.start_tracking()
