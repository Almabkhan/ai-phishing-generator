import unittest
import sys
import os
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from phishing_generator import PhishingGenerator

class TestPhishingGenerator(unittest.TestCase):
    
    def setUp(self):
        """Setup before each test"""
        self.generator = PhishingGenerator()
    
    def test_template_loading(self):
        """Test if templates load correctly"""
        self.assertGreater(len(self.generator.templates), 0, "No templates loaded")
    
    def test_email_generation(self):
        """Test email generation"""
        email = self.generator.generate_email("TestCompany", "TestUser")
        
        # Check if email has all required fields
        self.assertIn("subject", email)
        self.assertIn("body", email)
        self.assertIn("link", email)
        self.assertIn("risk_score", email)
        
        # Check if placeholders are replaced
        self.assertIn("TestCompany", email['body'])
        self.assertIn("TestUser", email['body'])
    
    def test_risk_score_range(self):
        """Test if risk score is between 70-95"""
        email = self.generator.generate_email("TestCompany", "TestUser")
        self.assertGreaterEqual(email['risk_score'], 70)
        self.assertLessEqual(email['risk_score'], 95)
    
    def test_save_to_file(self):
        """Test saving email to file"""
        email = self.generator.generate_email("TestCompany", "TestUser")
        filename = "test_email.txt"
        
        # Save to file
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Subject: {email['subject']}\n")
            f.write(f"Body: {email['body']}")
        
        # Check if file exists
        self.assertTrue(os.path.exists(filename))
        
        # Clean up
        os.remove(filename)
    
    def test_batch_generation(self):
        """Test batch email generation"""
        # Test batch_generate method
        if hasattr(self.generator, 'batch_generate'):
            emails = self.generator.batch_generate(3)
            self.assertEqual(len(emails), 3)

if __name__ == '__main__':
    unittest.main()
