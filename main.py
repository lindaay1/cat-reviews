#!/usr/bin/env python3
"""Cat Reviews Its Human — make.fun program entry.

Competition: u-motasimfuad-make-the-ai-judge-laugh-cat-reviews-its-42a34990.

A one-star review, in one line under 200 characters, from a cat about
its human. The approved review lives in the CONFIG table below; this
script checks it against the gate, files it as entry.txt with a second
copy at cat-review.txt, and proves the copies match by digest.
"""

import hashlib
import sys

CONFIG = {
    "text": (
        "One star. The human opens the good food at 3 a.m. only "
        "when I scream, then sleeps through my 5 a.m. performance "
        "review."
    ),
    "min_chars": 1,
    "max_chars": 200,
    "primary": "entry.txt",
    "mirror": "cat-review.txt",
}


def verify_only():
    """Check the files on disk against the approved review, write nothing."""
    import hashlib as _hl

    blob = CONFIG["text"].encode("utf-8")
    want = _hl.sha256(blob).hexdigest()
    for name in (CONFIG["primary"], CONFIG["mirror"]):
        with open(name, "rb") as fh:
            got = _hl.sha256(fh.read()).hexdigest()
        if got != want:
            print("verify fail: %s differs" % name, file=sys.stderr)
            return 1
    print("verify ok: %d chars, sha256 %s" % (len(CONFIG["text"]), want))
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        return verify_only()
    text = CONFIG["text"]
    problems = []
    if not isinstance(text, str):
        problems.append("review is not text")
    else:
        if not CONFIG["min_chars"] <= len(text) <= CONFIG["max_chars"]:
            problems.append(
                "review is %d chars, gate is %d-%d"
                % (len(text), CONFIG["min_chars"], CONFIG["max_chars"])
            )
        if text.strip() == "":
            problems.append("review is only whitespace")
        if any(c in text for c in ("\n", "\r")):
            problems.append("review must be a single line")
    if problems:
        for p in problems:
            print("gate fail: " + p, file=sys.stderr)
        return 1
    blob = text.encode("utf-8")
    for name in (CONFIG["primary"], CONFIG["mirror"]):
        with open(name, "wb") as fh:
            fh.write(blob)
    digests = {}
    for name in (CONFIG["primary"], CONFIG["mirror"]):
        with open(name, "rb") as fh:
            digests[name] = hashlib.sha256(fh.read()).hexdigest()
    want = hashlib.sha256(blob).hexdigest()
    if digests[CONFIG["primary"]] != want or digests[CONFIG["mirror"]] != want:
        print("gate fail: files on disk differ", file=sys.stderr)
        return 1
    print("wrote %d chars, sha256 %s" % (len(text), want))
    return 0


if __name__ == "__main__":
    sys.exit(main())
