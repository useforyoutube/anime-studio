"""Vault: the studio code lives encrypted in vault.enc (Fernet). Only a GitHub run with the REPO_KEY secret can
open it, so the repo can be public. python vault/boot.py open | seal"""
import base64
import io
import os
import sys
import tarfile

from cryptography.fernet import Fernet

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VAULT = os.path.join(ROOT, "vault.enc")
DIRS = ["studio"]


def fernet():
    key = os.environ.get("REPO_KEY")
    if not key:
        sys.exit("REPO_KEY secret missing - cannot open the vault")
    return Fernet(key.encode())


def seal():
    if not os.path.isdir(os.path.join(ROOT, "studio")):
        raise SystemExit("refusing to seal: studio/ missing")
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        for d in DIRS:
            tar.add(os.path.join(ROOT, d), arcname=d,
                    filter=lambda m: None if "__pycache__" in m.name else m)
    open(VAULT, "wb").write(base64.urlsafe_b64decode(fernet().encrypt(buf.getvalue())))
    print(f"vault sealed ({os.path.getsize(VAULT) / 1e3:.0f} KB)")


def open_():
    data = fernet().decrypt(base64.urlsafe_b64encode(open(VAULT, "rb").read()))
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        tar.extractall(ROOT, filter="data")
    print("vault opened")


if __name__ == "__main__":
    {"open": open_, "seal": seal}[sys.argv[1]]()
