from handlers.remember.base import RememberConfig, Remember
from schemas.base import RememberTypeEnum
from schemas.actions import ActionCreateSchema
from services.actions import get_action_service
from .state_routers.name.handlers import handler as name
from .state_routers.description.handlers import handler as description
from .state_routers.photo.handlers import handler as photo


config = RememberConfig(
    remember_type=RememberTypeEnum.create,
    item_prefix='action',
    service_caller=get_action_service,
    schema=ActionCreateSchema,
    queue=[name, description, photo, ],
    manage_caller=(
        'routers.actions.manage.handler'
    ),
)

handler = Remember(
    config=config
)
