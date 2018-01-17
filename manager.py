#encoding: utf-8

from cmdb import app
import os

# 项目运行位置
app.config['basedir'] = os.path.abspath(os.path.dirname(__file__))

# geoip库位置
app.config['GeoIP'] = os.path.abspath(os.path.join(os.path.dirname(__file__), 'utils/GeoLite_City/GeoLite2-City.mmdb'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)