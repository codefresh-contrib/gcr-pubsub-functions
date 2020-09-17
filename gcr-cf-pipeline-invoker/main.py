import base64
import json
import os
import requests

def run_codefresh_pipeline(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    print(pubsub_message)

    pubsub_dict = json.loads(pubsub_message)

    print(pubsub_dict['tag'])

    codefresh_api_address = os.getenv('CODEFRESH_API_URL', 'https://g.codefresh.io/api')
    codefresh_api_key = os.getenv('CODEFRESH_API_KEY')

    response = requests.request('GET', '{}/pipelines'.format(codefresh_api_address), headers={'Authorization': 'Bearer {}'.format(codefresh_api_key)})

    pipeline_data = response.json()

    docs = pipeline_data['docs']

    for pipeline in docs:
        if 'labels' in pipeline['metadata']:
            if pipeline['metadata']['labels']['tags']:
                for value in pipeline['metadata']['labels']['tags']: 
                    if value in pubsub_dict['tag']:
                        print('Pipeline Tag Found: {}'.format(value))
                        
                        pipeline_id = pipeline['metadata']['id']
                        pipeline_name = pipeline['metadata']['name']
                     
                        print('Running Pipeline: {}'.format(pipeline_name))
                        print('Pipeline Tag Found: {}'.format(value))

                        json_data = { 
                            "variables": {
                            "IMAGE_TAG": pubsub_dict['tag']
                            }
                        }

                        r = requests.post('{}/pipelines/run/{}'.format(codefresh_api_address, pipeline_id), json=json_data, headers={'Authorization': 'Bearer {}'.format(codefresh_api_key)})

                        print('Codefresh Build: {}'.format(r.text))
