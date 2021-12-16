import uvicorn
import os
from app.conf import settings

if __name__ == "__main__":
    uvicorn.run(
        "app.app:create_app",
        host="0.0.0.0",
        port=int(os.getenv("SERVER_PORT", 8002)),
        workers=int(os.getenv("WORKERS_NUMBER", 1)),
        debug=settings.DEBUG,
        reload=settings.DEBUG,
        factory=True,
    )
