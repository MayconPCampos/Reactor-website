from app import app
from flask import render_template


@app.route("/admin")
def admin_dashboard():
    return render_template("admin/admin_dashboard.html")
