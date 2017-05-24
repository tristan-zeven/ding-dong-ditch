from collections import namedtuple
from datetime import datetime, timedelta
import logging
import os.path
import pickle

from . import system_settings as settings
from . import firebase_user_settings_adapter

ADAPTERS = {
    'firebase': firebase_user_settings_adapter
}

logger = logging.getLogger(__name__)

Unit = namedtuple('Unit', 'should_ring_bell recipients')


def get_adapter():
    adapter_name = settings.USER_SETTINGS_ADAPTER
    if adapter_name not in ADAPTERS:
        raise ValueError('Unknown adapter: {}'.format(adapter_name))
    return ADAPTERS[adapter_name]


def get_data():
    adapter = get_adapter()
    logger.info('Getting user settings from adapter "%s"', adapter.NAME)

    try:
        data = adapter.get_settings()
    except Exception as e:
        logger.exception(
            'Could not load user settings from adapter "%s": %s', adapter.NAME, e
        )
        return None
    return data


def set_data(key, data, root='settings'):
    adapter = get_adapter()
    logger.info('Setting user settings with adapter "%s"', adapter.NAME)

    try:
        data = adapter.set_data(key, data, root)
    except Exception as e:
        logger.exception(
            'Could not set user settings with adapter "%s": %s', adapter.NAME, e
        )


def init_data():
    data = {
        settings.UNIT_1.id: 1,
        settings.UNIT_2.id: 1,
    }
    set_data('units', data, 'systemSettings')
    return get_data()


def get_unit_by_id(unit_id):
    """
    Return a Unit by its ID.
    """
    # unit ID should always be a string
    unit_id = str(unit_id)
    data = get_data()
    if data and unit_id in data:
        unit_data = data[unit_id]
        should_ring_bell = unit_data.get('chime', 1)
        recipients = list(unit_data.get('recipients', {}).keys())
        return Unit(
            should_ring_bell=should_ring_bell,
            recipients=recipients
        )
    return None
