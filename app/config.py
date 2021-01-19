#!/usr/bin/env python

setup_CORS = {
    'origin': [
        "localhost:3000",
        "http://localhost:3000"
    ],
    'allow_credentials': True,
    'allow_methods': ['GET', 'POST'],
    'allow_headers': ["*"]
}