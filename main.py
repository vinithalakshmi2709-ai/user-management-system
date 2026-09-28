from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, Base, get_db
from models import User, Profile
from schemas import UserCreate, UserLogin, ProfileCreate, ProfileUpdate
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user
)

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "User Management System API is running"}


@app.post("/auth/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)

    new_user = User( 
    name=user.name,
    email=user.email,
    password_hash=hashed_password
)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }

@app.post("/auth/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        existing_user.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": str(existing_user.id)}
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer"
    }

@app.get("/users/me")
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "profile": {
            "id": profile.id,
            "phone": profile.phone,
            "address": profile.address,
            "date_of_birth": profile.date_of_birth,
            "bio": profile.bio
        }
    }
@app.get("/users")
def get_all_users(
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return [
        {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
        for user in users
    ]

@app.post("/users/profile")
def create_profile(
    profile: ProfileCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists"
        )

    new_profile = Profile(
        user_id=current_user.id,
        phone=profile.phone,
        address=profile.address,
        date_of_birth=profile.date_of_birth,
        bio=profile.bio
    )

    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)

    return {
        "message": "Profile created successfully",
        "profile": {
            "id": new_profile.id,
            "user_id": new_profile.user_id,
            "phone": new_profile.phone,
            "address": new_profile.address,
            "date_of_birth": new_profile.date_of_birth,
            "bio": new_profile.bio
        }
    }

@app.put("/users/profile")
def update_profile(
    profile: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if not existing_profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    if profile.phone is not None:
        existing_profile.phone = profile.phone

    if profile.address is not None:
        existing_profile.address = profile.address

    if profile.date_of_birth is not None:
        existing_profile.date_of_birth = profile.date_of_birth

    if profile.bio is not None:
        existing_profile.bio = profile.bio

    db.commit()
    db.refresh(existing_profile)

    return {
        "message": "Profile updated successfully",
        "profile": {
            "id": existing_profile.id,
            "user_id": existing_profile.user_id,
            "phone": existing_profile.phone,
            "address": existing_profile.address,
            "date_of_birth": existing_profile.date_of_birth,
            "bio": existing_profile.bio
        }
    }

@app.delete("/users/profile")
def delete_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    existing_profile = db.query(Profile).filter(
        Profile.user_id == current_user.id
    ).first()

    if not existing_profile:
        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    db.delete(existing_profile)
    db.commit()

    return {
        "message": "Profile deleted successfully"
    }