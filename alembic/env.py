# alembic/env.py

# ... existing imports
from models import SQLModel # Import SQLModel from your models file

# ... existing code
# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# === ADD THIS ===
from models import * # This ensures all your model classes are loaded
target_metadata = SQLModel.metadata
# === END ADD ===

# ... rest of the file
