import os
import json
import shutil

UPLOAD_DIR = "/tmp/whistleblower_evidence"
CHAT_LOG = os.path.join(UPLOAD_DIR, "chat_history.json")

def initialize():
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    # Sample Evidences
    samples = [
        {
            "filename": "financial_records_leak.png",
            "chat": "Found these offshore account ledgers in the trash near the CFO's office. Multiple shell companies listed.",
            "report": "# Forensic Analysis - Financial Ledger\nSignificant evidence of tax evasion via Caymans-based shell corporations."
        },
        {
            "filename": "security_breach_photo.jpg",
            "chat": "Unauthorized access detected in Server Room B at 2 AM. This photo shows the physical bypass device used.",
            "report": "# Incident Report - Physical Security\nHigh-level physical breach involving a hardware key-logger and bypass rig."
        }
    ]

    history = [
        {"role": "system", "content": "Secure connection established. End-to-end encryption active."},
        {"role": "assistant", "content": "How can I help you today? You can share information or upload evidence securely."}
    ]

    for sample in samples:
        # Create dummy file
        path = os.path.join(UPLOAD_DIR, sample["filename"])
        with open(path, "w") as f:
            f.write("MOCK_IMAGE_DATA")
        
        # Create metadata
        with open(path + ".meta.json", "w") as f:
            json.dump({"chat_text": sample["chat"], "timestamp": os.path.getctime(path)}, f)
        
        # Add to chat history
        history.append({
            "role": "user", 
            "content": f"Uploaded evidence: [{sample['filename']}]", 
            "file_url": f"/evidence/{sample['filename']}", 
            "chat_text": sample["chat"]
        })
        history.append({
            "role": "assistant", 
            "content": f"Evidence ingested. Forensic tag: {sample['filename'].upper()}", 
            "report": sample["report"]
        })

    # Save history
    with open(CHAT_LOG, "w") as f:
        json.dump(history, f)

    print(f"Initialized {len(samples)} sample items in {UPLOAD_DIR}")

if __name__ == "__main__":
    initialize()
