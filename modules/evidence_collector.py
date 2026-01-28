import json
import os
from datetime import datetime

class EvidenceCollector:
    def save(self, data):
        os.makedirs("evidence", exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = os.path.join("evidence", f"{timestamp}.json")

        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"📁 Evidence saved to: {filename}")
