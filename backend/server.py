import grpc
from concurrent import futures
import logging
from timeseries_pb2 import StreamRequest, TimeSeriesData
from timeseries_pb2_grpc import TimeSeriesServiceServicer, add_TimeSeriesServiceServicer_to_server
from sqlalchemy import create_engine, Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure the database URL
DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:5433/postgres"

# Create SQLAlchemy engine, base class, and session maker
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class TimeSeriesDataModel(Base):
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

# Create session maker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# gRPC service implementation
class TimeSeriesService(TimeSeriesServiceServicer):
    def StreamTimeSeriesData(self, request, context):
        db = SessionLocal()
        try:
            start_timestamp = request.start_timestamp
            end_timestamp = request.end_timestamp
            limit = request.limit
            
            # Query data within the specified timestamp range
            query = db.query(TimeSeriesDataModel).filter(
                TimeSeriesDataModel.time >= start_timestamp,
                TimeSeriesDataModel.time <= end_timestamp
            ).limit(limit)
            
            for data_item in query:
                yield TimeSeriesData(
                    id=data_item.id,
                    time=data_item.time,
                    EEG_CZ_REF=data_item.EEG_CZ_REF,
                    EMG_REF=data_item.EMG_REF,
                    EEG_28_REF=data_item.EEG_28_REF,
                    EEG_30_REF=data_item.EEG_30_REF,
                    EEG_P4_REF=data_item.EEG_P4_REF,
                    EEG_29_REF=data_item.EEG_29_REF,
                    EEG_ROC_REF=data_item.EEG_ROC_REF,
                    EEG_T2_REF=data_item.EEG_T2_REF,
                    EEG_T3_REF=data_item.EEG_T3_REF,
                    EEG_O1_REF=data_item.EEG_O1_REF,
                    SUPPR=data_item.SUPPR,
                    EEG_P3_REF=data_item.EEG_P3_REF,
                    EEG_FZ_REF=data_item.EEG_FZ_REF,
                    EEG_F8_REF=data_item.EEG_F8_REF,
                    EEG_27_REF=data_item.EEG_27_REF,
                    EEG_A1_REF=data_item.EEG_A1_REF,
                    IBI=data_item.IBI,
                    BURSTS=data_item.BURSTS,
                    EEG_F4_REF=data_item.EEG_F4_REF,
                    EEG_EKG1_REF=data_item.EEG_EKG1_REF,
                    EEG_LOC_REF=data_item.EEG_LOC_REF,
                    EEG_T1_REF=data_item.EEG_T1_REF,
                    EEG_T4_REF=data_item.EEG_T4_REF,
                    EEG_C4_REF=data_item.EEG_C4_REF,
                    EEG_26_REF=data_item.EEG_26_REF,
                    EEG_T5_REF=data_item.EEG_T5_REF,
                    EEG_A2_REF=data_item.EEG_A2_REF,
                    EEG_FP2_REF=data_item.EEG_FP2_REF,
                    EEG_FP1_REF=data_item.EEG_FP1_REF,
                    EEG_F3_REF=data_item.EEG_F3_REF,
                    EEG_T6_REF=data_item.EEG_T6_REF,
                    EEG_PZ_REF=data_item.EEG_PZ_REF,
                    PHOTIC_REF=data_item.PHOTIC_REF,
                    EEG_F7_REF=data_item.EEG_F7_REF,
                    EEG_O2_REF=data_item.EEG_O2_REF,
                )
        
        finally:
            db.close()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_TimeSeriesServiceServicer_to_server(TimeSeriesService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("gRPC server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()
