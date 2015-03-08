#!/usr/bin/python
import os
from gecko import app


def main():
    app.debug = True
    app.run(host='0.0.0.0', port=8333)

if __name__ == '__main__':
    main()
