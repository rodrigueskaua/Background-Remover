import os

class Config:
    UPLOAD_FOLDER = os.path.join('uploads', 'original')
    OUTPUT_FOLDER = os.path.join('uploads', 'processed')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
