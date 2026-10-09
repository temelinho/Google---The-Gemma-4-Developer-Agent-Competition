"""
resolved=True gorevlerin traces'ini alir, LoRA egitimi icin SFT jsonl'e cevirir.
Gercek harness alanlarina dayanir: result.resolved, results_dir/traces/.

Kullanim:
  python 02_filter_build_sft.py <results_dir> <out.jsonl>
Birden cok kosuyu birlestirmek icin her results_dir icin tekrar calistir (append).
"""
import json, sys, pathlib

results_dir = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "training/results/gen_01")
out_path    = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "training/sft.jsonl")

# PASS gorevler: task_results.jsonl her satir bir gorev sonucu (resolved alani)
passed = []
tr = results_dir / "task_results.jsonl"
with open(tr, encoding="utf-8") as f:
    for line in f:
        r = json.loads(line)
        if r.get("resolved") is True:
            passed.append(r.get("instance_id") or r.get("id"))
print(f"[{results_dir.name}] PASS gorev: {len(passed)}")

# Her PASS gorevin trace'ini SFT ornegine cevir
# trace: results_dir/traces/trace_<instance_id>.json  (SessionTrace / ATIF)
n = 0
with open(out_path, "a", encoding="utf-8") as out:   # append: cok kosu birlestir
    for iid in passed:
        tf = results_dir / "traces" / f"trace_{iid}.json"
        if not tf.exists():
            continue
        trace = json.loads(tf.read_text(encoding="utf-8"))
        # trace["steps"] -> messages (system/user/assistant+tool_call/tool_response)
        # Gercek alan adlari ilk kosudan sonra tek bir trace acilip netlestirilecek.
        messages = trace.get("messages") or trace.get("steps")  # TODO: teyit
        out.write(json.dumps({"instance_id": iid, "messages": messages},
                             ensure_ascii=False) + "\n")
        n += 1
print(f"SFT'ye eklenen: {n} -> {out_path}")
