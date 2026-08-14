import logging
import os

from datetime import datetime

from src.config import (
    LOG_DIR,
    DATA_FILE
)

from src.data_loader import (
    prepare_data
)

from src.analyzer import (
    get_recent_week
)

from src.visualizer import (
    create_report_charts
)

from src.report_generator import (
    create_excel_report
)

from src.email_sender import (
    load_env,
    email_report
)


# ---------------------------------
# CREATE DIRECTORIES
# ---------------------------------

os.makedirs(
    LOG_DIR,
    exist_ok=True
)


# ---------------------------------
# LOGGING
# ---------------------------------

log_file = os.path.join(
    LOG_DIR,
    "automation.log"
)

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    )
)


def main():

    print(
        "\n"
        "====================================\n"
        " AUTOMATED SALES REPORTING SYSTEM\n"
        "====================================\n"
    )

    logging.info(
        "Automation started"
    )


    try:

        # ---------------------------------
        # STEP 1: LOAD AND CLEAN DATA
        # ---------------------------------

        print(
            "STEP 1: Loading and cleaning data..."
        )

        df = prepare_data()

        print(
            f"Clean dataset contains "
            f"{len(df)} rows."
        )


        # ---------------------------------
        # STEP 2: GET RECENT WEEK
        # ---------------------------------

        print(
            "\nSTEP 2: Selecting most recent week..."
        )

        df_recent_week = get_recent_week(
            df
        )

        print(
            f"Recent week contains "
            f"{len(df_recent_week)} rows."
        )

        print(
            "Date range:",
            df_recent_week[
                "Order_Date"
            ].min(),
            "to",
            df_recent_week[
                "Order_Date"
            ].max()
        )


        # ---------------------------------
        # STEP 3: CREATE CHART
        # ---------------------------------

        print(
            "\nSTEP 3: Creating dashboard..."
        )

        chart_path = create_report_charts(
            df_recent_week
        )

        print(
            f"Chart created: {chart_path}"
        )


        # ---------------------------------
        # STEP 4: CREATE EXCEL REPORT
        # ---------------------------------

        print(
            "\nSTEP 4: Creating Excel report..."
        )

        excel_path = create_excel_report(
            df_recent_week,
            chart_path
        )

        print(
            f"Excel report created: "
            f"{excel_path}"
        )


        # ---------------------------------
        # STEP 5: EMAIL
        # ---------------------------------

        print(
            "\nSTEP 5: Sending email..."
        )

        load_env()

        sender = os.environ.get(
            "EMAIL_USER"
        )

        password = os.environ.get(
            "EMAIL_PASS"
        )

        recipients = os.environ.get(
            "RECIPIENTS",
            ""
        )


        if sender and password and recipients:

            result = email_report(
                recipients,
                excel_path,
                chart_path,
                sender,
                password
            )

            if result:

                print(
                    "Email delivery completed."
                )

            else:

                print(
                    "Email delivery failed."
                )

        else:

            print(
                "Email credentials or "
                "recipients not configured."
            )


        # ---------------------------------
        # DONE
        # ---------------------------------

        logging.info(
            "Automation completed successfully"
        )

        print(
            "\n===================================="
        )

        print(
            " REPORT GENERATION COMPLETED"
        )

        print(
            "===================================="
        )


    except Exception as error:

        logging.exception(
            "Automation failed"
        )

        print(
            f"\nERROR: {error}"
        )

        raise


# ---------------------------------
# RUN
# ---------------------------------

if __name__ == "__main__":

    main()