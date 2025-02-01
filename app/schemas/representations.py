from datetime import datetime
from pydantic import Field, EmailStr
from uuid import UUID

from schemas.base import MyBaseModelUUID, SexEnum, ClientRoleEnum


class UserReprSchema(MyBaseModelUUID):
    """User representation."""
    login: str
    description: str
    created_at: datetime
    role: str

class ClientMinReprSchema(MyBaseModelUUID):
    """Client representation."""
    tg_id: int
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    photo_id: str | None = Field(max_length=100, default=None)
    photo_unique_id: str | None = Field(max_length=20, default=None)
    sex: SexEnum | None = Field(default=None)
    role: ClientRoleEnum | None = Field(default=None)
    created_at: datetime


class ClientReprSchema(ClientMinReprSchema):
    """Client representation."""
    companies: list['CompanyMinReprSchema'] = []
    subscriptions: list['SubscriptionMinReprSchema'] = []
    records: list['RecordMinReprSchema'] = []

class CompanyMinReprSchema(MyBaseModelUUID):
    """Company representation."""
    name: str = Field(max_length=50)
    creator_uuid: UUID
    description: str = Field(max_length=300)
    photo: str | None = Field(max_length=500, default=None)
    video: str | None = Field(max_length=500, default=None)
    email: EmailStr
    created_at: datetime


class CompanyReprSchema(CompanyMinReprSchema):
    """Company representation."""
    creator: ClientMinReprSchema
    locations: list['LocationMinReprSchema'] = []
    trainings: list['TrainingMinReprSchema'] = []
    instructors: list['InstructorMinReprSchema'] = []
    abonnements: list['AbonnementMinReprSchema'] = []
    subscriptions: list['SubscriptionMinReprSchema'] = []


class LocationMinReprSchema(MyBaseModelUUID):
    """Location representation."""
    name: str = Field(max_length=50)
    company_uuid: UUID
    description: str = Field(max_length=300)
    city: str = Field(max_length=50)
    street: str = Field(max_length=60)
    house: str = Field(max_length=10)
    flat: str = Field(max_length=10)
    photo: str | None = Field(max_length=500, default=None)
    video: str | None = Field(max_length=500, default=None)
    timezone: int
    created_at: datetime


class LocationReprSchema(LocationMinReprSchema):
    """Location representation."""
    company: CompanyMinReprSchema
    trainings: list['TrainingMinReprSchema'] = []
    abonnements: list['AbonnementMinReprSchema'] = []
    timeslots: list['TimeslotMinReprSchema'] = []


class TrainingMinReprSchema(MyBaseModelUUID):
    """Training representation."""
    name: str = Field(max_length=100)
    company_uuid: UUID
    description: str | None = Field(max_length=300, default=None)
    photo: str | None = Field(max_length=500, default=None)
    video: str | None = Field(max_length=500, default=None)
    created_at: datetime


class TrainingReprSchema(TrainingMinReprSchema):
    """Training representation."""
    company: CompanyMinReprSchema
    locations: list[LocationMinReprSchema] = []
    abonnements: list['AbonnementMinReprSchema'] = []
    timeslots: list['TimeslotMinReprSchema'] = []

class AbonnementMinReprSchema(MyBaseModelUUID):
    """Abonnement representation."""
    name: str = Field(max_length=50)
    company_uuid: UUID
    description: str | None = Field(max_length=300, default=None)
    by_delta: bool = False
    month_delta: int = None
    by_count: bool = False
    count: int = None
    created_at: datetime


class AbonnementReprSchema(AbonnementMinReprSchema):
    """Abonnement representation."""
    company: CompanyMinReprSchema
    locations: list[LocationMinReprSchema] = []
    trainings: list[TrainingMinReprSchema] = []

class InstructorMinReprSchema(MyBaseModelUUID):
    """Instructor representation."""
    company_uuid: UUID
    tg_id: int
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    photo: str | None = Field(max_length=500, default=None)
    video: str | None = Field(max_length=500, default=None)
    created_at: datetime


class InstructorReprSchema(InstructorMinReprSchema):
    """Instructor representation."""
    company: CompanyMinReprSchema
    timeslots: list['TimeslotMinReprSchema'] = []


class SubscriptionMinReprSchema(MyBaseModelUUID):
    """Subscription representation."""
    client_uuid: UUID
    company_uuid: UUID
    abonnement_uuid: UUID
    role: str
    created_at: datetime


class SubscriptionReprSchema(SubscriptionMinReprSchema):
    """Subscription representation."""
    client: ClientMinReprSchema
    company: CompanyMinReprSchema
    abonnement: AbonnementMinReprSchema


class RecordMinReprSchema(MyBaseModelUUID):
    """Record representation."""
    company_uuid: UUID
    client_uuid: UUID
    timeslot_uuid: UUID
    created_at: datetime


class RecordReprSchema(RecordMinReprSchema):
    """Record representation."""
    company: CompanyMinReprSchema
    client: ClientMinReprSchema
    timeslot: 'TimeslotMinReprSchema'


class TimeslotMinReprSchema(MyBaseModelUUID):
    """Timeslot representation."""
    description: str | None = Field(max_length=400, default=None)
    company_uuid: UUID
    location_uuid: UUID
    training_uuid: UUID
    instructor_uuid: UUID
    start: datetime
    end: datetime
    max_count: int


class TimeslotReprSchema(TimeslotMinReprSchema):
    """Timeslot representation."""
    company: CompanyMinReprSchema
    location: LocationMinReprSchema
    training: TrainingMinReprSchema
    instructor: InstructorMinReprSchema
    records: list[RecordMinReprSchema] = []

