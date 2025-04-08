from handlers.remember.base import RememberConfig, Remember
from schemas.base import RememberTypeEnum
from schemas.locations import LocationCreateSchema
from services.locations import get_location_service
from .state_routers.name.handlers import handler as name
from .state_routers.description.handlers import handler as description
from .state_routers.photo.handlers import handler as photo
from .state_routers.city.handlers import handler as city
from .state_routers.street.handlers import handler as street
from .state_routers.house.handlers import handler as house
from .state_routers.flat.handlers import handler as flat
from .state_routers.timezone.handlers import handler as timezone


config = RememberConfig(
    remember_type=RememberTypeEnum.create,
    item_prefix='location',
    service_caller=get_location_service,
    schema=LocationCreateSchema,
    queue=[name, description, photo, city, street, house, flat, timezone],
    manage_caller=(
        'routers.locations.manage.handler'
    ),
)

handler = Remember(
    config=config
)
