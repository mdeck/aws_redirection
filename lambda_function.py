# origin request event handler
def lambda_handler(event, context):
    request = event['Records'][0]['cf']['request']
    
    base = 'https://z.k2photo.gallery'
    uri = request['uri']
    qs = request['querystring']
    
    if len(qs) > 0:
        redirect_path = f'{base}{uri}?{qs}'
    else:
        redirect_path = f'{base}{uri}'

    response = {
        'status': 307,
        'headers': {
            'location': [
                {'key': 'Location', 'value': redirect_path}
            ]
        }
    }
    return response
