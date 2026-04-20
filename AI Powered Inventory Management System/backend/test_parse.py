#!/usr/bin/env python
import sys
sys.path.insert(0, '.')
from inventory_backend.app.ai.ai_service import _parse_ai_json

test = '```json\n{"test": true}\n```'
try:
    result = _parse_ai_json(test)
    print('Result:', result)
except Exception as e:
    print('Error:', type(e).__name__, str(e))
