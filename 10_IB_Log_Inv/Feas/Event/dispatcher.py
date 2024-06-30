from pydispatch import dispatcher

# 이벤트 수신자 정의
def handle_event(sender, **kwargs):
    print(f"Received signal from {sender} with arguments {kwargs}")

# 이벤트 신호 정의
SIGNAL = 'my-custom-signal'

# 이벤트 수신자 등록
dispatcher.connect(handle_event, signal=SIGNAL)

# 이벤트 신호 발송
dispatcher.send(signal=SIGNAL, sender='main', arg1='Hello', arg2='World')

# 이벤트 수신자 해제
dispatcher.disconnect(handle_event, signal=SIGNAL)
