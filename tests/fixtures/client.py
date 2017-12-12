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
            'client_uuid': 'abcdefab-1234-abcd-1234-abcdefabcdef',
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
    return 'abcdefab-1234-abcd-1234-abcdefabcdef'


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
            'client_uuid': 'abcdefab-1234-abcd-1234-abcdefabcdef',
            'user': {
                'user_uuid': 'abcdefab-1234-abcd-1234-abcdefabcdef',
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
def tile_active_response_200():
    """Define a successful tiles response."""
    return {
        'version': 1,
        'revision': 1,
        'timestamp': '2017-12-11T21:03:41.495Z',
        'timestamp_ms': 1513026221495,
        'result_code': 0,
        'result': {
            '1234567890abcdef': {
                'tileState': {
                    'connectionStateCode': 0,
                    'ringStateCode': 0,
                    'uuid': '1234567890abcdef',
                    'tile_uuid': '1234567890abcdef',
                    'client_uuid': '12345678-abcd-1234-abcd-123456789012',
                    'timestamp': 1512615215149,
                    'advertised_rssi': 1.4E-45,
                    'client_rssi': 1.4E-45,
                    'battery_level': 1.4E-45,
                    'latitude': 39.797571,
                    'longitude': -104.887826,
                    'altitude': 1588.002773,
                    'h_accuracy': 5.0,
                    'v_accuracy': 3.0,
                    'speed': 1.4E-45,
                    'course': 1.4E-45,
                    'authentication': None,
                    'owned': True,
                    'has_authentication': None,
                    'lost_timestamp': -1,
                    'connection_client_uuid': '12345678-abcd-1234-abcd-123456789012',
                    'connection_event_timestamp': 1512615234268,
                    'last_owner_update': 1512615215149,
                    'connection_state': 'READY',
                    'ring_state': 'STOPPED',
                    'voip_state': 'OFFLINE',
                    'is_lost': False
                },
                'thumbnailImage': 'https://local-tile-pub.s3.amazonaws.com/images/0799D74B-171D-4DD4-8C9B-3E45D5D8DC00-thumb.jpg',
                'tile_uuid': '19264d2dffdbca32',
                'firmware_version': '01.12.14.0',
                'owner_user_uuid': '12345678-abcd-1234-abcd-123456789012',
                'name': 'Wallet',
                'category': None,
                'image_url': 'https://local-tile-pub.s3.amazonaws.com/images/0799D74B-171D-4DD4-8C9B-3E45D5D8DC00.jpg',
                'visible': True,
                'is_dead': False,
                'hw_version': '02.09',
                'product': 'DUTCH1',
                'archetype': 'WALLET',
                'configuration': {
                    'fw10_advertising_interval': None
                },
                'last_tile_state': {
                    'connectionStateCode': 0,
                    'ringStateCode': 0,
                    'uuid': '1234567890abcdef',
                    'tile_uuid': '1234567890abcdef',
                    'client_uuid': '12345678-abcd-1234-abcd-123456789012',
                    'timestamp': 1512615215149,
                    'advertised_rssi': 1.4E-45,
                    'client_rssi': 1.4E-45,
                    'battery_level': 1.4E-45,
                    'latitude': 39.797571,
                    'longitude': -104.887826,
                    'altitude': 1588.002773,
                    'h_accuracy': 5.0,
                    'v_accuracy': 3.0,
                    'speed': 1.4E-45,
                    'course': 1.4E-45,
                    'authentication': None,
                    'owned': True,
                    'has_authentication': None,
                    'lost_timestamp': -1,
                    'connection_client_uuid': '12345678-abcd-1234-abcd-123456789012',
                    'connection_event_timestamp': 1512615234268,
                    'last_owner_update': 1512615215149,
                    'connection_state': 'READY',
                    'ring_state': 'STOPPED',
                    'voip_state': 'OFFLINE',
                    'is_lost': False
                },
                'firmware': {
                    'expected_firmware_version': '01.17.01.0',
                    'expected_firmware_imagename': 'Tile_FW_Image_01.17.01.0.bin',
                    'expected_firmware_urlprefix': 'https://s3.amazonaws.com/tile-tofu-fw/prod/',
                    'expected_firmware_publish_date': 1458000000000,
                    'expected_ppm': None,
                    'expected_advertising_interval': None,
                    'security_level': 1,
                    'expiry_timestamp': 1513047821494,
                    'expected_tdt_cmd_config': 'DFUZMg=='
                },
                'auth_key': 'qKmshYV05GpUyi35vtiqZQ==',
                'renewal_status': 'LEVEL2',
                'metadata': {},
                'auto_retile': False,
                'status': 'ACTIVATED',
                'tile_type': 'TILE',
                'is_lost': False,
                'auth_timestamp': 1512287015405,
                'registration_timestamp': 1482711833983,
                'activation_timestamp': 1482711835011,
                'last_modified_timestamp': 1513025587187
            }
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
        'result': [{
            'tileType': 'TILE',
            'user_uuid': '12345678-abcd-1234-abcd-123456789012',
            'tile_uuid': '1234567890abcdef',
            'other_user_uuid': '12345678-abcd-1234-abcd-123456789012',
            'other_user_email': 'email@address.com',
            'mode': 'OWNER',
            'last_modified_timestamp': 1482711833985
        }]
    }


@pytest.fixture(scope='session')
def user_uuid():
    """Define a user UUID."""
    return 'abcdefab-1234-abcd-1234-abcdefabcdef'
