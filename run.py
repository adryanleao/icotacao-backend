from app import create_app
from waitress import serve
import os

app = create_app()

port = os.environ.get('PORT', '4131')

if __name__ == "__main__":
    if os.environ.get('APP_ENV', 'development') == "production":
        app.logger.info('Environment prod running. Port %s', port)
        serve(app, host="0.0.0.0", port=port)
    else:
        app.run(debug=True, host='0.0.0.0', port=port)
