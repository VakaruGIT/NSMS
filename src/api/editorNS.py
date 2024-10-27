from flask import jsonify
from flask_restx import Namespace, Resource, fields

from ..model.agency import Agency
from ..model.editor import Editor

from uuid import uuid4

editor_ns = Namespace("editor", description="Editor related operations")

editor_model = editor_ns.model('EditorModel', {
    'editor_id': fields.Integer(required=True,
            help='The unique identifier of an editor'),
    'name': fields.String(required=True,
            help='The name of the editor, e.g. John Doe'),
    'address': fields.String(required=False,
            help='The address of the editor, e.g. 1234 Elm Street'),
    'newspapers': fields.List(fields.Integer, required=False)
    })

@editor_ns.route('/')
class EditorAPI(Resource):
    @editor_ns.doc(editor_model, description="Create an editor")
    @editor_ns.marshal_list_with(editor_model, envelope='editors')
    def post(self):
        editor_id = int(uuid4().int >> 64)
        new_editor = Editor(editor_id=editor_id,
                            name=editor_ns.payload['name'],
                            address=editor_ns.payload['address'])
        Agency.get_instance().add_editor(new_editor)
        return new_editor.serialize()

    @editor_ns.doc(editor_model, description="List all editors in the agency")
    @editor_ns.marshal_list_with(editor_model, envelope='editors')
    def get(self):
        return [editor.serialize() for editor in Agency.get_instance().get_all_editors()]

@editor_ns.route('/<int:editor_id>')
class EditorID(Resource):
    @editor_ns.doc(description="Get an editor information")
    @editor_ns.marshal_with(editor_model, envelope='editor')
    def get(self, editor_id):
        search_result = Agency.get_instance().get_editor(editor_id)
        if not search_result:
            return jsonify(f"Editor with ID {editor_id} was not found")
        return search_result.serialize()

    @editor_ns.doc(editor_model, description="Update an editor information")
    @editor_ns.marshal_list_with(editor_model, envelope='editors')
    def post(self, editor_id):
        targeted_editor = Agency.get_instance().get_editor(editor_id)
        if not targeted_editor:
            return jsonify(f"Editor with ID {editor_id} was not found"),404

        if 'name' in editor_ns.payload:
            targeted_editor.name = editor_ns.payload['name']
        if 'address' in editor_ns.payload:
            targeted_editor.address = editor_ns.payload['address']
        if 'editor_id' in editor_ns.payload:
            targeted_editor.editor_id = editor_ns.payload['editor_id']
        return targeted_editor.serialize()

@editor_ns.route('/<int:editor_id>')
class EditorID(Resource):
    def delete(self, editor_id):
        agency = Agency.get_instance()
        targeted_editor = agency.get_editor(editor_id)
        if not targeted_editor:
            return {"message":f"Editor with ID {editor_id} was not found"}, 404
        
        else:
            for issue_id in targeted_editor.get_editor_issues_ids():
                issue = agency.get_issue(issue_id)
                if issue is None:
                    continue
                other_editor = agency.get_any_other_editor(targeted_editor, issue.newspaper)
                if other_editor:
                    targeted_editor.reassign_issue(issue, other_editor)

            agency.remove_editor(targeted_editor)
            return {"message":f"Editor with ID {editor_id} was deleted"}, 200

@editor_ns.route('/<int:editor_id>/issues')
class EditorIssues(Resource):
    def get(self, editor_id):
        # get editor issues
        editor = Agency.get_instance().get_editor(editor_id)
        if not editor:
            return jsonify(f"Editor with ID {editor_id} was not found"),404
        editor_issue_ids = editor.get_editor_issues_ids()
        return {"message": f"Editor with ID {editor_id} was responsible for the following issues", "issues": editor_issue_ids}, 200