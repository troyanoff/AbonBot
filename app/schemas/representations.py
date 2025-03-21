from datetime import datetime, time
from pydantic import EmailStr
from uuid import UUID

from schemas.base import MyBaseModelRepr, BaseReprListSchema, SexEnum
from schemas.general import ItemNameReprMS, HumanNameReprMS, TGPhotoReprMS


# Users
class UserReprSchema(MyBaseModelRepr):
    """User representation."""
    login: str
    description: str
    role: str


class UserListSchema(BaseReprListSchema):
    items: list[UserReprSchema]


# Clients
class ClientMinReprSchema(TGPhotoReprMS, HumanNameReprMS, MyBaseModelRepr):
    """Client representation."""
    sex: SexEnum
    is_premium: bool


class ClientReprSchema(ClientMinReprSchema):
    """Client representation."""
    pass


class ClientListSchema(BaseReprListSchema):
    items: list[ClientReprSchema]


# Companies
class CompanyMinReprSchema(TGPhotoReprMS, ItemNameReprMS, MyBaseModelRepr):
    """Company representation."""
    creator_uuid: UUID
    email: EmailStr
    max_hour_cancel: int


class CompanyReprSchema(CompanyMinReprSchema):
    """Company representation."""
    pass


class CompanyListSchema(BaseReprListSchema):
    items: list[CompanyReprSchema]


# Locations
class LocationMinReprSchema(TGPhotoReprMS, ItemNameReprMS, MyBaseModelRepr):
    """Location representation."""
    company_uuid: UUID
    city: str
    street: str
    house: str
    flat: str
    timezone: int


class LocationReprSchema(LocationMinReprSchema):
    """Location representation."""
    company: CompanyMinReprSchema


class LocationListSchema(BaseReprListSchema):
    items: list[LocationReprSchema]


# Actions
class ActionMinReprSchema(TGPhotoReprMS, ItemNameReprMS, MyBaseModelRepr):
    """Action representation."""
    company_uuid: UUID


class ActionReprSchema(ActionMinReprSchema):
    """Action representation."""
    company: CompanyMinReprSchema


class ActionListSchema(BaseReprListSchema):
    items: list[ActionReprSchema]


# Cards
class CardMinReprSchema(ItemNameReprMS, MyBaseModelRepr):
    """Card representation."""
    company_uuid: UUID
    by_delta: bool
    month_delta: int
    by_count: bool
    count: int
    by_limit: bool
    time_limit: time | None
    freeze: bool
    freezing_days: int
    is_archived: bool


class CardReprSchema(CardMinReprSchema):
    """Card representation."""
    company: CompanyMinReprSchema
    events: list['EventMinReprSchema'] = []


class CardListSchema(BaseReprListSchema):
    items: list[CardReprSchema]


# Instructors
class InstructorMinReprSchema(TGPhotoReprMS, MyBaseModelRepr):
    """Instructor representation."""
    company_uuid: UUID
    client_uuid: UUID


class InstructorReprSchema(InstructorMinReprSchema):
    """Instructor representation."""
    company: CompanyMinReprSchema
    client: ClientMinReprSchema


class InstructorListSchema(BaseReprListSchema):
    items: list[InstructorReprSchema]


# Subscriptions
class SubscriptionMinReprSchema(MyBaseModelRepr):
    """Subscription representation."""
    client_uuid: UUID
    company_uuid: UUID
    role: str


class SubscriptionReprSchema(SubscriptionMinReprSchema):
    """Subscription representation."""
    client: ClientMinReprSchema
    company: CompanyMinReprSchema


class SubscriptionListSchema(BaseReprListSchema):
    items: list[SubscriptionReprSchema]


# Records
class RecordMinReprSchema(MyBaseModelRepr):
    """Record representation."""
    company_uuid: UUID
    client_uuid: UUID
    timeslot_uuid: UUID
    issuance_uuid: UUID


class RecordReprSchema(RecordMinReprSchema):
    """Record representation."""
    company: CompanyMinReprSchema
    client: ClientMinReprSchema
    timeslot: 'TimeslotMinReprSchema'


class RecordListSchema(BaseReprListSchema):
    items: list[RecordReprSchema]


# Timeslots
class TimeslotMinReprSchema(MyBaseModelRepr):
    """Timeslot representation."""
    company_uuid: UUID
    event_uuid: UUID
    instructor_uuid: UUID
    start_time: datetime
    end_time: datetime
    by_count: bool
    max_count: int
    section: str
    total_records: int
    cancel: bool
    cancel_total_records: int


class TimeslotReprSchema(TimeslotMinReprSchema):
    """Timeslot representation."""
    company: CompanyMinReprSchema
    event: 'EventLTReprSchema'
    instructor: InstructorMinReprSchema


class TimeslotListSchema(BaseReprListSchema):
    items: list[TimeslotReprSchema]


# Issuances
class IssuanceMinReprSchema(MyBaseModelRepr):
    """Issuance representation."""
    company_uuid: UUID
    client_uuid: UUID
    card_uuid: UUID
    start_at: datetime
    now_count: int
    was_spent: bool = None
    expired_at: datetime | None = None
    is_freeze: bool
    last_freezing: datetime | None
    freezing_interval: int


class IssuanceReprSchema(IssuanceMinReprSchema):
    """Issuance representation."""
    company: CompanyMinReprSchema
    client: ClientMinReprSchema
    card: CardMinReprSchema


class IssuanceListSchema(BaseReprListSchema):
    items: list[IssuanceReprSchema]


# Events
class EventMinReprSchema(MyBaseModelRepr):
    """Event representation."""
    company_uuid: UUID
    location_uuid: UUID
    action_uuid: UUID
    is_personal: bool


class EventLTReprSchema(EventMinReprSchema):
    location: LocationMinReprSchema
    action: ActionMinReprSchema


class EventReprSchema(EventLTReprSchema):
    """Event representation."""
    company: CompanyMinReprSchema


class EventListSchema(BaseReprListSchema):
    items: list[EventReprSchema]
