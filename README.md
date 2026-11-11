# Bypass-Four03 (Python Edition)

A Python-based security tool designed to automate techniques for bypassing HTTP `403 Forbidden` errors using various path manipulation, header injection, HTTP methods, and protocol version fuzzing.

> **Credits & Acknowledgement:**
> This is a pure Python port and adaptation of the original Bash tool **[Bypass-Four03](https://github.com/nazmul-ethi/Bypass-Four03)** created by **[nazmul__ethi](https://github.com/nazmul-ethi)**. This repository contains *only* the Python conversion to allow native execution on Windows (PowerShell/Command Prompt), macOS, and Linux without requiring a Bash environment.

---

## Features

- **Path Fuzzing:** Tests dozens of path traversal and manipulation patterns (e.g., `../`, `//`, `./`, URL encodings, extensions).
- **Header Fuzzing:** Injects common IP spoofing and proxy bypass headers (`X-Forwarded-For`, `X-Original-URL`, `X-Rewrite-URL`, `X-Custom-IP-Authorization`, etc.).
- **HTTP Method Fuzzing:** Tests alternative HTTP verbs (`PUT`, `POST`, `CONNECT`, `TRACE`, `PATCH`, `HEAD`).
- **HTTP Protocol Version Fuzzing:** Tests alternative HTTP versions to look for routing anomalies.

---

## Prerequisites

Make sure you have Python 3 installed on your system.

---

## Installation

1. **Clone the repository or download the script:**

   ```bash
   git clone https://github.com/nazmul-ethi/Bypass-Four03.git
   cd Bypass-Four03
   ```

2. **Install the required dependencies:**

   ```bash
   pip install requests
   ```

---

## Usage

Run the script from your terminal using Python 3, providing the target base URL and the restricted path you want to bypass.

```bash
python3 bypass.py [URL] [path]
```

### Example

```bash
python3 bypass.py https://example.com admin
```

---

## Status Code Color Legend

The tool color-codes HTTP responses in the terminal for quick analysis:

| Status Code | Meaning |
|-------------|---------|
| **200** | Success (Potential Bypass Found!) |
| **403 / 404 / 400** | Forbidden / Not Found / Bad Request |
| **405** | Method Not Allowed |
| **500** | Internal Server Error |

---

## Disclaimer

> **Legal Notice:** This tool is created for educational purposes and authorized security assessments only. Do not use it against targets without explicit prior permission. The authors assume no liability and are not responsible for any misuse or damage caused by this program.
