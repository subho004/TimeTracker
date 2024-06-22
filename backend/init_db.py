from main import engine, Base, SessionLocal, TimeSeriesData
import json
from sqlalchemy.exc import IntegrityError  # Import IntegrityError from sqlalchemy.exc


# Create the tables in the database
Base.metadata.create_all(bind=engine)


def load_initial_data():
    json_files = [
        '00004625_s002_t000.json',
        '00004625_s003_t001.json'
    ]

    db: Session = SessionLocal()
    try:
        for json_file in json_files:
            print(f"Loading data from {json_file}...")
            with open(json_file) as f:
                data = json.load(f)

                timestamps = data.get('time', [])
                total_records = len(timestamps)
                progress_count = 0

                for i in range(total_records):
                    timestamp = timestamps[i]

                    # Prepare data for all fields dynamically
                    db_data = TimeSeriesData(
                        time=str(timestamp),
                        EEG_CZ_REF=data.get('EEG CZ-REF', [])[i] if 'EEG CZ-REF' in data else None,
                        EMG_REF=data.get('EMG-REF', [])[i] if 'EMG-REF' in data else None,
                        EEG_28_REF=data.get('EEG 28-REF', [])[i] if 'EEG 28-REF' in data else None,
                        EEG_30_REF=data.get('EEG 30-REF', [])[i] if 'EEG 30-REF' in data else None,
                        EEG_P4_REF=data.get('EEG P4-REF', [])[i] if 'EEG P4-REF' in data else None,
                        EEG_29_REF=data.get('EEG 29-REF', [])[i] if 'EEG 29-REF' in data else None,
                        EEG_ROC_REF=data.get('EEG ROC-REF', [])[i] if 'EEG ROC-REF' in data else None,
                        EEG_T2_REF=data.get('EEG T2-REF', [])[i] if 'EEG T2-REF' in data else None,
                        EEG_T3_REF=data.get('EEG T3-REF', [])[i] if 'EEG T3-REF' in data else None,
                        EEG_O1_REF=data.get('EEG O1-REF', [])[i] if 'EEG O1-REF' in data else None,
                        SUPPR=data.get('SUPPR', [])[i] if 'SUPPR' in data else None,
                        EEG_P3_REF=data.get('EEG P3-REF', [])[i] if 'EEG P3-REF' in data else None,
                        EEG_FZ_REF=data.get('EEG FZ-REF', [])[i] if 'EEG FZ-REF' in data else None,
                        EEG_F8_REF=data.get('EEG F8-REF', [])[i] if 'EEG F8-REF' in data else None,
                        EEG_27_REF=data.get('EEG 27-REF', [])[i] if 'EEG 27-REF' in data else None,
                        EEG_A1_REF=data.get('EEG A1-REF', [])[i] if 'EEG A1-REF' in data else None,
                        IBI=data.get('IBI', [])[i] if 'IBI' in data else None,
                        BURSTS=data.get('BURSTS', [])[i] if 'BURSTS' in data else None,
                        EEG_F4_REF=data.get('EEG F4-REF', [])[i] if 'EEG F4-REF' in data else None,
                        EEG_EKG1_REF=data.get('EEG EKG1-REF', [])[i] if 'EEG EKG1-REF' in data else None,
                        EEG_LOC_REF=data.get('EEG LOC-REF', [])[i] if 'EEG LOC-REF' in data else None,
                        EEG_T1_REF=data.get('EEG T1-REF', [])[i] if 'EEG T1-REF' in data else None,
                        EEG_T4_REF=data.get('EEG T4-REF', [])[i] if 'EEG T4-REF' in data else None,
                        EEG_C4_REF=data.get('EEG C4-REF', [])[i] if 'EEG C4-REF' in data else None,
                        EEG_26_REF=data.get('EEG 26-REF', [])[i] if 'EEG 26-REF' in data else None,
                        EEG_T5_REF=data.get('EEG T5-REF', [])[i] if 'EEG T5-REF' in data else None,
                        EEG_A2_REF=data.get('EEG A2-REF', [])[i] if 'EEG A2-REF' in data else None,
                        EEG_FP2_REF=data.get('EEG FP2-REF', [])[i] if 'EEG FP2-REF' in data else None,
                        EEG_FP1_REF=data.get('EEG FP1-REF', [])[i] if 'EEG FP1-REF' in data else None,
                        EEG_F3_REF=data.get('EEG F3-REF', [])[i] if 'EEG F3-REF' in data else None,
                        EEG_T6_REF=data.get('EEG T6-REF', [])[i] if 'EEG T6-REF' in data else None,
                        EEG_PZ_REF=data.get('EEG PZ-REF', [])[i] if 'EEG PZ-REF' in data else None,
                        PHOTIC_REF=data.get('PHOTIC-REF', [])[i] if 'PHOTIC-REF' in data else None,
                        EEG_F7_REF=data.get('EEG F7-REF', [])[i] if 'EEG F7-REF' in data else None,
                        EEG_O2_REF=data.get('EEG O2-REF', [])[i] if 'EEG O2-REF' in data else None,
                        # Add more fields as needed
                    )

                    try:
                        db.add(db_data)
                        progress_count += 1
                        if progress_count % 1000 == 0:
                            print(f"Processed {progress_count}/{total_records} records...")

                        # Commit after each record
                        db.commit()

                    except Exception as e:
                        print(f"Error adding record for timestamp {timestamp}: {str(e)}")
                        db.rollback()

                # Commit remaining records
                db.commit()
                print(f"Data from {json_file} successfully loaded.")

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error occurred: {str(e)}")
        db.rollback()
    finally:
        db.close()

# Load the initial data
load_initial_data()



# def delete_all_data():
#     db = SessionLocal()
#     try:
#         db.query(TimeSeriesData).delete()
#         db.commit()
#         print("All data deleted from database.")
#     except Exception as e:
#         print(f"Error occurred: {str(e)}")
#         db.rollback()
#     finally:
#         db.close()

# # Delete all data from the database
# delete_all_data()

# def extract_column_names(json_files):
#     all_columns = set()

#     for json_file in json_files:
#         with open(json_file) as f:
#             data = json.load(f)
#             if isinstance(data, dict):
#                 columns = data.keys()
#                 all_columns.update(columns)

#     return list(all_columns)

# json_files = [
#     '00004625_s002_t000.json',
#     '00004625_s003_t001.json'
# ]

# columns = extract_column_names(json_files)
# print("All column names from JSON files:", columns)