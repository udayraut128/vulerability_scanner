from flask import Flask, request, render_template, send_file
from scanner.crawler import crawl_site
from scanner.vulns import check_sql_injection, check_xss
from scanner.server_info import get_server_info, check_ip_type, is_safe
from scanner.ssl_info import get_ssl_info
from scanner.portscan import port_scan
from scanner.geo import get_geo_location
from fpdf import FPDF

app = Flask(__name__)

def severity_score(results):
    if results["SQL Injection"] or results["XSS"]:
        return "High"
    elif results["Safety"] == "Potentially Unsafe":
        return "Medium"
    else:
        return "Low"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        target = request.form["url"]
        hostname = target.split("//")[-1].split("/")[0]
        ip, ip_type = check_ip_type(target)
        ssl_info = get_ssl_info(hostname)
        open_ports = port_scan(hostname)
        geo = get_geo_location(ip)

        results = {
            "SQL Injection": check_sql_injection(target),
            "XSS": check_xss(target),
            "Server": get_server_info(target),
            "IP Address": ip,
            "IP Type": ip_type,
            "Safety": is_safe(target),
            "SSL Info": ssl_info,
            "Open Ports": open_ports,
            "Geo Location": geo
        }
        results["Severity"] = severity_score(results)

        # Export PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)

        # Headline with URL
        pdf.cell(200, 10, txt=f"Web Vulnerability Scan Report for this:- {target}", ln=True, align="C")

        pdf.set_font("Arial", size=12)
        pdf.ln(10)  # line break

        # Add results to PDF
        for k, v in results.items():
            pdf.multi_cell(0, 10, f"{k}: {v}")

        # Save PDF outside the loop
        pdf.output("scan_report.pdf")

        return render_template("report.html", results=results)
    return render_template("index.html")

@app.route("/download")
def download_report():
    return send_file("scan_report.pdf", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)