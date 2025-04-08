from handlers.remember.base import RememberConfig, Remember
from schemas.base import RememberTypeEnum
from schemas.companies import CompanyCreateSchema
from services.companies import get_company_service
from .state_routers.name.handlers import handler as name
from .state_routers.description.handlers import handler as description
from .state_routers.email.handlers import handler as email
from .state_routers.photo.handlers import handler as photo
from .state_routers.max_hour_cancel.handlers import handler as max_hour_cancel


config = RememberConfig(
    remember_type=RememberTypeEnum.create,
    item_prefix='company',
    service_caller=get_company_service,
    generated_field='new_company',
    schema=CompanyCreateSchema,
    queue=[name, description, email, photo, max_hour_cancel],
    manage_caller=(
        'routers.companies.manage.handler'
    ),
    exists_fields=(('creator_uuid', 'client_uuid'), ),
)

handler = Remember(
    config=config
)
