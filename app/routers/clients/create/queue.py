

from handlers.remember.base import RememberConfig, RememberCreate
from schemas.clients import ClientCreateSchema
from services.clients import get_client_service
from .state_routers.first_name.handlers import handler as fn_h
from .state_routers.last_name.handlers import handler as ln_h
from .state_routers.sex.handlers import handler as sex_h
from .state_routers.photo.handlers import handler as photo_h


config = RememberConfig(
    service_caller=get_client_service,
    generated_field='new_client',
    schema=ClientCreateSchema,
    queue=[fn_h, ln_h, sex_h, photo_h],
    manage_caller=(
        'routers.clients.profile.state_routers.default.handlers.handler'
    )
)

handler = RememberCreate(
    config=config
)
