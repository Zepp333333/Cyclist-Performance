#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved
"""
Runner for HARDIO
Do not use it in a production deployment.
"""
from hardio import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


