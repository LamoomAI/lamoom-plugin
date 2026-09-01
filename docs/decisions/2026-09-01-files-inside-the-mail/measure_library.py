# The command behind every number in pricing.md.
#   manage_file action=list scope=user   -> library_listing.json
#   python3 measure_library.py
import json, re, collections
d = json.load(open("library_listing.json"))
f = d["files"]
def size(s):
    m = re.search(r"\((\d+(?:\.\d+)?)(KB|MB|B)\)$", s)
    if not m: return None
    v, u = float(m.group(1)), m.group(2)
    return v*1024 if u == "KB" else v*1048576 if u == "MB" else v
ok = [(x.rsplit(" (", 1)[0], size(x)) for x in f]
ok = [(p, s) for p, s in ok if s is not None]
tot = sum(s for _, s in ok)
folders = collections.Counter(p.rsplit("/", 1)[0] for p, _ in ok)
print("files listed        ", len(f))
print("total               %.1f MB" % (tot/1048576))
print("average per file    %.0f KB" % (tot/len(ok)/1024))
print("largest             %.1f MB  %s" % (max(s for _, s in ok)/1048576, max(ok, key=lambda t: t[1])[0]))
print("over 7MB            ", sum(1 for _, s in ok if s > 7*1048576))
print("over 1MB            ", sum(1 for _, s in ok if s > 1048576))
print("folders             ", len(folders))
print("folders over 10 files", sum(1 for _, v in folders.items() if v > 10))
# NB: the listing's "next" field is a prose instruction to the agent, not a pagination cursor.
# Whether 1560 files is the whole library is therefore unknown from this output.
