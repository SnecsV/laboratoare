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

# Partea 4: apelul scan_sites()
# Partea 5: apeluri pentru check_headers
# Partea 6: apeluri pentru retry_check
