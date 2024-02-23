from .database import Base;
from sqlalchemy import TIMESTAMP, Column,Integer,String,Boolean,ForeignKey; 
from sqlalchemy.sql.expression import text;
from sqlalchemy.orm import relationship;

class Post(Base):
    __tablename__ = "Post";
    
    id = Column(Integer,primary_key=True,nullable=False);
    title = Column(String,nullable=False);
    content = Column(String, nullable=False);
    published = Column(Boolean, server_default='True',nullable=False);
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'));
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'));
    owner_id = Column(Integer,ForeignKey("User.id", ondelete="CASCADE"), nullable=False);
    owner = relationship("User");
class User(Base):
    __tablename__ = "User";
    
    id = Column(Integer, primary_key=True, nullable=False);
    name = Column(String, nullable=False);
    email = Column(String, nullable=False, unique=True);
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'));
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'));
    
class Vote(Base):
    __tablename__ = "Vote";
    post_id = Column(Integer, ForeignKey("Post.id", ondelete="CASCADE"), primary_key=True);
    user_id = Column(Integer,ForeignKey("User.id", ondelete="CASCADE"), primary_key=True);