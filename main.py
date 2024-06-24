from app.app import App


def main():
    """
        Main entry point of the application.

        This function initializes and starts the application.
        It also handles any unexpected errors that might occur during execution.
    """

    # Create an instance of the App class and Start the application
    application = App()
    application.start()


if __name__ == "__main__":
    """
        This block ensures that the main() function is only executed if the script is run directly,
        and not if it's imported as a module.
    """
    main()
