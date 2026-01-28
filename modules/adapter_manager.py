class AdapterManager:
    def detect(self):
        return {
            "adapter": "wlan0",
            "supports_monitor": True,
            "driver": "ath9k"
        }
