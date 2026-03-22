import re

class IntelAnalyzer:
    """محرك تحليل الأنماط والكلمات المفتاحية المطور"""
    
    def __init__(self):
        # أنماط البحث الاحترافية (Regex Patterns)
        self.patterns = {
            'FINANCIAL': r'(bank|transaction|balance|رصيد|بنك|سحب|إيداع|تم تحويل|فوري|مصاري)',
            'SECURITY_CODES': r'(code|otp|verification|رمز|تفعيل|كلمة السر|تأكيد|password)',
            'URGENT': r'(ضروري|بسرعة|urgent|help|نجدة|لحق|أين أنت)',
            'CONTACTS': r'(واتساب|تليجرام|facebook|login|تسجيل دخول|رابط)'
        }

    def analyze_content(self, text):
        """تحليل النص وتصنيفه برمجياً"""
        if not text:
            return ["EMPTY_DATA"]
            
        found_categories = []
        for category, pattern in self.patterns.items():
            # البحث عن النمط بغض النظر عن حالة الأحرف (Large/Small)
            if re.search(pattern, text, re.IGNORECASE):
                found_categories.append(category)
        
        return found_categories if found_categories else ["GENERAL_INFO"]

    def get_critical_score(self, categories):
        """حساب مستوى الخطورة أو الأهمية للبيانات"""
        if "SECURITY_CODES" in categories or "FINANCIAL" in categories:
            return "CRITICAL"
        elif "URGENT" in categories:
            return "HIGH"
        return "NORMAL"
