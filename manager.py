#encoding: utf-8

from cmdb import app
import os

app.config['basedir'] = os.path.abspath(os.path.dirname(__file__))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)