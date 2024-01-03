from pydantic import BaseModel

# TODO: move somewhere
TAX_RATE = 0.01

class PublicMemberData(BaseModel):
    id: str
    name: str
    points: float = 0

class Member(BaseModel):
    public_data: PublicMemberData
    email: str
    hashed_PIN: str

    def get_member_type() -> str:
        return 'Member'
    
    def convert_price(self, price: float, points_used: float = 0.0) -> float:
        reduced = price - points_used
        if reduced < 0.0: 
            reduced = 0.0
        taxed = reduced * (1 + TAX_RATE)
        return taxed
    
class VIPMember(Member):
    discount_rate: float

    def get_member_type() -> str:
        return 'VIP Member'
    
    def convert_price(self, price: float, points_used: float = 0) -> float:
        discounted = price * (1 - self.discount_rate)
        return super().convert_price(discounted, points_used)