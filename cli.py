# cli.py

import requests

BASE_URL = "http://127.0.0.1:8000"

def print_menu():
    print("\nWelcome to Your Productivity Coach!\n")
    print("[1] Submit Focus for Today")
    print("[2] Log How Your Day Went")
    print("[3] View Past Logs")
    print("[4] Generate Today's Summary")
    print("[5] Check Server Health")
    print("[0] Exit\n")

def main():
    while True:
        print_menu()
        choice = input("Select an option: ").strip()

        if choice == "1":
            focus = input("What's your main focus for today? ").strip()
            if not focus:
                print("Focus cannot be empty.")
                continue

            payload = {
                "user_id": 1,
                "user_log": focus,
                "ai_summary": "Focus log: No AI summary yet."
            }

            try:
                response = requests.post(f"{BASE_URL}/submit-daily-log", params=payload)
                if response.status_code == 200:
                    print("✅ Focus submitted successfully!")
                else:
                    print(f"❌ Failed to submit focus: {response.text}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        elif choice == "2":
            reflection = input("How did your day go? ").strip()
            if not reflection:
                print("Reflection cannot be empty.")
                continue

            payload = {
                "user_id": 1,
                "user_log": reflection,
                "ai_summary": "Reflection log: No AI summary yet."
            }

            try:
                response = requests.post(f"{BASE_URL}/submit-daily-log", params=payload)
                if response.status_code == 200:
                    print("✅ Reflection submitted successfully!")
                else:
                    print(f"❌ Failed to submit reflection: {response.text}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        elif choice == "3":
            try:
                response = requests.get(f"{BASE_URL}/logs?limit=5")
                if response.status_code == 200:
                    logs = response.json()
                    if not logs:
                        print("📭 No logs found yet.")
                    else:
                        print("\n📜 Recent Logs:")
                        for log in logs:
                            print(f"\n🗓️ {log['created_at']}")
                            print(f"📝 User Log: {log['user_log']}")
                            print(f"🤖 AI Summary: {log['ai_summary']}")
                            print("-" * 40)
                else:
                    print(f"❌ Failed to fetch logs: {response.text}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")


        elif choice == "4":
            try:
                response = requests.post(f"{BASE_URL}/generate-summary?user_id=1")
                if response.status_code == 200:
                    data = response.json()
                    print("\n🧠 Today's AI Summary:")
                    print(data.get("summary", "No summary available."))
                else:
                    print(f"❌ Failed to generate summary: {response.text}")
            except Exception as e:
                print(f"❌ Error: {str(e)}")

        elif choice == "5":
            print("Checking server health...")
            # (we'll fill this next)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
