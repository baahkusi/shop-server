import falcon
import json
import shop40.actions as actions
from .middlewares import SetUserMiddleware, CORSComponent, PeeweeConnectionMiddleware


class Action():

    # def __init__(self, actions):

    #     self.actions = actions

    def __init__(self):
        
        self.action = []

    def on_post(self, req, resp):
        payload = json.loads(req.stream.read(req.content_length or 0))

        resp.body = json.dumps(self.prepare_response(req, payload))

    def prepare_response(self, req, payload):
        return self.handle_requests(self.actions, req, payload)

    def handle_requests(self, actions, req, payload):
        """
        This method takes a reqest format :payload: and returns
        a response format.
        ===============
        Request Format
        ===============
        {
            "request_id" : { 
                "action_name" : {"parameter":value, ...]},
                "000" : ["action_name" ...,]
                ...
            },
            ...,
            "000" : ["request_id" ...,],
            ...
        }


        ================
        Response Format
        ================
        {
            "request_id" : { 
                "action_name" : response = {'status': True | False, 'data': ...},
                ...
            },
            ...,
        }
        """

        response = {}
        for request_id in payload["000"]:
            request = payload[request_id]
            response[request_id] = {}
            for action in request["000"]:
                if action in actions.keys():
                    response[request_id][action] = actions[action](
                        req, **request[action])
                else:
                    response[request_id][action] = {
                        'status': False, 'data': 'Invalid Action'}
        return response


api = application = falcon.API(
    middleware=[
        CORSComponent(),
        # PeeweeConnectionMiddleware(),
        SetUserMiddleware(),
    ]
)

api.add_route('/action', Action())
