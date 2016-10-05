from flask import Flask, json, jsonify, request, redirect, url_for, Response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:c8h1e4n@db/mysql"

db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    category = db.Column(db.String(200))
    description = db.Column(db.String(200))
    link = db.Column(db.String(150))
    estimated_costs = db.Column(db.String(10))
    submit_date = db.Column(db.String(10))
    status = db.Column(db.String(20))
    decision_date = db.Column(db.String(10))

    def __init__(self, name, email, category, description, link, estimated_costs, submit_date):
        self.name = name
        self.email = email
        self.category = category
        self.description = description
        self.link = link
        self.estimated_costs = estimated_costs
        self.status = "pending"
        self.submit_date = submit_date
        self.decision_date = ""

    def __repr__(self):
        return '<Post %r>' % self.name


@app.route("/v1/expenses", methods = ["POST"])
def posting():
    if request.method == "POST":
        post_data = json.loads(request.data)
        send_data = Post(post_data['name'], post_data['email'], post_data['category'], post_data['description'], post_data['link'], post_data['estimated_costs'], post_data['submit_date']) 
        db.session.add(send_data)
        db.session.commit()
        
        send_data = Post.query.filter_by(name = post_data['name'], email = post_data['email'], category = post_data['category'], description = post_data['description'], link = post_data['link'], estimated_costs = post_data['estimated_costs'], submit_date = post_data['submit_date'])
        returned_query = send_data.first()
        returned_json = json.dumps({"id":returned_query.id, "name":returned_query.name, "email":returned_query.email, "category":returned_query.category, "description":returned_query.description, "link":returned_query.link, "estimated_costs":returned_query.estimated_costs, "submit_date":returned_query.submit_date, "status":returned_query.status, "decision_date":returned_query.decision_date})

        send_response = Response(returned_json, status = 201, mimetype='application/json')
        return send_response

@app.route("/v1/expenses/<expense_id>", methods = ["GET", "PUT", "DELETE"])
def modifying(expense_id):
    if request.method == "GET":
        send_data = Post.query.filter_by(id = expense_id)
        if Post.query.filter_by(id = expense_id).count() > 0:
            returned_query = send_data.first()
            returned_json = json.dumps({"id":returned_query.id, "name":returned_query.name, "email":returned_query.email,"category":returned_query.category, "description":returned_query.description, "link":returned_query.link, "estimated_costs":returned_query.estimated_costs, "submit_date":returned_query.submit_date, "status":returned_query.status, "decision_date":returned_query.decision_date})
            send_response = Response(returned_json, status = 200, mimetype='application/json')
        else: 
            send_response = Response(status = 404)
        return send_response

    elif request.method == "PUT":
        put_data = json.loads(request.data)
        for r in put_data:
            if r == "name":
                Post.query.filter_by(id = expense_id).update({Post.name : put_data['name']} )
                db.session.commit()
                send_response = Response(status = 202)
            elif r == "email":
                Post.query.filter_by(id = expense_id).update({Post.email : put_data['email']} )
                db.session.commit()
                send_response = Response(status = 202)
            elif r == "category":
                Post.query.filter_by(id = expense_id).update({Post.category : put_data['category']} )
                db.session.commit()
                send_response = Response(status = 202)
            elif r == "description":
                Post.query.filter_by(id = expense_id).update({Post.description : put_data['description']} )
                db.session.commit()
                send_response = Response(status = 202)
            elif r == "link":
                Post.query.filter_by(id = expense_id).update({Post.link : put_data['link']} )
                db.session.commit()
                send_response = Response(status = 202)
            elif r == "estimated_costs":
                Post.query.filter_by(id = expense_id).update({Post.estimated_costs : put_data['estimated_costs']} )
                db.session.commit()
                send_response = Response(status = 202)
            elif r == "submit_date":
                Post.query.filter_by(id = expense_id).update({Post.submit_date : put_data['submit_date']} )
                db.session.commit()
                send_response = Response(status = 202)
            elif r == "status":
                Post.query.filter_by(id = expense_id).update({Post.status : put_data['status']} )
                db.session.commit()
                send_response = Response(status = 202)
            elif r == "decision_date":    
                Post.query.filter_by(id = expense_id).update({Post.decision_date : put_data['decision_date']} )
                db.session.commit()
                send_response = Response(status = 202)
            else:
                send_response = Response(status = 404)  
        
        return send_response

    elif request.method == "DELETE":
        send_data = Post.query.filter_by(id = expense_id).delete()
        db.session.commit()
        send_response = Response(status = 204)
        return send_response
       
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True,host='0.0.0.0')

