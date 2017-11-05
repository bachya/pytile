"""Define tests for the client."""

import pytest


@pytest.fixture(scope='session')
def client_response_200():
    """Define a successful response for client confirmation."""
    return {
        'version': 1,
        'revision': 1,
        'timestamp': '2017-11-03T16:43:12.307Z',
        'timestamp_ms': 1509727392307,
        'result_code': 0,
        'result': {
            'locale': 'en-US',
            'client_uuid': '9a1f6b39-d980-4d70-a9ab-9abf2235d9ed',
            'app_id': 'ios-tile-production',
            'app_version': '2.21.1',
            'os_name': None,
            'os_release': '11.1',
            'model': None,
            'signed_in_user_uuid': None,
            'registration_timestamp': 1509727382065,
            'user_device_name': 'pytile Client',
            'beta_option': False,
            'last_modified_timestamp': 1509727382065
        }
    }


@pytest.fixture(scope='session')
def client_uuid():
    """Define a client UUID."""
    return '9a1f6b39-d980-4d70-a9ab-9abf2235d9ed'


@pytest.fixture(scope='session')
def session_response_200():
    """Define a successful response for session creation."""
    return {
        'version': 1,
        'revision': 1,
        'timestamp': '2017-11-03T16:45:11.201Z',
        'timestamp_ms': 1509727511201,
        'result_code': 0,
        'result': {
            'client_uuid': '9a1f6b39-d980-4d70-a9ab-9abf2235d9ed',
            'user': {
                'user_uuid': '9d828d98-164d-4fbc-9b61-cadbbdbcfec2',
                'full_name': None,
                'email': 'email@address.com',
                'beta_eligibility': False,
                'gift_recipient': True,
                'locale': 'en-US',
                'email_shared': True,
                'image_url': None,
                'status': 'ACTIVATED',
                'pw_exists': True,
                'linked_accounts': [],
                'registration_timestamp': 1482711582203,
                'last_modified_timestamp': 1482711859731
            },
            'session_start_timestamp': 1509727511194,
            'session_expiration_timestamp': 1509749111194,
            'changes': 'EXISTING_ACCOUNT'
        }
    }


@pytest.fixture(scope='session')
def tile_details_response_200():
    """Define a successful tiles response."""
    return {
        'version': 1,
        'revision': 1,
        'timestamp': '2017-11-03T20:21:48.855Z',
        'timestamp_ms': 1509740508855,
        'result_code': 0,
        'result': {
            '12618ba67acc': {
                'tileState': {
                    'uuid': '12618ba67acc',
                    'connectionStateCode': 1,
                    'ringStateCode': 0,
                    'tile_uuid': '19264d2dffdbca32',
                    'client_uuid': '9a1f6b39-d980-4d70-a9ab-9abf2235d9ed',
                    'timestamp': 1509736740094,
                    'advertised_rssi': 1.4E-45,
                    'client_rssi': 1.4E-45,
                    'battery_level': 1.4E-45,
                    'latitude': 39.735927,
                    'longitude': -104.987767,
                    'altitude': 1603.229126,
                    'h_accuracy': 65.0,
                    'v_accuracy': 10.0,
                    'speed': 1.4E-45,
                    'course': 1.4E-45,
                    'authentication': None,
                    'owned': True,
                    'has_authentication': None,
                    'lost_timestamp': -1,
                    'connection_client_uuid':
                    'a01bf97a-c89a-40e2-9534-29976010fb03',
                    'connection_event_timestamp': 1509731872770,
                    'last_owner_update': 1509736740094,
                    'connection_state': 'READY',
                    'ring_state': 'STOPPED',
                    'voip_state': 'OFFLINE',
                    'is_lost': False
                },
                'thumbnailImage':
                'https://local-tile-pub.s3.amazonaws.com/images/0799D74B-171D-4DD4-8C9B-3E45D5D8DC00-thumb.jpg',
                'tile_uuid': '19264d2dffdbca32',
                'firmware_version': '01.12.14.0',
                'owner_user_uuid': '2ea56f4d-6576-4b4e-af11-3410cc65e373',
                'name': 'Wallet',
                'category': None,
                'image_url':
                'https://local-tile-pub.s3.amazonaws.com/images/0799D74B-171D-4DD4-8C9B-3E45D5D8DC00.jpg',
                'visible': True,
                'is_dead': False,
                'hw_version': '02.09',
                'product': 'DUTCH1',
                'archetype': 'WALLET',
                'configuration': {
                    'fw10_advertising_interval': None
                },
                'last_tile_state': {
                    'uuid': '19264d2dffdbca32',
                    'connectionStateCode': 1,
                    'ringStateCode': 0,
                    'tile_uuid': '19264d2dffdbca32',
                    'client_uuid': '9a1f6b39-d980-4d70-a9ab-9abf2235d9ed',
                    'timestamp': 1509736740094,
                    'advertised_rssi': 1.4E-45,
                    'client_rssi': 1.4E-45,
                    'battery_level': 1.4E-45,
                    'latitude': 39.735927,
                    'longitude': -104.987767,
                    'altitude': 1603.229126,
                    'h_accuracy': 65.0,
                    'v_accuracy': 10.0,
                    'speed': 1.4E-45,
                    'course': 1.4E-45,
                    'authentication': None,
                    'owned': True,
                    'has_authentication': None,
                    'lost_timestamp': -1,
                    'connection_client_uuid':
                    'a01bf97a-c89a-40e2-9534-29976010fb03',
                    'connection_event_timestamp': 1509731872770,
                    'last_owner_update': 1509736740094,
                    'connection_state': 'READY',
                    'ring_state': 'STOPPED',
                    'voip_state': 'OFFLINE',
                    'is_lost': False
                },
                'firmware': {
                    'expected_firmware_version': '01.15.07.0',
                    'expected_firmware_imagename':
                    'Tile_FW_Image_01.15.07.0.bin',
                    'expected_firmware_urlprefix':
                    'https://s3.amazonaws.com/tile-tofu-fw/prod/',
                    'expected_firmware_publish_date': 1458000000000,
                    'expected_ppm': None,
                    'expected_advertising_interval': None,
                    'security_level': 1,
                    'expiry_timestamp': 1509762108855,
                    'expected_tdt_cmd_config': 'DFUZMg=='
                },
                'auth_key': 'qKmshYV05GpUyi35vtiqZQ==',
                'renewal_status': 'NONE',
                'metadata': {},
                'auto_retile': False,
                'status': 'ACTIVATED',
                'tile_type': 'TILE',
                'is_lost': False,
                'auth_timestamp': 1508648644330,
                'registration_timestamp': 1482711833983,
                'activation_timestamp': 1482711835011,
                'last_modified_timestamp': 1482783027671
            },
        }
    }


@pytest.fixture(scope='session')
def tile_list_response_200():
    """Define a successful user_tiles response."""
    return {
        'version': 1,
        'revision': 1,
        'timestamp': '2017-11-03T20:21:15.382Z',
        'timestamp_ms': 1509740475382,
        'result_code': 0,
        'result': [
            {
                'tileType': 'TILE',
                'user_uuid': '9a1f6b39-d980-4d70-a9ab-9abf2235d9ed',
                'tile_uuid': '19264d2dffdbca32',
                'other_user_uuid': '9a1f6b39-d980-4d70-a9ab-9abf2235d9ed',
                'other_user_email': 'email@address.com',
                'mode': 'OWNER',
                'last_modified_timestamp': 1482711833985
            }
        ]
    }


@pytest.fixture(scope='session')
def user_uuid():
    """Define a user UUID."""
    return '9d828d98-164d-4fbc-9b61-cadbbdbcfec2'
