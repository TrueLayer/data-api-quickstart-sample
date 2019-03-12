from typing import NamedTuple, List, Optional
from undictify import type_checked_constructor


@type_checked_constructor(skip=True, convert=True)
class Transaction(NamedTuple):

    transaction_id: str
    timestamp: str
    description: str
    transaction_type: str
    transaction_category: str
    transaction_classification: List[str]
    merchant_name: Optional[str]
    amount: float
    currency: str
