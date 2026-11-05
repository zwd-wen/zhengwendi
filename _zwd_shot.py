import json, subprocess, sys, time, urllib.request, base64, os, tempfile

CHROME = os.environ.get("ZWD_BROWSER", r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def shot(url, out, width, height, full=False, scale=1):
    port = 9333 if "chrome" in os.path.basename(CHROME).lower() else 9334
    profile = os.path.join(tempfile.gettempdir(), "zwd_" + os.path.basename(CHROME).lower() + "_profile")
    proc = subprocess.Popen([
        CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
        f"--remote-debugging-port={port}", "--remote-allow-origins=*",
        f"--user-data-dir={profile}", "about:blank"
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for _ in range(60):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1)
                break
            except Exception:
                time.sleep(0.2)
        targets = json.load(urllib.request.urlopen(f"http://127.0.0.1:{port}/json/list"))
        ws_url = [t for t in targets if t["type"] == "page"][0]["webSocketDebuggerUrl"]
        import websocket
        ws = websocket.create_connection(ws_url, timeout=30)
        i = [0]

        def send(method, params=None):
            i[0] += 1
            ws.send(json.dumps({"id": i[0], "method": method, "params": params or {}}))
            while True:
                msg = json.loads(ws.recv())
                if msg.get("id") == i[0]:
                    return msg.get("result", {})

        send("Page.enable")
        send("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": height, "deviceScaleFactor": scale, "mobile": width < 600
        })
        send("Page.navigate", {"url": url})
        time.sleep(2.5)
        if full:
            lm = send("Page.getLayoutMetrics")["cssContentSize"]
            h = int(lm["height"])
            send("Emulation.setDeviceMetricsOverride", {
                "width": width, "height": h, "deviceScaleFactor": scale, "mobile": width < 600
            })
            time.sleep(0.8)
            res = send("Page.captureScreenshot", {
                "format": "png", "captureBeyondViewport": True,
                "clip": {"x": 0, "y": 0, "width": width, "height": h, "scale": 1}
            })
        else:
            res = send("Page.captureScreenshot", {"format": "png"})
        with open(out, "wb") as f:
            f.write(base64.b64decode(res["data"]))
        print("saved", out)
        ws.close()
    finally:
        proc.terminate()


if __name__ == "__main__":
    args = sys.argv[1:]
    url, out, w, h = args[0], args[1], int(args[2]), int(args[3])
    full = len(args) > 4 and args[4] == "full"
    shot(url, out, w, h, full)
