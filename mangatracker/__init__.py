def run():
    import os
    import logging

    from mangatracker.interface.application import Application

    log_file = os.path.join(os.getcwd(), "mangatracker\\data\\log.log")

    # Ensure the path to the log file exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Configure the root logger which we will be using
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='[%(asctime)s] %(message)s',
        level=logging.NOTSET
    )

    logging.info("- - - PROGRAM LAUNCHED - - -")

    Application().mainloop()

    logging.info("- - - PROGRAM EXITED - - -")


