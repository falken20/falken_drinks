# Snippets de código comunes - Falken Drinks

## Nuevo endpoint API (route)

```python
@api_routes.route('/api/v1/resource', methods=['GET'])
@login_required
def get_resources():
    '''Get all resources'''
    try:
        resources = ControllerResource.get_all()
        return jsonify({
            'status': 'ok',
            'data': [r.serialize() for r in resources]
        })
    except Exception as e:
        Log.error(f'Error getting resources: {e}', sys.exc_info())
        return jsonify({'status': 'error', 'message': str(e)}), 500
```

## Nuevo controlador

```python
class ControllerResource:
    '''Controller for Resource model'''

    @staticmethod
    def get_all():
        '''Get all resources'''
        Log.info('Getting all resources')
        return Resource.query.all()

    @staticmethod
    def get_by_id(resource_id):
        '''Get resource by id'''
        Log.info(f'Getting resource by id: {resource_id}')
        return Resource.query.get(resource_id)

    @staticmethod
    def create(data):
        '''Create a new resource'''
        try:
            resource = Resource(**data)
            db.session.add(resource)
            db.session.commit()
            Log.info(f'Resource created: {resource}')
            return resource
        except Exception as e:
            db.session.rollback()
            Log.error(f'Error creating resource: {e}', sys.exc_info())
            raise
```

## Nuevo test

```python
class TestResource(BaseTestCase):
    '''Tests for Resource'''

    def test_get_resources_ok(self):
        '''Test get all resources returns 200'''
        self.create_user()
        self.login_http()
        response = self.client.get('/api/v1/resource')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'ok')

    def test_get_resources_unauthorized(self):
        '''Test get resources requires login'''
        response = self.client.get('/api/v1/resource')
        self.assertNotEqual(response.status_code, 200)
```
