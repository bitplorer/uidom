HAS_UVICORN = True

try:
    import uvicorn
except ImportError:
    pass
    HAS_UVICORN = False

if __name__ == "__main__":
    if HAS_UVICORN:
        uvicorn.run(
            "apps.routes:api",
            host="127.0.0.2",
            port=8081,
            reload=True,
            # ssl_keyfile='../apps/key.pem',
            # ssl_certfile='../apps/cert.pem'
        )
