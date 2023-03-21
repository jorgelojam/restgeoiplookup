import pygeoip
from flask import Flask,jsonify,request,abort

app = Flask(__name__)

cuidades = pygeoip.GeoIP('GeoIPCity.dat',pygeoip.MEMORY_CACHE)
isps = pygeoip.GeoIP('GeoIPISP.dat',pygeoip.MEMORY_CACHE)

@app.route('/geoipquery', methods = ['POST'])
def queryipinfo():
	if(request.headers.get('Content-Type')== 'application/json'):
		query = request.json
		ip = query.get("ip")
		resultado = cuidades.record_by_addr(ip)
		if resultado is None:
			abort(404,"No encontrado")
		isp = isps.org_by_addr(ip)
		if isp is None:
			resultado["isp"] = ""
		resultado["isp"] = isp
		return jsonify(resultado)
	else:
		abort(400,"No valido")


if __name__=='__main__':
	app.run(debug=False)
