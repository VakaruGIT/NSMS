from flask import jsonify
from flask_restx import Namespace, Resource, fields

from ..model.agency import Agency
from ..model.subscriber import Subscriber
from .newspaperNS import issue_model
from .newspaperNS import paper_model


from uuid import uuid4

subscriber_ns = Namespace("subscriber", description="Subscriber related operations")

subscriber_model = subscriber_ns.model('SubscriberModel', {
    'subscriber_id': fields.Integer(required=True,
            help='The unique identifier of a subscriber'),
    'name': fields.String(required=True,
            help='The name of the subscriber, e.g. John Doe'),
    'address': fields.String(required=True,
            help='The address of the subscriber, e.g. 1234 Elm Street'),
    'newspapers': fields.List(fields.Nested(paper_model), required=False,
            help='The newspapers that the subscriber is subscribed to'),
    'delivered_issues': fields.List(fields.Nested(issue_model), required=False,
            help='The issues that the subscriber is subscribed to')
    })

subscriber_stats_model = subscriber_ns.model('SubscriberStatsModel', {
    'monthly_cost': fields.Float(required=True,
            help='The monthly cost of the subscriptions'),
    'annual_cost': fields.Float(required=True,
            help='The annual cost of the subscriptions'),
    'number_of_subscriptions': fields.Integer(required=True,
            help='The number of subscriptions'),
    'number_of_issues': fields.Integer(required=True,
            help='The number of issues delivered')
    })

missing_issues_model = subscriber_ns.model('MissingIssuesModel', {
    'issue_id': fields.Integer(required=True,
            help='The unique identifier of an issue')
    })

@subscriber_ns.route('/')
class SubscriberAPI(Resource):
    def post (self):
        subscriber_id = int(uuid4().int >> 64)
        new_subscriber = Subscriber(subscriber_id=subscriber_id,
                                    name=subscriber_ns.payload['name'],
                                    address=subscriber_ns.payload['address'])
        Agency.get_instance().add_subscriber(new_subscriber)
        return new_subscriber.serialize()

    @subscriber_ns.doc(subscriber_model, description="List all subscribers in the agency")
    @subscriber_ns.marshal_list_with(subscriber_model, envelope='subscribers')
    def get(self):
        return [subscriber.serialize_subscriber_id() for subscriber in Agency.get_instance().all_subscribers()]

@subscriber_ns.route('/<int:subscriber_id>')
class SubscriberID(Resource): 
    @subscriber_ns.doc(subscriber_model, description="Get a subscriber")
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def get(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found"),404
        return targeted_subscriber.serialize()

    @subscriber_ns.doc(description="Update a subscriber")
    @subscriber_ns.expect(subscriber_model, validate=True)
    @subscriber_ns.marshal_with(subscriber_model, envelope='subscriber')
    def post(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found"),404

        if 'name' in subscriber_ns.payload:
            targeted_subscriber.name = subscriber_ns.payload['name']
        if 'address' in subscriber_ns.payload:
            targeted_subscriber.address = subscriber_ns.payload['address']
        return targeted_subscriber.serialize()

    @subscriber_ns.doc(description="Delete a subscriber")
    def delete(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return {"message":f"Subscriber with ID {subscriber_id} was not found"},404
        else:
            Agency.get_instance().remove_subscriber(targeted_subscriber)
            return {"message":f"Subscriber with ID {subscriber_id} was deleted"}, 200

@subscriber_ns.route('/<int:subscriber_id>/subscribe/<int:paper_id>')
class Subscribe(Resource):
    @subscriber_ns.doc(description="Subscribe a subscriber to a newspaper.(Transmit the newspaper ID as parameter)")
    def post(self, subscriber_id, paper_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found"),404
        targeted_newspaper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_newspaper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"),404
        targeted_subscriber.subscribe_to_newspaper(targeted_newspaper)
        return targeted_subscriber.serialize()

@subscriber_ns.route('/<int:subscriber_id>/stats')
class SubscriberStats(Resource):
    @subscriber_ns.doc(description="Return information about the specific subscriber (number of subscriptions, monthly and annual cost)")
    @subscriber_ns.marshal_with(subscriber_stats_model, envelope='stats subscriber')
    def get(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found"), 404

        number_of_subscriptions = targeted_subscriber.calculate_subscriptions()
        monthly_cost = targeted_subscriber.calculate_monthly_cost()
        annual_cost = monthly_cost * 12
        number_of_issues = targeted_subscriber.calculate_issues()

        return {"message": "Statistics for the subscriber",
                "number_of_subscriptions": number_of_subscriptions,
                "monthly_cost": monthly_cost,
                "annual_cost": annual_cost,
                "number_of_issues" : number_of_issues}, 200

@subscriber_ns.route('/<int:subscriber_id>/missingissues')
class MissingIssues(Resource):
    @subscriber_ns.doc(description="Check if there are any undelivered issues of the subscribed newspapers.")
    @subscriber_ns.marshal_list_with(missing_issues_model, envelope='missing_issues')
    def get(self, subscriber_id):
        targeted_subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return jsonify(f"Subscriber with ID {subscriber_id} was not found"), 404

        missing_issues = []
        for newspaper in targeted_subscriber.newspapers:
            for issue in newspaper.issues:
                if issue not in targeted_subscriber.delivered_issues:
                    missing_issues.append(issue)

        return [issue.serialize() for issue in missing_issues], 200