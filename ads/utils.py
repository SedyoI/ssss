def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_ad_response(ad, images=None):
   
    return {
        "id": ad.id,
        "title": ad.title,
        "description": ad.description,
        "location": ad.location,
        "price": ad.price,
        "images": images or []  
    }