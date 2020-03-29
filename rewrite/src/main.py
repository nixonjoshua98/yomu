
if __name__ == "__main__":
    import os
    import sys

    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    
    from src.interface import Application

    app = Application()

    app.mainloop()
