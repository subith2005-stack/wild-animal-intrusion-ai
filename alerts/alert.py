from datetime import datetime

def trigger_alert(animal_type, confidence):
    """
    Triggers an alert for a detected wild animal intrusion.
    """

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print("Alert! Wild Animal Intrusion Detected!")
    print("-------------------------------------")
    print("Time:", time_now)
    print("Animal Type:", animal_type)
    print("Confidence Level:", confidence)
    print("-------------------------------------")
    print("Take Immediate actions...")