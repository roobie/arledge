from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from pydantic import BaseModel, field_validator, model_validator

from . import config


class Creditor(BaseModel):

    id: Optional[int] = None
    name: str
    address: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    tax_id: Optional[str] = None
    payment_instructions: Optional[str] = None
    default_currency: str = "SEK"
    beancount_account: Optional[str] = None
    created_at: Optional[datetime] = None

    @field_validator("created_at", mode="before")
    def _coerce_created_at(cls, v):
        if v is None:
            return datetime.now(timezone.utc)
        if isinstance(v, str):
            return config.iso_to_dt(v)
        return v


class PaymentAccount(BaseModel):

    id: Optional[int] = None
    creditor_id: int
    type: str
    label: Optional[str] = None
    identifier: Optional[str] = None
    bank_name: Optional[str] = None
    currency: Optional[str] = None
    beancount_account: Optional[str] = None
    is_default: bool = False
    metadata: Dict[str, Any] = {}
    created_at: Optional[datetime] = None

    @field_validator("created_at", mode="before")
    def _coerce_created_at(cls, v):
        if v is None:
            return datetime.now(timezone.utc)
        if isinstance(v, str):
            return config.iso_to_dt(v)
        return v


class Customer(BaseModel):
    id: Optional[int] = None
    name: str
    email: Optional[str] = None
    address: Optional[str] = None


class InvoiceLine(BaseModel):
    description: str
    quantity: Decimal = Decimal("1")
    unit_price: Decimal
    vat_rate: Decimal = Decimal("0")
    net: Optional[Decimal] = None
    vat: Optional[Decimal] = None
    line_total: Optional[Decimal] = None

    @field_validator("quantity", "unit_price", "vat_rate", mode="before")
    def _coerce_decimal(cls, v):
        if isinstance(v, str):
            return Decimal(v)
        if isinstance(v, float):
            return Decimal(str(v))
        return v

    @model_validator(mode="after")
    def compute_totals(self):
        q = Decimal(self.quantity)
        up = Decimal(self.unit_price)
        net = (q * up).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        vat = (net * (Decimal(self.vat_rate) / Decimal("100"))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        lt = (net + vat).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        self.net = net
        self.vat = vat
        self.line_total = lt
        return self


class Invoice(BaseModel):

    id: Optional[int] = None
    customer_id: int
    status: str = "draft"
    created_at: Optional[datetime] = None
    due_at: Optional[datetime] = None
    description: Optional[str] = None
    creditor_id: Optional[int] = None
    currency: str = "SEK"
    lines: List[InvoiceLine] = []
    subtotal: Optional[Decimal] = None
    total_vat: Optional[Decimal] = None
    total: Optional[Decimal] = None

    @field_validator("created_at", "due_at", mode="before")
    def _coerce_datetimes(cls, v):
        if v is None:
            return None
        if isinstance(v, str):
            return config.iso_to_dt(v)
        return v

    @model_validator(mode="after")
    def compute_totals(self):
        # ensure lines are InvoiceLine instances
        lines = [l if isinstance(l, InvoiceLine) else InvoiceLine(**l) for l in self.lines]
        self.lines = lines
        subtotal = Decimal("0")
        total_vat = Decimal("0")
        for l in lines:
            subtotal += Decimal(l.net)
            total_vat += Decimal(l.vat)
        self.subtotal = subtotal.quantize(Decimal("0.01"))
        self.total_vat = total_vat.quantize(Decimal("0.01"))
        self.total = (self.subtotal + self.total_vat).quantize(Decimal("0.01"))
        if self.created_at is None:
            self.created_at = datetime.now(timezone.utc)
        return self
