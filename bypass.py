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
    elif code_str in ["403", "404", "400", "401"]:
        return f"{Colors.RED}{code_str}{Colors.RESET}"
    elif code_str.startswith("3"):
        return f"{Colors.BLUE}{code_str}{Colors.RESET}"
    elif code_str in ["405"]:
        return f"{Colors.YELLOW}{code_str}{Colors.RESET}"
    elif code_str == "500":
        return f"{Colors.VIOLET}{code_str}{Colors.RESET}"
    else:
        return f"{Colors.YELLOW}{code_str}{Colors.RESET}"

def print_banner():
    print(f"{Colors.YELLOW}")
    print("  Bypass-Four03 (Python Edition)")
    print("                    By nazmul__ethi (Converted & Updated)")
    print(f"{Colors.RESET}\n")

if len(sys.argv) < 3:
    print(f"Usage: python {sys.argv[0]} [URL] [path]")
    print(f"Example: python {sys.argv[0]} https://example.com admin")
    sys.exit(1)

target_url = sys.argv[1].rstrip('/')
path = sys.argv[2].strip('/')

print_banner()
print(f"Target: {target_url}/{path}\n")

def handle_response(url, r, extra_info=""):
    status = colorize_code(r.status_code)
    size = len(r.content)
    redirect_info = ""
    
    # If it's a redirect, grab the Location header
    if 300 <= r.status_code < 400 and 'Location' in r.headers:
        redirect_info = f" --> Redirects to: {Colors.CYAN}{r.headers['Location']}{Colors.RESET}"
        
    print(f"  --> {url} {extra_info} Response: [{status}] Size: {size}{redirect_info}")

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
        r = requests.get(p, verify=False, allow_redirects=False, timeout=5)
        handle_response(p, r)
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
            r = requests.get(base_target, headers=headers, verify=False, allow_redirects=False, timeout=5)
            handle_response(base_target, r, extra_info=f"[{h}: {val}]")
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
        r = requests.get(target_url, headers=sh, verify=False, allow_redirects=False, timeout=5)
        handle_response(target_url, r, extra_info=f"[Headers: {sh}]")
    except Exception as e:
        pass

# 3. HTTP Method Fuzzing
print(f"\n{Colors.VIOLET}=== HTTP METHOD FUZZING ==={Colors.RESET}")
methods = ["PUT", "POST", "CONNECT", "TRACE", "PATCH", "HEAD"]
for m in methods:
    try:
        r = requests.request(m, base_target, verify=False, allow_redirects=False, timeout=5)
        handle_response(base_target, r, extra_info=f"-X {m}")
    except Exception as e:
        print(f"  --> {base_target} -X {m} Error: {e}")
