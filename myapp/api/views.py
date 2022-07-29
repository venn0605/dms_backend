from flask import jsonify
from flask_restful import Resource , reqparse
from myapp.api import api

# from dbcurd import dbcurd
from myapp.dbcurd import dbcurd

dbs = dbcurd()


@api.resource("/mf4dirpath/<path:mf4dirpath>")
class mf4path(Resource):
    def get(self,mf4dirpath):
        print(mf4dirpath)
        mf4data = dbs.query(mf4dirpath.replace("/", "\\"))
        # json format data including mf4filenumber, mf4fileid, mf4name.
        return jsonify(mf4data)
        # return jsonify({"hello":"flask_restful"})




@api.resource("/mf4name/<path:dirpath>/<string:mf4name>/<int:mf4nameid>")
class mf4names(Resource):

    def get(self,dirpath,mf4name,mf4nameid):
        print(dirpath)
        print(mf4name)
        print(mf4nameid)

        imgsPath = dbs.imgsTransfer(mf4name)

        return jsonify(imgsPath)
        # return jsonify({"message":200})

