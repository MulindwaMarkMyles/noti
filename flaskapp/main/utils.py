from flask import request

def the_device():
        user_agent = request.headers.get("User-Agent").lower()
        mobile_devices = ["android", "iphone","ipod"]
        if any(device in user_agent for device in mobile_devices):
                return True
        return False