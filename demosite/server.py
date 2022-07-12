#!user/bin/env python

# Copyright (c) 2022 uidom
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "main:api",
        host="127.0.0.1",
        port=8000,
        reload=True,
        # ssl_keyfile='../demosite/key.pem',
        # ssl_certfile='../demosite/cert.pem'
    )

