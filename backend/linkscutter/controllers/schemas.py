
api_v1 = {
    'LinksCutter API v1': {
        'links': [
            {
                'method': 'GET',
                'route': '/api/v1/links?{page=%i},{size=%i}',
                'description': 'get list of links',
                'responce_example': {
                    'page': 1,
                    'size': 20,
                    'count': 1000,
                    'objects': [
                        {
                            'id': 1,
                            'url': 'www.site.com',
                            'key': 'aD2fvT',
                            'created_at': '2016-10-08T18:00:22',
                        },
                    ],
                },
            },
            {
                'method': 'GET',
                'route': '/api/v1/links/{key}',
                'description': 'get link by key',
                'responce_example': {
                    'id': 1,
                    'url': 'www.site.com',
                    'key': 'aD2fvT',
                    'created_at': '2016-10-08T18:00:22',
                },
            },
            {
                'method': 'POST',
                'route': '/api/v1/links',
                'description': 'create new link',
                'request_example': {
                    'url': 'www.site.com',
                },
                'responce_example': {
                    'id': 1,
                    'url': 'www.site.com',
                    'key': 'aD2fvT',
                    'created_at': '2016-10-08T18:00:22',
                },
            },
        ],
    },
}
