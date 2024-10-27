from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields

from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue

from uuid import uuid4


newspaper_ns = Namespace("newspaper", description="Newspaper related operations")

issue_model = newspaper_ns.model("IssueModel",{
    "release_date": fields.String(required=False,
            help="The date of publication of the issue, e.g. 2021-09-01"),
    "released": fields.Boolean(required=False,
            help="The status of the issue, e.g. True or False"),
    "page": fields.Integer(required=False,
            help="The number of pages in the issue, e.g. page 32"),
    "editor_id": fields.Integer(required=False,
            help="The editor of the issue, e.g. 24123"),
    "issue_id": fields.Integer(required=False,
            help="The unique identifier of the issue"),
    })

paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)'),
    'issues': fields.List(fields.Nested(issue_model), required=False,
            help='The list of issues of the newspaper'),
    'subscribers': fields.List(fields.Integer, required=False,
            help='The list of subscribers to the newspaper')
   })

stats_model = newspaper_ns.model('StatsModel', {
    'message': fields.String,
    'number_subscribers': fields.Integer,
    'monthly_revenue': fields.Float,
    'annual_revenue': fields.Float
    })

@newspaper_ns.route('/')
class NewspaperAPI(Resource):
    # WORKS
    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        paper_id = int(uuid4().int >> 64)
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'],)
        Agency.get_instance().add_newspaper(new_paper)

        return new_paper

    @newspaper_ns.doc(paper_model, description="List all newspapers in the agency")
    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self): # List all newspapers in the agency
        return [paper.serialize_paper_id() for paper in Agency.get_instance().all_newspapers()]

@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):
    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id): # Get a newspaper's information
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"), 404
        return targeted_paper.serialize_paper_id()

    @newspaper_ns.doc(parser=paper_model, description="Update a newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"), 404

        if 'name' in newspaper_ns.payload:
            targeted_paper.name = newspaper_ns.payload['name']
        if 'frequency' in newspaper_ns.payload:
            targeted_paper.frequency = newspaper_ns.payload['frequency']
        if 'price' in newspaper_ns.payload:
            targeted_paper.price = newspaper_ns.payload['price']

        return targeted_paper.serialize()
    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        agency = Agency.get_instance()
        targeted_paper = agency.get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"), 404
        else:
            agency.remove_newspaper(targeted_paper)
            return {"message": f"Newspaper with ID {paper_id} was deleted"}, 200

@newspaper_ns.route('/<int:paper_id>/issue')
class NewspaperIssue(Resource):
    @newspaper_ns.doc(parser=issue_model,description="Add a new issue to a newspaper")
    def post(self, paper_id):
        issue_id = int(uuid4().int >> 64)
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)

        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"), 404

        release_date = newspaper_ns.payload.get('release_date')
        released = newspaper_ns.payload.get('released')
        page = newspaper_ns.payload.get('page')
        editor_id = newspaper_ns.payload.get('editor_id')

        new_issue = Issue(
            releasedate=release_date,
            released=released,
            page=page,
            editor=editor_id,
            issue_id=issue_id)

        targeted_paper.add_issue(new_issue)

        return new_issue.serialize(), 201

    @newspaper_ns.doc(description="Get all issues for a newspaper")
    @newspaper_ns.marshal_with(issue_model, envelope='issue newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        if not search_result:
            return jsonify(f"Newspaper with ID {paper_id} was not found"), 404
        return search_result.issues

@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>')
class NewspaperIssueID(Resource):
    @newspaper_ns.doc(description="Get information of a newspaper issue")
    @newspaper_ns.marshal_with(issue_model, envelope='issue newspaper')
    def get(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"), 404
        for issue in targeted_paper.issues:
            if issue.issue_id == issue_id:
                return issue.serialize()
        return jsonify(f"Newspaper issue with ID {issue_id} was not found"), 404

@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/release')
class NewspaperIssueRelease(Resource):
    @newspaper_ns.doc(description="Release an issue of the newspaper")
    @newspaper_ns.marshal_with(issue_model, envelope="issue newspaper")
    def post(self, paper_id, issue_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return {"message": f"Newspaper with ID {paper_id} was not found"}, 404
        for issue in targeted_paper.issues:
            if issue.issue_id == issue_id:
                issue.released = True
                return issue.serialize(), 200

        return {"message": f"Newspaper issue with ID {issue_id} was not found"}, 404

@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/editor/<int:editor_id>')
class NewspaperIssueEditor(Resource):
    @newspaper_ns.doc(description="Assign an editor to an issue and add it to editor's newspaper list.")
    def post(self, paper_id, issue_id, editor_id):
        agency = Agency.get_instance()
        targeted_paper = agency.get_newspaper(paper_id)

        if not targeted_paper:
            return {"message": f"Newspaper with ID {paper_id} was not found"}, 404

        targeted_issue = None
        for issue in targeted_paper.issues:
            if issue.issue_id == issue_id:
                targeted_issue = issue
                break

        if not targeted_issue:
            return {"message": f"Newspaper issue with ID {issue_id} was not found"}, 404

        specific_editor = agency.get_editor(editor_id)
        if not specific_editor:
            return {"message": "No editor available for assignment."}, 404

        agency.set_editor_to_issue(specific_editor, targeted_issue, targeted_paper)

        return {"message": "Editor assigned successfully", "editor_id": specific_editor.editor_id}, 200

@newspaper_ns.route('/<int:paper_id>/issue/<int:issue_id>/deliver/<int:subscriber_id>')
class NewspaperIssueDeliver(Resource):
    @newspaper_ns.doc(description="Deliver an issue to a subscriber")
    def post(self, paper_id, issue_id, subscriber_id):
        agency = Agency.get_instance()
        targeted_paper = agency.get_newspaper(paper_id)
        if not targeted_paper:
            return {"message": f"Newspaper with ID {paper_id} was not found"}, 404

        targeted_issue = None
        for issue in targeted_paper.issues:
            if issue.issue_id == issue_id:
                targeted_issue = issue
                break

        if not targeted_issue:
            return {"message": f"Newspaper issue with ID {issue_id} was not found"}, 404

        targeted_subscriber = agency.get_subscriber(subscriber_id)
        if not targeted_subscriber:
            return {"message": f"Subscriber with ID {subscriber_id} was not found"}, 404

        targeted_issue.deliver_issue_id_to_subscriber(targeted_subscriber)

        return {"message": "Issue delivered successfully", "subscriber_id": targeted_subscriber.subscriber_id}, 200

@newspaper_ns.route('/<int:paper_id>/stats')
class NewspaperStats(Resource):
    @newspaper_ns.doc(description="Return information about the specific newspaper (number of subscribers, monthly and annual revenue)")
    @newspaper_ns.marshal_with(stats_model, envelope='stats newspaper')
    def get(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found"), 404

        number_subscribers = targeted_paper.calculate_subscribers()
        monthly_revenue = targeted_paper.calculate_monthly_revenue()
        annual_revenue = monthly_revenue * 12

        return {"message": "Statistics for the newspaper",
                "number_subscribers": number_subscribers,
                "monthly_revenue": monthly_revenue,
                "annual_revenue": annual_revenue}, 200