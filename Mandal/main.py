import os
import time

def main():
    msg = os.getenv("AZURE_STORAGE_QUEUE_MESSAGE")
    print(f"🔔 Processing Message: {msg}")
    time.sleep(10)
    print("✅ Job done")

if __name__ == "__main__":
    main()



