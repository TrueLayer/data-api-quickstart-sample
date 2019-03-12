from typing import NamedTuple
from undictify import type_checked_constructor


@type_checked_constructor()
class Provider(NamedTuple):
    display_name: str
    logo_uri: str
    provider_id: str
