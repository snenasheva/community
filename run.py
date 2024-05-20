import os
from com import app

print('Current directory:', os.getcwd())
if __name__ == '__main__':
    app.run(debug=True)