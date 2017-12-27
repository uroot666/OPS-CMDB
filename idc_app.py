#encoding=utf-8

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
import idc_model

app = Flask(__name__)

@app.route("/")
def index():
    return "IDC MANAGE 1"

@app.route("/idc_list/")
def idc_list():
    engineroom_all = idc_model.engineroom_list()
    return render_template('idc_list.html', engineroom_all=engineroom_all)

@app.route("/idc/add/")
def idc_add():
    return render_template('idc_create.html')

@app.route("/idc/add_save/")
def idc_add_save():
    idcname = request.args.get('idcname', '')
    area = request.args.get('area', '')
    ip_segment = request.args.get('ip_segment', '')
    machine_number = int(request.args.get('machine_number', 0))
    idc_model.idc_add_save(idcname, area, ip_segment, machine_number)
    return redirect('/idc_list/')

@app.route("/idc/view/")
def idc_view():
    idcid = int(request.args.get('id'))
    idc_tails = idc_model.idc_tails_get(idcid)
    idcname = idc_tails.get("idcname")
    area = idc_tails.get("area")
    ip_segment = idc_tails.get("ip_segment")
    machine_number = idc_tails.get("engineroom_number")
    return render_template('idc_view.html', idcid=idcid, idcname=idcname, ip_segment=ip_segment, area=area, machine_number=machine_number)

@app.route("/idc/view_save/")
def idc_view_save():
    idcid = int(request.args.get('idcid'))
    idcname = request.args.get('idcname')
    area = request.args.get('area')
    ip_segment = request.args.get("ip_segment")
    machine_number = int(request.args.get('machine_number'))
    idc_model.idc_view_save(idcid, idcname, area, ip_segment, machine_number)
    return redirect("/idc_list/")
if __name__ == "__main__":
    app.run(debug=True)