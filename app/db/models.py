from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Business(Base):
    """Business owner who registers their WhatsApp for AI video responses"""
    __tablename__ = "businesses"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    whatsapp_number = Column(String(20), unique=True, nullable=False, index=True)
    owner_name = Column(String(255))
    business_type = Column(String(100))
    
    # Media assets for video generation
    voice_sample_url = Column(String(500))  # ElevenLabs voice ID or file URL
    avatar_image_url = Column(String(500))  # Avatar image for video
    password_hash = Column(String(255))
    
    # Settings
    response_style = Column(String(50), default="professional")  # professional, casual, friendly
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    customers = relationship("Customer", back_populates="business")
    conversations = relationship("Conversation", back_populates="business")

class Customer(Base):
    """Customer who messages a business via WhatsApp"""
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), nullable=False, index=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    name = Column(String(255))
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    business = relationship("Business", back_populates="customers")
    conversations = relationship("Conversation", back_populates="customer")

class Conversation(Base):
    """Individual message exchange between customer and AI agent"""
    __tablename__ = "conversations"
    
    id = Column(Integer, primary_key=True, index=True)
    business_id = Column(Integer, ForeignKey('businesses.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    
    # Message content
    message_from_customer = Column(Text, nullable=False)
    ai_response_text = Column(Text)
    video_url = Column(String(500))
    
    # Status tracking
    status = Column(String(20), default="pending")  # pending, processing, sent, failed
    error_message = Column(Text)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    sent_at = Column(DateTime)
    
    # Relationships
    business = relationship("Business", back_populates="conversations")
    customer = relationship("Customer", back_populates="conversations")
