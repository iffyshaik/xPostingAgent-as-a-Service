# scripts/check_env.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.config import settings

print("✅ Loaded TYPEFULLY_API_KEY:", settings.typefully_api_key)





