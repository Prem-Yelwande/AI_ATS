from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List


class Project(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: List[str] = []
    live_link: Optional[str] = None

class Experience(BaseModel):
    company_name: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    location: Optional[str] = None
    responsibilities: List[str] = []

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    location: Optional[str] = None
    duration: Optional[str] = None
    gpa: Optional[str] = None
    coursework: List[str] = []


class ResumeData(BaseModel):
    model_config = ConfigDict(extra="allow")

    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    github: Optional[str] = None
    linkedin: Optional[str] = None
    location: Optional[str] = None

    education: List[Education] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    experience: List[Experience] = Field(default_factory=list)

    projects: List[Project] = Field(default_factory=list)

    certifications: List[str] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)

    summary: Optional[str] = None
