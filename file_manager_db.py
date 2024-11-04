import json
from sqlalchemy import create_engine, Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the SQLite database URL
DATABASE_URL = "sqlite:///file_info.db"

# Set up the database engine
engine = create_engine(DATABASE_URL, echo=True)

# Define a base class for our classes to inherit from
Base = declarative_base()

# Define the FileInfo model class
class FileInfo(Base):
    __tablename__ = "file_info"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)  # Enforcing uniqueness for name
    csv_file_path = Column(String, nullable=False)
    column_description = Column(String, nullable=True)

    def __repr__(self):
        return f"<FileInfo(name='{self.name}', csv_file_path='{self.csv_file_path}', column_description='{self.column_description}')>"

# Create the file_info table
Base.metadata.create_all(engine)

# Create a sessionmaker bound to the engine
Session = sessionmaker(bind=engine)

# Function to insert data into the table
def insert_file_info(name, csv_file_path, column_description=None):
    session = Session()
    try:
        # Check if a FileInfo with the given name already exists
        existing_file = session.query(FileInfo).filter_by(name=name).first()
        if existing_file:
            return json.dumps({"success": False, "message": f"A dataset with the name '{name}' already exists."})

        # Proceed with insertion if name does not exist
        file_info = FileInfo(name=name, csv_file_path=csv_file_path, column_description=column_description)
        session.add(file_info)
        session.commit()
        return json.dumps({"success": True, "message": f"Dataset '{name}' added successfully!"})
    except Exception as e:
        return json.dumps({"success": False, "message": f"Error inserting file info: {e}"})
    finally:
        session.close()

def update_column_description(name, column_description):
    session = Session()
    try:
        # Check if a FileInfo with the given name already exists
        existing_file = session.query(FileInfo).filter_by(name=name).first()
        if not existing_file:
            return json.dumps({"success": False, "message": f"A dataset with the name '{name}' does not exist."})

        # Proceed with insertion if name exist
        existing_file.column_description = column_description
        session.commit()
        return json.dumps({"success": True, "message": f"Column description for '{name}' updated successfully!"})
    except Exception as e:
        return json.dumps({"success": False, "message": f"Error updating column description: {e}"})
    finally:
        session.close()
# Function to retrieve all file names and paths
def get_all_file_info():
    session = Session()
    try:
        files = session.query(FileInfo).all()
        return [(file.name, file.csv_file_path, file.column_description) for file in files]
    finally:
        session.close()
