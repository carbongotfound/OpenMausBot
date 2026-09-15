from pathlib import Path

path = Path("server/index.ts")
text = path.read_text()
old = 'void startTurn(bot.id, resumed ? "Review the returned teammate results and continue the original request." : "Complete the addressed teammate request.", {'
new = 'void startTurn(bot.id, resumed ? "Review the returned teammate results and continue the original request." : `Complete the addressed teammate request:\\n\\n${node.text}`, {'
count = text.count(old)
if count != 1:
    raise SystemExit(f"expected one coordinated startTurn call, found {count}")
path.write_text(text.replace(old, new, 1))
