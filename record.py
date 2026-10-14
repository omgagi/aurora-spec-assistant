"""Re-records screenshots + walkthrough video. Needs: server running on :8765, playwright (pip) + chromium, ffmpeg."""
import glob, os, subprocess, shutil
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(D, "screenshots"); V = "/tmp/aurora-vid"
shutil.rmtree(V, ignore_errors=True)
with sync_playwright() as p:
    b = p.chromium.launch(); ctx = b.new_context(record_video_dir=V, record_video_size={"width": 1280, "height": 800}, viewport={"width": 1280, "height": 800})
    pg = ctx.new_page(); pg.on("dialog", lambda d: d.accept("the excerpt skipped the numeric value"))
    pg.goto("http://127.0.0.1:8765/"); pg.wait_for_timeout(2500); pg.screenshot(path=f"{OUT}/01-start.png")
    pg.locator(".tips button").nth(0).click(); pg.wait_for_selector(".cite"); pg.wait_for_timeout(5000); pg.screenshot(path=f"{OUT}/02-cited-answer.png", full_page=True)
    pg.fill("#q", "What is the speed limit on residential streets in Aurora?"); pg.wait_for_timeout(800); pg.press("#q", "Enter"); pg.wait_for_selector(".a.nf"); pg.wait_for_timeout(4000); pg.screenshot(path=f"{OUT}/03-not-found.png", full_page=True)
    pg.fill("#q", "What is the minimum culvert pipe diameter within the public right-of-way?"); pg.wait_for_timeout(800); pg.press("#q", "Enter"); pg.wait_for_selector(".cite >> nth=2"); pg.wait_for_timeout(4000)
    pg.locator("details summary").last.click(); pg.wait_for_timeout(3000); pg.screenshot(path=f"{OUT}/04-retrieval-path.png", full_page=True)
    pg.locator("button:text('👎')").last.click(); pg.wait_for_timeout(2500); pg.screenshot(path=f"{OUT}/05-feedback.png", full_page=True)
    pg.close(); ctx.close(); b.close()
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", glob.glob(V + "/*.webm")[0], "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{OUT}/demo-walkthrough.mp4"], check=True)
print("ok")
