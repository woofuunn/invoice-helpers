from flask import Flask, request
from flask_restful import Api, Resource
from utils.invoice import check_invoice, get_period, get_number

app = Flask(__name__)
api = Api(app)

class GetInvoicePeriod(Resource):
    def get(self):
        period = get_period
        return {"period": period}

class GetInvoiceNumber(Resource):
    def get(self):
        period = request.args.get("period")
        number = get_number(period)
        return number

class CheckInvoiceNumber(Resource):
    def post(self):
        req = request.get_json()
        number = req.get("number")
        period = req.get("period")
        print(f"API入口測試 號碼: {number}")
        result = check_invoice(number, period)
        return {"checkResult": result}

api.add_resource(GetInvoicePeriod, "/api/get_invoice_period")
api.add_resource(GetInvoiceNumber, "/api/get_invoice_number")
api.add_resource(CheckInvoiceNumber, "/api/check_invoice_number")

if __name__ == "__main__":
    app.run(port = 5000, host = "0.0.0.0", debug = True)
