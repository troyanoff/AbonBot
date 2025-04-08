from handlers.remember.base import RememberConfig, Remember
from schemas.base import RememberTypeEnum
from schemas.clients import ClientUpdateSchema
from services.clients import get_client_service
from .state_routers.first_name.handlers import handler as fn_h
from .state_routers.last_name.handlers import handler as ln_h
from .state_routers.sex.handlers import handler as sex_h
from .state_routers.photo.handlers import handler as photo_h


config = RememberConfig(
    remember_type=RememberTypeEnum.update,
    item_prefix='client',
    service_caller=get_client_service,
    schema=ClientUpdateSchema,
    queue=[fn_h, ln_h, sex_h, photo_h],
    manage_caller=(
        'routers.clients.profile.state_routers.default.handlers.handler'
    ),
    exists_fields=(
        ('uuid', 'client_uuid'),
    )
)

handler = Remember(
    config=config
)
