from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base, mapped_column

Column = mapped_column

metadata = MetaData()

BaseModel = declarative_base(metadata=metadata)
