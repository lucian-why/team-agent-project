"""
启动 FastAPI 应用
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=5055,
        reload=True,
    )
