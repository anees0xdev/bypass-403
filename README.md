# Bypass-Four03 (Python Edition)

A Python-based security tool designed to automate techniques for bypassing HTTP `403 Forbidden` errors using various path manipulation, header injection, HTTP methods, and protocol version fuzzing.

> **Credits & Acknowledgement:**  
> This is a pure Python port and adaptation of the original Bash tool **[Bypass-Four03](https://github.com/nazmul-ethi/Bypass-Four03)** created by **[nazmul__ethi](https://github.com/nazmul-ethi)**. This repository contains *only* the Python conversion to allow native execution on Windows (PowerShell/Command Prompt) and cross-platform environments without requiring WSL or a Linux bash shell.

---

## Features

- **Path Fuzzing:** Tests dozens of path traversal and manipulation patterns (e.g., `../`, `//`, `./`, URL encodings `%00`, `%2e%2e%2f`, etc.).
- **Header Fuzzing:** Injects common IP spoofing and proxy bypass headers (`X-Forwarded-For`, `X-Original-URL`, `X-Rewrite-URL`, `X-Custom-IP-Authorization`, etc.).
- **HTTP Method Fuzzing:** Tests alternative HTTP verbs (`PUT`, `POST`, `CONNECT`, `TRACE`, `PATCH`, `HEAD`).
- **HTTP Protocol Version Fuzzing:** Tests alternative HTTP versions (`0.9`, `1.0`, `1.1`).

---

## Prerequisites

Make sure you have Python 3 installed along with the `requests` library.

```bash
pip install requests