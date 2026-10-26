import base64, json, os, subprocess, time, urllib.request
import websocket

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
OUT = r"c:\Users\lenovo\.trae-cn\builtin\work\shots"
URL = "http://127.0.0.1:8765/%E5%9B%9B%E7%BA%A7%E9%A1%B9%E7%9B%AE1.html"
PROFILE = r"c:\Users\lenovo\.trae-cn\builtin\work\chromeprofile_cdp"
PORT = 9333

os.makedirs(OUT, exist_ok=True)
proc = subprocess.Popen([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                         "--no-first-run", "--no-default-browser-check",
                         "--remote-debugging-port=%d" % PORT,
                         "--remote-allow-origins=*",
                         "--user-data-dir=" + PROFILE, "about:blank"])

def wait_cdp():
    for _ in range(60):
        try:
            return json.load(urllib.request.urlopen("http://127.0.0.1:%d/json/list" % PORT))
        except Exception:
            time.sleep(0.5)
    raise RuntimeError("cdp not ready")

targets = wait_cdp()
ws = websocket.create_connection(targets[0]["webSocketDebuggerUrl"], timeout=60)
mid = [0]

def cmd(method, params=None):
    mid[0] += 1
    ws.send(json.dumps({"id": mid[0], "method": method, "params": params or {}}))
    while True:
        msg = json.loads(ws.recv())
        if msg.get("id") == mid[0]:
            if "error" in msg:
                raise RuntimeError(method + " -> " + str(msg["error"]))
            return msg.get("result", {})

def evaluate(expr):
    r = cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True})
    if "exceptionDetails" in r:
        print("JS ERROR:", json.dumps(r["exceptionDetails"], ensure_ascii=False)[:500])
    return r["result"].get("value")

def wait_page():
    for _ in range(80):
        ok = evaluate("!!document.getElementById('yl_sec_cards') && document.readyState==='complete' && Array.from(document.images).every(function(i){return i.complete})")
        if ok:
            return
        time.sleep(0.4)
    print("location:", evaluate("location.href"))
    raise RuntimeError("page not ready")

def shot(path, clip, scale=1):
    r = cmd("Page.captureScreenshot", {"format": "png", "captureBeyondViewport": True,
                                      "clip": {"x": clip[0], "y": clip[1], "width": clip[2], "height": clip[3], "scale": scale}})
    with open(os.path.join(OUT, path), "wb") as f:
        f.write(base64.b64decode(r["data"]))
    print("saved", path)

cmd("Page.enable")
cmd("Runtime.enable")

# ---------- 桌面 ----------
cmd("Emulation.setDeviceMetricsOverride", {"width": 1200, "height": 900, "deviceScaleFactor": 1, "mobile": False})
cmd("Page.navigate", {"url": URL})
wait_page()
time.sleep(1.2)
m = evaluate("JSON.stringify({r:['yl_sec_cards','yl_sec_feature','yl_sec_list'].map(function(id){var b=document.getElementById(id).getBoundingClientRect();return {id:id,top:Math.round(b.top+window.scrollY),height:Math.round(b.height),left:Math.round(b.left),width:Math.round(b.width)}}),doc:document.documentElement.scrollHeight})")
data = json.loads(m)
print(data)

shot("ch_desktop_full.png", (0, 0, 1200, data["doc"]), 1)
for item in data["r"]:
    shot("impl_%s.png" % item["id"], (item["left"] - 12, item["top"], item["width"] + 24, item["height"]), 2)

# ---------- 移动端 ----------
cmd("Emulation.setDeviceMetricsOverride", {"width": 390, "height": 844, "deviceScaleFactor": 1, "mobile": True})
cmd("Page.navigate", {"url": URL})
wait_page()
time.sleep(1.2)
m2 = evaluate("JSON.stringify({r:['yl_sec_cards','yl_sec_feature','yl_sec_list'].map(function(id){var b=document.getElementById(id).getBoundingClientRect();return {id:id,top:Math.round(b.top+window.scrollY),height:Math.round(b.height),left:Math.round(b.left),width:Math.round(b.width)}}),doc:document.documentElement.scrollHeight})")
d2 = json.loads(m2)
print(d2)
shot("ch_mobile_full.png", (0, 0, 390, d2["doc"]), 1)

ws.close()
proc.terminate()
print("done")
