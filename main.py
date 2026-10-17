import asyncio, subprocess, aiohttp
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, ListView, ListItem, Label, TabbedContent, TabPane
from db import Database

db = Database()

class TermuxIPTV(App):
    CSS = """
    Screen { background: #0d1117; }
    #stats_bar { height: 3; background: #161b22; color: #58a6ff; content-align: center middle; text-style: bold; border: solid #30363d; }
    ListView { background: #010409; border: solid #30363d; height: 1fr; }
    ListItem { padding: 1; color: #c9d1d9; }
    ListItem:focus { background: #1f6feb; color: #ffffff; text-style: bold; }
    .item_lbl { padding: 0; }
    """

    def __init__(self):
        super().__init__()
        self.server = "http://cf.suvek416.xyz"
        self.username = "5c7231eb77"
        self.password = "9a0fd4b161"

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Label("⚡ جاري جلب الأقسام...", id="stats_bar")
        with TabbedContent(initial="live_tab"):
            with TabPane("📺 البث", id="live_tab"): yield ListView(id="live_list")
            with TabPane("🎬 الأفلام", id="vod_tab"): yield ListView(id="vod_list")
            with TabPane("🍿 المسلسلات", id="series_tab"): yield ListView(id="series_list")
        yield Footer()

    async def on_mount(self) -> None:
        stats_label = self.query_one("#stats_bar", Label)
        live_list = self.query_one("#live_list", ListView)
        vod_list = self.query_one("#vod_list", ListView)
        series_list = self.query_one("#series_list", ListView)
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(f"{self.server}/player_api.php?username={self.username}&password={self.password}&action=get_live_streams", timeout=10) as r:
                    if r.status == 200:
                        for i in (await r.json())[:30]:
                            name = i.get("name", "قناة")
                            w = ListItem(Label(f"📺 {name}", classes="item_lbl"))
                            w.stream_url = f"{self.server}/live/{self.username}/{self.password}/{i.get("stream_id")}.ts"
                            w.stream_name = name
                            await live_list.append(w)
            except: pass
            
            try:
                async with session.get(f"{self.server}/player_api.php?username={self.username}&password={self.password}&action=get_vod_streams", timeout=10) as r:
                    if r.status == 200:
                        for i in (await r.json())[:30]:
                            name = i.get("name", "فيلم")
                            ext = i.get("container_extension", "mp4")
                            w = ListItem(Label(f"🎬 {name}", classes="item_lbl"))
                            w.stream_url = f"{self.server}/movie/{self.username}/{self.password}/{i.get("stream_id")}.{ext}"
                            w.stream_name = name
                            await vod_list.append(w)
            except: pass
            
            try:
                async with session.get(f"{self.server}/player_api.php?username={self.username}&password={self.password}&action=get_series", timeout=10) as r:
                    if r.status == 200:
                        for i in (await r.json())[:30]:
                            name = i.get("name", "مسلسل")
                            w = ListItem(Label(f"🍿 {name}", classes="item_lbl"))
                            w.is_series = True
                            w.stream_name = name
                            await series_list.append(w)
            except: pass
            
        stats_label.update("✅ جاهز! اختر المحتوى للتشغيل")

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if hasattr(item, "stream_url"):
            self.query_one("#stats_bar", Label).update(f"▶ جاري التشغيل: {item.stream_name}")
            subprocess.Popen(["mpv", "--hwdec=auto", "--vo=gpu", "--profile=low-latency", item.stream_url])
        elif getattr(item, "is_series", False):
            self.query_one("#stats_bar", Label).update(f"ℹ️ مسلسل: {item.stream_name}")

if __name__ == "__main__":
    TermuxIPTV().run()

# --- إضافة تلقائية من Termux: دالة دمج الصوت ---
from audio_mixer import mix_live_audio

def start_mixed_stream(live_url, local_audio):
    # مسار حفظ الملف الناتج
    out_path = "/sdcard/Download/mixed_stream.mp4"
    
    # استدعاء الدالة
    success, result = mix_live_audio(live_url, local_audio, out_path)
    
    if success:
        print(f"تم الدمج بنجاح! الملف موجود في: {result}")
        # هنا يمكنك إضافة كود لتشغيل الملف الناتج في مشغل Kivy
    else:
        print(f"فشل الدمج: {result}")
# -----------------------------------------------------
