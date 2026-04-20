import traceback
from inventory_backend.app.database import SessionLocal
from inventory_backend.app.ai import ai_service

db = SessionLocal()
try:
    result = ai_service.generate_insights(db)
    print('OK', len(result))
except Exception as e:
    print('ERR', type(e).__name__, str(e))
    traceback.print_exc()
finally:
    db.close()
