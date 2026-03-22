import re

class IntelAnalyzer:
    def __init__(self):
        self.patterns = {
            'FINANCIAL': r'(bank|transaction|رصيد|تم تحويل)',
            'SECURITY': r'(code|otp|رمز|تفعيل)'
        }

    def classify(self, text):
        results = []
        for category, pattern in self.patterns.items():
            if re.search(pattern, text, re.IGNORECASE):
                results.append(category)
        return results if results else ["GENERAL"]
