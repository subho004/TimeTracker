import grpc
from concurrent import futures
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import logging

from timeseries_pb2 import TimeSeriesData as ProtoTimeSeriesData, StreamRequest
from timeseries_pb2_grpc import TimeSeriesServiceServicer, add_TimeSeriesServiceServicer_to_server

DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5433/postgres"

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class TimeSeriesData(Base):
    __tablename__ = 'data3'
    id = Column(Integer, primary_key=True, index=True)
    time = Column(Float)
    EEG_CZ_REF = Column(Float)
    EMG_REF = Column(Float)
    EEG_28_REF = Column(Float)
    EEG_30_REF = Column(Float)
    EEG_P4_REF = Column(Float)
    EEG_29_REF = Column(Float)
    EEG_ROC_REF = Column(Float)
    EEG_T2_REF = Column(Float)
    EEG_T3_REF = Column(Float)
    EEG_O1_REF = Column(Float)
    SUPPR = Column(Float)
    EEG_P3_REF = Column(Float)
    EEG_FZ_REF = Column(Float)
    EEG_F8_REF = Column(Float)
    EEG_27_REF = Column(Float)
    EEG_A1_REF = Column(Float)
    IBI = Column(Float)
    BURSTS = Column(Float)
    EEG_F4_REF = Column(Float)
    EEG_EKG1_REF = Column(Float)
    EEG_LOC_REF = Column(Float)
    EEG_T1_REF = Column(Float)
    EEG_T4_REF = Column(Float)
    EEG_C4_REF = Column(Float)
    EEG_26_REF = Column(Float)
    EEG_T5_REF = Column(Float)
    EEG_A2_REF = Column(Float)
    EEG_FP2_REF = Column(Float)
    EEG_FP1_REF = Column(Float)
    EEG_F3_REF = Column(Float)
    EEG_T6_REF = Column(Float)
    EEG_PZ_REF = Column(Float)
    PHOTIC_REF = Column(Float)
    EEG_F7_REF = Column(Float)
    EEG_O2_REF = Column(Float)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# gRPC service implementation
class TimeSeriesService(TimeSeriesServiceServicer):
    def StreamTimeSeriesData(self, request, context):
        db = SessionLocal()
        try:
            limit = request.limit
            data = db.query(TimeSeriesData).limit(limit).all()
            for item in data:
                yield ProtoTimeSeriesData(
                    id=item.id,
                    time=item.time,
                    EEG_CZ_REF=item.EEG_CZ_REF,
                    EMG_REF=item.EMG_REF,
                    EEG_28_REF=item.EEG_28_REF,
                    EEG_30_REF=item.EEG_30_REF,
                    EEG_P4_REF=item.EEG_P4_REF,
                    EEG_29_REF=item.EEG_29_REF,
                    EEG_ROC_REF=item.EEG_ROC_REF,
                    EEG_T2_REF=item.EEG_T2_REF,
                    EEG_T3_REF=item.EEG_T3_REF,
                    EEG_O1_REF=item.EEG_O1_REF,
                    SUPPR=item.SUPPR,
                    EEG_P3_REF=item.EEG_P3_REF,
                    EEG_FZ_REF=item.EEG_FZ_REF,
                    EEG_F8_REF=item.EEG_F8_REF,
                    EEG_27_REF=item.EEG_27_REF,
                    EEG_A1_REF=item.EEG_A1_REF,
                    IBI=item.IBI,
                    BURSTS=item.BURSTS,
                    EEG_F4_REF=item.EEG_F4_REF,
                    EEG_EKG1_REF=item.EEG_EKG1_REF,
                    EEG_LOC_REF=item.EEG_LOC_REF,
                    EEG_T1_REF=item.EEG_T1_REF,
                    EEG_T4_REF=item.EEG_T4_REF,
                    EEG_C4_REF=item.EEG_C4_REF,
                    EEG_26_REF=item.EEG_26_REF,
                    EEG_T5_REF=item.EEG_T5_REF,
                    EEG_A2_REF=item.EEG_A2_REF,
                    EEG_FP2_REF=item.EEG_FP2_REF,
                    EEG_FP1_REF=item.EEG_FP1_REF,
                    EEG_F3_REF=item.EEG_F3_REF,
                    EEG_T6_REF=item.EEG_T6_REF,
                    EEG_PZ_REF=item.EEG_PZ_REF,
                    PHOTIC_REF=item.PHOTIC_REF,
                    EEG_F7_REF=item.EEG_F7_REF,
                    EEG_O2_REF=item.EEG_O2_REF
                )
        finally:
            db.close()

# Register gRPC service with server
grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

def serve():
    add_TimeSeriesServiceServicer_to_server(TimeSeriesService(), grpc_server)
    grpc_server.add_insecure_port('[::]:50051')
    grpc_server.start()
    logging.info("gRPC server started on port 50051")
    grpc_server.wait_for_termination()

# Endpoint to gracefully stop gRPC server
@app.on_event("shutdown")
def shutdown_event():
    grpc_server.stop(0)
    logging.info("gRPC server stopped")

# FastAPI endpoint to query data
@app.get("/data/")
def read_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = db.query(TimeSeriesData).offset(skip).limit(limit).all()
    return [{"id": item.id,
             "time": item.time,
             "EEG_CZ_REF": item.EEG_CZ_REF,
             "EMG_REF": item.EMG_REF,
             "EEG_28_REF": item.EEG_28_REF,
             "EEG_30_REF": item.EEG_30_REF,
             "EEG_P4_REF": item.EEG_P4_REF,
             "EEG_29_REF": item.EEG_29_REF,
             "EEG_ROC_REF": item.EEG_ROC_REF,
             "EEG_T2_REF": item.EEG_T2_REF,
             "EEG_T3_REF": item.EEG_T3_REF,
             "EEG_O1_REF": item.EEG_O1_REF,
             "SUPPR": item.SUPPR,
             "EEG_P3_REF": item.EEG_P3_REF,
             "EEG_FZ_REF": item.EEG_FZ_REF,
             "EEG_F8_REF": item.EEG_F8_REF,
             "EEG_27_REF": item.EEG_27_REF,
             "EEG_A1_REF": item.EEG_A1_REF,
             "IBI": item.IBI,
             "BURSTS": item.BURSTS,
             "EEG_F4_REF": item.EEG_F4_REF,
             "EEG_EKG1_REF": item.EEG_EKG1_REF,
             "EEG_LOC_REF": item.EEG_LOC_REF,
             "EEG_T1_REF": item.EEG_T1_REF,
             "EEG_T4_REF": item.EEG_T4_REF,
             "EEG_C4_REF": item.EEG_C4_REF,
             "EEG_26_REF": item.EEG_26_REF,
             "EEG_T5_REF": item.EEG_T5_REF,
             "EEG_A2_REF": item.EEG_A2_REF,
             "EEG_FP2_REF": item.EEG_FP2_REF,
             "EEG_FP1_REF": item.EEG_FP1_REF,
             "EEG_F3_REF": item.EEG_F3_REF,
             "EEG_T6_REF": item.EEG_T6_REF,
             "EEG_PZ_REF": item.EEG_PZ_REF,
             "PHOTIC_REF": item.PHOTIC_REF,
             "EEG_F7_REF": item.EEG_F7_REF,
             "EEG_O2_REF": item.EEG_O2_REF
            } for item in data]

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    serve()
