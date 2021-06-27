
from datetime import datetime
from Utils.utils import ToDict

class TransactionAdminViewModel(ToDict):
    id: int
    creation_date: str
    quantity: int
    total: float
    product_id: int
    product_name: str
    product_imageSrc: str
    user_id: int
    user_username: str
    