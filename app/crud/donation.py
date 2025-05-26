from app.models import Donation
from app.schemas.donation import (
    DonationCreate,
    DonationDB
)
from app.crud.base import CRUDBase


class DonationCRUD(CRUDBase[Donation, DonationCreate, DonationDB]):
    pass


donation_crud = DonationCRUD(Donation)
