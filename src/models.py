from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Employee:
    full_name: Optional[str]
    title: Optional[str]
    email: Optional[str]


@dataclass
class Exhibitor:
    company_name: Optional[str]
    industry: Optional[str]
    country: Optional[str]
    website: Optional[str]
    employees: list[Employee] = field(default_factory=list)

