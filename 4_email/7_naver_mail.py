import smtplib
from email.mime.text import MIMEText
from account import *

with smtplib.SMTP("smtp.naver.com", 587) as smtp:
    smtp.ehlo() # 연결이 잘 수립되는지 확인
    smtp.starttls() # 모든 내용이 암호화되어 전송
    smtp.login(NAVER_EMAIL_ADDRESS, NAVER_EMAIL_PASSWORD) # 로그인

    msg = MIMEText('본문 테스트 메시지')
    msg['To'] = 'pidokige0204@gmail.com'
    msg['Subject'] = '메일 발송 시험 (2021.08.05)'
    msg['From'] = NAVER_EMAIL_ADDRESS

    # 발신자, 수신자, 정해진 형식의 메시지
    smtp.sendmail(NAVER_EMAIL_ADDRESS, "pidokige0204@gmail.com", msg.as_string())
    # smtp.sendmail(EMAIL_ADDRESS, "jinha.hwang@ge.com", msg)
