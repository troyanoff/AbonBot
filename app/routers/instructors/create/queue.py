from handlers.remember.base import RememberConfig, Remember
from schemas.base import RememberTypeEnum
from schemas.instructors import InstructorCreateSchema
from services.instructors import get_instructor_service
from .state_routers.photo.handlers import handler as photo


config = RememberConfig(
    remember_type=RememberTypeEnum.create,
    item_prefix='instructor',
    service_caller=get_instructor_service,
    schema=InstructorCreateSchema,
    queue=[photo, ],
    manage_caller=(
        'routers.instructors.manage.handler'
    ),
    exists_fields=(
        ('company_uuid', 'company_uuid'),
        ('client_uuid', 'sub_client_uuid')
    ),
)

handler = Remember(
    config=config
)
