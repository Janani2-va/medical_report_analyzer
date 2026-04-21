import pytesseract
import re

# 🔧 Set Tesseract path (change if needed)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# 🧾 OCR Function
def extract_text(img):
    return pytesseract.image_to_string(img)


# 🔍 Extract multiple lab parameters
def extract_values(text):
    data = {}

    patterns = {
        "glucose": r'Glucose[:\s]+(\d+)',
        "hemoglobin": r'Hemoglobin[:\s]+(\d+\.?\d*)',
        "cholesterol": r'Cholesterol[:\s]+(\d+)',
        "bp": r'(\d{2,3})/(\d{2,3})',
        "platelets": r'Platelets[:\s]+(\d+)',
        "wbc": r'(WBC|White Blood Cells)[:\s]+(\d+)',
        "rbc": r'(RBC|Red Blood Cells)[:\s]+(\d+\.?\d*)'
    }

    for key, pattern in patterns.items():
        match = re.findall(pattern, text, re.IGNORECASE)

        if match:
            if key == "bp":
                systolic, diastolic = match[0]
                data[key] = (int(systolic), int(diastolic))

            elif key in ["wbc", "rbc"]:
                data[key] = float(match[0][1])  # second group

            else:
                data[key] = float(match[0])

    return data


# 📊 Individual Analysis Functions

def analyze_glucose(val):
    if val < 70:
        return "Low"
    elif val <= 140:
        return "Normal"
    else:
        return "High"


def analyze_hemoglobin(val):
    if val < 12:
        return "Low"
    elif val <= 17:
        return "Normal"
    else:
        return "High"


def analyze_cholesterol(val):
    if val < 200:
        return "Normal"
    elif val <= 240:
        return "Borderline"
    else:
        return "High"


def analyze_bp(bp):
    sys, dia = bp
    if sys < 90 or dia < 60:
        return "Low BP"
    elif sys <= 120 and dia <= 80:
        return "Normal BP"
    elif sys <= 140 and dia <= 90:
        return "Pre-High BP"
    else:
        return "High BP"


def analyze_platelets(val):
    if val < 150000:
        return "Low"
    elif val <= 450000:
        return "Normal"
    else:
        return "High"


def analyze_wbc(val):
    if val < 4000:
        return "Low"
    elif val <= 11000:
        return "Normal"
    else:
        return "High"


def analyze_rbc(val):
    if val < 4.0:
        return "Low"
    elif val <= 6.0:
        return "Normal"
    else:
        return "High"


# 🧠 Final Combined Analysis
def analyze_report(data):
    results = {}

    if "glucose" in data:
        results["Glucose"] = analyze_glucose(data["glucose"])

    if "hemoglobin" in data:
        results["Hemoglobin"] = analyze_hemoglobin(data["hemoglobin"])

    if "cholesterol" in data:
        results["Cholesterol"] = analyze_cholesterol(data["cholesterol"])

    if "bp" in data:
        results["Blood Pressure"] = analyze_bp(data["bp"])

    if "platelets" in data:
        results["Platelets"] = analyze_platelets(data["platelets"])

    if "wbc" in data:
        results["WBC"] = analyze_wbc(data["wbc"])

    if "rbc" in data:
        results["RBC"] = analyze_rbc(data["rbc"])

    return results