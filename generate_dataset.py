import csv
import random

urls = []

# ─── CATEGORY 1: LOCALHOST ATTACKS ───
localhost_bases = [
    "127.0.0.1", "localhost", "127.1",
    "0.0.0.0", "0177.0.0.1", "0x7f000001",
    "2130706433", "[::1]", "127.000.000.001"
]
paths = [
    "/admin", "/config", "/secret", "/internal",
    "/api", "/dashboard", "/manager", "/console",
    "/status", "/health", "/debug", "/env",
    "/users", "/backup", "/panel", "/private",
    "/restricted", "/login", "/setup", "/install",
    "/phpmyadmin", "/wp-admin", "/cpanel", "/webmail"
]
ports = [
    "", ":8080", ":3000", ":8443", ":9090",
    ":8888", ":4040", ":5000", ":22", ":21",
    ":25", ":3306", ":5432", ":6379", ":27017"
]

for base in localhost_bases:
    for path in paths:
        for port in ports[:6]:
            urls.append({
                "url": f"http://{base}{port}{path}",
                "label": "SSRF"
            })

# ─── CATEGORY 2: AWS METADATA ───
aws_paths = [
    "/latest/meta-data/",
    "/latest/meta-data/iam/",
    "/latest/meta-data/iam/security-credentials/",
    "/latest/meta-data/iam/security-credentials/admin",
    "/latest/meta-data/iam/security-credentials/ec2-default-ssm",
    "/latest/meta-data/hostname",
    "/latest/meta-data/public-ipv4",
    "/latest/meta-data/local-ipv4",
    "/latest/meta-data/ami-id",
    "/latest/meta-data/instance-id",
    "/latest/meta-data/instance-type",
    "/latest/meta-data/network/",
    "/latest/meta-data/placement/",
    "/latest/meta-data/reservation-id",
    "/latest/meta-data/security-groups",
    "/latest/meta-data/instance-action",
    "/latest/user-data/",
    "/latest/dynamic/instance-identity/document",
    "/latest/api/token",
    "/openstack/latest/meta_data.json",
    "/openstack/",
]

for path in aws_paths:
    urls.append({"url": f"http://169.254.169.254{path}", "label": "SSRF"})
    urls.append({"url": f"https://169.254.169.254{path}", "label": "SSRF"})
    urls.append({"url": f"http://169.254.169.254:80{path}", "label": "SSRF"})
    urls.append({"url": f"http://169.254.169.254:8080{path}", "label": "SSRF"})

# ─── CATEGORY 3: AZURE AND GCP METADATA ───
azure_urls = [
    "http://169.254.169.254/metadata/instance",
    "http://169.254.169.254/metadata/identity",
    "http://169.254.169.254/metadata/instance?api-version=2021-02-01",
    "http://169.254.169.254/metadata/instance?api-version=2020-09-01",
    "http://169.254.169.254/metadata/instance?api-version=2019-11-01",
    "http://169.254.169.254/metadata/identity/oauth2/token",
    "http://169.254.169.254/metadata/scheduledevents",
    "http://169.254.169.254/metadata/attested/document",
]

gcp_urls = [
    "http://metadata.google.internal/computeMetadata/v1/",
    "http://metadata.google.internal/computeMetadata/v1/instance/",
    "http://metadata.google.internal/computeMetadata/v1/project/",
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/",
    "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
    "http://metadata.google.internal/computeMetadata/v1/project/project-id",
    "http://metadata.google.internal/computeMetadata/v1/instance/hostname",
    "http://metadata.google.internal/computeMetadata/v1/instance/id",
    "http://metadata.google.internal/computeMetadata/v1/instance/zone",
    "http://metadata.google.internal/",
]

for url in azure_urls + gcp_urls:
    urls.append({"url": url, "label": "SSRF"})

# ─── CATEGORY 4: PRIVATE IP ATTACKS ───
private_ips = []

for i in range(0, 100):
    private_ips.append(f"192.168.{i % 10}.{i + 1}")
for i in range(0, 80):
    private_ips.append(f"10.0.{i % 20}.{i + 1}")
for i in range(0, 50):
    private_ips.append(f"172.16.{i % 16}.{i + 1}")
for i in range(0, 30):
    private_ips.append(f"172.31.{i}.1")
for i in range(0, 20):
    private_ips.append(f"10.10.{i}.1")

private_paths = [
    "/admin", "/internal", "/api", "/config",
    "/secret", "/database", "/backup", "/panel",
    "/dashboard", "/management", "/console", "/status"
]

for ip in private_ips:
    for path in private_paths[:4]:
        urls.append({
            "url": f"http://{ip}{path}",
            "label": "SSRF"
        })

# ─── CATEGORY 5: BYPASS TECHNIQUES ───
bypass_urls = [
    # Hex encoding
    "http://0x7f000001/admin",
    "http://0x7f000001/secret",
    "http://0x7f000001/config",
    "http://0x7f000001/internal",
    "http://0x7f000001/dashboard",
    # Decimal encoding
    "http://2130706433/admin",
    "http://2130706433/secret",
    "http://2130706433/config",
    "http://2130706433/internal",
    # URL encoding
    "http://%31%32%37%2e%30%2e%30%2e%31/admin",
    "http://%31%32%37%2e%30%2e%30%2e%31/secret",
    "http://%31%36%39%2e%32%35%34%2e%31%36%39%2e%32%35%34/credentials",
    # Octal
    "http://0177.0.0.1/admin",
    "http://0177.0.0.1/secret",
    "http://0177.0.0.1/config",
    # Shortened
    "http://127.1/admin",
    "http://127.1/config",
    "http://127.1/secret",
    "http://127.1/internal",
    "http://127.1/dashboard",
    # IPv6
    "http://[::1]/admin",
    "http://[::1]/secret",
    "http://[::1]/config",
    "http://[0:0:0:0:0:0:0:1]/admin",
    "http://[0:0:0:0:0:ffff:127.0.0.1]/admin",
    "http://[0:0:0:0:0:ffff:7f00:0001]/admin",
    # Zero padded
    "http://127.000.000.001/admin",
    "http://127.000.000.001/secret",
    # DNS based bypass
    "http://127.0.0.1.nip.io/admin",
    "http://127.0.0.1.xip.io/admin",
    "http://localtest.me/admin",
    # Protocol bypass
    "file:///etc/passwd",
    "file:///etc/shadow",
    "file:///proc/self/environ",
    "file:///proc/self/cmdline",
    "file:///windows/system32/drivers/etc/hosts",
    "dict://127.0.0.1:11211/",
    "gopher://127.0.0.1:6379/",
    "gopher://127.0.0.1:3306/",
    "sftp://127.0.0.1/secret",
    "ldap://127.0.0.1/",
    # Mixed
    "http://0x7f.0x0.0x0.0x1/admin",
    "http://2852039166/admin",
    "http://0/admin",
    "http://127.0.0.1%2fadmin",
    "http://127.0.0.1%2fconfig",
]

for url in bypass_urls:
    urls.append({"url": url, "label": "SSRF"})

# ─── CATEGORY 6: BENIGN SAFE URLS ───
safe_domains = [
    "google.com", "youtube.com", "facebook.com",
    "twitter.com", "instagram.com", "linkedin.com",
    "github.com", "stackoverflow.com", "wikipedia.org",
    "bbc.co.uk", "cnn.com", "reddit.com",
    "amazon.com", "microsoft.com", "apple.com",
    "netflix.com", "spotify.com", "medium.com",
    "nytimes.com", "theguardian.com", "forbes.com",
    "techcrunch.com", "wired.com", "freecodecamp.org",
    "python.org", "nodejs.org", "djangoproject.com",
    "flask.palletsprojects.com", "reactjs.org", "vuejs.org",
    "angular.io", "mongodb.com", "postgresql.org",
    "mysql.com", "docker.com", "kubernetes.io",
    "aws.amazon.com", "cloud.google.com", "azure.microsoft.com",
    "owasp.org", "nist.gov", "cloudflare.com",
    "digitalocean.com", "heroku.com", "vercel.com",
    "netlify.com", "stripe.com", "twilio.com",
    "sendgrid.com", "zendesk.com", "shopify.com",
]

safe_paths = [
    "/", "/news", "/about", "/contact", "/search",
    "/home", "/blog", "/docs", "/products", "/services",
    "/login", "/signup", "/profile", "/settings", "/help",
    "/support", "/terms", "/privacy", "/faq", "/careers",
    "/api/docs", "/download", "/features", "/pricing",
    "/blog/latest", "/tutorials", "/examples", "/community",
    "/forum", "/newsletter", "/resources", "/partners",
    "/press", "/events", "/webinar", "/case-studies",
    "/documentation", "/changelog", "/status", "/security",
]

for domain in safe_domains:
    for path in safe_paths:
        urls.append({
            "url": f"https://{domain}{path}",
            "label": "SAFE"
        })

# ─── REMOVE DUPLICATES ───
seen = set()
unique_urls = []
for item in urls:
    if item["url"] not in seen:
        seen.add(item["url"])
        unique_urls.append(item)
urls = unique_urls

print(f"After removing duplicates: {len(urls)}")

# ─── SPLIT AND BALANCE ───
random.shuffle(urls)

ssrf_urls = [u for u in urls if u["label"] == "SSRF"]
safe_urls = [u for u in urls if u["label"] == "SAFE"]

print(f"Total unique SSRF: {len(ssrf_urls)}")
print(f"Total unique SAFE: {len(safe_urls)}")


final_ssrf = ssrf_urls[:2000]
final_safe = safe_urls[:2000]
final = final_ssrf + final_safe
random.shuffle(final)

# ─── SAVE TO CSV ───
with open("data/urls.csv", "w",
          newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f,
                            fieldnames=["url", "label"])
    writer.writeheader()
    writer.writerows(final)

print(f"\nDataset saved to data/urls.csv")
print(f"Total URLs: {len(final)}")
print(f"SSRF: {len(final_ssrf)}")