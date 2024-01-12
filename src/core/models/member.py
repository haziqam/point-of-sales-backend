from pydantic import BaseModel


class PublicMemberData(BaseModel):
    id: str
    name: str
    points: float = 0.0


class Member(BaseModel):
    public_data: PublicMemberData
    email: str
    hashed_PIN: str

    def get_member_type(self) -> str:
        return "Member"

    def convert_price(self, price: float, points_used: float = 0.0) -> float:
        reduced = price - points_used
        return 0.0 if reduced < 0.0 else reduced


DEFAULT_DISCOUNT_RATE: float = 0.15


class VIPMember(Member):
    discount_rate: float

    @classmethod
    def from_member(
        cls, member: Member, discount_rate: float = DEFAULT_DISCOUNT_RATE
    ) -> "VIPMember":
        return cls(
            public_data=member.public_data,
            email=member.email,
            hashed_PIN=member.hashed_PIN,
            discount_rate=discount_rate,
        )

    def get_member_type(self) -> str:
        return "VIP Member"

    def convert_price(self, price: float, points_used: float = 0.0) -> float:
        discounted = price * (1 - self.discount_rate)
        return super().convert_price(discounted, points_used)
