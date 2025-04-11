from handlers.remember.base import RememberConfig, Remember
from schemas.base import RememberTypeEnum
from schemas.instructors import InstructorUpdateSchema
from services.instructors import get_instructor_service
from .state_routers.photo.handlers import handler as photo


config = RememberConfig(
    remember_type=RememberTypeEnum.update,
    item_prefix='instructor',
    service_caller=get_instructor_service,
    schema=InstructorUpdateSchema,
    queue=[photo, ],
    manage_caller=(
        'routers.instructors.manage.handler'
    ),
    exists_fields=(('uuid', 'instructor_uuid'), ),
)

handler = Remember(
    config=config
)
