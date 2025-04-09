# from sqlalchemy import select
# from sqlalchemy.orm import Session
# from app.db.database import get_engine
# from app.db import models


# def update_setting_in_db_by_key(key: str, value: str):
#     result_dict = {
#         "success": False,
#         "message": None
#     }

#     engine = get_engine()
#     with Session(engine) as session:
#         found_entry = select(models.Setting).where(models.Setting.key == key)
#         result = session.execute(found_entry).scalars().first()

#         if not result:
#             result_dict['message'] = f"Setting with key '{key}' not found."
#         else:
#             result.value = value
#             session.add(result)
#             session.commit()

#             result_dict['success'] = True
#             result_dict['message'] = f"Setting with key '{key}' updated successfully."
    
#     return result_dict

# def update_settings_in_db_from_dict(settings_dict: dict):
#     result_dict = {
#         "success": False,
#         "message": None
#     }

#     engine = get_engine()
#     with Session(engine) as session:
#         for key, value in settings_dict.items():
#             found_entry = select(models.Setting).where(models.Setting.key == key)
#             result = session.execute(found_entry).scalars().first()

#             if not result:
#                 result_dict['message'] = f"Setting with key '{key}' not found."
#                 return result_dict
#             else:
#                 result.value = value
#                 session.add(result)

#         session.commit()

#         result_dict['success'] = True
#         result_dict['message'] = "Settings updated successfully."
    
#     return result_dict
