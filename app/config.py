#!/usr/bin/env python

setup_CORS = {
    'origin': [
        "http://localhost:3000",
    ],
    'allow_credentials': False,
    'allow_methods': ['GET'],
    'allow_headers': ["*"]
}