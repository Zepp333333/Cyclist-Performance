#  Copyright (c) 2021. Sergei Sazonov. All Rights Reserved

from cycperf import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)


