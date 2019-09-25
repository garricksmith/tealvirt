#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import http.server

PORT=8080

Handler = http.server.CGIHTTPRequestHandler

with http.server.HTTPServer(('127.0.0.1', PORT), Handler) as httpd:
    print('serving on port', PORT)
    httpd.serve_forever()
#

