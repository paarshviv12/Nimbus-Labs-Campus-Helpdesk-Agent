#!/usr/bin/env python3
"""Raw JSON-RPC client over stdio: spawns server.py and records every message sent/received.
Writes logs/trace.jsonl (one record per message) and prints a readable trace."""
import json, subprocess, sys, select, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOG = ROOT / "logs" / "trace.jsonl"


class Rpc:
    def __init__(self, tag):
        self.tag = tag
        self.p = subprocess.Popen([sys.executable, str(ROOT / "server.py")],
                                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                  text=True, bufsize=1, cwd=ROOT)

    def _log(self, direction, msg):
        rec = {"session": self.tag, "dir": direction, "msg": msg}
        with open(LOG, "a") as f:
            f.write(json.dumps(rec) + "\n")
        print(f"[{self.tag}] {direction} {json.dumps(msg)}")

    def send(self, msg, wait=True):
        self._log("C->S", msg)
        self.p.stdin.write(json.dumps(msg) + "\n"); self.p.stdin.flush()
        if not wait or "id" not in msg:
            return None
        end = time.time() + 15
        while time.time() < end:
            r, _, _ = select.select([self.p.stdout], [], [], 0.5)
            if r:
                line = self.p.stdout.readline()
                if not line:
                    break
                resp = json.loads(line)         # stdout must be pure JSON-RPC, else this raises
                self._log("S->C", resp)
                return resp
        raise TimeoutError(f"no response to {msg}")

    def close(self):
        self.p.stdin.close()                    # spec: client closes stdin to shut down stdio server
        try:
            self.p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.p.terminate()
        err = self.p.stderr.read()
        print(f"[{self.tag}] server exit code={self.p.returncode}; stderr bytes={len(err)}")
        (ROOT / "logs" / f"stderr_{self.tag}.log").write_text(err)


def main():
    LOG.write_text("")
    # Session 1: normal flow
    s = Rpc("main")
    s.send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-11-25", "capabilities": {},
        "clientInfo": {"name": "trace-client", "version": "0.1"}}})
    s.send({"jsonrpc": "2.0", "method": "notifications/initialized"}, wait=False)
    s.send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    s.send({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "get_timetable", "arguments": {"batch": "B1", "day": "Wed"}}})
    s.send({"jsonrpc": "2.0", "id": 4, "method": "tools/call",
            "params": {"name": "get_fee_status", "arguments": {"student_id": "S9999"}}})   # failure case
    s.send({"jsonrpc": "2.0", "id": 5, "method": "tools/call",
            "params": {"name": "delete_everything", "arguments": {}}})                      # unknown tool
    s.send({"jsonrpc": "2.0", "id": 6, "method": "resources/list"})
    s.send({"jsonrpc": "2.0", "id": 7, "method": "resources/read", "params": {"uri": "hostel://rules"}})
    s.close()
    # Session 2: what happens with a made-up version like the invalid date "2025-02-30"?
    s2 = Rpc("badversion")
    s2.send({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
        "protocolVersion": "2025-02-30", "capabilities": {},
        "clientInfo": {"name": "trace-client", "version": "0.1"}}})
    s2.close()


if __name__ == "__main__":
    main()
