import json
import zlib
import base64
from typing import List  # Add this import

class HealthDataCompressor:
    @staticmethod
    def compress_data(data: dict) -> str:
        """Compress health data to reduce token usage"""
        json_str = json.dumps(data)
        compressed = zlib.compress(json_str.encode('utf-8'))
        return base64.b64encode(compressed).decode('utf-8')
    
    @staticmethod
    def decompress_data(compressed_str: str) -> dict:
        """Decompress health data"""
        compressed = base64.b64decode(compressed_str.encode('utf-8'))
        json_str = zlib.decompress(compressed).decode('utf-8')
        return json.loads(json_str)
    
    @staticmethod
    def summarize_for_ai(medical_history: dict, wellness_data: List[dict]) -> str:
        """Create a concise summary for AI processing"""
        summary = f"""
Medical Profile:
- Conditions: {', '.join(medical_history.get('conditions', []))}
- Medications: {', '.join(medical_history.get('medications', []))}
- Allergies: {', '.join(medical_history.get('allergies', []))}

Recent Wellness (Last 7 days):
- Avg Sleep: {sum(d['sleep_hours'] for d in wellness_data[-7:])/7:.1f}h
- Avg Exercise: {sum(d['exercise_minutes'] for d in wellness_data[-7:])/7:.0f}min
- Avg Stress: {sum(d['stress_level'] for d in wellness_data[-7:])/7:.1f}/10
"""
        return summary