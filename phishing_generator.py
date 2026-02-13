import random
import json
import os
from datetime import datetime

class PhishingGenerator:
    def __init__(self, template_file="templates.json"):
        self.template_file = template_file
        self.templates = self.load_templates()
        self.generated_count = 0
        
    def load_templates(self):
        """Load email templates from JSON file"""
        try:
            with open(self.template_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default templates if file not found
            return [
                {
                    "subject": "Urgent: Your {company} account will be suspended",
                    "body": "Dear {name},\n\nYour {company} account requires verification. Please login immediately:\n{link}\n\nFailure to verify within 24 hours will result in account suspension.\n\nRegards,\n{company} Security Team"
                },
                {
                    "subject": "Unusual login attempt detected",
                    "body": "Hello {name},\n\nWe detected a login attempt from an unknown device. If this wasn't you, please secure your account:\n{link}\n\n{company} Support"
                },
                {
                    "subject": "{company}: Password expired",
                    "body": "Hi {name},\n\nYour {company} password has expired. Please update it immediately:\n{link}\n\n{company} IT Department"
                }
            ]
    
    def generate_email(self, company, user_name):
        """Generate a personalized phishing email"""
        template = random.choice(self.templates)
        
        # Generate fake but realistic link
        fake_domains = ["secure-verify.com", "account-update.net", "login-confirm.org"]
        fake_domain = random.choice(fake_domains)
        link = f"https://{company.lower().replace(' ', '')}.{fake_domain}/login"
        
        # Personalize the email
        subject = template['subject'].replace("{company}", company)
        body = template['body'].replace("{company}", company)
        body = body.replace("{name}", user_name)
        body = body.replace("{link}", link)
        
        # Calculate risk score (70-95%)
        risk_score = random.randint(70, 95)
        
        self.generated_count += 1
        
        return {
            "id": self.generated_count,
            "subject": subject,
            "body": body,
            "link": link,
            "risk_score": risk_score,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "company": company,
            "target": user_name
        }
    
    def save_to_file(self, email, filename="generated_emails.txt"):
        """Save generated email to file"""
        with open(filename, 'a') as f:
            f.write(f"\n{'='*50}\n")
            f.write(f"ID: {email['id']}\n")
            f.write(f"Timestamp: {email['timestamp']}\n")
            f.write(f"Company: {email['company']}\n")
            f.write(f"Target: {email['target']}\n")
            f.write(f"Subject: {email['subject']}\n")
            f.write(f"Link: {email['link']}\n")
            f.write(f"Risk Score: {email['risk_score']}%\n")
            f.write(f"Body:\n{email['body']}\n")
        print(f"[+] Email saved to {filename}")
    
    def batch_generate(self, num_emails=5):
        """Generate multiple emails"""
        companies = ["PayPal", "Amazon", "Netflix", "Google", "Microsoft", "Apple", "Facebook"]
        names = ["John Doe", "Sarah Khan", "Ahmed Ali", "Fatima Zafar", "Usman Chaudhry"]
        
        emails = []
        for i in range(num_emails):
            company = random.choice(companies)
            name = random.choice(names)
            email = self.generate_email(company, name)
            emails.append(email)
            print(f"[{i+1}] Generated: {email['subject'][:50]}...")
        
        return emails

def main():
    print("="*60)
    print("🔐 AI PHISHING GENERATOR (Educational Purpose Only)")
    print("="*60)
    print("\n⚠️  WARNING: This tool is for security awareness training only!")
    print("   Never use for actual phishing attacks.\n")
    
    generator = PhishingGenerator()
    
    while True:
        print("\n📌 MENU:")
        print("1. Generate single email")
        print("2. Generate batch (5 emails)")
        print("3. View statistics")
        print("4. Exit")
        
        choice = input("\nEnter choice (1-4): ").strip()
        
        if choice == "1":
            company = input("Enter company name: ")
            name = input("Enter target name: ")
            email = generator.generate_email(company, name)
            
            print("\n" + "="*60)
            print(f"📧 GENERATED EMAIL (Risk: {email['risk_score']}%)")
            print("="*60)
            print(f"Subject: {email['subject']}")
            print(f"Link: {email['link']}")
            print(f"\nBody:\n{email['body']}")
            print("="*60)
            
            save = input("\nSave to file? (y/n): ").lower()
            if save == 'y':
                generator.save_to_file(email)
        
        elif choice == "2":
            num = input("How many emails? (default 5): ").strip()
            num = int(num) if num else 5
            emails = generator.batch_generate(num)
            print(f"\n✅ Generated {len(emails)} emails")
            
            save = input("Save all to file? (y/n): ").lower()
            if save == 'y':
                for email in emails:
                    generator.save_to_file(email)
        
        elif choice == "3":
            print(f"\n📊 Statistics:")
            print(f"Total emails generated: {generator.generated_count}")
            print(f"Templates loaded: {len(generator.templates)}")
        
        elif choice == "4":
            print("\n👋 Stay ethical! Remember: With great power comes great responsibility.")
            break
        
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()