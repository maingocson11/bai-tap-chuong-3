import os
import shutil
import smtplib
import schedule
import time
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")
SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKUP_DIR = os.path.join(SOURCE_DIR, "backup")
os.makedirs(BACKUP_DIR, exist_ok=True)

def send_email(subject, body):
    """Gửi email thông báo."""
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = EMAIL_RECEIVER
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email đã được gửi thành công.")
    except Exception as e:
        print(f"Lỗi khi gửi email: {e}")

def backup_databases():
    """Thực hiện sao lưu các tệp .sql và .sqlite3."""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        files_backed_up = []

        for file in os.listdir(SOURCE_DIR):
            if file.endswith(".sql") or file.endswith(".sqlite3"):
                source_file = os.path.join(SOURCE_DIR, file)
                backup_file = os.path.join(BACKUP_DIR, f"{file}_{timestamp}")
                shutil.copy2(source_file, backup_file)
                files_backed_up.append(file)

        if files_backed_up:
            subject = "Sao lưu cơ sở dữ liệu thành công"
            body = f"Các tệp sau đã được sao lưu thành công:\n" + "\n".join(files_backed_up)
        else:
            subject = "Không tìm thấy tệp để sao lưu"
            body = "Không có tệp .sql hoặc .sqlite3 nào để sao lưu."

        send_email(subject, body)
    except Exception as e:
        subject = "Sao lưu cơ sở dữ liệu thất bại"
        body = f"Đã xảy ra lỗi trong quá trình sao lưu: {e}"
        send_email(subject, body)
schedule.every().day.at("00:00").do(backup_databases)

if __name__ == "__main__":
    print("Đang chạy lịch trình sao lưu...")
    while True:
        schedule.run_pending()
        time.sleep(60)  # Kiểm tra mỗi phút
