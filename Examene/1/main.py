from checker import build_url, is_https, show_response, check_site,scan_sites, check_headers, retry_check

# Partea 1: apeluri pentru build_url și is_https
print(build_url("example.com", "/login"))
print(build_url("example.com", "login"))
print(is_https("https://example.com"))
print(is_https("http://example.com"))

# Partea 2: apeluri pentru show_response
show_response("https://httpbin.org/html")
show_response("https://httpbin.org/status/404")
# Partea 3: apeluri pentru check_site
check_site("https://httpbin.org/html")
check_site("https://httpbin.org/status/404")
# Partea 4: apelul scan_sites()
scan_sites()
# Partea 5: apeluri pentru check_headers
check_headers("https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff")
check_headers("https://httpbin.org/response-headers?x-frame-options=DENY")
# Partea 6: apeluri pentru retry_check
retry_check("https://httpbin.org/status/200,500")
