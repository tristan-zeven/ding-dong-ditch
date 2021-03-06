from collections import namedtuple
from gpiozero import Button, DigitalOutputDevice

from . import system_settings as settings

Unit = namedtuple('Unit', 'id buzzer bell strike')


class Strike(DigitalOutputDevice):
    """A class to represent an electronic gate strike."""
    _instances = {}

    DEFAULT_DURATION = 3

    def release(self, duration=None):
        """Release the strike, thus opening the door/gate it is guarding.

        Arguments:
            duration: The duration that the strike should remain open, in seconds.
        """
        on_time = duration or self.DEFAULT_DURATION
        super(Strike, self).blink(on_time=on_time, off_time=1, n=1, background=True)

    @classmethod
    def get(cls, pin=None, *args, **kwargs):
        try:
            return cls._instances[pin]
        except KeyError:
            instance = cls(pin, *args, **kwargs)
            cls._instances[pin] = instance
            return instance


class Bell(DigitalOutputDevice):
    """A class to represent a doorbell chime."""

    def ring(self, ding_dong=.5):
        """Ring a doorbell chime with a friendly DING-DONG sound.

        Arguments:
            ding_dong: The duration of the gap between "ding" and "dong", in seconds.
        """
        super(Bell, self).blink(on_time=ding_dong, off_time=1, n=1, background=True)


UNIT_1 = UNIT_2 = None

if settings.UNIT_1.id:
    UNIT_1 = Unit(
        id=settings.UNIT_1.id,
        buzzer=Button(pin=settings.UNIT_1.buzzer, hold_time=settings.BUZZER_HOLD),
        bell=Bell(settings.UNIT_1.bell),
        strike=Strike.get(settings.UNIT_1.strike)
    )

if settings.UNIT_2.id:
    UNIT_2 = Unit(
        id=settings.UNIT_2.id,
        buzzer=Button(pin=settings.UNIT_2.buzzer, hold_time=settings.BUZZER_HOLD),
        bell=Bell(settings.UNIT_2.bell),
        strike=Strike.get(settings.UNIT_2.strike)
    )


def get_unit_by_id(unit_id):
    """
    Return a Unit by its ID.
    """
    # unit ID should always be a string
    unit_id = str(unit_id)
    if unit_id == UNIT_1.id:
        return UNIT_1
    elif unit_id == UNIT_2.id:
        return UNIT_2
    return None
