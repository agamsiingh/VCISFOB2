"""
Value Chain Integration System for Oilseed By-Products
A production-ready AgriTech platform for marketplace, IoT, blockchain-style transactions, and AI forecasting.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from Crypto.Hash import SHA256
from sklearn.ensemble import RandomForestRegressor
import json, os

# =====================================================================
# DATABASE INITIALIZATION (CLOUD-SAFE)
# =====================================================================
Base = declarative_base()

DB_PATH = os.path.join(os.path.dirname(__file__), "valuechain.db")
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)

try:
    Base.metadata.create_all(engine)
except Exception as e:
    st.warning(f"Database initialization issue: {e}")

# =====================================================================
# MODELS
# =====================================================================

class Device(Base):
    __tablename__ = 'devices'
    id = Column(Integer, primary_key=True)
    device_id = Column(String(50), unique=True, nullable=False)
    device_type = Column(String(50))
    location = Column(String(100))
    temperature = Column(Float)
    humidity = Column(Float)
    production_rate = Column(Float)
    timestamp = Column(DateTime, default=datetime.now)


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    tx_type = Column(String(50))
    seller = Column(String(100))
    buyer = Column(String(100))
    product = Column(String(100))
    quantity = Column(Float)
    price = Column(Float)
    payload = Column(Text)
    tx_hash = Column(String(64), unique=True)
    timestamp = Column(DateTime, default=datetime.now)


class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    seller = Column(String(100))
    product = Column(String(100))
    quantity = Column(Float)
    price_per_kg = Column(Float)
    quality_grade = Column(String(20))
    location = Column(String(100))
    status = Column(String(20), default='active')
    created_at = Column(DateTime, default=datetime.now)


class PriceHistory(Base):
    __tablename__ = 'price_history'
    id = Column(Integer, primary_key=True)
    product = Column(String(100))
    price = Column(Float)
    date = Column(DateTime)

# =====================================================================
# UTILS
# =====================================================================

def hash_transaction(payload: dict) -> str:
    payload_str = json.dumps(payload, sort_keys=True)
    hash_obj = SHA256.new(payload_str.encode("utf-8"))
    return hash_obj.hexdigest()

def log_transaction(tx_type, seller, buyer, product, quantity, price):
    session = Session()
    payload = {
        "type": tx_type,
        "seller": seller,
        "buyer": buyer,
        "product": product,
        "quantity": quantity,
        "price": price,
        "timestamp": datetime.now().isoformat(),
    }
    tx_hash = hash_transaction(payload)
    tx = Transaction(
        tx_type=tx_type,
        seller=seller,
        buyer=buyer,
        product=product,
        quantity=quantity,
        price=price,
        payload=json.dumps(payload),
        tx_hash=tx_hash,
    )
    session.add(tx)
    session.commit()
    session.close()
    return tx_hash

def generate_iot_telemetry():
    return {
        "temperature": round(np.random.uniform(20, 35), 2),
        "humidity": round(np.random.uniform(40, 70), 2),
        "production_rate": round(np.random.uniform(100, 500), 2),
    }

# =====================================================================
# MAIN UI ENTRY POINT
# =====================================================================

def main():
    st.set_page_config(
        page_title="AgriTech Value Chain Integration",
        page_icon="🌾",
        layout="wide"
    )
    st.title("🌾 Value Chain Integration System for Oilseed By-Products")
    st.markdown("**AI-Powered Marketplace | IoT | Blockchain | Predictive Analytics**")

    # Load Tabs (abbreviated here — reuse your existing tab definitions)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Marketplace", "🔌 IoT Devices", "📈 AI Forecasting",
        "🔐 Ledger", "🌍 Export", "🗺️ Roadmap"
    ])

    with tab1:
        st.write("🛒 Marketplace working... (trimmed for brevity)")
        st.info("This is just a startup test section; your full logic goes here.")

    with tab6:
        st.success("✅ App initialized successfully on Streamlit Cloud!")

# =====================================================================
# EXECUTION SAFEGUARD
# =====================================================================

if __name__ == "__main__":
    main()
