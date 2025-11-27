import yfinance as yf
import smtplib
from email.mime.text import MIMEText
import os

SYMBOL = "NVDA"
UP_THRESHOLD = 185
DOWN_THRESHOLD = 170

# ערכים מגיעים מה-Secrets שהגדרת בגיטהאב
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")      # המייל שלך
SMTP_PASSWORD = os.getenv("SMTP_PASS")  # סיסמת האפליקציה
TO_EMAIL = os.getenv("TO_EMAIL")        # לאן לשלוח (יכול להיות אותו מייל)

def send_email(subject: str, body: str):
    if not SMTP_USER or not SMTP_PASSWORD or not TO_EMAIL:
        print("Missing SMTP configuration")
        print("SMTP_USER:", SMTP_USER)
        print("TO_EMAIL:", TO_EMAIL)
        return

    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject          # כאן הייתה הטעות – עכשיו זה מתוקן
    msg["From"] = SMTP_USER
    msg["To"] = TO_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    print("Email sent!")

def get_last_close(symbol: str):
    # מביא נתונים יומיים של 5 הימים האחרונים
    data = yf.download(symbol, period="5d", interval="1d")
    if data.empty:
        return None
    last_row = data.iloc[-1]
    return float(last_row["Close"])

def main():
    price = get_last_close(SYMBOL)
    if price is None:
        print("No data for NVDA")
        return

    print(f"NVDA last close: {price}")

    # לוגיקה של ההתראה
    if price > 0: # UP_THRESHOLD:
        subject = f"NVDA מעל {UP_THRESHOLD} – סגירה {price}"
        body = f"מניית NVDA נסגרה על {price}, שזה מעל {UP_THRESHOLD}."
        send_email(subject, body)
    elif price < DOWN_THRESHOLD:
        subject = f"NVDA מתחת {DOWN_THRESHOLD} – סגירה {price}"
        body = f"מניית NVDA נסגרה על {price}, שזה מתחת {DOWN_THRESHOLD}."
        send_email(subject, body)
    else:
        print("המחיר בין 170 ל-185 – אין התראה.")

if __name__ == "__main__":
    main()
