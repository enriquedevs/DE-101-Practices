from datetime import datetime

def slack_message(username: str) -> str:
  return f"{username}'s - Data pipeline finished successfully on *{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"
