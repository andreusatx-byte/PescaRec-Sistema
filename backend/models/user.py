from sqlalchemy import Column, String, Boolean, Text
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    full_name = Column(String(255), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    
    # Perfil
    bio = Column(Text, nullable=True)
    experience_level = Column(String(50), default="iniciante")  # 'iniciante', 'intermediário', 'avançado'
    
    # Status
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    # Preferências
    preferred_species = Column(String(255), nullable=True)
    preferred_locations = Column(String(255), nullable=True)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
