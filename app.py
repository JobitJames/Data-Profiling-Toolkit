import os
import time
from flask import Flask, request, render_template, send_file
import pandas as pd
from ydata_profiling import ProfileReport

app = Flask(__name__)

BASE_DIR = os.path.dirname(__file__)  # Get the current script's directory
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

# Ensure necessary directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)  # Fix: Ensure reports folder is created

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if not file or not file.filename.endswith(".csv"):
            return "Invalid file type. Please upload a CSV file.", 400

        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        print(f"✅ File uploaded successfully: {filepath}")  # Debugging

        # Read CSV
        try:
            df = pd.read_csv(filepath, low_memory=False)
            print(df.head())  # Debugging: Show first 5 rows
        except Exception as e:
            print(f"❌ Error reading CSV: {e}")
            return f"Error reading CSV file: {e}", 500

        # Generate unique report filename
        report_filename = f"report_{int(time.time())}.html"
        report_path = os.path.join(REPORT_FOLDER, report_filename)

        # Generate profiling report
        try:
            profile = ProfileReport(df, explorative=True)
            print("✅ ProfileReport object created successfully")  # Debugging
            print(f"Attempting to save report to: {report_path}")
            profile.to_file(report_path)
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            return f"Error generating report: {e}", 500

        # Ensure file exists before sending
        time.sleep(2)  # Small delay
        if not os.path.exists(report_path):
            print("❌ ERROR: Report file is missing after generation!")
            print("Current files in reports/:", os.listdir(REPORT_FOLDER))  # Debugging
            return f"Error: Report file {report_filename} was not found!", 500

        print(f"✅ Report successfully saved at: {report_path}")
        print("✅ Sending report for download...")
        return send_file(report_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
